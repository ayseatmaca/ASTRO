# 📡 MODÜL 1: Veri Edinme ve İyileştirme Katmanı

> **Modül Sahibi:** Veri Mühendisliği Ekibi  
> **Önkoşullar:** Space-Track hesabı, PostgreSQL kurulumu  
> **Tahmini Süre:** 8 hafta (Ay 1–2)  
> **Durum:** ⬜ Başlanmadı

---

## 1.1 Modül Amacı ve Kapsamı

Bu modül, uzay nesnelerine ait ham yörünge verilerini çeşitli kaynaklardan toplayarak, makine öğrenmesi modeline beslenecek formata dönüştürmekten sorumludur. Modülün üç temel görevi vardır:

1. **Veri Toplama:** Space-Track API üzerinden TLE (Two-Line Element) ve VCM (Vector Covariance Message) verilerini periyodik olarak çekmek
2. **Koordinat Dönüşümü:** TLE formatındaki yörünge elemanlarını SGP4 propagatörü ile Kartezyen koordinatlara ($x, y, z, v_x, v_y, v_z$) dönüştürmek
3. **Feature Mühendisliği:** Fiziksel pertürbasyon etkilerini sayısal feature'lar olarak veriye eklemek

### Veri Akışı

```
┌─────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Space-Track     │     │   CelesTrak      │     │   USSTRATCOM     │
│  REST API        │     │   (Yedek)        │     │   (Manuel)       │
└────────┬────────┘     └────────┬─────────┘     └────────┬─────────┘
         │                       │                         │
         ▼                       ▼                         ▼
┌────────────────────────────────────────────────────────────────────┐
│                    VERİ TOPLAMA KATMANI                            │
│  • Rate Limiting  • Retry Logic  • Hata Yönetimi  • Loglama      │
└────────────────────────────────┬───────────────────────────────────┘
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────────┐
│                    SGP4 PROPAGASYON KATMANI                        │
│  • TLE → ECI Dönüşüm  • ECI → ECEF  • Hız Hesaplama             │
└────────────────────────────────┬───────────────────────────────────┘
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────────┐
│                    FEATURE MÜHENDİSLİĞİ                          │
│  • J2 Pertürbasyonu  • SRP  • Atmosferik Drag  • 3. Cisim Etkisi│
└────────────────────────────────┬───────────────────────────────────┘
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────────┐
│                    VERİTABANI KATMANI                              │
│  • PostgreSQL + TimescaleDB  • Hypertable  • ETL Pipeline        │
└────────────────────────────────────────────────────────────────────┘
```

---

## 1.2 TLE (Two-Line Element) Formatı — Derinlemesine Analiz

### TLE Nedir?

TLE, bir uzay nesnesinin yörüngesini tanımlayan standart bir formattır. NORAD (North American Aerospace Defense Command) tarafından geliştirilmiş olup, her uydu için iki satırlık bir veri kümesi içerir.

### TLE Yapısı

```
Line 0: TÜRKSAT 5A
Line 1: 1 53159U 22068A   26088.50000000  .00000012  00000-0  00000-0 0  9991
Line 2: 2 53159   0.0523 264.7320 0001432 217.5200 142.4800  1.00270000 13521
```

### Satır 1 — Alan Açıklamaları

