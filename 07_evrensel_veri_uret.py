import pandas as pd
import numpy as np
from skyfield.api import load, Topos
from datetime import datetime
import os

def evrensel_veri_zengini():
    input_path = "data/processed/IMECE_Train_Data.csv"
    output_path = "data/processed/MULTI_BODY_Train_Data.csv"
    
    if not os.path.exists(input_path):
        print("❌ Kaynak veri bulunamadı!")
        return

    df = pd.read_csv(input_path)
    df['time'] = pd.to_datetime(df['time'])
    
    # Skyfield Efemeris (Gezegen Konumları) Yükle
    planets = load('de421.bsp') # NASA Efemeris Dosyası
    earth = planets['earth']
    moon = planets['moon']
    sun = planets['sun']
    ts = load.timescale()

    print("🌌 Güneş ve Ay konumları yörünge verisine ekleniyor...")
    
    moon_x, moon_y, moon_z = [], [], []
    sun_x, sun_y, sun_z = [], [], []

    # Her zaman adımı için Güneş ve Ay'ın uydumuza göre (ECI) konumunu hesapla
    for idx, row in df.iterrows():
        t = ts.from_datetime(row['time'])
        
        # Ay Konumu (Dünya-merkezli ECI)
        m_pos = earth.at(t).observe(moon).position.km
        moon_x.append(m_pos[0]); moon_y.append(m_pos[1]); moon_z.append(m_pos[2])
        
        # Güneş Konumu (Dünya-merkezli ECI)
        s_pos = earth.at(t).observe(sun).position.km
        sun_x.append(s_pos[0]); sun_y.append(s_pos[1]); sun_z.append(s_pos[2])

    df['moon_x'], df['moon_y'], df['moon_z'] = moon_x, moon_y, moon_z
    df['sun_x'], df['sun_y'], df['sun_z'] = sun_x, sun_y, sun_z
    
    df.to_csv(output_path, index=False)
    print(f"✅ Multi-Body veri seti hazır: {output_path}")

if __name__ == "__main__":
    evrensel_veri_zengini()
