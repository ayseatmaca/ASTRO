# 🔧 MODÜL 2: Kalman Filtresi — Veri Füzyonu ve Gürültü Temizleme

> **Modül Sahibi:** Sinyal İşleme / Kontrol Mühendisliği Ekibi  
> **Önkoşullar:** Modül 1 (Veri Edinme) tamamlanmış olmalı  
> **Tahmini Süre:** 8 hafta (Ay 3–4)  
> **Durum:** ⬜ Başlanmadı

---

## 2.1 Modül Amacı ve Kapsamı

Kalman Filtresi modülü, farklı sensörlerden (radar, teleskop, TLE) gelen gürültülü yörünge ölçümlerini birleştirerek:

1. **Gürültü temizleme:** Sensör hatalarını minimize etme
2. **Veri füzyonu:** Birden fazla kaynağı tek bir "en iyi tahmin"de birleştirme
3. **Durum tahmini:** Ölçüm olmadığı anlarda fizik kullanarak pozisyon tahmini
4. **Belirsizlik takibi:** Her tahminin ne kadar güvenilir olduğunu kovaryans matrisi ile ifade etme

### Neden Kalman Filtresi?

```
                Sensör Verileri (Gürültülü)              Kalman Çıktısı (Temiz)
    
    Position                                      Position
    (km)                                          (km)
    │  ╳    ╳                                     │
    │    ╳   ╳  ╳                                 │     ─────────────
    │  ╳  ╳╳  ╳   ╳                               │    /             \
    │ ╳ ╳    ╳ ╳ ╳  ╳                              │   /               \
    │╳   ╳ ╳    ╳  ╳  ╳                            │  /                 \
    │  ╳  ╳  ╳ ╳  ╳   ╳                            │ /                   \
    │ ╳    ╳   ╳ ╳  ╳                              │/                     \
    └──────────────────── t                        └──────────────────────── t
    
    Ham veri: gürültülü, sıçramalı               Filtre çıktısı: pürüzsüz,
    sensör ölçümleri                             güvenilir durum tahmini
```

---

## 2.2 Kalman Filtresi Temelleri

### Temel Konsept

Kalman Filtresi, iki bilgi kaynağını optimal şekilde birleştirir:

1. **Sistem modeli (fizik):** "Uydu şu anda buradaysa, 1 saniye sonra nerede olur?" → **Predict**
2. **Sensör ölçümü:** "Radar uyduyu şurada gördü" → **Update**

```
    ┌─────────────────────────────────────────────────────┐
    │                KALMAN FİLTRE DÖNGÜSÜ                │
    │                                                     │
    │   ┌───────────┐                ┌───────────┐        │
    │   │  PREDICT  │───────────────▶│  UPDATE   │        │
    │   │           │                │           │        │
    │   │ Fizik ile │                │ Ölçüm ile │        │
    │   │ ileriye   │                │ düzeltme  │        │
    │   │ tahmin    │                │           │        │
    │   └─────┬─────┘                └─────┬─────┘        │
    │         │                            │              │
    │         │     ┌─────────────┐        │              │
    │         └────▶│  Optimal    │◀───────┘              │
    │               │  Tahmin     │                       │
    │               │  x̂, P      │                       │
    │               └──────┬──────┘                       │
    │                      │                              │
    │                      ▼                              │
    │              Sonraki zaman adımı                    │
    │              (döngü tekrarlanır)                    │
    └─────────────────────────────────────────────────────┘
```

### Doğrusal Kalman Filtresi (Temel Formlar)

Önce doğrusal versiyonu anlayalım, sonra doğrusal olmayan (EKF) versiyona geçeceğiz.

**Durum Denklemi:**
$$\mathbf{x}_{k} = \mathbf{F}_k \mathbf{x}_{k-1} + \mathbf{B}_k \mathbf{u}_k + \mathbf{w}_k$$

**Ölçüm Denklemi:**
$$\mathbf{z}_k = \mathbf{H}_k \mathbf{x}_k + \mathbf{v}_k$$

