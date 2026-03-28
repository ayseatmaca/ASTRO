# 📚 Kaynak Envanteri — Mevcut Proje Kaynakları

> **Son Güncelleme:** 2026-03-28  
> Bu dosya, projede kullanılabilecek tüm mevcut kaynak kodlarını ve referans materyalleri listeler.

---

## 🗂️ Klasör Yapısı

```
ASTRO/
├── SGP4/                          ← SGP4 propagasyon kütüphaneleri
│   ├── python-sgp4-master/        ← ⭐ Ana Python SGP4 kütüphanesi
│   ├── sgp4-master/               ← Rust SGP4 implementasyonu
│   ├── sgp4-master 342/           ← SGP4 varyantı
│   ├── SPG4E/                     ← Çok dilli SGP4 (C++, Java, MATLAB, Fortran, Pascal)
│   ├── SPG23/                     ← Rust SGP4 (detaylı README ile)
│   └── Sgp4-Library-master/       ← Arduino/C++ SGP4 kütüphanesi
│
├── Two_Line_Elements/             ← TLE formatı ve araçları
│   ├── NORAD-TLE-two-line-element-set-format-main/  ← ⭐ TLE Parser (Python)
│   ├── Impact-of-Outdated-TLE.../  ← ⭐ TLE Yaşlanma Analizi (MATLAB)
│   ├── Two_Line_Elements-main/    ← TLE scripts
│   ├── TwoLineElements-master/    ← C# TLE kütüphanesi
│   └── TwoLineElementUtilities-master/  ← TLE araçları
│
├── kalman/                        ← Kalman Filtresi kaynakları
│   ├── Kalman-and-Bayesian-Filters-in-Python-master/  ← ⭐ Kapsamlı KF kitabı (14 bölüm)
│   ├── KalmanNet_TSP-main/        ← ⭐ KalmanNet (Neural Network + Kalman)
│   ├── KalmanFilter-master/       ← C++ Kalman implementasyonu
│   ├── kalman-cpp-master/         ← C++ Kalman varyantı
│   └── kalman-master/             ← Basit Kalman
│
├── MODUL_1_VERI_EDINME.md
├── MODUL_2_KALMAN_FILTRESI.md
├── MODUL_3_ML_TAHMIN.md
├── MODUL_4_CARPISMA_ANALIZI.md
├── MODUL_5_GORSELLESTIRME.md
└── YORUNGE_TEMIZLIGI_PROJE_PLANI.md
```

---

## ⭐ Kritik Kaynaklar — Detaylı Analiz

### 1. python-sgp4-master (Modül 1 için)

| Özellik | Detay |
|---|---|
| **Konum** | `SGP4/python-sgp4-master/` |
| **Dil** | Python |
| **Lisans** | MIT |
| **Kullanım** | TLE → Kartezyen dönüşüm (Modül 1, Checkpoint 1.2) |
| **Ana Dosya** | `sgp4/propagation.py` (74 KB — tam SGP4 algoritması) |
| **API** | `sgp4/api.py` — `Satrec.twoline2rv()` ile TLE okuma |

**Bu kütüphane ne sağlar:**
- TLE verilerini okuyan `io.py` modülü
- SGP4/SDP4 propagasyon algoritmasının tam Python implementasyonu (`propagation.py`)
- WGS72 ve WGS84 yer çekim modelleri (`earth_gravity.py`)
- ECI koordinat çıktısı (pozisyon + hız)
- Doğrulama verileri (`SGP4-VER.TLE`, `tcppver.out`)

**Projede nasıl kullanılır:**
```python
# SGP4/python-sgp4-master/sgp4/api.py referans alınarak
from sgp4.api import Satrec, WGS72
from sgp4.api import jday

sat = Satrec.twoline2rv(line1, line2, WGS72)
jd, fr = jday(2026, 3, 28, 12, 0, 0)
error, position, velocity = sat.sgp4(jd, fr)
# position = (x, y, z) km — ECI
# velocity = (vx, vy, vz) km/s — ECI
```

---

### 2. TLE Yaşlanma Analizi (Modül 1 için)

| Özellik | Detay |
|---|---|
| **Konum** | `Two_Line_Elements/Impact-of-Outdated-TLE.../` |
| **Dil** | MATLAB |
| **Kullanım** | TLE'nin ne kadar süre geçerli kaldığını kanıtlama |
| **Ana Dosya** | `SGP4.m` — Yaşlanma karşılaştırma scripti |

**Bulgular (projemiz için kritik):**

| TLE Yaşı | Tipik Hata |
|---|---|
| 1 Gün | Birkaç km |
| 3 Gün | Onlarca km |
| 6 Gün | Yüzlerce km |

