import json
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sgp4.api import Satrec, WGS72, jday

# Senin yapıştırdığın JSON verisi (örnek olarak bir kısmını buraya aldım)
# Not: Manuel kopyaladığın veriyi dosyaya koyarsan daha iyi olur.
# Ben doğrudan dosyadan okuyacak şekilde yapıyorum.

def json_to_csv():
    json_path = "data/tle_cache/imece_gecmis_tle.json"
    output_path = "data/processed/IMECE_Train_Data.csv"
    
    if not os.path.exists(json_path):
        print(f"❌ {json_path} bulunamadı! Lütfen oraya yapıştır.")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    rows = []
    print(f"Processing {len(data)} TLE records...")

    for entry in data:
        l1 = entry.get("TLE_LINE1")
        l2 = entry.get("TLE_LINE2")
        epoch_str = entry.get("EPOCH")
        
        if not (l1 and l2): continue
        
        try:
            sat = Satrec.twoline2rv(l1, l2, WGS72)
            dt_epoch = datetime.fromisoformat(epoch_str.replace('Z', ''))
            
            # Her TLE'den 5 dk arayla 1 saatlik veri
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

    df = pd.DataFrame(rows)
    df = df.sort_values("time").drop_duplicates(subset=["time"])
    df.to_csv(output_path, index=False)
    print(f"✅ Eğitim verisi hazır: {output_path} ({len(df)} satır)")

if __name__ == "__main__":
    json_to_csv()