Burada:
- $\mathbf{x}_k$ = Durum vektörü (pozisyon + hız)
- $\mathbf{F}_k$ = Durum geçiş matrisi ("fizik kuralları")
- $\mathbf{B}_k$ = Kontrol girdi matrisi (manevra varsa)
- $\mathbf{u}_k$ = Kontrol vektörü (itme kuvveti)
- $\mathbf{H}_k$ = Gözlem matrisi (ne ölçüyoruz?)
- $\mathbf{w}_k$ = Süreç gürültüsü: $\mathbf{w}_k \sim \mathcal{N}(0, \mathbf{Q}_k)$
- $\mathbf{v}_k$ = Ölçüm gürültüsü: $\mathbf{v}_k \sim \mathcal{N}(0, \mathbf{R}_k)$

---

## 2.3 Durum Uzayı Modeli — Yörünge Problemine Uygulama

### Durum Vektörü

Uzay nesnesinin tam durumunu tanımlayan 8 boyutlu vektör:

$$\mathbf{x} = \begin{bmatrix} x \\ y \\ z \\ v_x \\ v_y \\ v_z \\ C_D \\ C_{SRP} \end{bmatrix} \leftarrow \begin{matrix} \text{ECI x pozisyon (km)} \\ \text{ECI y pozisyon (km)} \\ \text{ECI z pozisyon (km)} \\ \text{ECI x hız (km/s)} \\ \text{ECI y hız (km/s)} \\ \text{ECI z hız (km/s)} \\ \text{Sürüklenme katsayısı (birimiz)} \\ \text{SRP katsayısı (birimsiz)} \end{matrix}$$

**Neden $C_D$ ve $C_{SRP}$ duruma dahil?**

Bu katsayılar kesin olarak bilinmez ve zamanla değişebilir. Kalman filtresi, bu parametreleri de ölçümlerden "öğrenerek" tahmin eder. Bu yaklaşıma **Consider Parameters** veya **Augmented State** denir.

### Durum Geçiş Fonksiyonu $f(\mathbf{x}, t)$

Yörünge dinamiği, 2. derece diferansiyel denklem sistemine dayanır:

$$\ddot{\mathbf{r}} = -\frac{\mu}{|\mathbf{r}|^3}\mathbf{r} + \mathbf{a}_{J2} + \mathbf{a}_{drag} + \mathbf{a}_{SRP} + \mathbf{a}_{3rd}$$

Bu, birinci dereceye indirgendiğinde durum denklemi olur:

$$\dot{\mathbf{x}} = f(\mathbf{x}) = \begin{bmatrix} v_x \\ v_y \\ v_z \\ a_x^{total} \\ a_y^{total} \\ a_z^{total} \\ 0 \\ 0 \end{bmatrix}$$

**İvme Bileşenleri:**

$$\mathbf{a}^{total} = \mathbf{a}^{kepler} + \mathbf{a}^{J2} + \mathbf{a}^{drag} + \mathbf{a}^{SRP} + \mathbf{a}^{sun} + \mathbf{a}^{moon}$$

**Kepler İvmesi (İki Cisim):**

$$\mathbf{a}^{kepler} = -\frac{\mu}{r^3}\mathbf{r}, \quad r = \sqrt{x^2 + y^2 + z^2}$$

**J2 İvmesi:**

$$a_x^{J2} = -\frac{3}{2} J_2 \frac{\mu R_E^2}{r^5} x \left(1 - 5\frac{z^2}{r^2}\right)$$

$$a_y^{J2} = -\frac{3}{2} J_2 \frac{\mu R_E^2}{r^5} y \left(1 - 5\frac{z^2}{r^2}\right)$$

$$a_z^{J2} = -\frac{3}{2} J_2 \frac{\mu R_E^2}{r^5} z \left(3 - 5\frac{z^2}{r^2}\right)$$

**Atmosferik Sürüklenme İvmesi:**

$$\mathbf{a}^{drag} = -\frac{1}{2} C_D \frac{A}{m} \rho |\mathbf{v}_{rel}| \mathbf{v}_{rel}$$

$$\mathbf{v}_{rel} = \mathbf{v} - \boldsymbol{\omega}_E \times \mathbf{r}, \quad \boldsymbol{\omega}_E = \begin{bmatrix} 0 \\ 0 \\ 7.2921 \times 10^{-5} \end{bmatrix} \text{rad/s}$$

---

## 2.4 Genişletilmiş Kalman Filtresi (EKF) — Tam Türetme

### Neden EKF?

