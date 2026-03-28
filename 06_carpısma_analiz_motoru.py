import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist

def calculate_tca(sat_coords, debris_coords, times):
    """
    Time of Closest Approach (TCA) ve Minimum Mesafe hesaplar.
    sat_coords: (N, 3) - Uydu pozisyonları (km)
    debris_coords: (N, 3) - Enkaz pozisyonları (km)
    times: (N,) - Zaman damgaları
    """
    # Her zaman adımı için aradaki mesafeyi hesapla
    distances = np.linalg.norm(sat_coords - debris_coords, axis=1)
    
    # En yakın yaklaşma
    min_dist = np.min(distances)
    idx = np.argmin(distances)
    tca_time = times[idx]
    
    return min_dist, tca_time

def check_collision_risk(min_dist, threshold=2.0):
    """Mesafe 2 km'den az ise yüksek risk uyarısı verir."""
    if min_dist < threshold:
        return "⚠️ YÜKSEK RİSK: ÇARPISMA OLABİLİR!"
    elif min_dist < threshold * 5:
        return "🟡 ORTA RİSK: YAKIN GEÇİŞ."
    else:
        return "🟢 DÜŞÜK RİSK: GÜVENLİ MESAFA."

# SİMÜLASYON TESTİ (Model eğitilirken mantığı doğrulayalım)
if __name__ == "__main__":
    print("🛰️ Çarpışma Analiz Motoru Başlatılıyor...")
    
    # Örnek veri (AI modelimizden gelecek gibi simüle ediyoruz)
    num_points = 50
    times = pd.date_range("2026-03-28 14:00", periods=num_points, freq="1min")
    
    # Uydu Rotası (Dairesel yörünge simülasyonu)
    theta = np.linspace(0, 0.1, num_points)
    sat_pos = 7000 * np.array([np.cos(theta), np.sin(theta), np.zeros(num_points)]).T
    
    # Enkaz Rotası (Uydumuza yaklaşan bir enkaz simülasyonu)
    debris_pos = sat_pos + np.array([1.5, 0.8, 0.5]) # 2 km yakınından geçen bir rota
    
    min_d, tca = calculate_tca(sat_pos, debris_pos, times)
    risk = check_collision_risk(min_d)
    
    print("-" * 30)
    print(f"⏰ En Yakın Geçiş Zamanı (TCA): {tca}")
    print(f"📏 Minimum Mesafe: {min_d:.4f} KM")
    print(f"🛡️ Risk Durumu: {risk}")
    print("-" * 30)