| Kolon | Alan | Açıklama | Örnek |
|---|---|---|---|
| 01 | Satır No | Her zaman "1" | `1` |
| 03-07 | NORAD ID | Katalog numarası | `53159` |
| 08 | Sınıflandırma | U=Unclassified, C=Classified, S=Secret | `U` |
| 10-11 | Fırlatma Yılı | Son 2 hane | `22` |
| 12-14 | Fırlatma Numarası | O yıl kaçıncı fırlatma | `068` |
| 15-17 | Parça Tanımlayıcı | A=Ana gövde, B,C...=Parçalar | `A` |
| 19-20 | Epoch Yılı | TLE'nin geçerli olduğu yıl | `26` |
| 21-32 | Epoch Günü | Yılın kaçıncı günü (ondalıklı) | `088.50000000` |
| 34-43 | Mean Motion Türevi | $\dot{n}/2$ (rev/day²) — Sürüklenme göstergesi | `.00000012` |
| 45-52 | Mean Motion 2. Türevi | $\ddot{n}/6$ (rev/day³) — Genelde sıfır | `00000-0` |
| 54-61 | BSTAR Drag Terimi | Atmosferik sürüklenme katsayısı | `00000-0` |
| 63 | Ephemeris Tipi | 0=SGP4, genelde hep 0 | `0` |
| 65-68 | Element Set No | Kaçıncı güncelleme | `999` |
| 69 | Checksum | Satır doğrulama (mod 10) | `1` |

### Satır 2 — Alan Açıklamaları

| Kolon | Alan | Birim | Açıklama | Örnek |
|---|---|---|---|---|
| 01 | Satır No | - | Her zaman "2" | `2` |
| 03-07 | NORAD ID | - | Line 1 ile aynı | `53159` |
| 09-16 | İnklinasyon ($i$) | Derece | Yörünge eğikliği | `0.0523` |
| 18-25 | RAAN ($\Omega$) | Derece | Çıkış düğümünün rektasensiyonu | `264.7320` |
| 27-33 | Eksentriklik ($e$) | - | Ondalık nokta örtük (0. ile başlar) | `0001432` → `0.0001432` |
| 35-42 | Perigee Argümanı ($\omega$) | Derece | Yörünge düzleminde perigee yönü | `217.5200` |
| 44-51 | Mean Anomali ($M$) | Derece | Perigee'den itibaren uydu konumu | `142.4800` |
| 53-63 | Mean Motion ($n$) | rev/day | Günlük tur sayısı | `1.00270000` |
| 64-68 | Devir Sayısı | - | Fırlatmadan beri toplam tur | `13521` |
| 69 | Checksum | - | Mod 10 doğrulama | - |

### Yörünge Elemanları Arasındaki İlişkiler

```
                         Yörünge Düzlemi
                              │
                    ┌─────────┤
                    │    i (inklinasyon)
                    │         │
                    │    ┌────┘
              Ω (RAAN)  │
                    │    │
              ──────┼────┼──────── Ekvator Düzlemi
                    │    │
                    │    ω (perigee argümanı)
                    │    │
                    │    ●──── M (mean anomali) ──→ Uydu pozisyonu
                    │   Perigee
                    │
                 Çıkış Düğümü
```

**6 Klasik Yörünge Elemanı:**

1. **$a$ (Yarı-büyük eksen):** Yörüngenin boyutunu belirler. Mean Motion'dan hesaplanır: $a = \left(\frac{\mu}{n^2}\right)^{1/3}$
2. **$e$ (Eksentriklik):** Yörüngenin dairesellikten sapması. $e=0$ → daire, $0<e<1$ → elips
3. **$i$ (İnklinasyon):** Yörünge düzleminin ekvator düzlemiyle yaptığı açı
4. **$\Omega$ (RAAN):** Çıkış düğümünün güneş yönüne göre konumu
5. **$\omega$ (Perigee Argümanı):** Perigee noktasının çıkış düğümüne göre pozisyonu
6. **$M$ (Mean Anomali):** Uydunun perigee'den itibaren kat ettiği "ortalama" açı

---

## 1.3 SGP4 Propagasyon Algoritması — Detaylı Açıklama

### SGP4 Nedir?

**Simplified General Perturbations 4 (SGP4)**, NORAD tarafından geliştirilen ve TLE verilerini kullanarak bir uzay nesnesinin herhangi bir andaki konumunu hesaplayan bir analitik yörünge propagasyon algoritmasıdır.

### SGP4 vs Sayısal Propagasyon