Standart Kalman Filtresi doğrusal sistemler için çalışır. Yörünge dinamiği ise **şiddetle doğrusal olmayan** bir sistemdir (yer çekimi $1/r^2$'ye bağlı). EKF, doğrusal olmayan fonksiyonları Jacobian matrisleri ile lokal olarak doğrusallaştırır.

### EKF Algoritması — Adım Adım

```
╔══════════════════════════════════════════════════════════════════════╗
║                    EKF PREDICT (TAHMİN) ADIMI                       ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  Girdi: x̂(k-1|k-1), P(k-1|k-1)                                    ║
║                                                                      ║
║  1. Durum tahmini (doğrusal olmayan propagasyon):                    ║
║     x̂(k|k-1) = f(x̂(k-1|k-1), Δt)                                 ║
║     → RK4 entegrasyonu ile orbital dinamik denklemleri çöz          ║
║                                                                      ║
║  2. Jacobian matrisi hesapla:                                        ║
║     F(k) = ∂f/∂x |_{x=x̂(k-1|k-1)}                                ║
║                                                                      ║
║  3. Kovaryans tahmini:                                               ║
║     P(k|k-1) = F(k) · P(k-1|k-1) · F(k)ᵀ + Q(k)                  ║
║                                                                      ║
║  Çıktı: x̂(k|k-1), P(k|k-1)                                        ║
║         (a priori tahmin ve belirsizliği)                            ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

                              │
                              ▼

╔══════════════════════════════════════════════════════════════════════╗
║                    EKF UPDATE (GÜNCELLEME) ADIMI                    ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  Girdi: x̂(k|k-1), P(k|k-1), z(k)                                  ║
║                                                                      ║
║  1. Gözlem Jacobian'ı hesapla:                                       ║
║     H(k) = ∂h/∂x |_{x=x̂(k|k-1)}                                  ║
║                                                                      ║
║  2. İnovasyon (yenilik) hesapla:                                     ║
║     ỹ(k) = z(k) - h(x̂(k|k-1))                                     ║
║     → Ölçüm ile tahmin arasındaki fark                              ║
║                                                                      ║
║  3. İnovasyon kovaryansı:                                            ║
║     S(k) = H(k) · P(k|k-1) · H(k)ᵀ + R(k)                        ║
║                                                                      ║
║  4. Kalman Kazancı:                                                  ║
║     K(k) = P(k|k-1) · H(k)ᵀ · S(k)⁻¹                             ║
║     → "Ölçüme ne kadar güvenelim?" kararı                          ║
║                                                                      ║
║  5. Durum güncelleme:                                                ║
║     x̂(k|k) = x̂(k|k-1) + K(k) · ỹ(k)                             ║
║                                                                      ║
║  6. Kovaryans güncelleme (Joseph Form — sayısal kararlı):           ║
║     I_KH = I - K(k) · H(k)                                         ║
║     P(k|k) = I_KH · P(k|k-1) · I_KHᵀ + K(k) · R(k) · K(k)ᵀ      ║
║                                                                      ║
║  Çıktı: x̂(k|k), P(k|k)                                            ║
║         (a posteriori tahmin ve belirsizliği)                        ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
```

### Jacobian Matrisi $\mathbf{F}$ (Durum Geçişi)

8×8 boyutlu Jacobian matrisi, durum geçiş fonksiyonunun kısmi türevlerinden oluşur:

$$\mathbf{F} = \frac{\partial f}{\partial \mathbf{x}} = \begin{bmatrix} \frac{\partial \dot{x}}{\partial x} & \frac{\partial \dot{x}}{\partial y} & \cdots & \frac{\partial \dot{x}}{\partial C_{SRP}} \\ \frac{\partial \dot{y}}{\partial x} & \frac{\partial \dot{y}}{\partial y} & \cdots & \frac{\partial \dot{y}}{\partial C_{SRP}} \\ \vdots & \vdots & \ddots & \vdots \\ \frac{\partial \dot{C}_{SRP}}{\partial x} & \frac{\partial \dot{C}_{SRP}}{\partial y} & \cdots & \frac{\partial \dot{C}_{SRP}}{\partial C_{SRP}} \end{bmatrix}$$

**Blok yapısı:**

$$\mathbf{F} = \begin{bmatrix} \mathbf{0}_{3 \times 3} & \mathbf{I}_{3 \times 3} & \mathbf{0}_{3 \times 2} \\ \frac{\partial \mathbf{a}}{\partial \mathbf{r}} & \frac{\partial \mathbf{a}}{\partial \mathbf{v}} & \frac{\partial \mathbf{a}}{\partial \mathbf{p}} \\ \mathbf{0}_{2 \times 3} & \mathbf{0}_{2 \times 3} & \mathbf{0}_{2 \times 2} \end{bmatrix}$$

**Gravitasyonel ivmenin pozisyona göre kısmi türevleri:**

$$\frac{\partial a_x^{kep}}{\partial x} = -\frac{\mu}{r^3} + \frac{3\mu x^2}{r^5}$$

$$\frac{\partial a_x^{kep}}{\partial y} = \frac{3\mu xy}{r^5}$$

$$\frac{\partial a_x^{kep}}{\partial z} = \frac{3\mu xz}{r^5}$$

Genel form (gravitasyon Jacobian'ı):

$$\frac{\partial \mathbf{a}^{kep}}{\partial \mathbf{r}} = -\frac{\mu}{r^3}\left(\mathbf{I} - 3\frac{\mathbf{r}\mathbf{r}^T}{r^2}\right)$$

### Gözlem Modeli $h(\mathbf{x})$

Sensör tipine göre farklı gözlem modelleri kullanılır:

**a) Radar Gözlem Modeli (Range, Azimuth, Elevation):**

$$h_{radar}(\mathbf{x}) = \begin{bmatrix} \rho \\ Az \\ El \\ \dot{\rho} \end{bmatrix} = \begin{bmatrix} \sqrt{(x-x_s)^2 + (y-y_s)^2 + (z-z_s)^2} \\ \arctan\left(\frac{y-y_s}{x-x_s}\right) \\ \arcsin\left(\frac{z-z_s}{\rho}\right) \\ \frac{(x-x_s)\dot{x} + (y-y_s)\dot{y} + (z-z_s)\dot{z}}{\rho} \end{bmatrix}$$

Burada $(x_s, y_s, z_s)$ yer istasyonunun ECI koordinatlarıdır.

**b) Optik Gözlem Modeli (Right Ascension, Declination):**

