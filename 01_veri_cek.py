"""
Yörünge Temizliği — Modül 1: Veri Edinme
==========================================
Hedef Uydu: İMECE (NORAD: 58901)
- İMECE TLE verisi çekme
- SGP4 ile 24 saatlik yörünge hesaplama
- İMECE yörüngesine yakın enkaz tespiti

Çalıştırma: python 01_veri_cek.py
"""

import os
import json
import httpx
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
from sgp4.api import Satrec, WGS72
from sgp4.api import jday

load_dotenv()

# ============================================
# İMECE BİLGİLERİ
# ============================================
IMECE = {
    "ad": "İMECE",
    "norad_id": 58901,
    "tip": "LEO",
    "yukseklik_km": 680,        # Nominal yükseklik
    "inklinasyon_deg": 98.0,    # Güneş-senkron yörünge
}


# ============================================
# TLE ÇEKİCİ
# ============================================
def celestrak_tle_cek(norad_id: int) -> dict | None:
    """CelesTrak'tan TLE çeker (hesapsız)."""
    url = f"https://celestrak.org/NORAD/elements/gp.php?CATNR={norad_id}&FORMAT=TLE"
    try:
        resp = httpx.get(url, timeout=15)
        resp.raise_for_status()
        lines = resp.text.strip().split('\n')
        if len(lines) >= 2:
            name = lines[0].strip() if len(lines) >= 3 else f"NORAD {norad_id}"
            l1 = lines[-2].strip() if len(lines) >= 3 else lines[0].strip()
            l2 = lines[-1].strip()
            return {"name": name, "tle_line1": l1, "tle_line2": l2}
        return None
    except Exception as e:
        print(f"  ❌ CelesTrak hatası: {e}")
        return None


def spacetrack_tle_cek(norad_id: int) -> dict | None:
    """Space-Track API'den TLE çeker."""
    email = os.getenv("SPACETRACK_EMAIL")
    password = os.getenv("SPACETRACK_PASSWORD")
    if not email or not password:
        return None

    base = "https://www.space-track.org"
    try:
        with httpx.Client(timeout=30) as client:
            client.post(f"{base}/ajaxauth/login", data={"identity": email, "password": password})
            resp = client.get(f"{base}/basicspacedata/query/class/tle_latest/NORAD_CAT_ID/{norad_id}/ORDINAL/1/format/tle")
            lines = resp.text.strip().split('\n')
            if len(lines) >= 2:
                return {"name": f"NORAD {norad_id}", "tle_line1": lines[0].strip(), "tle_line2": lines[1].strip()}
    except Exception as e:
        print(f"  ❌ Space-Track hatası: {e}")
    return None


