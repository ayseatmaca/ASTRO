import torch
import torch.nn as nn
import pandas as pd
import numpy as np
import joblib

class OrbitPredictor(nn.Module):
    def __init__(self, input_size=3, hidden_size=128, num_layers=3):
        super(OrbitPredictor, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, bidirectional=True, dropout=0.2)
        self.fc = nn.Linear(hidden_size * 2, input_size)
    def forward(self, x):
        o, _ = self.lstm(x)
        return self.fc(o[:, -1, :])

def main():
    m = OrbitPredictor()
    m.load_state_dict(torch.load('models/imece_prediction_model.pth', weights_only=True))
    m.eval()
    s = joblib.load('models/orbit_scaler.pkl')
    df = pd.read_csv('data/processed/IMECE_Train_Data.csv')
    d = s.transform(df[['px', 'py', 'pz']].values)
    SEQ = 24
    preds, acts = [], []
    with torch.no_grad():
        for i in range(len(d) - SEQ - 100, len(d) - SEQ):
            seq = torch.FloatTensor(d[i:i+SEQ]).unsqueeze(0)
            preds.append(m(seq).numpy().flatten())
            acts.append(d[i+SEQ])
    p_r = s.inverse_transform(preds)
    a_r = s.inverse_transform(acts)
    err = np.linalg.norm(a_r - p_r, axis=1)
    print("\n" + "="*40)
    print(f"🚀 AI YÖRÜNGE TAHMİNİ SONUCU 🚀")
    print(f"📍 Ortalama Hata: {np.mean(err):.4f} KM")
    print(f"📉 En Küçük Hata: {np.min(err):.4f} KM")
    print(f"📈 En Büyük Hata: {np.max(err):.4f} KM")
    print("="*40 + "\n")

if __name__ == "__main__":
    main()