| Özellik | SGP4 (Analitik) | Sayısal Propagasyon |
|---|---|---|
| Hız | Çok hızlı (< 1 ms) | Yavaş (saniyeler) |
| Doğruluk (kısa vadeli) | Orta (~1 km) | Yüksek (< 10 m) |
| Doğruluk (uzun vadeli) | Düşük (bozulur) | Yüksek (kararlı) |
| Hesaplama Maliyeti | Düşük | Yüksek |
| Kullanım Alanı | İlk tarama, genel takip | Hassas manevra planlaması |

### SGP4 Algoritma Adımları

```
┌──────────────┐
│ TLE Girdi    │
│ (Yörünge     │
│  Elemanları) │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────────┐
│ ADIM 1: Sabitler ve Başlatma              │
│ • Dünya parametreleri (μ, J2, J3, J4)    │
│ • Epoch'tan itibaren zaman farkı (Δt)    │
│ • Mean Motion düzeltmeleri                │
└──────────────────┬───────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────┐
│ ADIM 2: Seküler Pertürbasyonlar           │
│ • J2 etkisi → Ω ve ω kayması            │
│ • Atmosferik sürüklenme (BSTAR)          │
│ • Mean Anomali güncelleme                 │
└──────────────────┬───────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────┐
│ ADIM 3: Periyodik Pertürbasyonlar         │
│ • Kısa periyot düzeltmeleri               │
│ • Uzun periyot düzeltmeleri               │
│ • Eksentriklik ve inklinasyon güncelleme  │
└──────────────────┬───────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────┐
│ ADIM 4: Kepler Denklemi Çözümü            │
│ • Mean Anomali → Eccentric Anomali       │
│ • Newton-Raphson iterasyonu               │
│ • E = M + e·sin(E) yakınsaması           │
└──────────────────┬───────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────┐
│ ADIM 5: Koordinat Dönüşümü                │
│ • True Anomali (ν) hesaplama             │
│ • Perifocal koordinatlara dönüşüm        │
│ • ECI (Geocentric Inertial) koordinatlar │
│ • Çıktı: r = (x,y,z) ve v = (vx,vy,vz) │
└──────────────────────────────────────────┘
```

### Kepler Denklemi ve Çözümü

Kepler denklemi, yörünge mekaniğinin temel denklemidir:

$$M = E - e \cdot \sin(E)$$

