import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

def indir():
    email = "muhammetatmaca79@gmail.com"
    passw = "muhammet1234.AAA"
    
    # 1. Oturum Başlat
    session = requests.Session()
    login_url = "https://www.space-track.org/ajaxauth/login"
    
    print(f"🚀 Space-Track'e giriş yapılıyor: {email}")
    
    # Giriş yap
    payload = {'identity': email, 'password': passw}
    r = session.post(login_url, data=payload)
    
    if r.status_code == 200 and "Login Failed" not in r.text:
        print("✅ Giriş başarılı!")
        
        # Test için 58901 (Enkaz) - Kullanıcı tarayıcıda açabildiğini onayladı
        query_url = "https://www.space-track.org/basicspacedata/query/class/gp_history/NORAD_CAT_ID/58901/CREATION_DATE/%3Enow-180/orderby/EPOCH%20asc/format/json"
        
        print("📡 Veri indiriliyor (bu işlem 10-20 saniye sürebilir)...")
        resp = session.get(query_url)
        
        if resp.status_code == 200:
            data = resp.json()
            if len(data) > 0:
                output_path = "data/tle_cache/imece_gecmis_tle.json"
                os.makedirs("data/tle_cache", exist_ok=True)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                
                print(f"🎉 BAŞARILI! {len(data)} adet TLE kaydı indirildi.")
                print(f"📍 Konum: {output_path}")
            else:
                print("⚠️ Giriş yapıldı ama hiç veri dönmedi. NORAD ID doğru mu?")
        else:
            print(f"❌ Sorgu hatası: {resp.status_code}")
            print("Hata içeriği:", resp.text[:200])
    else:
        print("❌ Giriş başarısız! E-posta veya şifre hatalı olabilir.")

if __name__ == "__main__":
    indir()
