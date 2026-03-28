import json
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sgp4.api import Satrec, WGS72, jday
import random

def create_xgboost_data():
    json_path = "data/tle_cache/imece_gecmis_tle.json"
    output_path = "data/processed/XGBoost_Train_Data.csv"
    
    if not os.path.exists(json_path):
        print(f"❌ {json_path} bulunamadı!")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    rows = []
    print(f"📦 Processing {len(data)} TLE records for XGBoost pipeline...")

    # Simüle edilmiş bir enkazın başlangıç sapmaları (km ve km/s cinsinden)
    debris_offset_pos = np.array([50.0, 50.0, 50.0])
    debris_offset_vel = np.array([-0.01, 0.02, -0.01])

    np.random.seed(42) # Tekrarlanabilirlik için

    for entry in data:
        l1 = entry.get("TLE_LINE1")
        l2 = entry.get("TLE_LINE2")
        epoch_str = entry.get("EPOCH")
        
        if not (l1 and l2): continue
        
        try:
            sat = Satrec.twoline2rv(l1, l2, WGS72)
            dt_epoch = datetime.fromisoformat(epoch_str.replace('Z', ''))
            
            # Feature: B-STAR (Sürtünme Katsayısı) ve Eğiklik (Inclination)
            bstar = sat.bstar
            inclination_deg = np.degrees(sat.inclo)

            # Her TLE noktasından 1 saatlik veri, 1 dakikalık adımlarla
            for m in range(0, 60, 1):
                t = dt_epoch + timedelta(minutes=m)
                jd, fr = jday(t.year, t.month, t.day, t.hour, t.minute, t.second)
                e, p, v = sat.sgp4(jd, fr)
                
                if e == 0:
                    p_arr = np.array(p)
                    v_arr = np.array(v)
                    
                    # Dinamik hareket eden bir enkaz simülasyonu
                    # Ara sıra "Yüksek Risk" sınıfı oluşturmak için rastgele yaklaşmalar (%5 ihtimal)
                    is_risk_event = np.random.random() < 0.05
                    
                    if is_risk_event:
                        # 1.5 km içinde yakın geçiş simüle et
                        current_debris_p = p_arr + np.random.uniform(-1.5, 1.5, 3) 
                        current_debris_v = v_arr + np.random.uniform(-0.05, 0.05, 3) 
                    else:
                        # Normal zamanlarda uzak mesafede uçuş
                        time_factor = m * 60 # saniye
                        current_debris_p = p_arr + debris_offset_pos + (debris_offset_vel * time_factor) + np.random.normal(0, 5, 3)
                        current_debris_v = v_arr + debris_offset_vel + np.random.normal(0, 0.01, 3)
                        
                        # Eğer enkaz çok uzaklaştıysa geri merkeze doğru çek (veriyi dengeli tutmak için)
                        if np.linalg.norm(current_debris_p - p_arr) > 200:
                            debris_offset_pos = np.random.uniform(-50, 50, 3)
                    
                    # Feature 3: Bağıl Mesafe (Relative Distance)
                    rel_distance = np.linalg.norm(current_debris_p - p_arr)
                    
                    # Feature 4: Bağıl Hız (Relative Velocity)
                    rel_velocity = np.linalg.norm(current_debris_v - v_arr)
                    
                    # Hedef (Target): Mesafe < 2km ise Risk=1
                    risk_label = 1 if rel_distance < 2.0 else 0

                    rows.append({
                        "time": t,
                        "bstar": bstar,
                        "inclination": inclination_deg,
                        "rel_distance": rel_distance,
                        "rel_velocity": rel_velocity,
                        "Risk": risk_label,
                        "sat_px": p[0], "sat_py": p[1], "sat_pz": p[2],
                        "sat_vx": v[0], "sat_vy": v[1], "sat_vz": v[2],
                        "deb_px": current_debris_p[0], "deb_py": current_debris_p[1], "deb_pz": current_debris_p[2],
                        "deb_vx": current_debris_v[0], "deb_vy": current_debris_v[1], "deb_vz": current_debris_v[2]
                    })
        except Exception: 
            continue

    df = pd.DataFrame(rows)
    df = df.sort_values("time").drop_duplicates(subset=["time"])
    
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(output_path, index=False)
    
    # Bilgi ve Doğrulama Yazıları
    print(f"✅ XGBoost Eğitim verisi oluşturuldu: {output_path} ({len(df)} satır)")
    print("-" * 40)
    print("📊 Veri Seti Özeti:")
    print(df[['bstar', 'inclination', 'rel_distance', 'rel_velocity']].describe())
    print("-" * 40)
    print(f"⚠️ Toplam Risk=1 Durumu (Mesafe < 2km): {df['Risk'].sum()} / {len(df)}")

if __name__ == "__main__":
    create_xgboost_data()
