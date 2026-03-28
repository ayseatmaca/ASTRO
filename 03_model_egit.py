import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import os
import joblib

# CPU mu GPU mu?
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"🚀 Eğitim {device} üzerinde yapılacak.")

# 1. Veri Hazırlama
def veri_yukle():
    df = pd.read_csv("data/processed/IMECE_Train_Data.csv")
    # Sadece pozisyon (x,y,z) verilerini kullanalım
    data = df[['px', 'py', 'pz']].values
    
    # Normalizasyon
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)
    
    # Model ve Scaler'ı sonra kullanmak için kaydedelim
    os.makedirs("models", exist_ok=True)
    joblib.dump(scaler, "models/orbit_scaler.pkl")
    
    return scaled_data, scaler

def create_sequences(data, seq_length=24):
    """24 nokta (2 saat) bakıp bir sonraki noktayı tahmin etmek için veri seti üretir."""
    xs, ys = [], []
    for i in range(len(data) - seq_length):
        x = data[i:(i + seq_length)]
        y = data[i + seq_length]
        xs.append(x)
        ys.append(y)
    return np.array(xs), np.array(ys)

# 2. LSTM Model Mimarisi
class OrbitPredictor(nn.Module):
    def __init__(self, input_size=3, hidden_size=128, num_layers=3):
        super(OrbitPredictor, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, bidirectional=True, dropout=0.2)
        self.fc = nn.Linear(hidden_size * 2, input_size) 
        
    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :]) 
        return out

# 3. Eğitim Döngüsü
def eğit():
    data, scaler = veri_yukle()
    X, y = create_sequences(data, seq_length=24)
    
    # Torch formatına çevir
    X_train = torch.FloatTensor(X).to(device)
    y_train = torch.FloatTensor(y).to(device)
    
    model = OrbitPredictor().to(device)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.0005)
    
    print("🧠 Model (Gelişmiş) yeniden eğitiliyor...")
    epochs = 200
    losses = []
    
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        
        output = model(X_train)
        loss = criterion(output, y_train)
        
        loss.backward()
        optimizer.step()
        
        losses.append(loss.item())
        if (epoch+1) % 10 == 0:
            print(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.6f}")
    
    # Modeli kaydet
    torch.save(model.state_dict(), "models/imece_prediction_model.pth")
    print("✅ Model kaydedildi: models/imece_prediction_model.pth")
    
    # Kayıp Grafiği
    plt.plot(losses)
    plt.title("Eğitim Kaybı (Loss)")
    plt.savefig("data/processed/training_loss.png")
    print("📊 Kayıp grafiği oluşturuldu: data/processed/training_loss.png")

if __name__ == "__main__":
    eğit()