# ============================================
# SGP4 PROPAGASYON
# ============================================
def tle_to_yorunge(tle: dict, dakika_aralik: int = 1, sure_saat: int = 24) -> pd.DataFrame:
    """TLE → 24 saatlik konum/hız zaman serisi."""
    sat = Satrec.twoline2rv(tle["tle_line1"], tle["tle_line2"], WGS72)
    now = datetime.utcnow()
    records = []

    for i in range((sure_saat * 60) // dakika_aralik):
        t = now + timedelta(minutes=i * dakika_aralik)
        jd, fr = jday(t.year, t.month, t.day, t.hour, t.minute, t.second)
        error, pos, vel = sat.sgp4(jd, fr)

        if error != 0:
            continue

        x, y, z = pos
        vx, vy, vz = vel
        r = np.sqrt(x**2 + y**2 + z**2)

        records.append({
            "zaman_utc": t.strftime("%Y-%m-%d %H:%M:%S"),
            "x_km": round(x, 3),
            "y_km": round(y, 3),
            "z_km": round(z, 3),
            "vx_km_s": round(vx, 6),
            "vy_km_s": round(vy, 6),
            "vz_km_s": round(vz, 6),
            "r_km": round(r, 3),
            "yukseklik_km": round(r - 6371.0, 3),
            "hiz_km_s": round(np.sqrt(vx**2 + vy**2 + vz**2), 6),
        })

    return pd.DataFrame(records)


# ============================================
# İMECE YAKININDAKI ENKAZ VERİSİ
# ============================================
def enkaz_verisi_cek() -> pd.DataFrame:
    """
    CelesTrak'tan İMECE'nin yörüngesine yakın enkaz/çöpleri çeker.
    LEO bölgesindeki aktif enkaz grupları:
    - Cosmos 2251 enkazları
    - Fengyun-1C enkazları  
    - Starlink/OneWeb parçaları
    - Genel uzay enkazı
    """
    enkaz_gruplari = {
        "cosmos-2251-debris":  "https://celestrak.org/NORAD/elements/gp.php?GROUP=cosmos-2251-debris&FORMAT=tle",
        "fengyun-1c-debris":   "https://celestrak.org/NORAD/elements/gp.php?GROUP=1999-025&FORMAT=tle",
        "iridium-33-debris":   "https://celestrak.org/NORAD/elements/gp.php?GROUP=iridium-33-debris&FORMAT=tle",
        "active-debris":       "https://celestrak.org/NORAD/elements/gp.php?GROUP=2019-006&FORMAT=tle",
    }

    tum_enkaz = []

    for grup_adi, url in enkaz_gruplari.items():
        print(f"  🗑️  {grup_adi} çekiliyor...")
        try:
            resp = httpx.get(url, timeout=30)
            resp.raise_for_status()
            lines = resp.text.strip().split('\n')

            # 3 satırlık TLE formatı (isim + line1 + line2)
            i = 0
            sayac = 0
            while i < len(lines) - 1:
                # Satır 1 ile başlayan bul
                if lines[i].strip().startswith('1 ') and i + 1 < len(lines) and lines[i+1].strip().startswith('2 '):
                    l1 = lines[i].strip()
                    l2 = lines[i+1].strip()
                    norad = int(l1[2:7].strip())

                    # SGP4 ile inklinasyon ve yükseklik kontrol
                    try:
                        sat = Satrec.twoline2rv(l1, l2, WGS72)
                        jd, fr = jday(2026, 3, 28, 12, 0, 0)
                        err, pos, vel = sat.sgp4(jd, fr)
                        if err == 0:
                            r = np.sqrt(pos[0]**2 + pos[1]**2 + pos[2]**2)
                            yukseklik = r - 6371.0

                            # İMECE bandına yakın mı? (±200 km)
                            if abs(yukseklik - IMECE["yukseklik_km"]) < 200:
                                tum_enkaz.append({
                                    "norad_id": norad,
                                    "grup": grup_adi,
                                    "tle_line1": l1,
                                    "tle_line2": l2,
                                    "yukseklik_km": round(yukseklik, 1),
                                    "x_km": round(pos[0], 3),
                                    "y_km": round(pos[1], 3),
                                    "z_km": round(pos[2], 3),
                                })
                                sayac += 1
                    except:
                        pass

                    i += 2
                else:
                    i += 1

            print(f"     ✅ İMECE bandında {sayac} enkaz bulundu")

        except Exception as e:
            print(f"     ❌ Hata: {e}")

    return pd.DataFrame(tum_enkaz)


# ============================================
# ANA FONKSİYON
# ============================================
def main():
    print("=" * 60)
    print("🛰️  YÖRÜNGE TEMİZLİĞİ — İMECE UYDU TAKİP SİSTEMİ")
    print("=" * 60)
    print(f"  Hedef:     {IMECE['ad']}")
    print(f"  NORAD ID:  {IMECE['norad_id']}")
    print(f"  Yörünge:   {IMECE['tip']} (~{IMECE['yukseklik_km']} km)")
    print()

    os.makedirs("data/tle_cache", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    # --- ADIM 1: İMECE TLE ---
    print("📡 ADIM 1: İMECE TLE Verisi")
    print("-" * 40)

    tle = spacetrack_tle_cek(IMECE["norad_id"])
    if not tle:
        print("  Space-Track'tan alınamadı, CelesTrak deneniyor...")
        tle = celestrak_tle_cek(IMECE["norad_id"])

    if not tle:
        print("  ❌ İMECE TLE verisi alınamadı! Çıkılıyor.")
        return

    print(f"  ✅ TLE alındı: {tle['name']}")
    print(f"     Line 1: {tle['tle_line1']}")
    print(f"     Line 2: {tle['tle_line2']}")

    with open("data/tle_cache/imece_tle.json", "w", encoding="utf-8") as f:
        json.dump(tle, f, ensure_ascii=False, indent=2)

    # --- ADIM 2: SGP4 ile 24 Saatlik Yörünge ---
    print(f"\n📐 ADIM 2: SGP4 Propagasyon (24 saat, 1 dk aralık)")
    print("-" * 40)

    df_imece = tle_to_yorunge(tle, dakika_aralik=1, sure_saat=24)
    df_imece.to_csv("data/processed/IMECE_orbit_24h.csv", index=False)

    print(f"  ✅ {len(df_imece)} veri noktası hesaplandı")
    print(f"  📊 Yükseklik:  {df_imece['yukseklik_km'].min():.1f} — {df_imece['yukseklik_km'].max():.1f} km")
    print(f"  📊 Ortalama:   {df_imece['yukseklik_km'].mean():.1f} km")
    print(f"  📊 Hız:        {df_imece['hiz_km_s'].mean():.3f} km/s")
    print(f"  📊 Periyot:    ~{(2*np.pi*df_imece['r_km'].mean()) / (df_imece['hiz_km_s'].mean()*60):.1f} dakika")

    # --- ADIM 3: İMECE Yörüngesindeki Enkazlar ---
    print(f"\n🗑️  ADIM 3: İMECE Bandındaki Uzay Enkazı ({IMECE['yukseklik_km']}±200 km)")
    print("-" * 40)

    df_enkaz = enkaz_verisi_cek()

    if not df_enkaz.empty:
        df_enkaz.to_csv("data/processed/IMECE_yakin_enkaz.csv", index=False)
        print(f"\n  📊 TOPLAM: {len(df_enkaz)} enkaz parçası İMECE bandında")
        print(f"  📊 Grup dağılımı:")
        for grup, count in df_enkaz['grup'].value_counts().items():
            print(f"     • {grup}: {count} parça")
        print(f"  💾 Kaydedildi: data/processed/IMECE_yakin_enkaz.csv")
    else:
        print("  ⚠️  İMECE bandında enkaz bulunamadı")

    # --- ÖZET ---
    print("\n" + "=" * 60)
    print("📋 ÖZET")
    print("=" * 60)
    print(f"  🛰️  İMECE yörünge verisi: {len(df_imece)} nokta (24 saat)")
    print(f"  🗑️  Yakın enkaz sayısı:    {len(df_enkaz)}")
    print(f"  💾  Dosyalar:")
    print(f"      • data/processed/IMECE_orbit_24h.csv")
    print(f"      • data/processed/IMECE_yakin_enkaz.csv")
    print(f"\n✅ Veri edinme tamamlandı!")
    print(f"   Sonraki adım: python 02_analiz.py")


if __name__ == "__main__":
    main()