$$h_{optical}(\mathbf{x}) = \begin{bmatrix} \alpha \\ \delta \end{bmatrix} = \begin{bmatrix} \arctan\left(\frac{y-y_s}{x-x_s}\right) \\ \arcsin\left(\frac{z-z_s}{\rho}\right) \end{bmatrix}$$

**c) Doğrudan Kartezyen Gözlem (TLE'den dönüştürülmüş):**

$$h_{cartesian}(\mathbf{x}) = \begin{bmatrix} x \\ y \\ z \end{bmatrix}, \quad \mathbf{H} = \begin{bmatrix} 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \end{bmatrix}$$

---

## 2.5 Gürültü Matrisleri — $\mathbf{Q}$ ve $\mathbf{R}$ Tasarımı

### Süreç Gürültüsü $\mathbf{Q}$ (Sistem Belirsizliği)

$\mathbf{Q}$ matrisi, modelimizin ne kadar iyi olduğunu ifade eder. Mükemmel bir fizik modelimiz olsaydı $\mathbf{Q} = 0$ olurdu, ama gerçek dünyada modellenmemiş etkiler vardır.

**State Noise Compensation (SNC) Yaklaşımı:**

$$\mathbf{Q} = \begin{bmatrix} \frac{\Delta t^3}{3}\sigma_a^2 \mathbf{I}_3 & \frac{\Delta t^2}{2}\sigma_a^2 \mathbf{I}_3 & \mathbf{0} \\ \frac{\Delta t^2}{2}\sigma_a^2 \mathbf{I}_3 & \Delta t \cdot \sigma_a^2 \mathbf{I}_3 & \mathbf{0} \\ \mathbf{0} & \mathbf{0} & \mathbf{Q}_{params} \end{bmatrix}$$

Burada $\sigma_a$ = modellenmeyen ivme belirsizliği (m/s²)

| Yörünge | $\sigma_a$ (m/s²) | Açıklama |
|---|---|---|
| LEO (< 500 km) | $10^{-7}$ – $10^{-6}$ | Atmosfer yoğunluk belirsizliği baskın |
| LEO (500–1000 km) | $10^{-8}$ – $10^{-7}$ | Drag azalır, J2 baskın |
| MEO | $10^{-9}$ – $10^{-8}$ | Pertürbasyonlar küçük |
| GEO | $10^{-9}$ | SRP ve 3. cisim etkisi baskın |

**$C_D$ ve $C_{SRP}$ için $Q$ değerleri:**

$$\mathbf{Q}_{params} = \begin{bmatrix} \sigma_{C_D}^2 \Delta t & 0 \\ 0 & \sigma_{C_{SRP}}^2 \Delta t \end{bmatrix}$$

| Parametre | $\sigma$ / saat | Açıklama |
|---|---|---|
| $C_D$ | 0.01 – 0.1 | Atmosfer modeli belirsizliği |
| $C_{SRP}$ | 0.001 – 0.01 | Yüzey özelliği belirsizliği |

### Ölçüm Gürültüsü $\mathbf{R}$ (Sensör Hatalar)

$\mathbf{R}$ matrisi, sensörlerin doğruluğunu ifade eder. Genelde çapraz (diagonal) matristir.

**Radar Sensörü İçin:**

$$\mathbf{R}_{radar} = \begin{bmatrix} \sigma_\rho^2 & 0 & 0 & 0 \\ 0 & \sigma_{Az}^2 & 0 & 0 \\ 0 & 0 & \sigma_{El}^2 & 0 \\ 0 & 0 & 0 & \sigma_{\dot{\rho}}^2 \end{bmatrix}$$

| Ölçüm | Tipik $1\sigma$ Hata | Birim |
|---|---|---|
| Range ($\rho$) | 5 – 100 m | m |
| Azimuth ($Az$) | 0.005° – 0.05° | derece |
| Elevation ($El$) | 0.005° – 0.05° | derece |
| Range Rate ($\dot{\rho}$) | 0.01 – 1.0 m/s | m/s |

**Optik Teleskop İçin:**

$$\mathbf{R}_{optical} = \begin{bmatrix} \sigma_\alpha^2 & 0 \\ 0 & \sigma_\delta^2 \end{bmatrix}$$

| Ölçüm | Tipik $1\sigma$ Hata |
|---|---|
| Right Ascension ($\alpha$) | 0.5 – 5.0 arcsec |
| Declination ($\delta$) | 0.5 – 5.0 arcsec |

---

## 2.6 Sayısal Propagasyon — RK4 Entegrasyonu

EKF predict adımında $f(\mathbf{x})$ fonksiyonunu entegre etmek için 4. derece Runge-Kutta (RK4) kullanılır.

### RK4 Algoritması

$$\mathbf{k}_1 = \Delta t \cdot f(\mathbf{x}_n, t_n)$$
$$\mathbf{k}_2 = \Delta t \cdot f\left(\mathbf{x}_n + \frac{\mathbf{k}_1}{2}, t_n + \frac{\Delta t}{2}\right)$$
$$\mathbf{k}_3 = \Delta t \cdot f\left(\mathbf{x}_n + \frac{\mathbf{k}_2}{2}, t_n + \frac{\Delta t}{2}\right)$$
$$\mathbf{k}_4 = \Delta t \cdot f(\mathbf{x}_n + \mathbf{k}_3, t_n + \Delta t)$$

$$\mathbf{x}_{n+1} = \mathbf{x}_n + \frac{1}{6}(\mathbf{k}_1 + 2\mathbf{k}_2 + 2\mathbf{k}_3 + \mathbf{k}_4)$$

### Adım Boyutu Seçimi

| Yörünge | Periyot | Önerilen $\Delta t$ | Açıklama |
|---|---|---|---|
| LEO (400 km) | ~92 dk | 10 – 30 s | Hızlı hareket, drag değişken |
| LEO (800 km) | ~101 dk | 30 – 60 s | Orta hız |
| MEO (20000 km) | ~12 saat | 60 – 120 s | Yavaş hareket |
| GEO (36000 km) | ~24 saat | 60 – 300 s | Çok yavaş hareket |

---

## 2.7 Unscented Kalman Filtresi (UKF) — Alternatif Yaklaşım

### EKF'nin Sınırlamaları

EKF, Jacobian matrisi aracılığıyla birinci dereceden (doğrusal) yaklaşım yapar. Yüksek eksentrikli yörüngelerde veya uzun propagasyon sürelerinde bu yaklaşım yetersiz kalabilir.

### UKF Temel Fikri

Jacobian hesaplamak yerine, "sigma noktaları" adı verilen örnekleme noktaları oluşturarak doğrusal olmayan dönüşümü **doğrudan** yapar.

```
    EKF Yaklaşımı                      UKF Yaklaşımı
    
    ┌──────────────┐                   ┌──────────────┐
    │  Doğrusal    │                   │   Sigma      │
    │  yaklaşım    │                   │   Noktaları  │
    │  (Jacobian)  │                   │   ●  ●  ●    │
    │      /       │                   │  ● ● ● ●    │
    │     /        │                   │   ●  ●  ●    │
    │    / ← teğet │                   │              │
    │   /   çizgi  │                   │  Her noktayı │
    │  /           │                   │  ayrı ayrı   │
    │ ● mevcut     │                   │  dönüştür    │
    │   durum      │                   │              │
    └──────────────┘                   └──────────────┘
    
    Hata: 2. derece ve üzeri           Hata: 4. derece ve üzeri
    kaybolur → Büyük hata              kaybolur → Küçük hata
```

### UKF Sigma Noktaları

$n$ boyutlu durum vektörü için $2n + 1$ sigma noktası oluşturulur:

$$\boldsymbol{\chi}_0 = \bar{\mathbf{x}}$$
$$\boldsymbol{\chi}_i = \bar{\mathbf{x}} + \left(\sqrt{(n+\lambda)\mathbf{P}}\right)_i, \quad i = 1, ..., n$$
$$\boldsymbol{\chi}_{i+n} = \bar{\mathbf{x}} - \left(\sqrt{(n+\lambda)\mathbf{P}}\right)_i, \quad i = 1, ..., n$$

Burada:
- $\lambda = \alpha^2(n + \kappa) - n$ (ölçeklendirme parametresi)
- $\alpha$ = Sigma noktalarının yayılımı (tipik: $10^{-3}$ – 1)
- $\kappa$ = İkincil ölçeklendirme (tipik: $3 - n$)
- $\beta$ = Dağılım bilgisi (Gaussian için $\beta = 2$)

### UKF Ağırlıkları

$$W_0^{(m)} = \frac{\lambda}{n + \lambda}$$
$$W_0^{(c)} = \frac{\lambda}{n + \lambda} + (1 - \alpha^2 + \beta)$$
$$W_i^{(m)} = W_i^{(c)} = \frac{1}{2(n + \lambda)}, \quad i = 1, ..., 2n$$

### UKF Predict

1. Sigma noktalarını oluştur: $\boldsymbol{\chi}_i$
2. Her birini doğrusal olmayan fonksiyondan geçir: $\boldsymbol{\gamma}_i = f(\boldsymbol{\chi}_i)$
3. Ağırlıklı ortalama ile tahmin:

$$\hat{\mathbf{x}}_{k|k-1} = \sum_{i=0}^{2n} W_i^{(m)} \boldsymbol{\gamma}_i$$

$$\mathbf{P}_{k|k-1} = \sum_{i=0}^{2n} W_i^{(c)} (\boldsymbol{\gamma}_i - \hat{\mathbf{x}}_{k|k-1})(\boldsymbol{\gamma}_i - \hat{\mathbf{x}}_{k|k-1})^T + \mathbf{Q}$$

### UKF Update

1. Sigma noktalarını gözlem fonksiyonundan geçir: $\boldsymbol{Z}_i = h(\boldsymbol{\gamma}_i)$
2. Tahmin edilen ölçüm:

$$\hat{\mathbf{z}}_{k|k-1} = \sum_{i=0}^{2n} W_i^{(m)} \boldsymbol{Z}_i$$

3. İnovasyon kovaryansı:

$$\mathbf{S}_k = \sum_{i=0}^{2n} W_i^{(c)} (\boldsymbol{Z}_i - \hat{\mathbf{z}})(\boldsymbol{Z}_i - \hat{\mathbf{z}})^T + \mathbf{R}$$

4. Çapraz kovaryans:

$$\mathbf{P}_{xz} = \sum_{i=0}^{2n} W_i^{(c)} (\boldsymbol{\gamma}_i - \hat{\mathbf{x}})(\boldsymbol{Z}_i - \hat{\mathbf{z}})^T$$

5. Kalman kazancı ve güncelleme:

$$\mathbf{K} = \mathbf{P}_{xz} \mathbf{S}_k^{-1}$$
$$\hat{\mathbf{x}}_{k|k} = \hat{\mathbf{x}}_{k|k-1} + \mathbf{K}(\mathbf{z}_k - \hat{\mathbf{z}}_{k|k-1})$$
$$\mathbf{P}_{k|k} = \mathbf{P}_{k|k-1} - \mathbf{K}\mathbf{S}_k\mathbf{K}^T$$

### EKF vs UKF Karşılaştırma

| Özellik | EKF | UKF |
|---|---|---|
| Doğrusallaştırma | Birinci derece (Jacobian) | İkinci derece (Sigma noktaları) |
| Jacobian Gerekli mi? | ✅ Evet (analitik türetilmeli) | ❌ Hayır |
| Hesaplama Maliyeti | Düşük | Orta (2n+1 propagasyon) |
| Doğruluk (düşük eksentriklik) | ✅ İyi | ✅ İyi |
| Doğruluk (yüksek eksentriklik) | ⚠️ Zayıf | ✅ İyi |
| Numerik Kararlılık | Orta | İyi |
| Uygulama Kolaylığı | Orta (Jacobian zor) | Kolay |

**Karar:** 
- Dairesel/düşük eksentrikli yörüngeler (TÜRKSAT, çoğu LEO) → **EKF** yeterli
- Yüksek eksentrikli yörüngeler (HEO, Molniya) → **UKF** tercih et

---

## 2.8 Çoklu Sensör Füzyonu

### Füzyon Stratejileri

```
    ┌──────────┐  ┌──────────┐  ┌──────────┐
    │  Radar   │  │ Teleskop │  │   TLE    │
    │  z_r(k)  │  │  z_o(k)  │  │  z_t(k)  │
    └────┬─────┘  └────┬─────┘  └────┬─────┘
         │             │             │
         ▼             ▼             ▼
    ┌────────────────────────────────────────┐
    │       FÜZYON STRATEJİSİ SEÇİMİ       │
    ├────────────────────────────────────────┤
    │                                        │
    │  A) Sıralı (Sequential) Update         │
    │     → Her sensörü sırayla uygula       │
    │     → Basit ve kararlı                 │
    │                                        │
    │  B) Eşzamanlı (Batch) Update           │
    │     → Tüm ölçümleri tek seferde       │
    │     → Stacked observation vector       │
    │                                        │
    │  C) Federe Kalman                      │
    │     → Her sensör kendi KF'ini çalıştır │
    │     → Sonuçları merkezi KF birleştir   │
    │                                        │
    └────────────────────────────────────────┘
```

### Sıralı Update (Tercih Edilen)

Her sensör ölçümü geldiğinde ayrı bir update adımı çalıştırılır:

```
Predict → Update(Radar) → Update(Teleskop) → Update(TLE) → Predict → ...
```

**Avantajları:**
- Her sensörün farklı $\mathbf{H}$ ve $\mathbf{R}$ matrisleri olabilir
- Numerik olarak kararlı
- Sensörler farklı zamanlarda veri gönderebilir

### Sensör Güvenilirlik Ağırlıklandırma

Zaman içinde sensör performansı değişebilir. İnovasyon dizisi analizi ile otomatik ağırlıklandırma:

**Normalize İnovasyon Karesi (NIS):**

$$\epsilon_k = \tilde{\mathbf{y}}_k^T \mathbf{S}_k^{-1} \tilde{\mathbf{y}}_k$$

Eğer filtre tutarlıysa: $\mathbb{E}[\epsilon_k] = dim(\mathbf{z})$ (ölçüm boyutu)

| $\epsilon_k$ Durumu | Yorum | Aksiyon |
|---|---|---|
| $\epsilon_k \approx dim(\mathbf{z})$ | Filtre tutarlı ✅ | Devam et |
| $\epsilon_k \gg dim(\mathbf{z})$ | Ölçüm kötü veya model yetersiz | $\mathbf{R}$'yi büyüt veya ölçümü reddet |
| $\epsilon_k \ll dim(\mathbf{z})$ | $\mathbf{R}$ çok büyük | $\mathbf{R}$'yi küçült |

### Gate Testi (Outlier Tespiti)

Aşırı sapan ölçümleri reddetmek için inovasyon gate testi:

$$\epsilon_k \leq \chi^2_{n_z, \alpha}$$

| Güven Düzeyi | $\chi^2$ (3 ölçüm) | Açıklama |
|---|---|---|
| %95 | 7.81 | Normal operasyon |
| %99 | 11.34 | Geniş gate |
| %99.9 | 16.27 | Çok geniş gate (başlangıç) |

Gate dışındaki ölçümler reddedilir ve loglanır.

---

## 2.9 Filtre Başlatma (Initialization)

### İlk Durum Tahmini

İlk ölçüm geldiğinde filtreyi nasıl başlatacağız?

**Yöntem 1: TLE'den Başlatma**
```
x̂₀ = SGP4(TLE, t₀)  →  (x, y, z, vx, vy, vz)
P₀ = diag([1², 1², 1², 0.01², 0.01², 0.01², 0.5², 0.1²])
     → Büyük başlangıç belirsizliği (km², (km/s)²)
```

**Yöntem 2: İki Noktalı Gauss Yöntemi (Optik gözlem)**
```
t₁: (α₁, δ₁)  →  İlk gözlem
t₂: (α₂, δ₂)  →  İkinci gözlem (birkaç dakika sonra)
→ Gauss IOD ile başlangıç yörüngesi belirle
```

**Yöntem 3: Üç Noktalı Gibbs Yöntemi (Radar)**
```
t₁: r₁ = (x₁, y₁, z₁)
t₂: r₂ = (x₂, y₂, z₂)  
t₃: r₃ = (x₃, y₃, z₃)
→ Gibbs vektör yöntemi ile v₂ hesapla → Tam durum elde et
```

---

## 2.10 Performans Metrikleri ve Doğrulama

### Filtre Tutarlılık Testleri

**1. NEES (Normalized Estimation Error Squared):**

$$\text{NEES}_k = (\mathbf{x}_k - \hat{\mathbf{x}}_k)^T \mathbf{P}_k^{-1} (\mathbf{x}_k - \hat{\mathbf{x}}_k)$$

Tutarlı filtre için: $\mathbb{E}[\text{NEES}] = n_x$ (durum boyutu = 8)

**2. NIS (Normalized Innovation Squared):**

$$\text{NIS}_k = \tilde{\mathbf{y}}_k^T \mathbf{S}_k^{-1} \tilde{\mathbf{y}}_k$$

**3. Konum RMS Hatası:**

$$\text{RMS}_{pos} = \sqrt{\frac{1}{N}\sum_{k=1}^{N} \left[(x_k-\hat{x}_k)^2 + (y_k-\hat{y}_k)^2 + (z_k-\hat{z}_k)^2\right]}$$

### Hedef Performans Değerleri

| Metrik | Hedef | Açıklama |
|---|---|---|
| Konum RMS (LEO) | < 100 m | Kalman çıktısı |
| Konum RMS (GEO) | < 500 m | Kalman çıktısı |
| Hız RMS | < 0.1 m/s | Kalman çıktısı |
| Gürültü Azaltma | ≥ %60 | Ham verime göre iyileşme |
| NEES Ortalama | 7–9 | 8 durumlu vektör için |
| NIS Ortalama | $n_z \pm 2\sqrt{2n_z/N}$ | İstatistiksel tutarlılık |
| Kovaryans Realizm | %90 içerme | 2σ bound'ları içinde |
| Yakınsama Süresi | < 1 yörünge periyodu | Başlangıçtan kararlı duruma |

---

## 2.11 Checkpoint Özet Tablosu

| Checkpoint | Görev | Durum | Başarı Kriteri |
|---|---|---|---|
| 2.1 | Durum Uzayı Modeli | ⬜ | Birim testlerden geçmesi |
| 2.2 | EKF İmplementasyonu | ⬜ | Gürültüde ≥%60 azalma |
| 2.3 | UKF Alternatifi | ⬜ | Yüksek eksentriklikte EKF'den iyi |
| 2.4 | Çoklu Sensör Füzyonu | ⬜ | Tek sensöre göre ≥%30 iyileşme |
| 2.5 | Q/R Matris Tuning | ⬜ | NEES/NIS tutarlılık testleri |
| 2.6 | Filtre Başlatma | ⬜ | < 1 periyotte yakınsama |
| 2.7 | Outlier Tespiti | ⬜ | Yanlış ölçüm reddetme oranı > %95 |

---

> **Önceki Modül:** [Modül 1 — Veri Edinme](./MODUL_1_VERI_EDINME.md)  
> **Sonraki Modül:** [Modül 3 — ML Yörünge Tahmini](./MODUL_3_ML_TAHMIN.md)
