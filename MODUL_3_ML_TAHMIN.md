# 🤖 MODÜL 3: Makine Öğrenmesi ile Yörünge Tahmini

> **Modül Sahibi:** ML / Deep Learning Ekibi  
> **Önkoşullar:** Modül 2 (Kalman Filtresi) tamamlanmış, temiz zaman serisi verisi hazır  
> **Tahmini Süre:** 12 hafta (Ay 5–7)  
> **Durum:** ⬜ Başlanmadı

---

## 3.1 Modül Amacı ve Kapsamı

Bu modül, Kalman filtresinden gelen temiz yörünge zaman serisi verisini kullanarak **48 saat ileriye** güvenilir yörünge tahmini yapmaktan sorumludur.

### Neden ML? SGP4 Yeterli Değil mi?

```
    Tahmin Hatası vs Zaman Ufku
    
    Hata
    (km)
    │
    │                                          ╱  SGP4/TLE
    │                                        ╱     (analitik)
    │                                      ╱
    │                                    ╱
    │                                  ╱
    │                                ╱
    │                        ╱── ──╱
    │                      ╱    ╱
    │                    ╱   ╱
    │                  ╱  ╱
    │              ╱─╱    ML Tahmin
    │            ╱╱        (Bi-LSTM/Informer)
    │         ╱╱
    │     ╱──╱
    │  ╱──╱
    │╱──╱── Kalman Filtresi
    ├──────┬──────┬──────┬──────┬──────┬──── Zaman
    0     4h    12h    24h    36h    48h
```

| Yaklaşım | 1 saat | 12 saat | 24 saat | 48 saat |
|---|---|---|---|---|
| SGP4 (salt TLE) | ~500 m | ~3 km | ~8 km | ~20 km |
| Kalman (EKF) | ~50 m | ~500 m | ~2 km | ~10 km |
| **ML (Bi-LSTM)** | ~20 m | ~100 m | ~300 m | ~500 m |
| **ML (Informer)** | ~15 m | ~80 m | ~250 m | ~400 m |

**ML'nin avantajları:**
- Pertürbasyon modelindeki hataları veriden öğrenir
- Tekrarlayan yörünge kalıplarını (periyodiklik) yakalayabilir
- Atmosfer yoğunluk değişimlerini dolaylı olarak öğrenir
- Birden fazla nesneyi paralel olarak tahmin edebilir

---

## 3.2 Veri Pipeline'ı — Kalman'dan ML'ye

### Veri Akışı

```
┌──────────────────┐
│ Kalman Çıktısı   │
│ (Temiz zaman     │
│  serisi)         │
│                  │
│ Her dakika:      │
│ [x,y,z,vx,vy,vz│
│  j2,drag,srp,   │
│  f107,ap]        │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────────────────┐
│              VERİ ÖN İŞLEME                      │
│                                                  │
│  1. Eksik veri interpolasyonu (cubic spline)     │
│  2. Outlier tespiti ve temizleme (3σ kuralı)     │
│  3. Feature normalizasyonu (StandardScaler)      │
│  4. Zaman serisi windowing                       │
│  5. Train/Val/Test bölme                         │
└────────┬─────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────┐
│              WİNDOWİNG                            │
│                                                  │
│  Girdi penceresi: 30 gün = 43,200 dakika        │
│  Çıktı penceresi: 48 saat = 2,880 dakika        │
│  Kaydırma adımı: 60 dakika                       │
│                                                  │
│  ┌─────────────────────┬──────────┐              │
│  │     GİRDİ (30 gün)  │ÇIKTI(48h)│             │
│  │  ← 43,200 adım →   │← 2,880 →│             │
│  └─────────────────────┴──────────┘              │
│  ← stride=60 →                                   │
│  ┌─────────────────────┬──────────┐              │
│  │     GİRDİ (30 gün)  │ÇIKTI(48h)│             │
│  └─────────────────────┴──────────┘              │
└──────────────────────────────────────────────────┘
```

### Feature Vektörü (10 Boyutlu)

