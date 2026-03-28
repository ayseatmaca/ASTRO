# ⚠️ MODÜL 4: Çarpışma Analizi ve Karar Destek Sistemi

> **Modül Sahibi:** Uçuş Dinamiği / Operasyon Ekibi  
> **Önkoşullar:** Modül 3 (ML Tahmin) tamamlanmış, 48 saatlik yörünge tahminleri hazır  
> **Tahmini Süre:** 8 hafta (Ay 8–9)  
> **Durum:** ⬜ Başlanmadı

---

## 4.1 Modül Amacı ve Kapsamı

Bu modül, ML modelinden gelen yörünge tahminlerini kullanarak:

1. **Yaklaşma olaylarını tespit etmek** (screening)
2. **Çarpışma olasılığını hesaplamak** ($P_c$)
3. **Risk sınıflandırması yapmak** (alarm sistemi)
4. **Kaçınma manevraları planlamak** (Delta-V optimizasyonu)

### Conjunction Assessment (CA) Akışı

```
    ┌──────────────────────────────────────────────────────────┐
    │                 CONJUNCTION ASSESSMENT AKIŞI              │
    │                                                          │
    │  Tüm nesne çiftleri                                     │
    │  (~20.000 × 6 Türk uydu = ~120.000 çift)               │
    │         │                                                │
    │         ▼                                                │
    │  ┌──────────────┐                                       │
    │  │  1. ELEME    │  Kaba filtre: Yörünge bandı kontrolü  │
    │  │  (Screening) │  → ~5.000 çifte düşer                 │
    │  └──────┬───────┘                                       │
    │         │                                                │
    │         ▼                                                │
    │  ┌──────────────┐                                       │
    │  │  2. DETAYLI   │  TCA bulma + Miss distance           │
    │  │  ANALİZ      │  → ~200 olay (< 25 km)               │
    │  └──────┬───────┘                                       │
    │         │                                                │
    │         ▼                                                │
    │  ┌──────────────┐                                       │
    │  │  3. OLASILIK  │  Pc hesaplama (Kovaryans analizi)    │
    │  │  HESABI      │  → ~20 olay (Pc > 10⁻⁷)             │
    │  └──────┬───────┘                                       │
    │         │                                                │
    │         ▼                                                │
    │  ┌──────────────┐                                       │
    │  │  4. RİSK      │  Sınıflandırma + Alarm              │
    │  │  DEĞERLENDİRME│  → 1-5 kritik olay                  │
    │  └──────┬───────┘                                       │
    │         │                                                │
    │         ▼                                                │
    │  ┌──────────────┐                                       │
    │  │  5. MANEVRA   │  Delta-V optimizasyonu               │
    │  │  PLANLAMA    │  → Uygulanabilir manevra önerisi      │
    │  └──────────────┘                                       │
    │                                                          │
    └──────────────────────────────────────────────────────────┘
```

---

## 4.2 Adım 1: Kaba Eleme (Coarse Screening)

### Neden Eleme Gerekli?

$N$ nesne varsa, kontrol edilecek çift sayısı $\binom{N}{2} = \frac{N(N-1)}{2}$. 20.000 nesne için bu ~200 milyon çift demektir. Her çifti detaylı analiz etmek hesaplama açısından imkansızdır.

### Filtre 1: Yörünge Bandı (Apogee-Perigee Filtresi)

İki nesnenin yörünge bandları örtüşmüyorsa, çarpışma imkansızdır.

```
    Yükseklik (km)
    │
    │  ════════════ Apogee 2 ════════════
    │  ─────────── Perigee 2 ────────────   ← Nesne 2 bandı
    │
    │                                        ÖRTÜŞME YOK → ELEME
    │
    │  ════════════ Apogee 1 ════════════
    │  ─────────── Perigee 1 ────────────   ← Nesne 1 bandı
    │
    └────────────────────────────────────── Zaman
```

**Koşul:** Eğer $\text{Apogee}_1 + \delta < \text{Perigee}_2$ veya $\text{Apogee}_2 + \delta < \text{Perigee}_1$ → **Ele**

$\delta$ = Güvenlik tamponu (tipik: 50 km)