**Projede nasıl kullanılır:**
- Modül 1'de TLE güncelleme frekansını belirlemek için referans
- LEO uyduları için TLE'nin her 2 saatte bir güncellenmesi gerektiğini kanıtlar
- ML modelinin (Modül 3) neden gerekli olduğunu gösteren motivasyon verisi
- `SGP4_Errors.m` dosyası hata büyüme eğrisini çiziyor — bunu raporlarımıza referans olarak ekleyebiliriz

---

### 3. NORAD TLE Parser (Modül 1 için)

| Özellik | Detay |
|---|---|
| **Konum** | `Two_Line_Elements/NORAD-TLE.../` |
| **Dil** | Python |
| **Kullanım** | TLE dosyalarını parse etme ve JSON'a çevirme |
| **Ana Dosya** | `TLE-reader.py` (94 satır) |

**Bu script ne yapıyor:**
- TLE dosyasını okur (uydu adı + 2 satır)
- Her alanı NORAD standardına göre parse eder (kolon bazlı)
- JSON formatında çıktı verir
- Örnek TLE: STARLINK-34935

**Projede nasıl kullanılır:**
- ETL pipeline'ının ilk adımı — ham TLE → yapılandırılmış veri
- `line1_fields` ve `line2_fields` sözlükleri doğrudan Modül 1 Checkpoint 1.1'de kullanılabilir
- Space-Track API'den gelen verileri validate etmek için checksum kontrolü eklenebilir

---

### 4. Kalman and Bayesian Filters in Python (Modül 2 için)

| Özellik | Detay |
|---|---|
| **Konum** | `kalman/Kalman-and-Bayesian-Filters-in-Python-master/` |
| **Dil** | Python (Jupyter Notebooks) |
| **Kullanım** | KF/EKF/UKF öğrenme ve referans implementasyon |
| **Tip** | Tam bir online kitap (Roger Labbe) |

**Bölüm yapısı ve projemize karşılığı:**

| Bölüm | Notebook | Modül İlişkisi |
|---|---|---|
| 01 | g-h Filter | Temel kavram |
| 04 | 1D Kalman Filter | KF temeli |
| 05 | Multivariate Gaussians | Kovaryans anlayışı |
| 06 | Multivariate KF | ⭐ **Modül 2 — Temel KF** |
| 07 | KF Math | Matematiksel türetme |
| 08 | Designing KF | ⭐ **Modül 2 — Q/R tasarımı** |
| 09 | Nonlinear Filtering | EKF motivasyonu |
| 10 | UKF | ⭐ **Modül 2 — UKF implementasyonu** |
| 11 | EKF | ⭐ **Modül 2 — EKF implementasyonu** |
| 12 | Particle Filters | Alternatif yöntem |
| 13 | Smoothing | Post-processing |
| 14 | Adaptive Filtering | ⭐ **Q/R otomatik ayarlama** |
| App-E | Ensemble KF | Büyük sistemler için |

**Projede nasıl kullanılır:**
- EKF ve UKF Python implementasyonlarını doğrudan referans alarak kendi yörünge filtremizi yaz
- `filterpy` kütüphanesinin yazarının kitabı — API tam uyumlu
- Bölüm 8 (Designing KF) → Q/R matris tuning stratejisi
- Bölüm 14 (Adaptive Filtering) → Sensör güvenilirlik ağırlıklandırma

---

### 5. KalmanNet — Neural Network Aided Kalman (Modül 2 + Modül 3 köprüsü)