| # | Feature | Birim | Normalizasyon |
|---|---|---|---|
| 1 | x (ECI) | km | StandardScaler |
| 2 | y (ECI) | km | StandardScaler |
| 3 | z (ECI) | km | StandardScaler |
| 4 | $v_x$ (ECI) | km/s | StandardScaler |
| 5 | $v_y$ (ECI) | km/s | StandardScaler |
| 6 | $v_z$ (ECI) | km/s | StandardScaler |
| 7 | J2 İvmesi | m/s² | Log + StandardScaler |
| 8 | Drag İvmesi | m/s² | Log + StandardScaler |
| 9 | F10.7 İndeksi | SFU | MinMaxScaler (0–1) |
| 10 | Ap İndeksi | nT | MinMaxScaler (0–1) |

### Neden Normalizasyon Kritik?

Pozisyon değerleri (~7000 km) ile drag ivmesi değerleri (~$10^{-8}$ m/s²) arasında **19 büyüklük sırası** fark var. Normalizasyon yapılmazsa gradient'ler patlar veya küçük feature'lar görmezden gelinir.

**StandardScaler:**

$$x_{norm} = \frac{x - \mu}{\sigma}$$

**Log dönüşümü (çok küçük değerler için):**

$$x_{log} = \log_{10}(|x| + \epsilon), \quad \epsilon = 10^{-15}$$

---

## 3.3 Veri Bölme Stratejisi

### Zamana Dayalı Bölme (Chronological Split)

Zaman serisi verisinde **asla rastgele bölme yapılmaz** — gelecek verisi ile geçmiş verisi karışır (data leakage).

```
    ├───────────── Toplam Veri (12+ ay) ──────────────┤
    │                                                  │
    │  ┌──────────────────┬─────────┬─────────┐       │
    │  │    EĞİTİM (%70)  │VAL(%15) │TEST(%15)│       │
    │  │                  │         │         │       │
    │  │   İlk 8.4 ay    │ 1.8 ay  │ 1.8 ay  │       │
    │  └──────────────────┴─────────┴─────────┘       │
    │                                                  │
    │  Zaman akışı ────────────────────────────▶       │
    │                                                  │
    │  ⚠️ VAL ve TEST setleri her zaman EĞİTİM'den    │
    │     sonra gelmelidir!                            │
    └──────────────────────────────────────────────────┘
```

### Uydu Bazlı Bölme

Her uydu için ayrı model mu, tek genel model mi?

| Yaklaşım | Avantaj | Dezavantaj |
|---|---|---|
| **Uydu-özel model** | Yüksek doğruluk | Her uydu için ayrı eğitim |
| **Genel model** | Transfer öğrenme, az veri | Düşük doğruluk |
| **Hibrit (Önerilen)** | Genel model + fine-tune | Orta karmaşıklık |

**Önerilen strateji:**
1. Tüm uydularla genel bir model eğit (pre-training)
2. Her Türk uydusu için ayrıca fine-tune yap (transfer learning)

---

## 3.4 Model Mimarisi 1: Bi-LSTM (Bidirectional LSTM)

### LSTM Hücre Yapısı

LSTM (Long Short-Term Memory), vanilya RNN'in "uzun vadeli bağımlılık" problemini çözmek için tasarlanmıştır.

```
                         LSTM Hücresi Detayı
    
    ┌────────────────────────────────────────────────────┐
    │                                                    │
    │    c(t-1) ──────────┬──────── × ───┬──── c(t)     │
    │                     │              │               │
    │                   forget         add               │
    │                    gate         gate               │
    │                     │              │               │
    │                  ┌──┴──┐      ┌──┴──────┐         │
    │                  │  σ  │      │  σ  tanh │         │
    │                  │ f_t │      │ i_t  c̃_t │         │
    │                  └──┬──┘      └──┬──┬───┘         │
    │                     │            │  │              │
    │    h(t-1) ──┬───────┼────────────┼──┼──┐          │
    │             │       │            │  │  │          │
    │    x(t) ────┼───────┼────────────┼──┘  │          │
    │             │       │            │     │          │
    │             │    ┌──┴──┐         │  ┌──┴──┐       │
    │             │    │     │         │  │  σ  │       │
    │             │    │     │         │  │ o_t │       │
    │             │    └─────┘         │  └──┬──┘       │
    │             │                    │     │          │
    │             │                    │     × ── tanh  │
    │             │                    │     │          │
    │             └────────────────────┘     │          │
    │                                    h(t) ─────▶    │
    │                                                    │
    └────────────────────────────────────────────────────┘
```