### Filtre 2: İnklinasyon ve RAAN Kontrolü

Yörünge düzlemleri çok farklıysa, kesişme olasılığı düşüktür:

$$\Delta \Omega_{max} = \arccos\left(\frac{\cos(i_1)\cos(i_2) + \sin(i_1)\sin(i_2)}{\sin(i_1)\sin(i_2)}\right)$$

$\Delta\Omega > \Delta\Omega_{max}$ → Yörüngeler kesişmez → **Ele**

### Filtre 3: Zaman Penceresi Filtresi

ML modeli 48 saatlik tahmin üretir. Bu 48 saat içinde iki nesne hiç yakınlaşmıyorsa ele:

**Hızlı minimum mesafe tahmini:**

Her 10 dakikada bir pozisyon sample'ı al, mesafeyi hesapla:

$$d_{min}^{approx} = \min_{t \in \{0, 10, 20, ..., 2880\}} ||\mathbf{r}_1(t) - \mathbf{r}_2(t)||$$

$d_{min}^{approx} > 100$ km → **Ele**

### Eleme Sonuçları (Tipik)

| Aşama | Kalan Çift Sayısı | Eleme Oranı |
|---|---|---|
| Başlangıç | ~120.000 | — |
| Yörünge Bandı Filtresi | ~15.000 | %87 |
| İnklinasyon/RAAN Filtresi | ~8.000 | %47 |
| Zaman Penceresi Filtresi | ~200 | %97.5 |
| **Toplam Eleme** | **~200** | **%99.83** |

---

## 4.3 Adım 2: En Yakın Yaklaşma Analizi (TCA/PCA)

### TCA (Time of Closest Approach) Bulma

Elenmemiş her nesne çifti için en yakın yaklaşma zamanı hassas olarak hesaplanır.

**Mesafe fonksiyonu:**

$$d(t) = ||\mathbf{r}_1(t) - \mathbf{r}_2(t)|| = \sqrt{(x_1-x_2)^2 + (y_1-y_2)^2 + (z_1-z_2)^2}$$

**1. Aşama — Kaba Arama (Grid Search):**

48 saatlik pencereyi 1 dakikalık adımlarla tara, yerel minimumlari bul:

$$t_i^{*} = \arg\min_{t \in [t_i, t_{i+1}]} d(t), \quad \text{1 dk aralıklarla}$$

