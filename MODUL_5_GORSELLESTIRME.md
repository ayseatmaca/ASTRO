# 📊 MODÜL 5: Görselleştirme ve Kontrol Paneli

> **Modül Sahibi:** Frontend / Veri Görselleştirme Ekibi  
> **Önkoşullar:** Modül 1-4 tamamlanmış, API backend hazır  
> **Tahmini Süre:** 12 hafta (Ay 10–12)  
> **Durum:** ⬜ Başlanmadı

---

## 5.1 Modül Amacı ve Kapsamı

Bu modül, tüm sistemi operatörlerin etkin bir şekilde kullanabileceği görsel bir arayüzle sunmaktan sorumludur:

1. **3D Dünya Görünümü:** CesiumJS ile uyduları ve enkazları gerçek zamanlı göster
2. **Kontrol Paneli (Dashboard):** İstatistikler, alarmlar ve grafikler
3. **Alarm Arayüzü:** Yakın geçiş olaylarının visual alert'leri
4. **Raporlama:** Otomatik PDF rapor üretimi

### Kullanıcı Profilleri

| Kullanıcı | İhtiyaç | Erişim Seviyesi |
|---|---|---|
| **Uçuş Operatörü** | Anlık durum, alarmlar, manevra onay | Tam erişim |
| **Analist** | Detaylı veriler, grafikler, geçmiş analiz | Tam erişim |
| **Yönetici** | Özet raporlar, istatistikler | Salt okunur |
| **Dış İzleyici** | Genel durum görünümü | Sınırlı |

---

## 5.2 Dashboard Genel Yerleşim Tasarımı

### Ana Ekran Layout

```
┌────────────────────────────────────────────────────────────────────┐
│  🛰️ Yörünge Temizliği — Uzay Çöpü Takip Sistemi     🔔 3  👤 Admin│
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐│
│  │  AKTİF   │ │  TAKİP   │ │  YAKIN   │ │  KRİTİK  │ │  SON     ││
│  │  UYDU    │ │  ENKAZ   │ │  GEÇİŞ   │ │  ALARM   │ │  MANEVRA ││
│  │    6     │ │  1,247   │ │   23     │ │    3     │ │  2 gün   ││
│  │  ▲ +0   │ │  ▲ +12  │ │  ▼ -5   │ │  ▲ +1   │ │  önce    ││
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘│
│                                                                    │
│  ┌─────────────────────────────────┐ ┌──────────────────────────┐ │
│  │                                 │ │   YAKIN GEÇİŞ TABLOSU   │ │
│  │         CesiumJS                │ │                          │ │
│  │       3D DÜNYA                  │ │ Uydu    Enkaz   Pc   ⚠️ │ │
│  │       GÖRÜNÜMÜ                  │ │ ────────────────────── │ │
│  │                                 │ │ T5A    COS2251 2×10⁻⁴ 🔴│ │
│  │    🌍 ← İnteraktif globe      │ │ İMECE  SL-16   8×10⁻⁶ 🟠│ │
│  │    ← Uydu yörüngeleri          │ │ GK-1   Fengyun 3×10⁻⁶ 🟠│ │
│  │    ← Enkaz bulutu              │ │ T5B    NOAA15  1×10⁻⁷ 🟡│ │
│  │    ← Risk bölgeleri            │ │ GK-2   CZ-2C   5×10⁻⁸ 🟢│ │
│  │                                 │ │                          │ │
│  │  [Zoom]  [Track]  [Timeline]   │ │ 1/5 sayfa    [Detay →]  │ │
│  └─────────────────────────────────┘ └──────────────────────────┘ │
│                                                                    │
│  ┌─────────────────────────────────┐ ┌──────────────────────────┐ │
│  │   MİSS DİSTANCE ZAMAN SERİSİ  │ │   RİSK DAĞILIMI (PIE)   │ │
│  │                                 │ │                          │ │
│  │   km                            │ │      🟢 Düşük: 156      │ │
│  │   │ ╲    ╱╲                     │ │      🟡 Orta: 42        │ │
│  │   │  ╲  ╱  ╲    ╱╲             │ │      🟠 Yüksek: 5       │ │
│  │   │   ╲╱    ╲  ╱  ╲            │ │      🔴 Kritik: 3       │ │
│  │   │          ╲╱    ╲           │ │                          │ │
│  │   └──────────────── t           │ │   [Son 24h] [7 gün]    │ │
│  └─────────────────────────────────┘ └──────────────────────────┘ │
│                                                                    │
│  [📄 Rapor]  [⚙️ Ayarlar]  [📊 Analiz]  [📁 Geçmiş]  [❓ Yardım]│
└────────────────────────────────────────────────────────────────────┘
```