**LSTM Denklemleri:**

$$\mathbf{f}_t = \sigma(\mathbf{W}_f [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_f)$$
$$\mathbf{i}_t = \sigma(\mathbf{W}_i [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_i)$$
$$\tilde{\mathbf{c}}_t = \tanh(\mathbf{W}_c [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_c)$$
$$\mathbf{c}_t = \mathbf{f}_t \odot \mathbf{c}_{t-1} + \mathbf{i}_t \odot \tilde{\mathbf{c}}_t$$
$$\mathbf{o}_t = \sigma(\mathbf{W}_o [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_o)$$
$$\mathbf{h}_t = \mathbf{o}_t \odot \tanh(\mathbf{c}_t)$$

Burada:
- $\mathbf{f}_t$ = Forget gate ("Eski bilgiyi ne kadar tut?")
- $\mathbf{i}_t$ = Input gate ("Yeni bilgiyi ne kadar al?")
- $\mathbf{o}_t$ = Output gate ("Ne kadar çıktı ver?")
- $\odot$ = Eleman-bazlı çarpım (Hadamard product)
- $\sigma$ = Sigmoid fonksiyonu: $\sigma(x) = \frac{1}{1+e^{-x}}$

### Bidirectional Yapı

Tek yönlü LSTM sadece geçmişe bakar. Bi-LSTM hem geçmişe hem "geleceğe" bakar:

```
    İleri LSTM:   x₁ → x₂ → x₃ → ... → x_T  →  h⃗_T
    Geri LSTM:    x₁ ← x₂ ← x₃ ← ... ← x_T  →  h⃖_T
    
    Birleşik:     h_t = [h⃗_t ; h⃖_t]  (concatenation)
```

**Yörünge tahmininde neden bidirectional?**

Bir yörüngenin "periyodik" yapısı var. Bir noktadaki durumu anlamak için hem önceki hem sonraki noktaları bilmek faydalıdır. Bi-LSTM, bu periyodik kalıpları daha iyi öğrenir.

### Tam Model Mimarisi

```
┌──────────────────────────────────────────────────────────┐
│                    Bi-LSTM Orbit Predictor                │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Input: (batch, 43200, 10)                              │
│  │      └─dakika─┘ └feat┘                               │
│  │                                                       │
│  ├─── Temporal Subsampling ─────────────────────────────│
│  │    43200 dakika → 720 saat (saatlik ortalama)        │
│  │    Çıktı: (batch, 720, 10)                           │
│  │                                                       │
│  ├─── Bi-LSTM Katman 1 ────────────────────────────────│
│  │    hidden_size = 256, bidirectional = True           │
│  │    Çıktı: (batch, 720, 512)  [256×2]                │
│  │                                                       │
│  ├─── Layer Normalization ─────────────────────────────│
│  │                                                       │
│  ├─── Dropout (0.2) ──────────────────────────────────│
│  │                                                       │
│  ├─── Bi-LSTM Katman 2 ────────────────────────────────│
│  │    hidden_size = 128, bidirectional = True           │
│  │    Çıktı: (batch, 720, 256)  [128×2]                │
│  │                                                       │
│  ├─── Multi-Head Self Attention ───────────────────────│
│  │    embed_dim = 256, num_heads = 8                   │
│  │    → Periyodik kalıpları yakalamak için             │
│  │    Çıktı: (batch, 720, 256)                         │
│  │                                                       │
│  ├─── Residual Connection ─────────────────────────────│
│  │    attn_out + lstm2_out                             │
│  │                                                       │
│  ├─── Bi-LSTM Katman 3 ────────────────────────────────│
│  │    hidden_size = 64, bidirectional = True            │
│  │    return only last hidden state                    │
│  │    Çıktı: (batch, 128)  [64×2]                      │
│  │                                                       │
│  ├─── FC Katman 1 ─────────────────────────────────────│
│  │    Linear(128, 256) + ReLU + Dropout(0.2)           │
│  │                                                       │
│  ├─── FC Katman 2 ─────────────────────────────────────│
│  │    Linear(256, 48 × 3) = Linear(256, 144)           │
│  │                                                       │
│  ├─── Reshape ─────────────────────────────────────────│
│  │    (batch, 144) → (batch, 48, 3)                    │
│  │                                                       │
│  Output: (batch, 48, 3)                                 │
│          └─saat─┘ └xyz┘                                 │
│          48 saatlik x, y, z konum tahmini               │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Parametre Sayısı Hesabı

| Katman | Parametreler | Hesaplama |
|---|---|---|
| Bi-LSTM 1 | 1,118,208 | $4 \times [(10+256) \times 256 + 256] \times 2$ |
| Bi-LSTM 2 | 657,408 | $4 \times [(512+128) \times 128 + 128] \times 2$ |
| Attention | 263,168 | $3 \times 256 \times 256 + 256 \times 256$ |
| Bi-LSTM 3 | 164,864 | $4 \times [(256+64) \times 64 + 64] \times 2$ |
| FC 1 | 33,024 | $128 \times 256 + 256$ |
| FC 2 | 36,992 | $256 \times 144 + 144$ |
| **Toplam** | **~2.27M** | Eğitilebilir parametreler |

---

## 3.5 Model Mimarisi 2: Informer (Long-Sequence Transformer)

### Neden Informer?

Standart Transformer'ın self-attention mekanizması $O(L^2)$ karmaşıklığa sahiptir (L = sekans uzunluğu). 720 adımlık bir girdi için bu, $720^2 = 518,400$ attention skoru demektir — hesaplama ve bellek açısından pahalıdır.

Informer, **ProbSparse Attention** ile bu karmaşıklığı $O(L \log L)$'ye düşürür.

### Standart Attention vs ProbSparse Attention

**Standart Self-Attention:**

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

Her query, **tüm** key'lere bakar → $O(L^2)$

**ProbSparse Attention:**

$$\text{ProbSparse}(Q, K, V) = \text{softmax}\left(\frac{\bar{Q}K^T}{\sqrt{d_k}}\right)V$$

Sadece **en bilgilendirici** query'ler seçilir → $O(L \log L)$

```
    Standart Attention              ProbSparse Attention
    
    Q₁ ─┬─┬─┬─┬─┬─▶               Q₁ ─┬─────┬───▶
    Q₂ ─┼─┼─┼─┼─┼─▶               Q₂ ────────────▶ (seçilmedi)
    Q₃ ─┼─┼─┼─┼─┼─▶               Q₃ ─┼──┬──┼───▶
    Q₄ ─┼─┼─┼─┼─┼─▶               Q₄ ────────────▶ (seçilmedi)
    Q₅ ─┼─┼─┼─┼─┼─▶               Q₅ ─┼─┬──────▶
        K₁K₂K₃K₄K₅                    K₁K₂K₃K₄K₅
    
    Tüm Q-K çiftleri               Sadece önemli Q'lar
    hesaplanır (L²)                 hesaplanır (L·log L)
```

### Query Seçimi — KL Divergence

Bir query'nin "bilgilendirici" olup olmadığını anlamak için attention dağılımının uniform dağılımdan sapması ölçülür:

$$M(q_i, K) = \max_j \left(\frac{q_i k_j^T}{\sqrt{d}}\right) - \frac{1}{L_K}\sum_{j=1}^{L_K} \frac{q_i k_j^T}{\sqrt{d}}$$

$M$ değeri büyükse → Query bilgilendirici (seçilir)
$M$ değeri küçükse → Query uniform'a yakın (atlanır)

Seçilen query sayısı: $\bar{u} = c \cdot \ln L_Q$ (c = sabit, tipik: 5)

### Distilling (Damıtma) Katmanları

Her encoder katmanından sonra sekans uzunluğu yarıya indirilir:

```
    Encoder Layer 1: L = 720 → Distill → L = 360
    Encoder Layer 2: L = 360 → Distill → L = 180
    Encoder Layer 3: L = 180 → Distill → L = 90
    
    Her Distill:
    ┌─────────────────────────┐
    │ Conv1D(kernel=3, stride=1) │
    │ + ELU activation           │
    │ + MaxPool1D(stride=2)      │
    └─────────────────────────┘
```

### Tam Informer Mimarisi

```
┌──────────────────────────────────────────────────────────┐
│                    Informer Architecture                  │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─── ENCODER ─────────────────────────────────────┐    │
│  │                                                  │    │
│  │  Input Embedding                                │    │
│  │  ├── Token Embedding: Conv1D(10, 512)           │    │
│  │  ├── Positional Encoding: Sinusoidal            │    │
│  │  └── Temporal Encoding: Zaman bilgisi           │    │
│  │                                                  │    │
│  │  Encoder Layer 1 (L=720)                        │    │
│  │  ├── ProbSparse Multi-Head Attention (8 heads)  │    │
│  │  ├── Layer Norm + Residual                      │    │
│  │  ├── Feed Forward (512 → 2048 → 512)           │    │
│  │  └── Distilling → L=360                         │    │
│  │                                                  │    │
│  │  Encoder Layer 2 (L=360)                        │    │
│  │  ├── ProbSparse Multi-Head Attention (8 heads)  │    │
│  │  ├── Layer Norm + Residual                      │    │
│  │  ├── Feed Forward (512 → 2048 → 512)           │    │
│  │  └── Distilling → L=180                         │    │
│  │                                                  │    │
│  │  Encoder Layer 3 (L=180)                        │    │
│  │  ├── ProbSparse Multi-Head Attention (8 heads)  │    │
│  │  ├── Layer Norm + Residual                      │    │
│  │  ├── Feed Forward (512 → 2048 → 512)           │    │
│  │  └── Distilling → L=90                          │    │
│  │                                                  │    │
│  └── Encoder Output: (batch, 90, 512) ─────────┐  │    │
│                                                  │  │    │
│  ┌─── DECODER ──────────────────────────────────┤  │    │
│  │                                               │  │    │
│  │  Start Token: Son 24 saatlik gerçek veri     │  │    │
│  │  + 48 saatlik sıfır padding (tahmin kısmı)   │  │    │
│  │                                               │  │    │
│  │  Decoder Layer 1                              │  │    │
│  │  ├── Masked Multi-Head Attention (8 heads)   │  │    │
│  │  ├── Cross-Attention (Encoder çıktısına bak) │◀─┘    │
│  │  └── Feed Forward (512 → 2048 → 512)        │       │
│  │                                               │       │
│  │  Decoder Layer 2                              │       │
│  │  ├── Masked Multi-Head Attention (8 heads)   │       │
│  │  ├── Cross-Attention                         │       │
│  │  └── Feed Forward                            │       │
│  │                                               │       │
│  │  Linear Projection: 512 → 3 (x, y, z)       │       │
│  │                                               │       │
│  │  Output: (batch, 48, 3)                      │       │
│  │          └─ 48 saatlik konum tahmini         │       │
│  └───────────────────────────────────────────────┘       │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Informer vs Bi-LSTM Karşılaştırma

| Özellik | Bi-LSTM | Informer |
|---|---|---|
| Parametre Sayısı | ~2.3M | ~8.5M |
| Eğitim Süresi | Orta (~4 saat) | Yüksek (~12 saat) |
| Inference Süresi | ~50 ms | ~20 ms (generative decoder) |
| Kısa Vadeli Doğruluk (< 6h) | ✅ Çok iyi | ✅ Çok iyi |
| Uzun Vadeli Doğruluk (24-48h) | ⚠️ Bozulabilir | ✅ İyi |
| Periyodiklik Öğrenme | ⚠️ Orta | ✅ İyi (attention) |
| GPU Bellek | ~4 GB | ~8 GB |
| Uygulama Kolaylığı | ✅ Kolay | ⚠️ Orta |

---

## 3.6 Fizik-Bilgili Kayıp Fonksiyonu (Physics-Informed Loss)

### Neden Sadece MSE Yetmez?

Pure MSE ile eğitilen model, fizik kurallarını ihlal eden tahminler yapabilir:
- Enerji korunumu ihlali → Uydu aniden hızlanır/yavaşlar
- Kepler yasası ihlali → Yörünge geometrisi bozulur
- Momentum korunumu ihlali → Fiziksel olmayan yörünge

### Toplam Kayıp Fonksiyonu

$$\mathcal{L}_{total} = \mathcal{L}_{MSE} + \lambda_1 \mathcal{L}_{energy} + \lambda_2 \mathcal{L}_{kepler} + \lambda_3 \mathcal{L}_{smooth}$$

### Bileşen 1: MSE (Veri Uyumu)

$$\mathcal{L}_{MSE} = \frac{1}{N \cdot T} \sum_{i=1}^{N} \sum_{t=1}^{T} ||\hat{\mathbf{r}}_{i,t} - \mathbf{r}_{i,t}||^2$$

### Bileşen 2: Enerji Korunumu

Yörünge enerjisi yaklaşık olarak korunmalıdır (pertürbasyonlar küçük):

$$E = \frac{v^2}{2} - \frac{\mu}{r} \approx \text{sabit}$$

$$\mathcal{L}_{energy} = \frac{1}{T-1} \sum_{t=1}^{T-1} \left(E_{t+1} - E_t\right)^2$$

Burada hız yaklaşık olarak ardışık pozisyonlardan hesaplanır:

$$\mathbf{v}_t \approx \frac{\hat{\mathbf{r}}_{t+1} - \hat{\mathbf{r}}_t}{\Delta t}$$

### Bileşen 3: Kepler'in 2. Yasası (Alansal Hız Korunumu)

$$\mathbf{h} = \mathbf{r} \times \mathbf{v} \approx \text{sabit vektör}$$

$$\mathcal{L}_{kepler} = \frac{1}{T-1} \sum_{t=1}^{T-1} ||\mathbf{h}_{t+1} - \mathbf{h}_t||^2$$

### Bileşen 4: Pürüzsüzlük (Smoothness)

Tahmin edilen yörünge pürüzsüz olmalıdır (ani sıçramalar fiziksel değil):

$$\mathcal{L}_{smooth} = \frac{1}{T-2} \sum_{t=1}^{T-2} ||\hat{\mathbf{r}}_{t+2} - 2\hat{\mathbf{r}}_{t+1} + \hat{\mathbf{r}}_t||^2$$

### Hiperparametre Ağırlıkları

| Kayıp Bileşeni | $\lambda$ | Önerilen Başlangıç | Tuning Stratejisi |
|---|---|---|---|
| MSE | 1.0 (sabit) | — | — |
| Energy | $\lambda_1$ | 0.01 | Grid search: [0.001, 0.01, 0.1] |
| Kepler | $\lambda_2$ | 0.01 | Grid search: [0.001, 0.01, 0.1] |
| Smooth | $\lambda_3$ | 0.001 | Grid search: [0.0001, 0.001, 0.01] |

**Ağırlık zamanlama (Curriculum):**

Eğitimin başında fizik kayıplarının ağırlığını düşük tut, model veriyi öğrendikçe artır:

$$\lambda_i(epoch) = \lambda_i^{max} \cdot \min\left(1, \frac{epoch}{warmup}\right)$$

---

## 3.7 Eğitim Stratejisi

### Optimizer: AdamW

$$\theta_{t+1} = \theta_t - \alpha \left(\frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \epsilon} + \lambda_w \theta_t\right)$$

| Parametre | Değer | Açıklama |
|---|---|---|
| Learning Rate ($\alpha$) | $10^{-4}$ | Başlangıç öğrenme hızı |
| $\beta_1$ | 0.9 | Momentum |
| $\beta_2$ | 0.999 | İkinci moment |
| $\epsilon$ | $10^{-8}$ | Sayısal kararlılık |
| Weight Decay ($\lambda_w$) | 0.01 | L2 düzenleme |

### Learning Rate Scheduler: Cosine Annealing + Warm Restart

```
    LR
    │
    │  ╲                    ╲                    ╲
    │   ╲                    ╲                    ╲
    │    ╲                    ╲                    ╲
    │     ╲                    ╲                    ╲
    │      ╲                    ╲                    ╲
    │       ╲                    ╲                    ╲
    │        ╲___                 ╲___                 ╲___
    │            ╲                    ╲
    │             ╲                    ╲
    │              ╲_______________     ╲_______________
    │
    └──────────┬──────────┬──────────┬──────── Epoch
               T₀         2T₀        3T₀
    
    T₀ = İlk restart periyodu (örn: 50 epoch)
    T_mult = 2 (her restart'ta periyot 2× uzar)
```

$$\eta_t = \eta_{min} + \frac{1}{2}(\eta_{max} - \eta_{min})\left(1 + \cos\left(\frac{T_{cur}}{T_i}\pi\right)\right)$$

### Erken Durdurma (Early Stopping)

```
patience = 15 epoch
min_delta = 0.001 km (MSE iyileşme eşiği)

if val_loss(epoch) < best_val_loss - min_delta:
    best_val_loss = val_loss(epoch)
    patience_counter = 0
    save_checkpoint("best_model.pt")
else:
    patience_counter += 1
    if patience_counter >= patience:
        STOP TRAINING
```

### Gradient Clipping

Gradient patlamasını engellemek için:

$$\text{if } ||\nabla \mathcal{L}|| > \text{max\_norm}: \quad \nabla \mathcal{L} \leftarrow \frac{\text{max\_norm}}{||\nabla \mathcal{L}||} \nabla \mathcal{L}$$

`max_norm = 1.0` (tipik değer)

### Veri Artırma (Data Augmentation)

| Teknik | Açıklama | Etki |
|---|---|---|
| Gürültü Enjeksiyonu | $\mathbf{x}' = \mathbf{x} + \mathcal{N}(0, \sigma^2)$ | Gürültüye dayanıklılık |
| Yörünge Döndürme | RAAN'ı rastgele döndür | Rotasyonal invarians |
| Zaman Kayması | Pencereyi ±birkaç saat ötelendir | Zamansal invarians |
| Feature Maskeleme | Rastgele feature'ları sıfırla | Eksik veri dayanıklılığı |

---

## 3.8 Model Değerlendirme ve Analiz

### Zaman Ufku Bazlı Hata Analizi

```
    RMS Hata (km)
    │
  2.0│
    │                                              ╱
  1.5│                                           ╱
    │                                         ╱
    │                                      ╱──── SGP4
  1.0│                                   ╱
    │                              ╱──╱
    │                           ╱──╱
  0.5│                    ╱──╱──╱──────────── Bi-LSTM
    │              ╱──╱──╱
    │        ╱──╱──╱  ╱─────────────────── Informer
  0.1│  ╱──╱──╱──╱──╱
    │╱──╱──╱──╱
    ├──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬── Saat
    0  4  8  12 16 20 24 28 32 36 40 44 48
```

### Hedef Metrikler (Uydu Tipine Göre)

**LEO Uyduları (İMECE, GÖKTÜRK):**

| Zaman Ufku | MSE Hedef | MAE Hedef | Max Error |
|---|---|---|---|
| 1 saat | < 20 m | < 15 m | < 100 m |
| 6 saat | < 50 m | < 40 m | < 200 m |
| 12 saat | < 100 m | < 80 m | < 500 m |
| 24 saat | < 250 m | < 200 m | < 1 km |
| 48 saat | < 500 m | < 400 m | < 2 km |

**GEO Uyduları (TÜRKSAT):**

| Zaman Ufku | MSE Hedef | MAE Hedef | Max Error |
|---|---|---|---|
| 1 saat | < 50 m | < 40 m | < 200 m |
| 6 saat | < 100 m | < 80 m | < 400 m |
| 12 saat | < 200 m | < 150 m | < 800 m |
| 24 saat | < 400 m | < 300 m | < 1.5 km |
| 48 saat | < 800 m | < 600 m | < 3 km |

### Hata Dağılımı Analizi

Tahmin hatalarının Gaussian dağılıma uyup uymadığını kontrol et:

```
    Hata Histogram                     QQ Plot
    
    Frekans                           Teorik Quantile
    │     ┌─┐                         │          ●●●
    │    ┌┤ ├┐                        │        ●●●
    │   ┌┤ │ ├┐                       │      ●●●
    │  ┌┤ │ │ ├┐                      │    ●●●
    │ ┌┤ │ │ │ ├┐                     │  ●●●
    │┌┤ │ │ │ │ ├┐                    │●●●
    └┴──┴─┴─┴─┴──┴─── Hata (km)      └────────────── Empirik
    
    ✅ İdeal: Simetrik, sıfır              ✅ İdeal: Düz çizgi
       merkezli Gaussian                        (45° açı)
```

### Model Karşılaştırma Pipeline

```
┌──────────────────────────────────────────────────────┐
│                MODEL KARŞILAŞTIRMA                    │
├──────────────────────────────────────────────────────┤
│                                                      │
│  1. Baseline Modeller                               │
│     ├── SGP4 (TLE propagasyon)                     │
│     ├── Kalman Filtresi (EKF çıktısı)             │
│     └── Linear Regression (basit regresyon)        │
│                                                      │
│  2. ML Modeller                                      │
│     ├── Vanilla LSTM (tek yönlü)                   │
│     ├── Bi-LSTM (önerilen)                         │
│     ├── Bi-LSTM + Attention (önerilen)             │
│     ├── Informer (önerilen)                        │
│     └── Bi-LSTM + Physics-Informed Loss            │
│                                                      │
│  3. Ensemble                                         │
│     └── Bi-LSTM + Informer ağırlıklı ortalama     │
│                                                      │
│  Karşılaştırma: MSE, MAE, RMSE, R², Max Error     │
│  Her model × Her uydu × Her zaman ufku             │
└──────────────────────────────────────────────────────┘
```

---

## 3.9 Model Dağıtımı ve Inference

### Inference Pipeline

```
┌────────────────┐    ┌────────────────┐    ┌────────────────┐
│  Son 30 Gün    │    │   Normalize    │    │   Model        │
│  Kalman        │───▶│   + Window     │───▶│   Inference    │
│  Verisi        │    │                │    │   (GPU/CPU)    │
└────────────────┘    └────────────────┘    └───────┬────────┘
                                                     │
                                                     ▼
                                              ┌────────────────┐
                                              │  Denormalize   │
                                              │  + Post-Process │
                                              └───────┬────────┘
                                                      │
                                                      ▼
                                              ┌────────────────┐
                                              │  48 Saatlik    │
                                              │  Tahmin        │
                                              │  (x, y, z)    │
                                              └────────────────┘
```

### Performans Gereksinimleri

| Metrik | Gereksinim | Açıklama |
|---|---|---|
| Inference Süresi | < 100 ms / uydu | Gerçek zamanlı için |
| Batch Inference | < 5 sn / 100 uydu | Toplu tahmin |
| Model Boyutu | < 100 MB | Dağıtım kolaylığı |
| GPU Bellek (Inf.) | < 2 GB | Küçük GPU yeterli |

### Model Optimizasyonu

| Teknik | Hız Artışı | Doğruluk Kaybı |
|---|---|---|
| ONNX Export | 2–3× | Sıfır |
| TorchScript | 1.5–2× | Sıfır |
| FP16 Quantization | 2× | < %1 |
| INT8 Quantization | 4× | %1–5 |
| Pruning (structured) | 1.5–2× | %1–3 |

---

## 3.10 Checkpoint Özet Tablosu

| Checkpoint | Görev | Durum | Başarı Kriteri |
|---|---|---|---|
| 3.1 | Veri Ön İşleme & Windowing | ⬜ | 10.000+ eğitim penceresi |
| 3.2 | Bi-LSTM Model İmplementasyonu | ⬜ | Model derlenmesi |
| 3.3 | Informer İmplementasyonu | ⬜ | Model derlenmesi |
| 3.4 | Physics-Informed Loss | ⬜ | Enerji korunumu < %1 |
| 3.5 | Eğitim & Hiperparametre Tuning | ⬜ | Val loss yakınsaması |
| 3.6 | Model Değerlendirme | ⬜ | MSE < 500 m (48h) |
| 3.7 | Model Karşılaştırma | ⬜ | En iyi model seçimi |
| 3.8 | Model Dağıtımı (ONNX) | ⬜ | Inference < 100 ms |

---

> **Önceki Modül:** [Modül 2 — Kalman Filtresi](./MODUL_2_KALMAN_FILTRESI.md)  
> **Sonraki Modül:** [Modül 4 — Çarpışma Analizi](./MODUL_4_CARPISMA_ANALIZI.md)
