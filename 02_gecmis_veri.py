"""
Yörünge Temizliği — Geçmiş TLE Verileri (v3 - Tarayıcı Simülasyonu)
==================================================================
İMECE (NORAD: 58901) için son 6 aylık veriyi çeker.
Gerçek tarayıcı başlıkları kullanarak oturum sorununu çözer.
"""

import os
import json
import requests
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
from sgp4.api import Satrec, WGS72
from sgp4.api import jday

load_dotenv()

IMECE_NORAD = 58901

def spacetrack_browser_sim(norad_id, ay_sayisi=6):
    email = os.getenv("SPACETRACK_EMAIL")
    password = os.getenv("SPACETRACK_PASSWORD")
    
    if not (email and password):
        print("❌ .env dosyasında bilgiler eksik!")
        return []

    base_url = "https://www.space-track.org"
    login_url = f"{base_url}/ajaxauth/login"
    
    # Tarayıcı başlıkları (Gerçek bir Chrome gibi davranalım)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://www.space-track.org',
        'Referer': 'https://www.space-track.org/auth/login'
    }

    url = (
        f"{base_url}/basicspacedata/query/class/gp_history/"
        f"NORAD_CAT_ID/{norad_id}/"
        f"CREATION_DATE/%3Enow-{ay_sayisi * 30}/"
        f"orderby/EPOCH%20asc/format/json"
    )

    session = requests.Session()
    session.headers.update(headers)

    print(f"🔑 Giriş denemesi: {email}")
    
    try:
        # 1. Giriş Yap
        login_data = {
            'identity': email,
            'password': password
        }
        r_login = session.post(login_url, data=login_data)
        
        if r_login.status_code == 200:
            print("✅ Oturum başarıyla açıldı, veriler isteniyor...")
            
            # 2. Veriyi İste
            r_query = session.get(url)
            
            if r_query.status_code == 200:
                data = r_query.json()
                print(f"📦 Veri Alındı: {len(data)} adet TLE kaydı bulundu.")
                return data
            else:
                print(f"❌ Veri çekme hatası: {r_query.status_code}")
                print(f"Hata detayı: {r_query.text[:200]}")
        else:
            print(f"❌ Giriş hatası: {r_login.status_code}")
            
    except Exception as e:
        print(f"❌ Kritik Hata: {e}")
        
    return []

# --- SGP4 ve Veri Hazırlama ---

def tile_to_positions(data_list):
    rows = []
    print(f"🚀 {len(data_list)} TLE verisinden eğitim seti oluşturuluyor...")
    
    for entry in data_list:
        l1 = entry.get("TLE_LINE1")
        l2 = entry.get("TLE_LINE2")
        epoch_str = entry.get("EPOCH")
        
        if not (l1 and l2): continue
        
        try:
            sat = Satrec.twoline2rv(l1, l2, WGS72)
            dt_epoch = datetime.fromisoformat(epoch_str.replace('Z', ''))
            
            # Her TLE kaydı başına 12 nokta üret (5 dk arayla 1 saat)
            for m in range(0, 60, 5):
                t = dt_epoch + timedelta(minutes=m)
                jd, fr = jday(t.year, t.month, t.day, t.hour, t.minute, t.second)
                e, p, v = sat.sgp4(jd, fr)
                
                if e == 0:
                    rows.append({
                        "id": entry.get("NORAD_CAT_ID"),
                        "time": t,
                        "px": p[0], "py": p[1], "pz": p[2],
                        "vx": v[0], "vy": v[1], "vz": v[2],
                        "h": np.sqrt(p[0]**2 + p[1]**2 + p[2]**2) - 6371.0
                    })
        except: continue
        
    return pd.DataFrame(rows)

def main():
    data = spacetrack_browser_sim(IMECE_NORAD, ay_sayisi=6)
    if not data:
        print("😢 Veri alınamadığı için işlem iptal edildi.")
        return
        
    df = tile_to_positions(data)
    if df.empty:
        print("❌ Veri işlenemedi.")
        return
        
    df = df.sort_values("time").drop_duplicates(subset=["time"])
    f_path = "data/processed/IMECE_Train_Data.csv"
    df.to_csv(f_path, index=False)
    
    print("\n" + "="*30)
    print(f"🔥 EĞİTİM VERİSİ HAZIR!")
    print(f"📁 Konum: {f_path}")
    print(f"📈 Satır Sayısı: {len(df)}")
    print(f"📅 Zaman Aralığı: {df['time'].min()} -- {df['time'].max()}")
    print("="*30)

if __name__ == "__main__":
    main()