### Yan Menü — Uydu Detay Paneli

```
┌──────────────────────────┐
│  🛰️ TÜRKSAT 5A            │
│  NORAD: 53159             │
│  Durum: ● AKTİF          │
├──────────────────────────┤
│                          │
│  Yörünge Bilgileri       │
│  ──────────────────      │
│  Tip:      GEO           │
│  Yükseklik: 35,786 km    │
│  İnklinasyon: 0.05°      │
│  Periyot: 23h 56m        │
│  RAAN: 264.73°           │
│  Eksentriklik: 0.00014   │
│                          │
│  Anlık Konum (ECI)       │
│  ──────────────────      │
│  x:  -21,467.3 km        │
│  y:   35,212.8 km        │
│  z:      -32.1 km        │
│  v: 3.075 km/s           │
│                          │
│  Alt-nokta               │
│  ──────────────────      │
│  Lat:  0.04° N           │
│  Lon: 31.0° E            │
│  (Türkiye üzeri ✓)       │
│                          │
│  Risk Durumu             │
│  ──────────────────      │
│  Aktif Yaklaşma: 3       │
│  En Yakın TCA: 18.7h     │
│  Max Pc: 2.3×10⁻⁴ 🔴    │
│                          │
│  [YÖRÜNGEYİ TAKİP ET]   │
│  [MANEVRA GEÇMİŞİ]      │
│  [TAHMİN GRAFİĞİ]       │
│                          │
└──────────────────────────┘
```

---

## 5.3 CesiumJS 3D Dünya Görünümü — Detaylı Tasarım

### Görünüm Katmanları

```
    Katman Hiyerarşisi (Aşağıdan yukarıya)
    
    ┌──────────────────────────────────────────┐
    │  Katman 6: UI Overlay (Etiketler, Info)  │  ← Her zaman görünür
    ├──────────────────────────────────────────┤
    │  Katman 5: Alarm Göstergeleri             │  ← Kritik olay varsa
    ├──────────────────────────────────────────┤
    │  Katman 4: Yaklaşma Çizgileri             │  ← Seçili yaklaşmalar
    ├──────────────────────────────────────────┤
    │  Katman 3: Uydu Yörüngeleri               │  ← Her zaman görünür
    ├──────────────────────────────────────────┤
    │  Katman 2: Enkaz Bulutu (Point Cloud)    │  ← Toggle ile aç/kapa
    ├──────────────────────────────────────────┤
    │  Katman 1: Dünya Modeli (Terrain)        │  ← Temel katman
    └──────────────────────────────────────────┘
```

### Uydu Gösterimi

Her Türk uydusu ayrı renkle gösterilir:

