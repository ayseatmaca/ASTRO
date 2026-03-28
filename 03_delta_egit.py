import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib
import os

# CPU/GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def veri_yukle_delta():
    df = pd.read_csv("data/processed/IMECE_Train_Data.csv")
    
    # 🌟 ÇOK ÖNEMLİ: Ham koordinat yerine Koordinat FARKLARINI (Delta) alıyoruz
    # Bu AI'nın binlerce KM yerine metreler bazındaki hareketleri öğrenmesini sağlar
    df[['dx', 'dy', 'dz']] = df[['px', 'py', 'pz']].diff()
    df = df.dropna() # İlk satırda fark yoktur
    
    # Girdi: [px, py, pz, vx, vy, vz], Çıktı: [dx, dy, dz]
    # Yani AI; "Bu konumda ve bu hızdayım, birazdan ne kadar yer değiştireceğim?" sorusuna yanıt verecek.
    train_cols = ['px', 'py', 'pz', 'vx', 'vy', 'vz']
    target_cols = ['dx', 'dy', 'dz']
    
    scaler_x = StandardScaler()
    scaler_y = StandardScaler()
    
    X_scaled = scaler_x.fit_transform(df[train_cols].values)
    Y_scaled = scaler_y.fit_transform(df[target_cols].values)
    
    os.makedirs("models", exist_ok=True)
    joblib.dump(scaler_x, "models/scaler_x.pkl")
    joblib.dump(scaler_y, "models/scaler_y.pkl")
    
    return X_scaled, Y_scaled

class CollisionOrbitNet(nn.Module):
    def __init__(self, input_size=6, hidden_size=256, num_layers=3):
        super(CollisionOrbitNet, self).__init__()
        # Çarpışma riski için daha fazla hücre (256)
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, dropout=0.3)
        self.fc = nn.Sequential(
            nn.Linear(hidden_size, 128),
            nn.ReLU(),
            nn.Linear(128, 3) # dx, dy, dz tahmini
        )
        
    def forward(self, x):
        out, _ = self.lstm(x)
        return self.fc(out[:, -1, :])

def eğit():
    X, Y = veri_yukle_delta()
    
    # Sequence Length: 24 (2 saatlik tarihçe)
    seq_len = 24
    xs, ys = [], []
    for i in range(len(X) - seq_len):
        xs.append(X[i:i+seq_len])
        ys.append(Y[i+seq_len])
    
    X_torch = torch.FloatTensor(np.array(xs)).to(device)
    Y_torch = torch.FloatTensor(np.array(ys)).to(device)
    
    model = CollisionOrbitNet().to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.0001, weight_decay=1e-5)
    criterion = nn.HuberLoss() # Outlier (anormal hareket) korumalı kayıp fonksiyonu
    
    print("🎯 Çarpışma Analizi için geliştirilmiş Delta Modeli eğitiliyor...")
    epochs = 150
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        output = model(X_torch)
        loss = criterion(output, Y_torch)
        loss.backward()
        optimizer.step()
        
        if (epoch+1) % 10 == 0:
            print(f"📡 Epoch {epoch+1}/{epochs} | Sapma Payı: {loss.item():.8f}")
            
    torch.save(model.state_dict(), "models/collision_orbit_net.pth")
    print("✅ Çarpışma uyarı sistemi modeli kaydedildi: models/collision_orbit_net.pth")

if __name__ == "__main__":
    eğit()