**2. Aşama — İnce Arama (Brent's Method):**

Her yerel minimumun etrafında ±5 dakika pencerede hassas optimizasyon:

```
    d(t)
    │
    │   ╲         ╱╲
    │    ╲       ╱  ╲         ╱╲
    │     ╲     ╱    ╲       ╱  ╲
    │      ╲   ╱      ╲     ╱    ╲
    │       ╲ ╱        ╲   ╱      ╲
    │        ●          ╲ ╱        ╲
    │      TCA₁          ●          ╲
    │     (birincil)    TCA₂         ╲
    │                  (ikincil)
    └──────────────────────────────── t
```

Her bir TCA için kayıt:

| Alan | Açıklama |
|---|---|
| `tca_time` | En yakın yaklaşma zamanı (UTC) |
| `miss_distance_km` | Minimum mesafe (km) |
| `relative_velocity_km_s` | Bağıl hız büyüklüğü (km/s) |
| `r1_at_tca` | Nesne 1'in TCA'daki pozisyonu |
| `r2_at_tca` | Nesne 2'nin TCA'daki pozisyonu |
| `v1_at_tca` | Nesne 1'in TCA'daki hızı |
| `v2_at_tca` | Nesne 2'nin TCA'daki hızı |

### Miss Distance Eşikleri

| Miss Distance | Aksiyon |
|---|---|
| > 25 km | Dikkate alma |
| 5 – 25 km | İzle (monitoring) |
| 1 – 5 km | Detaylı analiz (Pc hesapla) |
| < 1 km | **Yüksek öncelik** — Manevra değerlendir |
| < 200 m | **KRİTİK** — Acil manevra planla |

---

## 4.4 Adım 3: Çarpışma Olasılığı Hesabı ($P_c$)

### Teorik Arka Plan

Çarpışma olasılığı, iki nesnenin pozisyon belirsizliklerini (kovaryans elipsoidlerini) dikkate alarak hesaplanır. Sadece mesafe bak olmaz — belirsizliğin boyutu ve yönü kritiktir.

```
    ╱╲                 Düşük Belirsizlik + Küçük Mesafe
   ╱  ╲   ◯           → YÜKSEK Pc
  ╱ ●  ╲   ●
  ╲    ╱
   ╲  ╱
    ╲╱

    ╱────────────╲     Yüksek Belirsizlik + Büyük Mesafe
   ╱              ╲   → Belirsiz ama muhtemelen DÜŞÜK Pc
  ╱    ●           ╲           ◯       ●
  ╲                ╱
   ╲              ╱
    ╲────────────╱
```

### B-Plane (Impact Plane) Dönüşümü

Çarpışma olasılığı hesabı, 3D problemi 2D'ye indirgemek için **B-plane** (hedef düzlemi) kullanır. B-plane, TCA'daki bağıl hız vektörüne dik olan düzlemdir.

```
                    Bağıl Hız Vektörü
                    (v_rel)
                       │
                       │
                       │  ╱──── B-plane
                       │╱       (bağıl hıza dik düzlem)
               ────────●──────────
                      ╱│
                    ╱  │
                  ╱    │
                       │
                       │
              ξ ◀──────┼──────▶ η
                       │
              (B-plane koordinatları)
```

**B-plane koordinat sistemi:**

$$\hat{\mathbf{e}}_1 = \frac{\mathbf{v}_{rel}}{|\mathbf{v}_{rel}|}$$

$$\hat{\mathbf{e}}_2 = \frac{\hat{\mathbf{e}}_1 \times \hat{\mathbf{z}}}{|\hat{\mathbf{e}}_1 \times \hat{\mathbf{z}}|}$$

$$\hat{\mathbf{e}}_3 = \hat{\mathbf{e}}_1 \times \hat{\mathbf{e}}_2$$

B-plane miss vector:

$$\mathbf{b} = \begin{bmatrix} \xi \\ \eta \end{bmatrix} = \begin{bmatrix} \Delta \mathbf{r} \cdot \hat{\mathbf{e}}_2 \\ \Delta \mathbf{r} \cdot \hat{\mathbf{e}}_3 \end{bmatrix}$$

### Birleşik Kovaryans Matrisi

İki nesnenin TCA'daki kovaryans matrisleri birleştirilir:

$$\mathbf{C}_{combined} = \mathbf{C}_1 + \mathbf{C}_2$$

(Bağımsız nesne belirsizlikleri toplanır)

B-plane'e projekte et:

$$\mathbf{C}_B = \mathbf{T} \cdot \mathbf{C}_{combined, pos} \cdot \mathbf{T}^T$$

Burada $\mathbf{T}$ = 3D → 2D projeksiyon matrisi (B-plane eksenleri)

$$\mathbf{C}_B = \begin{bmatrix} \sigma_\xi^2 & \rho\sigma_\xi\sigma_\eta \\ \rho\sigma_\xi\sigma_\eta & \sigma_\eta^2 \end{bmatrix}$$

### Hard-Body Radius

İki nesnenin toplam çarpışma yarıçapı:

$$r_{HB} = r_1 + r_2$$

| Nesne Tipi | Tipik Yarıçap |
|---|---|
| Küçük enkaz (1-10 cm) | 0.01 – 0.05 m |
| Orta enkaz (10 cm – 1 m) | 0.05 – 0.5 m |
| Büyük enkaz / roket gövdesi | 0.5 – 5 m |
| Aktif uydu (küçük) | 0.5 – 2 m |
| Aktif uydu (TÜRKSAT) | 3 – 5 m |

### $P_c$ Hesaplama Yöntemleri

#### Yöntem 1: Alfano / Chan Analitik Yaklaşım

Gaussian dağılım varsayımı altında 2D integral:

$$P_c = \frac{1}{2\pi|\mathbf{C}_B|^{1/2}} \iint_{r \leq r_{HB}} \exp\left(-\frac{1}{2}\mathbf{b}^T \mathbf{C}_B^{-1} \mathbf{b}\right) d\xi \, d\eta$$

**Chan'ın Seri Açılımı:**

Kovaryans matrisini eigen decomposition ile köşegenleştir, sonra seri açılımı uygula:

$$P_c = \frac{r_{HB}^2}{2\sigma_\xi'\sigma_\eta'} \exp\left(-\frac{u^2}{2\sigma_\xi'^2} - \frac{v^2}{2\sigma_\eta'^2}\right) \sum_{k=0}^{K} \frac{(-1)^k}{k!} \left(\frac{r_{HB}^2}{4\sigma_\xi'^2\sigma_\eta'^2}\right)^k \cdot L_k$$

Burada $K = 20$ terim genelde yeterlidir. $L_k$ = Laguerre polinomları.

#### Yöntem 2: Foster Sayısal İntegrasyon

Split Gaussian yöntemi ile B-plane üzerinde 1D sayısal integrasyon:

1. Kovaryans matrisini $U\Sigma U^T$ decompose et
2. Bir eksen boyunca analitik integre et
3. Diğer eksen boyunca sayısal integre et (Simpson kuralı)

#### Yöntem 3: Monte Carlo Simülasyonu

En doğru ama en yavaş yöntem. Doğrulama amacıyla kullanılır.

```
N_samples = 100,000

Pc_mc = 0
for i in range(N_samples):
    r1_sample = r1_nominal + np.random.multivariate_normal(0, C1)
    r2_sample = r2_nominal + np.random.multivariate_normal(0, C2)
    distance = ||r1_sample - r2_sample||
    if distance < r_HB:
        Pc_mc += 1

Pc_mc /= N_samples
```

**Monte Carlo Yakınsama:**

| Sample Sayısı | $P_c$ Doğruluk | Hesaplama Süresi |
|---|---|---|
| 10,000 | ± %30 | ~1 s |
| 100,000 | ± %10 | ~10 s |
| 1,000,000 | ± %3 | ~100 s |
| 10,000,000 | ± %1 | ~1000 s |

### $P_c$ Geçerlilik Kontrolleri

$P_c$ hesabının güvenilir olması için bazı varsayımlar kontrol edilmelidir:

| Varsayım | Kontrol | Eğer ihlal edilirse |
|---|---|---|
| Kısa süreli geçiş | $\Delta t_{encounter} < 1$ saniye | Uzun geçişli model kullan |
| Doğrusal hareket yaklaşımı | Eğrilik yarıçapı >> miss distance | Eğrisel model kullan |
| Gaussian dağılım | Mahalanobis mesafe < 5 | Monte Carlo kullan |
| Küçük hard-body | $r_{HB} \ll \sigma_{min}$ | Genişletilmiş $P_c$ formülü |

---

## 4.5 Adım 4: Risk Sınıflandırma ve Alarm

### Risk Matrisi

```
    Bağıl Hız (km/s)
    │
 15 │  🟡    🟠    🔴    🔴    🔴
    │
 10 │  🟢    🟡    🟠    🔴    🔴
    │
  5 │  🟢    🟢    🟡    🟠    🔴
    │
  1 │  🟢    🟢    🟢    🟡    🟠
    │
    └───┬──────┬──────┬──────┬─────── Pc
       10⁻⁸  10⁻⁶  10⁻⁵  10⁻⁴

    🟢 Düşük   🟡 Orta   🟠 Yüksek   🔴 Kritik
```

### Detaylı Risk Seviyeleri

| Seviye | $P_c$ Aralığı | Aksiyon | Bildirim | Süreç |
|---|---|---|---|---|
| **Seviye 0** — Güvenli | $P_c < 10^{-7}$ | Sadece kayıt | Yok | Otomatik |
| **Seviye 1** — İzleme | $10^{-7} \leq P_c < 10^{-5}$ | Aktif izleme | Günlük rapor | Otomatik |
| **Seviye 2** — Dikkat | $10^{-5} \leq P_c < 10^{-4}$ | Manevra hazırlığı | E-posta + SMS | Yarı-otomatik |
| **Seviye 3** — Yüksek | $10^{-4} \leq P_c < 10^{-3}$ | Manevra planı yap | Anlık alarm | Manuel onay |
| **Seviye 4** — Kritik | $P_c \geq 10^{-3}$ | **ACİL MANEVRA** | Tüm kanallar | Acil operasyon |

### Alarm Eskalasyon Zaman Çizelgesi

```
    TCA'ya kalan süre
    ─────────────────────────────────────────────────────▶
    
    48h          24h          12h          6h          TCA
    │            │            │            │            │
    │  Seviye 2+ │  Seviye 2+ │  Seviye 3+ │  Seviye 3+│
    │  → E-posta │  → Tekrar  │  → SMS +   │  → Acil   │
    │            │    e-posta  │    Telefon  │    Toplantı│
    │            │  + Manevra  │  + Manevra  │  + Manevra│
    │            │    analizi  │    kararı   │    UYGULA │
    │            │    başla    │    al       │            │
```

### Alarm Mesaj Formatı

```
╔══════════════════════════════════════════════════════════════╗
║  ⚠️  YAKIN GEÇİŞ ALARMI — SEVİYE 3 (YÜKSEK)               ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Birincil Nesne:  TÜRKSAT 5A (NORAD: 53159)                ║
║  İkincil Nesne:   COSMOS 2251 Debris (NORAD: 34567)         ║
║                                                              ║
║  TCA:             2026-04-15 14:23:47 UTC                   ║
║  Kalan Süre:      18 saat 42 dakika                          ║
║                                                              ║
║  Miss Distance:   0.87 km                                    ║
║  Bağıl Hız:       12.4 km/s                                  ║
║  Çarpışma Olasılığı: Pc = 2.3 × 10⁻⁴                       ║
║                                                              ║
║  Önerilen Manevra:                                           ║
║  • Zaman:   TCA - 6 saat (2026-04-15 08:23:47 UTC)          ║
║  • Delta-V: 0.15 m/s (in-track yönünde)                     ║
║  • Yakıt:   ~0.3 kg                                          ║
║  • Sonuç:   Miss distance → 15 km, Pc → 10⁻⁸               ║
║                                                              ║
║  [MANEVRA ONAYLA]  [DETAY GÖSTER]  [ERTELe]                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 4.6 Adım 5: Manevra Planlama (Collision Avoidance Maneuver — CAM)

### Manevra Tipleri

```
    ┌──────────────────────────────────────────────────────┐
    │               MANEVRA TİPLERİ                        │
    ├──────────┬──────────┬──────────┬────────────────────┤
    │          │          │          │                    │
    │ In-Track │ Cross-   │ Radial   │ Combined           │
    │ (hız     │ Track    │ (yarıçap │ (optimal)          │
    │ yönünde) │ (yörünge │ yönünde) │                    │
    │          │ düzlemine│          │                    │
    │    ──▶   │ dik)     │    ↑     │  ↗                │
    │ Δv_T     │    ⊙     │  Δv_R    │  Δv_combined      │
    │          │  Δv_N    │          │                    │
    └──────────┴──────────┴──────────┴────────────────────┘
```

| Manevra Tipi | Etkisi | Kullanım |
|---|---|---|
| **In-Track (T)** | Yörünge periyodunu değiştirir, zamanlama kayar | En yaygın, LEO |
| **Cross-Track (N)** | Yörünge düzlemini eğer | Nadiren tek başına |
| **Radial (R)** | Yörünge şeklini değiştirir | GEO uydular |
| **Combined** | Minimum yakıt için optimal yön | Her zaman tercih |

### In-Track Manevra — Detaylı Analiz

En yaygın kaçınma manevrası. Uydunun ilerleme yönünde küçük bir hız değişimi yapılır.

**Fizik:**

$$\Delta v_T \rightarrow \Delta a = \frac{2a^2}{\mu} v \cdot \Delta v_T$$

Bu yarı-büyük eksen değişimi, yörünge periyodunu değiştirerek TCA'da uyduyu farklı bir konuma getirir.

**Zamanlama etkisi:**

$$\Delta_{along-track}(t) \approx \frac{3}{2} n \cdot \Delta a \cdot (t - t_{maneuver})$$

$t_{maneuver}$ = Manevra zamanı, $n$ = mean motion

**Örnek:**

- TCA'dan 6 saat önce 0.1 m/s in-track manevra
- $\Delta a \approx$ 150 m
- TCA'da along-track kayma: $\approx$ 10 km
- Bu, miss distance'ı dramatik şekilde artırır

### Optimizasyon Problemi Formülasyonu

**Amaç:** Minimum yakıt kullanarak risk eşiğinin altına düş

$$\min_{\Delta \mathbf{v}, t_m} ||\Delta \mathbf{v}||$$

**Kısıtlar:**

$$P_c(\text{yeni yörünge}) < P_c^{threshold} = 10^{-7}$$

$$||\Delta \mathbf{v}|| < \Delta v_{max}$$

$$t_{now} + t_{prep} < t_m < t_{TCA} - t_{safety}$$

Burada:
- $t_{prep}$ = Hazırlık süresi (tipik: 2 saat)
- $t_{safety}$ = Güvenlik tamponu (tipik: 1 yörünge periyodu)
- $\Delta v_{max}$ = Yakıt bütçesi sınırı

### Manevra Zamanı Optimizasyonu

Manevranın ne zaman yapılacağı, etkinliğini dramatik şekilde etkiler:

```
    Gerekli Δv (m/s)
    │
    │                                 ●
  2.0│                              ●
    │                           ●
  1.5│                        ●
    │                     ●
  1.0│                  ●
    │               ●
  0.5│            ●
    │        ●
  0.1│  ●  ●
    │●
    ├─┬──┬──┬──┬──┬──┬──┬──┬── TCA'ya kalan süre
    48 42 36 30 24 18 12  6  0  (saat)
    
    ← Erken manevra = Az yakıt                    
    Geç manevra = Çok yakıt →                     
```

**Kural:** Manevra ne kadar erken yapılırsa, o kadar az yakıt gerekir. Tipik olarak TCA'dan 12-24 saat önce optimal nokta.

### Çoklu Manevra Seçenekleri

Operatöre birden fazla seçenek sunulur:

| Seçenek | Δv (m/s) | Yakıt (kg) | Sonuç Miss (km) | Sonuç $P_c$ | Manevra Zamanı |
|---|---|---|---|---|---|
| A (Minimum Yakıt) | 0.05 | 0.1 | 5.2 | $3 \times 10^{-6}$ | TCA - 24h |
| B (Orta) | 0.12 | 0.24 | 12.8 | $8 \times 10^{-8}$ | TCA - 18h |
| **C (Önerilen)** | **0.15** | **0.3** | **15.3** | **$2 \times 10^{-8}$** | **TCA - 12h** |
| D (Güvenli) | 0.30 | 0.6 | 28.5 | $< 10^{-9}$ | TCA - 6h |

### Post-Manevra Analizi

Manevra sonrası yeni yörünge için kontroller:

```
✓ Yeni yörünge, hedeflenen enkaz ile güvenli mesafede mi?
✓ Yeni yörünge, başka nesnelerle yakınlaşma yaratıyor mu?
✓ Yakıt harcaması bütçe içinde mi?
✓ Uydunun görev yörüngesine dönüş manevra maliyeti nedir?
✓ İletişim penceresi etkileniyor mu?
```

---

## 4.7 Kovaryans Realizmi (Covariance Realism)

### Neden Kovaryans Realizmi Kritik?

$P_c$ hesabı tamamen kovaryans matrislerine dayanır. Kovaryans gerçekçi değilse:

- **Kovaryans çok küçükse** → Gerçek risk küçümsenir → Çarpışma riski artar
- **Kovaryans çok büyükse** → Yanlış alarmlar → Gereksiz manevra → Yakıt israfı

### Kovaryans Kalibrasyon Yöntemleri

**1. Konsistans Testi:**

TLE tahminlerini birbirleriyle karşılaştır. Tahmin hatası, kovaryansla tutarlı mı?

$$\chi^2 = (\mathbf{r}_{actual} - \mathbf{r}_{predicted})^T \mathbf{C}^{-1} (\mathbf{r}_{actual} - \mathbf{r}_{predicted})$$

Beklenen: $\chi^2 \sim \chi^2(3)$, ortalama = 3

**2. Ölçeklendirme Faktörü:**

$$\mathbf{C}_{calibrated} = \alpha^2 \cdot \mathbf{C}_{original}$$

$\alpha$ = Mahalanobis mesafelerinin istatistiksel analizinden hesaplanan ölçek faktörü

**3. Minima Formülü (VCM yoksa):**

VCM (Vector Covariance Message) mevcut değilse, TLE kovaryansını tahmin et:

| Yörünge Tipi | Along-Track $\sigma$ | Cross-Track $\sigma$ | Radial $\sigma$ |
|---|---|---|---|
| LEO (< 500 km) | 1 – 5 km | 0.1 – 0.5 km | 0.05 – 0.2 km |
| LEO (500-1000 km) | 0.5 – 2 km | 0.05 – 0.2 km | 0.02 – 0.1 km |
| MEO | 0.2 – 1 km | 0.02 – 0.1 km | 0.01 – 0.05 km |
| GEO | 0.5 – 3 km | 0.05 – 0.5 km | 0.05 – 0.3 km |

---

## 4.8 Özel Durumlar ve Gelişmiş Analizler

### Çoklu Yaklaşma (Multiple Conjunction)

Bir uydu, aynı zaman aralığında birden fazla nesne ile yakın geçiş yapıyor olabilir:

```
    Zaman ──────────────────────────────────────────▶
    
    TÜRKSAT 5A  ═══════╪══════════╪═══════════╪════
                     TCA₁       TCA₂        TCA₃
                   Enkaz A    Enkaz B     Enkaz C
                   Pc=10⁻⁵   Pc=10⁻⁴    Pc=10⁻⁶
```

**Zorluk:** Enkaz A'dan kaçınma manevrası, Enkaz B ile çarpışma riskini artırabilir!

**Çözüm:** Tüm yaklaşmaları aynı anda optimize et:

$$\min ||\Delta \mathbf{v}|| \quad \text{s.t.} \quad P_c^{(j)} < 10^{-7} \quad \forall j \in \{1, 2, ..., M\}$$

### Uzun Vadeli Çarpışma Riski (Long-term Assessment)

48 saatlik pencere ötesinde, Monte Carlo yörünge simülasyonu ile kümülatif risk hesabı:

$$P_{cumulative} = 1 - \prod_{i=1}^{N_{events}} (1 - P_c^{(i)})$$

### Kessler Sendromu Analizi

Büyük bir çarpışma, 1000'lerce yeni enkaz parçası oluşturabilir. Bu parçacıkların dağılımı:

$$N(d > d_{min}) = 0.1 \cdot M_{total}^{0.75} \cdot d_{min}^{-1.71}$$

$M_{total}$ = Toplam çarpışma kütlesi (kg), $d_{min}$ = Minimum parça boyutu (m)

---

## 4.9 Checkpoint Özet Tablosu

| Checkpoint | Görev | Durum | Başarı Kriteri |
|---|---|---|---|
| 4.1 | Kaba Eleme (Screening) | ⬜ | %99+ eleme oranı |
| 4.2 | TCA/PCA Hesabı | ⬜ | TCA doğruluğu < 1 s |
| 4.3 | $P_c$ Hesaplama (Chan) | ⬜ | Monte Carlo ile < %5 fark |
| 4.4 | Risk Sınıflandırma | ⬜ | Recall > %99 |
| 4.5 | Alarm Sistemi | ⬜ | Gecikme < 5 s |
| 4.6 | Manevra Planlama | ⬜ | $\Delta V$ < 1 m/s (LEO) |
| 4.7 | Kovaryans Realizmi | ⬜ | $\chi^2$ tutarlılığı |
| 4.8 | Çoklu Yaklaşma Yönetimi | ⬜ | Eşzamanlı optimizasyon |

---

> **Önceki Modül:** [Modül 3 — ML Yörünge Tahmini](./MODUL_3_ML_TAHMIN.md)  
> **Sonraki Modül:** [Modül 5 — Görselleştirme](./MODUL_5_GORSELLESTIRME.md)
