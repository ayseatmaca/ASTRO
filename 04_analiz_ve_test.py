import torch
import torch.nn as nn
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

# 1. GÜNCEL Model Mimarisi (3 Katman, 128 Hidden)
class OrbitPredictor(nn.Module):
    def __init__(self, input_size=3, hidden_size=128, num_layers=3):
        super(OrbitPredictor, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, bidirectional=True, dropout=0.2)
        self.fc = nn.Linear(hidden_size * 2, input_size)
        
    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])
        return out

def test_ai_accuracy():
    # 2. Veri ve Araçları Yükle
    model_path = "models/imece_prediction_model.pth"
    scaler_path = "models/orbit_scaler.pkl"
    data_path = "data/processed/IMECE_Train_Data.csv"
    
    scaler = joblib.load(scaler_path)
    df = pd.read_csv(data_path)
    
    # Son 200 veriyi test için ayıralım (AI görmediği kısımlar)
    data = df[['px', 'py', 'pz']].values
    scaled_data = scaler.transform(data)
    
    # Modeli Yükle
    model = OrbitPredictor()
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu'), weights_only=True))
    model.eval()
    
    # Tahmin pencere uzunluğu (Seq Length = 24 yapmıştık)
    SEQ_LENGTH = 24
    
    predictions = []
    actuals = []
    
    with torch.no_grad():
        # Sadece son 50 nokta üzerinde test yapalım
        for i in range(len(scaled_data) - SEQ_LENGTH - 50, len(scaled_data) - SEQ_LENGTH):
            seq = torch.FloatTensor(scaled_data[i:i+SEQ_LENGTH]).unsqueeze(0)
            pred = model(seq)
            predictions.append(pred.numpy().flatten())
            actuals.append(scaled_data[i+SEQ_LENGTH])
            
    # Normalize edilmiş veriyi geri çevir
    predictions_rescaled = scaler.inverse_transform(predictions)
    actuals_rescaled = scaler.inverse_transform(actuals)
    
    # 3. Görselleştirme
    print(f"📊 Sonuçlar karşılaştırılıyor...")
    plt.figure(figsize=(14, 7))
    
    # X Koordinatı Karşılaştırması
    plt.subplot(1, 2, 1)
    plt.plot(actuals_rescaled[:, 0], label='GERÇEK (SGP4)', color='#1f77b4', linewidth=2)
    plt.plot(predictions_rescaled[:, 0], '--', label='AI TAHMİNİ', color='#ff7f0e', linewidth=2)
    plt.title("X Pozisyonu Karşılaştırması (KM)")
    plt.xlabel("Zaman Adımı")
    plt.ylabel("Pozisyon (KM)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Hata Grafiği (L2 Norm Distance)
    errors = np.linalg.norm(actuals_rescaled - predictions_rescaled, axis=1)
    plt.subplot(1, 2, 2)
    plt.fill_between(range(len(errors)), errors, color='red', alpha=0.2)
    plt.plot(errors, color='red', label='Sapma (KM)')
    plt.title("Pozisyonel Sapma (Kilometre)")
    plt.xlabel("Zaman Adımı")
    plt.ylabel("KM Cinsinden Hata")
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig("data/processed/final_ai_performance.png")
    
    print("-" * 30)
    print(f"✅ ORTALAMA HATA: {np.mean(errors):.4f} KM")
    print(f"📂 Sonuç Grafiği: data/processed/final_ai_performance.png")
    print("-" * 30)

if __name__ == "__main__":
    test_ai_accuracy()