Burada:
- $M$ = Mean Anomali (bilinen, TLE'den gelir)
- $E$ = Eccentric Anomali (bilinmeyen, çözülecek)
- $e$ = Eksentriklik (bilinen, TLE'den gelir)

**Newton-Raphson Çözümü:**

$$E_{n+1} = E_n - \frac{E_n - e \cdot \sin(E_n) - M}{1 - e \cdot \cos(E_n)}$$

Yakınsama kriteri: $|E_{n+1} - E_n| < 10^{-12}$ rad

**True Anomali Hesabı:**

$$\tan\left(\frac{\nu}{2}\right) = \sqrt{\frac{1+e}{1-e}} \cdot \tan\left(\frac{E}{2}\right)$$

### ECI Koordinat Dönüşümü

Perifocal düzlemden ECI'ye dönüşüm rotasyon matrisleri ile yapılır:

$$\mathbf{r}_{ECI} = R_3(-\Omega) \cdot R_1(-i) \cdot R_3(-\omega) \cdot \mathbf{r}_{perifocal}$$

Perifocal koordinatlar:

$$\mathbf{r}_{perifocal} = \begin{bmatrix} r \cos(\nu) \\ r \sin(\nu) \\ 0 \end{bmatrix}, \quad r = \frac{a(1-e^2)}{1 + e\cos(\nu)}$$

Rotasyon matrisleri:

$$R_1(\theta) = \begin{bmatrix} 1 & 0 & 0 \\ 0 & \cos\theta & -\sin\theta \\ 0 & \sin\theta & \cos\theta \end{bmatrix}, \quad R_3(\theta) = \begin{bmatrix} \cos\theta & -\sin\theta & 0 \\ \sin\theta & \cos\theta & 0 \\ 0 & 0 & 1 \end{bmatrix}$$

---

## 1.4 Koordinat Referans Çerçeveleri

### ECI (Earth-Centered Inertial)

```
                    Z (Kuzey Kutbu)
                    │
                    │
                    │      • Uydu (x, y, z)
                    │     /
                    │    /
                    │   /
                    ●──────────── X (Vernal Equinox yönü)
                   / Dünya
                  /
                 /
                Y
```

- **Orijin:** Dünya'nın kütle merkezi
- **X ekseni:** Vernal Equinox (İlkbahar noktası) yönü — sabit
- **Z ekseni:** Kuzey kutbu yönü
- **Y ekseni:** Sağ el kuralı ile tamamlanır
- **Özellik:** İnersiyal (döndürülmüyor), SGP4 çıktısı bu çerçevededir

### ECEF (Earth-Centered Earth-Fixed)

- ECI ile aynı orijin ama **Dünya ile birlikte döner**
- GPS koordinatları bu çerçevededir
- ECI → ECEF dönüşümü: Greenwich Sidereal Time (GST) açısı kadar Z ekseni etrafında rotasyon

$$\mathbf{r}_{ECEF} = R_3(\theta_{GST}) \cdot \mathbf{r}_{ECI}$$

### Geodetik Koordinatlar (Enlem, Boylam, Yükseklik)

ECEF'den geodetik koordinatlara dönüşüm iteratif bir süreçtir (Bowring yöntemi):

$$\lambda = \arctan\left(\frac{y}{x}\right)$$
$$\phi = \arctan\left(\frac{z + e'^2 \cdot b \cdot \sin^3(\beta)}{p - e^2 \cdot a \cdot \cos^3(\beta)}\right)$$
$$h = \frac{p}{\cos(\phi)} - N(\phi)$$

---

## 1.5 Pertürbasyon Feature Mühendisliği — Tam Detay

### Neden Pertürbasyonlar Önemli?

İdeal Kepler yörüngesi sadece iki cisim problemi için geçerlidir. Gerçek dünyada uydunun yörüngesini etkileyen birçok bozucu kuvvet vardır:

```
                    Pertürbasyon Hiyerarşisi (Kuvvet Büyüklüğüne Göre)
    
    LEO (< 2000 km)                          GEO (~36000 km)
    ─────────────────                        ─────────────────
    1. J2 (Dünya basıklığı) ████████████     1. J2              ████████
    2. Atmosferik Drag      ████████         2. Ay/Güneş Çekimi ████████
    3. Güneş/Ay Çekimi      ███              3. SRP             ██████
    4. SRP                  ██               4. Atmosferik Drag ░ (ihmal)
    5. J3, J4...            █                5. J3, J4...       ██
    6. Gelgit Kuvvetleri    ░                6. Dünya Albedosu  █
```

### Feature 1: J2 Pertürbasyonu

Dünya tam bir küre değildir; ekvator bölgesinde şişkin, kutuplarda basıktır. Bu asimetri $J_2$ katsayısı ile modellenir.

**J2 Katsayısı:** $J_2 = 1.08262668 \times 10^{-3}$

**Etkileri:**

1. **RAAN Kayması (Nodal Precession):**

$$\dot{\Omega} = -\frac{3}{2} n J_2 \left(\frac{R_E}{a(1-e^2)}\right)^2 \cos(i)$$

   - $i < 90°$: Batıya kayma (negatif)
   - $i > 90°$: Doğuya kayma (pozitif)
   - $i = 90°$: Kayma yok (kutupsal yörünge)

2. **Perigee Argümanı Kayması (Apsidal Precession):**

$$\dot{\omega} = \frac{3}{2} n J_2 \left(\frac{R_E}{a(1-e^2)}\right)^2 \left(2 - \frac{5}{2}\sin^2(i)\right)$$

   - $i = 63.4°$ veya $i = 116.6°$: Kayma yok (kritik inklinasyon — Molniya yörüngesi)

3. **Mean Motion Düzeltmesi:**

$$\Delta n = \frac{3}{2} n J_2 \left(\frac{R_E}{a(1-e^2)}\right)^2 \left(1 - \frac{3}{2}\sin^2(i)\right) \sqrt{1-e^2}$$

**Feature Vektörü:**

```python
j2_features = {
    'raan_drift_rate_deg_day':     Ω_dot * (180/π) * 86400,   # °/gün
    'arg_perigee_drift_deg_day':   ω_dot * (180/π) * 86400,   # °/gün
    'mean_motion_correction':       Δn,                         # rad/s
    'j2_acceleration_magnitude':    |a_J2|,                     # m/s²
}
```

### Feature 2: Atmosferik Sürüklenme (Drag)

LEO uydular için en kritik pertürbasyon. Yörünge yüksekliği düştükçe etkisi katlanarak artar.

**Sürüklenme Kuvveti:**

$$\mathbf{F}_{drag} = -\frac{1}{2} \rho C_D \frac{A}{m} v_{rel}^2 \hat{v}_{rel}$$

Burada:
- $\rho$ = Atmosfer yoğunluğu (kg/m³) — yüksekliğe bağlı
- $C_D$ = Sürüklenme katsayısı (~2.2 tipik uydu için)
- $A/m$ = Yüzey alanı / kütle oranı (m²/kg)
- $v_{rel}$ = Atmosfere göre bağıl hız (km/s)

**Atmosfer Yoğunluk Modelleri:**

| Model | Karmaşıklık | Doğruluk | Kullanım |
|---|---|---|---|
| Üstel Model | Düşük | Düşük | İlk tahmin |
| Harris-Priester | Orta | Orta | Hızlı hesaplama |
| Jacchia-Bowman 2008 | Yüksek | Yüksek | Operasyonel |
| NRLMSISE-00 | Yüksek | Yüksek | Araştırma standardı |

**Basit Üstel Atmosfer Modeli:**

$$\rho(h) = \rho_0 \exp\left(-\frac{h - h_0}{H}\right)$$

| Yükseklik Bandı (km) | $\rho_0$ (kg/m³) | $H$ (km) |
|---|---|---|
| 200 – 300 | $2.789 \times 10^{-10}$ | 37.105 |
| 300 – 400 | $7.248 \times 10^{-11}$ | 45.546 |
| 400 – 500 | $2.418 \times 10^{-11}$ | 53.628 |
| 500 – 600 | $9.158 \times 10^{-12}$ | 53.298 |
| 600 – 700 | $3.725 \times 10^{-12}$ | 58.515 |
| 700 – 800 | $1.585 \times 10^{-12}$ | 60.828 |

**Güneş Aktivitesinin Etkisi:**

Güneş aktivitesi atmosfer yoğunluğunu dramatik şekilde etkiler:
- **F10.7 İndeksi:** 10.7 cm dalga boyundaki güneş radyo akısı (SFU)
  - Minimum: ~70 SFU → Düşük atmosfer yoğunluğu
  - Maksimum: ~250 SFU → Yüksek atmosfer yoğunluğu (10x fark!)
- **Ap/Kp İndeksi:** Jeomanyetik aktivite → Ani yoğunluk artışları

**Feature Vektörü:**

```python
drag_features = {
    'atmospheric_density':        rho,              # kg/m³
    'drag_acceleration':          a_drag,           # m/s²
    'ballistic_coefficient':      Cd * A / m,       # m²/kg
    'solar_flux_f107':            F107,             # SFU
    'solar_flux_f107_avg':        F107_81day_avg,   # SFU (81 gün ort.)
    'geomagnetic_ap':             Ap,               # nT
    'orbital_decay_rate':         da_dt,            # km/gün
    'estimated_lifetime_days':    lifetime,         # gün
}
```

### Feature 3: Güneş Radyasyon Basıncı (SRP)

Güneş fotonları uydu yüzeyine çarparak küçük ama sürekli bir kuvvet uygular. GEO uydular için önemlidir.

**SRP Kuvveti:**

$$\mathbf{F}_{SRP} = -P_{SR} \cdot C_R \cdot \frac{A_{\odot}}{m} \cdot \frac{AU^2}{|\mathbf{r}_{\odot} - \mathbf{r}|^2} \cdot \hat{r}_{\odot}$$

Burada:
- $P_{SR} = 4.56 \times 10^{-6}$ N/m² (1 AU'da güneş radyasyon basıncı)
- $C_R$ = Yansıtıcılık katsayısı (1.0 = tam emici, 2.0 = tam yansıtıcı)
- $A_{\odot}/m$ = Güneşe bakan yüzey alanı / kütle oranı
- $AU$ = Astronomik birim (149,597,870.7 km)

**Gölge Modeli (Eclipse):**

Uydu Dünya'nın gölgesine girdiğinde SRP sıfırlanır. Silindirik gölge modeli:

```
        Güneş ☀️
           │
           │  ← Güneş ışınları
           │
    ┌──────┴──────┐
    │             │
    │   Yarı      │ ← Penumbra (kısmi gölge)
    │   Gölge     │
    │             │
    │  ┌───────┐  │
    │  │ Tam   │  │ ← Umbra (tam gölge)
    │  │Gölge  │  │
    │  └───────┘  │
    │      🌍     │
    └─────────────┘
```

**Feature Vektörü:**

```python
srp_features = {
    'srp_acceleration':       a_srp,           # m/s²
    'eclipse_fraction':       shadow_func,     # 0.0-1.0
    'cr_coefficient':         Cr,              # yansıtıcılık
    'area_to_mass_ratio':     A_sun / m,       # m²/kg
    'sun_distance_au':        r_sun,           # AU
}
```

### Feature 4: Üçüncü Cisim Çekimi (Ay ve Güneş)

**Pertürbasyon İvmesi:**

$$\mathbf{a}_{3rd} = \mu_{3rd} \left(\frac{\mathbf{r}_{3rd} - \mathbf{r}}{|\mathbf{r}_{3rd} - \mathbf{r}|^3} - \frac{\mathbf{r}_{3rd}}{|\mathbf{r}_{3rd}|^3}\right)$$

| Cisim | $\mu$ (km³/s²) | LEO Etkisi | GEO Etkisi |
|---|---|---|---|
| Güneş | $1.327 \times 10^{11}$ | Düşük | Orta |
| Ay | $4.903 \times 10^{3}$ | Düşük | Yüksek |

**Feature Vektörü:**

```python
third_body_features = {
    'sun_perturbation_acc':    a_sun,        # m/s²
    'moon_perturbation_acc':   a_moon,       # m/s²
    'sun_satellite_angle':     angle_sun,    # derece
    'moon_satellite_angle':    angle_moon,   # derece
    'moon_phase':              phase,        # 0-1 (yeni ay-dolunay)
}
```

---

## 1.6 Veritabanı Şeması — Detaylı Tasarım

### Tablo: `satellites` (Uydu Kataloğu)

```sql
CREATE TABLE satellites (
    norad_id        INTEGER PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    intl_designator VARCHAR(20),
    country         VARCHAR(50) DEFAULT 'TUR',
    launch_date     DATE,
    orbit_type      VARCHAR(10),     -- LEO, MEO, GEO, HEO
    orbit_altitude  DOUBLE PRECISION, -- km
    status          VARCHAR(20),     -- ACTIVE, DECAYED, DEORBITED
    object_type     VARCHAR(30),     -- PAYLOAD, ROCKET_BODY, DEBRIS
    rcs_size        VARCHAR(10),     -- SMALL, MEDIUM, LARGE
    mass_kg         DOUBLE PRECISION,
    cross_section   DOUBLE PRECISION, -- m²
    is_turkish      BOOLEAN DEFAULT FALSE,
    priority        INTEGER DEFAULT 5, -- 1=En yüksek, 10=En düşük
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);
```

### Tablo: `tle_history` (TLE Geçmişi)

```sql
CREATE TABLE tle_history (
    id              BIGSERIAL,
    time            TIMESTAMPTZ NOT NULL,
    norad_id        INTEGER NOT NULL REFERENCES satellites(norad_id),
    tle_line1       VARCHAR(70) NOT NULL,
    tle_line2       VARCHAR(70) NOT NULL,
    epoch           TIMESTAMPTZ NOT NULL,
    inclination     DOUBLE PRECISION,   -- derece
    raan            DOUBLE PRECISION,   -- derece
    eccentricity    DOUBLE PRECISION,
    arg_perigee     DOUBLE PRECISION,   -- derece
    mean_anomaly    DOUBLE PRECISION,   -- derece
    mean_motion     DOUBLE PRECISION,   -- rev/day
    bstar           DOUBLE PRECISION,
    semi_major_axis DOUBLE PRECISION,   -- km
    period_minutes  DOUBLE PRECISION,
    apogee_km       DOUBLE PRECISION,
    perigee_km      DOUBLE PRECISION,
    PRIMARY KEY (time, norad_id)
);

SELECT create_hypertable('tle_history', 'time');
```

### Tablo: `orbital_states` (Kartezyen Durum Vektörleri)

```sql
CREATE TABLE orbital_states (
    time            TIMESTAMPTZ NOT NULL,
    norad_id        INTEGER NOT NULL REFERENCES satellites(norad_id),
    -- Pozisyon (ECI, km)
    x               DOUBLE PRECISION NOT NULL,
    y               DOUBLE PRECISION NOT NULL,
    z               DOUBLE PRECISION NOT NULL,
    -- Hız (ECI, km/s)
    vx              DOUBLE PRECISION NOT NULL,
    vy              DOUBLE PRECISION NOT NULL,
    vz              DOUBLE PRECISION NOT NULL,
    -- Geodetik Koordinatlar
    latitude        DOUBLE PRECISION,
    longitude       DOUBLE PRECISION,
    altitude_km     DOUBLE PRECISION,
    -- Pertürbasyon Feature'ları
    j2_acc          DOUBLE PRECISION,
    drag_acc        DOUBLE PRECISION,
    srp_acc         DOUBLE PRECISION,
    sun_acc         DOUBLE PRECISION,
    moon_acc        DOUBLE PRECISION,
    -- Atmosfer Verileri
    atm_density     DOUBLE PRECISION,
    f107_index      DOUBLE PRECISION,
    ap_index        DOUBLE PRECISION,
    -- Meta
    data_source     VARCHAR(20),  -- TLE, RADAR, OPTICAL
    quality_score   DOUBLE PRECISION,
    PRIMARY KEY (time, norad_id)
);

SELECT create_hypertable('orbital_states', 'time');

-- İndeksler
CREATE INDEX idx_orbital_states_norad ON orbital_states (norad_id, time DESC);
CREATE INDEX idx_orbital_states_altitude ON orbital_states (altitude_km);
```

### Veri Tutma Politikası

```sql
-- 1 yıldan eski verileri otomatik sil
SELECT add_retention_policy('orbital_states', INTERVAL '1 year');
SELECT add_retention_policy('tle_history', INTERVAL '2 years');

-- Sürekli toplama (continuous aggregates) — 1 saatlik özetler
CREATE MATERIALIZED VIEW orbital_states_hourly
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 hour', time) AS bucket,
    norad_id,
    AVG(x) AS avg_x, AVG(y) AS avg_y, AVG(z) AS avg_z,
    AVG(altitude_km) AS avg_altitude,
    MAX(drag_acc) AS max_drag,
    COUNT(*) AS sample_count
FROM orbital_states
GROUP BY bucket, norad_id;
```

---

## 1.7 ETL Pipeline Tasarımı

### Pipeline Akışı

```
┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐
│EXTRACT │    │VALIDATE│    │TRANSFORM│   │ ENRICH │    │  LOAD  │
│        │───▶│        │───▶│        │───▶│        │───▶│        │
│API Call│    │Checksum│    │SGP4    │    │Feature │    │DB Write│
│        │    │Schema  │    │Convert │    │Eng.    │    │        │
└────────┘    └────────┘    └────────┘    └────────┘    └────────┘
     │              │             │             │             │
     ▼              ▼             ▼             ▼             ▼
  raw_tle/      rejected/     cartesian/    enriched/     ✅ Done
  log            log           log           log
```

### Zamanlama Stratejisi

| Görev | Frekans | Açıklama |
|---|---|---|
| TLE Güncellemesi (Türk Uyduları) | Her 2 saat | Yüksek öncelikli |
| TLE Güncellemesi (İlgili Enkaz) | Her 6 saat | İlgili yörünge bandındaki nesneler |
| TLE Güncellemesi (Tam Katalog) | Günlük | Tüm katalog (~20.000 nesne) |
| SGP4 Propagasyon | Her 1 dakika | Gerçek zamanlı pozisyon hesaplama |
| Feature Güncelleme (F10.7, Ap) | Her 3 saat | Uzay hava durumu verileri |
| Veritabanı Bakımı | Haftalık | Vacuum, reindex |

---

## 1.8 Hata Yönetimi ve Güvenilirlik

### Retry Stratejisi

| Hata Türü | Retry Sayısı | Bekleme Süresi | Aksiyon |
|---|---|---|---|
| API Timeout | 3 | Exponential (2s, 4s, 8s) | CelesTrak'a geç |
| Rate Limit (429) | 5 | 60 saniye sabit | Bekle ve tekrar dene |
| Auth Failure (401) | 1 | — | Token yenile |
| Server Error (5xx) | 3 | Exponential (5s, 10s, 20s) | Logla ve alarm |
| Invalid TLE | 0 | — | Reddet ve logla |
| SGP4 Propagation Error | 0 | — | NaN olarak işaretle |

### Veri Kalitesi Kontrolleri

```
✓ TLE checksum doğrulama (mod 10)
✓ Epoch tarihi makul aralıkta mı? (30 gün içinde)
✓ Mean Motion makul aralıkta mı? (0.5 - 16 rev/day)
✓ Eksentriklik 0-1 arasında mı?
✓ İnklinasyon 0-180° arasında mı?
✓ SGP4 çıktısı NaN/Inf içeriyor mu?
✓ Pozisyon dünya yarıçapından büyük mü? (r > 6371 km)
✓ Hız kaçış hızından küçük mü? (v < 11.2 km/s)
✓ Ardışık TLE'ler arasında tutarsızlık var mı?
```

---

## 1.9 Checkpoint Özet Tablosu

| Checkpoint | Görev | Durum | Başarı Kriteri |
|---|---|---|---|
| 1.1 | Space-Track API Entegrasyonu | ⬜ | 24 saat kesintisiz veri çekme |
| 1.2 | SGP4 Koordinat Dönüşümü | ⬜ | Hata < 1 km |
| 1.3 | Veritabanı Kurulumu | ⬜ | 30+ gün veri biriktirme |
| 1.4 | Pertürbasyon Feature'ları | ⬜ | Tahmin doğruluğunda ≥%15 artış |
| 1.5 | ETL Pipeline | ⬜ | Otomatik ve güvenilir çalışma |
| 1.6 | Veri Kalitesi Kontrolleri | ⬜ | Hatalı veri oranı < %0.1 |

---

> **Sonraki Modül:** [Modül 2 — Kalman Filtresi](./MODUL_2_KALMAN_FILTRESI.md)