| Özellik | Detay |
|---|---|
| **Konum** | `kalman/KalmanNet_TSP-main/` |
| **Dil** | Python (PyTorch) |
| **Makale** | [KalmanNet: Neural Network Aided Kalman Filtering](https://arxiv.org/abs/2107.10043) |
| **Kullanım** | Kalman Kazancını (K) nöral ağ ile öğrenme |

**Mimari (KalmanNet_nn.py analizi):**

```
KalmanNet Mimarisi:

Girdi: Ölçüm farkları (obs_diff, obs_innov_diff)
       Durum farkları (fw_evol_diff, fw_update_diff)
                    │
    ┌───────────────┼───────────────┐
    │               │               │
    ▼               ▼               ▼
  FC5 → GRU_Q    FC6             FC7
    │               │               │
    ▼               │               │
  GRU_Q ─────→ GRU_Sigma          │
                    │               │
                    ▼               │
                  FC1 ──────→ GRU_S ← ┘
                                │
                    ┌───────────┤
                    │           │
                    ▼           ▼
                  FC2 (Kalman Gain)
                    │
         ┌──────────┤
         │          │
         ▼          ▼
       FC3        FC4 (→ GRU_Sigma hidden state güncelle)
```

**Anahtar konseptler:**
- 3 adet GRU: Q (süreç gürültüsü), Sigma (kovaryans), S (inovasyon kovaryansı) takibi
- 7 adet FC katmanı: Forward + Backward akış
- **Kalman Kazancı nöral ağ tarafından tahmin edilir** — klasik $K = P H^T S^{-1}$ yerine
- Batched processing desteği (verimlilik)

**Projede nasıl kullanılır:**
- Modül 2 ve Modül 3 arasında **hibrit model** olarak
- Klasik EKF ile KalmanNet performans karşılaştırması
- Q ve R matrisleri bilinmediğinde → KalmanNet bunları otomatik öğrenir
- Yörünge tahmini için `main_linear_CA.py` şablonu (Constant Acceleration modeli) doğrudan adapte edilebilir

---

### 6. SPG4E — Çok Dilli SGP4 Referans İmplementasyonu

| Özellik | Detay |
|---|---|
| **Konum** | `SGP4/SPG4E/` |
| **Diller** | C++, Java, MATLAB, Fortran, Pascal |
| **Kullanım** | Referans doğrulama ve çapraz platform |
| **Doğrulama** | `SGP4-VER.TLE` + `sgp4_CodeReadme.pdf` |

**Projede nasıl kullanılır:**
- Python implementasyonumuzu doğrulamak için C++/MATLAB versiyonlarını karşılaştırma referansı olarak kullan
- `SGP4-VER.TLE` doğrulama veri seti — modelimizin çıktısını bu referansla karşılaştır
- `sgp4_CodeReadme.pdf` — SGP4 algoritmasının resmi dokümantasyonu

---

## 📋 Kaynak → Modül Eşleme Matrisi

| Kaynak | M1 (Veri) | M2 (Kalman) | M3 (ML) | M4 (Çarpışma) | M5 (Görs.) |
|---|---|---|---|---|---|
| python-sgp4-master | ⭐ Ana | — | — | — | — |
| TLE-reader.py | ⭐ Parser | — | — | — | — |
| TLE Yaşlanma Analizi | ⭐ Motivasyon | — | ⭐ ML Motivasyon | — | — |
| KF Kitap (14 bölüm) | — | ⭐ Referans | — | — | — |
| KalmanNet | — | ⭐ Hibrit Model | ⭐ NN-Kalman | — | — |
| SPG4E (çok dilli) | ✓ Doğrulama | — | — | — | — |
| SGP4 Rust (sgp4-master) | ✓ Performans | — | — | — | — |
| SGP4 Arduino (Library) | — | — | — | — | ✓ Edge |
| KalmanFilter C++ | — | ✓ Embedded | — | — | — |
| kalman-cpp | — | ✓ Embedded | — | — | — |

---

## 🔧 Önerilen Kullanım Sırası

### Aşama 1 (Ay 1–2): Modül 1 — Veri Edinme
1. `NORAD-TLE.../TLE-reader.py` → TLE parsing mantığını adapte et
2. `python-sgp4-master/sgp4/` → SGP4 propagasyonu doğrudan kullan
3. `Impact-of-Outdated-TLE.../SGP4_Errors.m` → TLE güncelleme frekansı kararı

### Aşama 2 (Ay 3–4): Modül 2 — Kalman Filtresi
4. `Kalman-and-Bayesian-Filters.../06-Multivariate-KF.ipynb` → KF temeli
5. `Kalman-and-Bayesian-Filters.../11-Extended-KF.ipynb` → EKF implementasyonu
6. `Kalman-and-Bayesian-Filters.../10-UKF.ipynb` → UKF implementasyonu
7. `KalmanNet_TSP.../KNet/KalmanNet_nn.py` → Hibrit KalmanNet denemesi

### Aşama 3 (Ay 5–7): Modül 3 — ML Tahmin
8. `KalmanNet_TSP.../main_linear_CA.py` → Pipeline yapısını referans al
9. `KalmanNet_TSP.../Pipelines/` → Eğitim pipeline şablonu
10. Kendi Bi-LSTM ve Informer modellerini yaz (yeni kod)

### Aşama 4–5 (Ay 8–12): Modül 4–5
11. Çarpışma analizi ve dashboard için yeni kod geliştir
12. `SPG4E/` → Cross-validation için referans çıktılar kullan

---

> **Not:** Tüm kaynaklar MIT veya benzeri açık lisanslardır. Ticari kullanım kısıtlaması yoktur. Yine de her kaynak için lisans dosyasını referans vermek iyi pratiktir.