| Uydu | Renk | İkon |
|---|---|---|
| TÜRKSAT 5A | Cyan (#00FFFF) | 🛰️ |
| TÜRKSAT 5B | Aquamarine (#7FFFD4) | 🛰️ |
| İMECE | Lime (#00FF00) | 🛰️ |
| GÖKTÜRK-1 | Gold (#FFD700) | 🛰️ |
| GÖKTÜRK-2 | Orange (#FFA500) | 🛰️ |

### Yörünge Çizimi

Her uydu için:
- **Trail (geçmiş):** Son 1 yörünge periyodu, soluk renk, opacity azalan
- **Lead (gelecek):** Sonraki 1 yörünge periyodu, parlak renk
- **Çizgi kalınlığı:** 2 px (normal), 4 px (seçili)
- **Glow efekti:** `PolylineGlowMaterial` ile neon efekt

### Enkaz Bulutu Gösterimi

20.000+ enkaz parçasını performanslı göstermek için farklı teknikler:

| Nesne Sayısı | Teknik | FPS |
|---|---|---|
| < 1.000 | Individual entities | 60 |
| 1.000 – 10.000 | Point primitives (batch) | 60 |
| 10.000 – 50.000 | Point cloud (WebGL) | 45-60 |
| > 50.000 | LOD (Level of Detail) + clustering | 60 |

**Renk Kodlaması (Enkaz):**

| Risk Seviyesi | Renk | Boyut |
|---|---|---|
| Güvenli | Gri, %40 opacity | 2 px |
| İzleme | Sarı, %60 opacity | 3 px |
| Yüksek Risk | Turuncu, %80 opacity | 4 px |
| Kritik | Kırmızı, yanıp sönen | 6 px |

### Yaklaşma Gösterimi

İki nesne birbirine yaklaştığında:

```
    Uydu ●─────────── Kırmızı kesikli çizgi ───────────● Enkaz
         │                                              │
         │            TCA noktası                       │
         │               ⊗ (yanıp sönen)               │
         │            [0.87 km]                         │
         │            [Pc: 2.3×10⁻⁴]                   │
         │                                              │
```

- İki nesne arasında kırmızı kesikli çizgi
- TCA noktasında yanıp sönen sembol
- Üzerinde miss distance ve Pc bilgisi
- Tıklanınca detay popup açılır

### Zaman Kontrolü

```
    ◀◀  ◀  ▶  ▶▶   ⏸   |  ──────●──────────── |  🕐 2026-03-28 14:23 UTC
    -4x -1x +1x +4x Dur    ← Zaman slider →       Anlık saat
    
    [Şimdi]  [TCA'ya Git]  [Geçmiş 24h]  [Gelecek 48h]
```

---

## 5.4 Detaylı Grafik ve Çizelgeler

### Grafik 1: Miss Distance Zaman Serisi

```
    Miss Distance (km)   — TÜRKSAT 5A vs COSMOS 2251 Debris
    │
  50│                                                    
    │  ╲                                                 
  40│   ╲                                                
    │    ╲         ╱╲                                    
  30│     ╲       ╱  ╲                                   
    │      ╲     ╱    ╲                                  
  20│       ╲   ╱      ╲         ╱╲                     
    │        ╲ ╱        ╲       ╱  ╲                    
  10│         ╳          ╲     ╱    ╲                   
    │        ╱ ╲          ╲   ╱      ╲                  
   5│───────╱───╲──────────╲─╱────────╲── Eşik (5 km)  
    │      ╱     ╲          ●          ╲               
   1│     ╱       ╲       TCA          ╲              
    │                    (0.87 km)                      
    ├──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬── Saat          
    0  4  8  12 16 20 24 28 32 36 40 44 48              
    
    ── Gerçek mesafe
    ── ML tahmini
    ▓▓ Belirsizlik bandı (2σ)
    ── Alarm eşiği
```

### Grafik 2: Çarpışma Olasılığı Zaman Serisi

```
    -log₁₀(Pc)    — Yüksek = Güvenli, Düşük = Tehlikeli
    │
   9│  ──────────────────────────────                    
    │                               ╲                    
   8│                                ╲                   
    │                                 ╲                  
   7│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─╲─ ─ Güvenli     
    │                                   ╲               
   6│                                    ╲              
    │                                     ╲             
   5│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ╲ ─ Dikkat   
    │                                      ╲            
   4│  ═══════════════════════════════════════ KRİTİK   
    │                                        ● TCA      
   3│                                      (Pc=2×10⁻⁴) 
    │                                                    
    ├──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬── Saat          
    0  4  8  12 16 20 24 28 32 36 40 44 48              
```

### Grafik 3: Kovaryans Elipsleri (B-Plane Görünümü)

```
    η (km)
    │
  5 │        ╱────────╲
    │      ╱    C₂      ╲
  3 │    ╱   (Enkaz)      ╲
    │   │                   │
  1 │   │       ●           │
    │   │     Miss          │
  0 ├───┼─────Point─────────┼────── ξ (km)
    │   │                   │
 -1 │   │  ╱─────╲         │
    │   │ ╱  C₁    ╲       │
 -3 │    ╱ (Uydu)    ╲    ╱
    │    ╲             ╲╱
 -5 │     ╲           ╱
    │      ╲─────────╱
    │
    └──┬──┬──┬──┬──┬──┬──── ξ (km)
      -5 -3 -1  1  3  5
    
    C₁ = Uydu kovaryans elipsi (2σ)
    C₂ = Enkaz kovaryans elipsi (2σ)
    ◉  = Hard-body (çarpışma) yarıçapı
    ●  = Miss point (en yakın nokta)
```

### Grafik 4: Uydu Yükseklik Profili

```
    Yükseklik (km)
    │
  700│  ╱╲    ╱╲    ╱╲    ╱╲    ╱╲    ╱╲    ╱╲
     │ ╱  ╲  ╱  ╲  ╱  ╲  ╱  ╲  ╱  ╲  ╱  ╲  ╱  ╲
  680│╱    ╲╱    ╲╱    ╲╱    ╲╱    ╲╱    ╲╱    ╲╱
     │                                           
  660│  ← İMECE yörünge yüksekliği                
     │     (680 km nominal, ±20 km salınım)       
     │                                            
  640│                                            
     │
     ├──┬──┬──┬──┬──┬──┬──┬──┬──┬── Zaman (periyot)
     0  1  2  3  4  5  6  7  8  9  10
```

### Grafik 5: ML Model Performans Takibi

```
    MSE (km)     Model Performans Dashboard
    │
  2.0│  
    │                              ╳ SGP4
  1.5│                           ╳
    │                         ╳ 
  1.0│                       ╳
    │  ── ── ── ── ── ── ── ── ──  Hedef: 0.5 km
  0.5│                ● ● ● ● ●── Bi-LSTM (stabil)
    │          ○ ○ ○ ○ ○ ○ ○ ○──── Informer
  0.1│    ●──●──●
    │  ●──● 
    ├──┬──┬──┬──┬──┬──┬──┬──┬── Tahmin Ufku (saat)
    0  4  8  12 16 20 24 36 48
```

---

## 5.5 Alarm Arayüzü Detayları

### Alarm Banner Tasarımı

**Kritik Alarm (Seviye 4):**

```
╔══════════════════════════════════════════════════════════════════╗
║  🔴 ⚠️  KRİTİK ALARM — TÜRKSAT 5A   ⚠️ 🔴   [×] kapat       ║
║                                                                  ║
║  Çarpışma Riski: Pc = 2.3 × 10⁻⁴                               ║
║  TCA: 2026-04-15 14:23 UTC (18 saat 42 dakika kaldı)           ║
║  Miss Distance: 0.87 km  |  Bağıl Hız: 12.4 km/s              ║
║                                                                  ║
║  [🔍 DETAY]  [📋 MANEVRA PLANI]  [✅ ONAYLA]  [⏰ ERTELE]     ║
╚══════════════════════════════════════════════════════════════════╝

  ↑ Kırmızı arka plan, 2 saniyede bir yanıp söner
  ↑ Ses alarm eşlik eder (opsiyonel)
```

**Yüksek Risk Alarm (Seviye 3):**

```
┌──────────────────────────────────────────────────────────────────┐
│  🟠 YAKIN GEÇİŞ — İMECE  |  Pc = 8 × 10⁻⁶  |  TCA: 32h     │
│  Miss: 2.3 km  |  [DETAY]                                      │
└──────────────────────────────────────────────────────────────────┘

  ↑ Turuncu arka plan, sabit (yanıp sönmez)
```

### Alarm Detay Modal Penceresi

```
┌──────────────────────────────────────────────────────────────────┐
│  ⚠️  Yakın Geçiş Detayı                                  [×]   │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─── Nesne Bilgileri ─────────────────────────────────────┐    │
│  │                                                          │    │
│  │  BİRİNCİL: TÜRKSAT 5A (53159)        İKİNCİL: COS2251  │    │
│  │  Tip: Aktif GEO Uydu                  Tip: Enkaz         │    │
│  │  Kütle: 4,500 kg                      Kütle: ~100 kg     │    │
│  │  Boyut: 3.5 m                         Boyut: ~0.5 m      │    │
│  │                                                          │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌─── Yaklaşma Parametreleri ──────────────────────────────┐    │
│  │                                                          │    │
│  │  TCA:              2026-04-15 14:23:47 UTC              │    │
│  │  Miss Distance:    0.872 km                             │    │
│  │  Bağıl Hız:        12.41 km/s                           │    │
│  │  Pc (Chan):        2.31 × 10⁻⁴                         │    │
│  │  Pc (Monte Carlo): 2.18 × 10⁻⁴ (10⁶ sample)          │    │
│  │  Güven Aralığı:    [1.9, 2.7] × 10⁻⁴ (%95)            │    │
│  │                                                          │    │
│  │  Kovaryans Bilgisi:                                     │    │
│  │  σ_along: 1.23 km  σ_cross: 0.15 km  σ_radial: 0.08 km│    │
│  │                                                          │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌─── Manevra Seçenekleri ─────────────────────────────────┐    │
│  │                                                          │    │
│  │  Seçenek │ Δv(m/s)│Yakıt(kg)│  Sonuç  │ Yeni Pc       │    │
│  │  ────────┼────────┼─────────┼─────────┼──────────────  │    │
│  │  A(min)  │  0.05  │   0.1   │ 5.2 km  │ 3×10⁻⁶       │    │
│  │  B(orta) │  0.12  │   0.24  │ 12.8 km │ 8×10⁻⁸       │    │
│  │  C(öner.)│  0.15  │   0.3   │ 15.3 km │ 2×10⁻⁸  ★   │    │
│  │  D(güv.) │  0.30  │   0.6   │ 28.5 km │ <10⁻⁹        │    │
│  │                                                          │    │
│  │  [SEÇ: A]  [SEÇ: B]  [SEÇ: C ★]  [SEÇ: D]            │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌─── Zaman Serisi Grafik ─────────────────────────────────┐    │
│  │  [Miss Distance]  [Pc]  [B-Plane]  [3D Yörünge]        │    │
│  │                                                          │    │
│  │  (İlgili grafik burada gösterilir)                      │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌─── Aksiyon ─────────────────────────────────────────────┐    │
│  │                                                          │    │
│  │  [📋 RAPOR OLUŞTUR]  [📧 E-POSTA GÖNDER]               │    │
│  │  [✅ MANEVRA ONAYLA]  [❌ İPTAL ET]                     │    │
│  │                                                          │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 5.6 Bildirim Kanalları

### Çok Kanallı Bildirim Matrisi

| Alarm Seviyesi | Dashboard | E-posta | SMS | Webhook (Slack) | Telefon |
|---|---|---|---|---|---|
| Seviye 0 (Güvenli) | Log | — | — | — | — |
| Seviye 1 (İzleme) | Banner | Günlük özet | — | — | — |
| Seviye 2 (Dikkat) | Banner | Anında | — | ✅ | — |
| Seviye 3 (Yüksek) | Tam ekran | Anında | ✅ | ✅ | — |
| Seviye 4 (Kritik) | Yanıp sönen | Anında | ✅ | ✅ | ✅ |

### E-posta Şablonu

```
Konu: ⚠️ [SEVİYE 3] Yakın Geçiş Alarmı — TÜRKSAT 5A

Tarih: 2026-04-14 20:00 UTC
Sistem: Yörünge Temizliği — Uzay Çöpü Takip

═══════════════════════════════════════════

YAKIN GEÇİŞ DETAYI:

Birincil:     TÜRKSAT 5A (NORAD: 53159)
İkincil:      COSMOS 2251 Debris (#34567)
TCA:          2026-04-15 14:23:47 UTC
Kalan Süre:   18 saat 23 dakika
Miss Distance: 0.87 km
Çarpışma Olasılığı: Pc = 2.3 × 10⁻⁴

ÖNERILEN AKSİYON:
In-Track manevra: Δv = 0.15 m/s
Manevra zamanı: 2026-04-15 08:23 UTC (TCA - 6h)
Tahmini yakıt: 0.3 kg

═══════════════════════════════════════════

Dashboard: https://stm.example.com/conjunction/12345
Bu alarm otomatik oluşturulmuştur.
```

### Webhook Payload (Slack / Teams)

```json
{
  "type": "conjunction_alert",
  "severity": "HIGH",
  "level": 3,
  "timestamp": "2026-04-14T20:00:00Z",
  "primary": {
    "name": "TÜRKSAT 5A",
    "norad_id": 53159
  },
  "secondary": {
    "name": "COSMOS 2251 Debris",
    "norad_id": 34567
  },
  "tca": "2026-04-15T14:23:47Z",
  "miss_distance_km": 0.872,
  "relative_velocity_km_s": 12.41,
  "collision_probability": 2.31e-4,
  "recommended_maneuver": {
    "delta_v_m_s": 0.15,
    "direction": "in-track",
    "time": "2026-04-15T08:23:00Z",
    "result_miss_km": 15.3,
    "result_pc": 2e-8
  },
  "dashboard_url": "https://stm.example.com/conjunction/12345"
}
```

---

## 5.7 Raporlama Sistemi

### Günlük Otomatik Rapor (Daily Report)

```
╔══════════════════════════════════════════════════════════════╗
║           GÜNLÜK UZAY DURUMU RAPORU                         ║
║           2026-04-14                                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  1. GENEL DURUM                                             ║
║  ─────────────                                              ║
║  Aktif Türk Uydusu:        6                                ║
║  İzlenen Uzay Nesnesi:     21,347                           ║
║  Yeni Kataloglanan Nesne:  +12 (son 24 saat)               ║
║  Çürüyen Nesne:            -3 (atmosfere giriş)            ║
║                                                              ║
║  2. YAKIN GEÇİŞ ÖZETİ                                      ║
║  ─────────────────────                                      ║
║  Toplam Yaklaşma Olayı:    23                               ║
║  Kritik (Seviye 4):        0                                ║
║  Yüksek (Seviye 3):        1  ← TÜRKSAT 5A detayı aşağıda ║
║  Dikkat (Seviye 2):        4                                ║
║  İzleme (Seviye 1):        18                               ║
║                                                              ║
║  3. KRİTİK OLAY DETAYI                                     ║
║  ─────────────────────                                      ║
║  Olay #1:                                                    ║
║  TÜRKSAT 5A ↔ COSMOS 2251 Debris                            ║
║  TCA: 2026-04-15 14:23 UTC | Pc: 2.3×10⁻⁴                 ║
║  Miss: 0.87 km | Bağıl hız: 12.4 km/s                      ║
║  Durum: Manevra planlanıyor                                  ║
║                                                              ║
║  4. MODEL PERFORMANSI                                        ║
║  ─────────────────────                                      ║
║  ML Tahmin MSE (24h): 0.28 km ✅ (hedef: < 0.5 km)         ║
║  Kalman Filtre Tutarlılığı: NEES = 7.8 ✅                   ║
║  Veri Kalitesi: %99.7 ✅                                    ║
║                                                              ║
║  5. SİSTEM SAĞLIĞI                                          ║
║  ─────────────────                                          ║
║  API Uptime: %99.99                                          ║
║  DB Boyutu: 24.3 GB / 100 GB                                ║
║  Son TLE Güncellemesi: 2 saat önce                          ║
║  GPU Kullanımı: %45                                          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Manevra Raporu

Bir manevra gerçekleştirildiğinde detaylı rapor:

```
═══ MANEVRA RAPORU #2026-042 ═══

Tarih: 2026-04-15 08:23:00 UTC
Uydu: TÜRKSAT 5A (NORAD: 53159)

MANEVRA ÖNCESİ:
  Hedef Enkaz: COSMOS 2251 Debris (#34567)
  TCA: 2026-04-15 14:23:47 UTC  
  Miss Distance: 0.87 km
  Pc: 2.31 × 10⁻⁴

UYGULANAN MANEVRA:
  Tip: In-Track
  Δv: 0.148 m/s (komut: 0.150 m/s)
  Süre: 12.3 saniye
  Yakıt Harcaması: 0.29 kg
  Uygulama Hatası: < %1.5

MANEVRA SONRASI:
  Yeni Miss Distance: 14.8 km (hedef: 15.3 km) ✅
  Yeni Pc: 1.8 × 10⁻⁸ ✅
  İkincil Çarpışma Kontrolü: Temiz ✅
  Görev Yörüngesine Dönüş: 72 saat içinde (Δv = 0.005 m/s)
  
SONUÇ: ✅ BAŞARILI
```

---

## 5.8 Performans ve Optimizasyon

### Frontend Performans Hedefleri

| Metrik | Hedef | Açıklama |
|---|---|---|
| İlk Yükleme Süresi | < 3 saniye | Tüm kaynaklar dahil |
| CesiumJS FPS | ≥ 60 FPS | 10.000+ nesne ile |
| Dashboard Güncelleme | 5 saniyede bir | WebSocket veya SSE |
| Grafik Render | < 200 ms | Plotly grafikleri |
| Alarm Gecikme | < 1 saniye | Backend → Frontend |

### Optimizasyon Teknikleri

| Alan | Teknik | Etki |
|---|---|---|
| CesiumJS | Level of Detail (LOD) | Uzak nesneleri basitleştir |
| CesiumJS | Point Primitive batching | 10× daha fazla nesne |
| CesiumJS | Entity clustering | Yakın nesneleri grupla |
| Dashboard | WebSocket real-time | Polling yerine push |
| Grafikler | Canvas renderer | SVG yerine Canvas |
| Veri | Server-side pagination | Tüm veriyi yükleme |
| Genel | CDN + Lazy loading | İlk yükleme hızı |

### Responsive Tasarım

```
    Desktop (> 1200px)          Tablet (768-1200px)       Mobil (< 768px)
    ┌──────┬──────┐             ┌──────────────┐          ┌──────────┐
    │      │      │             │    Stats     │          │  Stats   │
    │ Map  │Table │             ├──────────────┤          ├──────────┤
    │      │      │             │     Map      │          │   Map    │
    ├──────┴──────┤             ├──────────────┤          ├──────────┤
    │   Graphs    │             │    Table     │          │  Table   │
    └─────────────┘             ├──────────────┤          ├──────────┤
                                │   Graphs     │          │ Graphs   │
                                └──────────────┘          └──────────┘
```

---

## 5.9 API Backend Yapısı

### REST API Endpoints

| Method | Endpoint | Açıklama |
|---|---|---|
| GET | `/api/v1/satellites` | Tüm uyduları listele |
| GET | `/api/v1/satellites/{norad_id}` | Uydu detayı |
| GET | `/api/v1/satellites/{norad_id}/orbit` | Anlık yörünge verisi |
| GET | `/api/v1/satellites/{norad_id}/prediction` | 48h tahmin |
| GET | `/api/v1/conjunctions` | Tüm yakın geçişler |
| GET | `/api/v1/conjunctions/{id}` | Yakın geçiş detayı |
| GET | `/api/v1/conjunctions/{id}/maneuvers` | Manevra seçenekleri |
| POST | `/api/v1/conjunctions/{id}/maneuvers/{option}/approve` | Manevra onayla |
| GET | `/api/v1/alerts` | Aktif alarmlar |
| GET | `/api/v1/debris` | Enkaz listesi (pagination) |
| GET | `/api/v1/stats` | Dashboard istatistikleri |
| GET | `/api/v1/reports/daily` | Günlük rapor |
| GET | `/api/v1/model/metrics` | ML model metrikleri |

### WebSocket Channels

| Channel | Veri | Güncelleme Sırası |
|---|---|---|
| `ws://stm/positions` | Tüm nesne pozisyonları | 1 saniye |
| `ws://stm/alerts` | Yeni alarmlar | Anlık |
| `ws://stm/conjunctions` | Yakın geçiş güncellemeleri | 5 saniye |
| `ws://stm/stats` | Dashboard istatistikleri | 10 saniye |

---

## 5.10 Güvenlik ve Erişim Kontrolü

### Kimlik Doğrulama

| Yöntem | Kullanım |
|---|---|
| JWT Token | API erişimi |
| OAuth 2.0 | SSO entegrasyonu |
| API Key | Dış sistem erişimi |
| 2FA (TOTP) | Kritik işlemler (manevra onay) |

### Yetkilendirme Matrisi

| İşlem | Operatör | Analist | Yönetici | İzleyici |
|---|---|---|---|---|
| Dashboard Görüntüleme | ✅ | ✅ | ✅ | ✅ |
| Alarm Detayı | ✅ | ✅ | ✅ | ❌ |
| Manevra Planlama | ✅ | ✅ | ❌ | ❌ |
| Manevra Onaylama | ✅ | ❌ | ❌ | ❌ |
| Sistem Ayarları | ✅ | ❌ | ✅ | ❌ |
| Rapor İndirme | ✅ | ✅ | ✅ | ❌ |

---

## 5.11 Karanlık Mod Renk Paleti

### Tasarım Dili

| Element | Renk | Hex |
|---|---|---|
| Arka Plan (Ana) | Çok Koyu Lacivert | `#0a0e1a` |
| Arka Plan (Panel) | Koyu Lacivert | `#111827` |
| Arka Plan (Kart) | Koyu Gri-Mavi | `#1f2937` |
| Kenarlık | Grimsi Mavi | `#374151` |
| Metin (Birincil) | Beyaz | `#f9fafb` |
| Metin (İkincil) | Gri | `#9ca3af` |
| Vurgu (Primary) | Cyan | `#06b6d4` |
| Başarı (Güvenli) | Yeşil | `#10b981` |
| Uyarı (Dikkat) | Sarı | `#f59e0b` |
| Tehlike (Yüksek) | Turuncu | `#f97316` |
| Kritik (Alarm) | Kırmızı | `#ef4444` |
| Uydu Yörüngesi | Neon Cyan | `#00ffff` |
| Enkaz | Turuncu-Kırmızı | `#ff6b35` |

### Tipografi

| Kullanım | Font | Boyut | Ağırlık |
|---|---|---|---|
| Başlık (H1) | Inter | 28px | 700 (Bold) |
| Alt Başlık (H2) | Inter | 22px | 600 (SemiBold) |
| Panel Başlığı | Inter | 16px | 600 |
| Gövde Metin | Inter | 14px | 400 (Regular) |
| Sayısal Veri | JetBrains Mono | 20px | 600 |
| Küçük Veri | JetBrains Mono | 12px | 400 |
| Etiket | Inter | 12px | 500 |

---

## 5.12 Checkpoint Özet Tablosu

| Checkpoint | Görev | Durum | Başarı Kriteri |
|---|---|---|---|
| 5.1 | CesiumJS 3D Entegrasyonu | ⬜ | 10.000+ nesne, 60 FPS |
| 5.2 | Dashboard Layout | ⬜ | Tüm paneller çalışır |
| 5.3 | Zaman Serisi Grafikleri | ⬜ | Gerçek zamanlı güncelleme |
| 5.4 | Alarm Arayüzü | ⬜ | Gecikme < 1 saniye |
| 5.5 | Bildirim Sistemi | ⬜ | E-posta + SMS + Webhook |
| 5.6 | Manevra Onay Arayüzü | ⬜ | 2FA ile güvenli onay |
| 5.7 | Raporlama (PDF) | ⬜ | Otomatik günlük rapor |
| 5.8 | API Backend | ⬜ | REST + WebSocket |
| 5.9 | Responsive Tasarım | ⬜ | Desktop + Tablet + Mobil |
| 5.10 | Güvenlik (Auth) | ⬜ | JWT + 2FA + RBAC |

---

> **Önceki Modül:** [Modül 4 — Çarpışma Analizi](./MODUL_4_CARPISMA_ANALIZI.md)  
> **Ana Plan:** [Proje Planı](./YORUNGE_TEMIZLIGI_PROJE_PLANI.md)
