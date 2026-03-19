"""Add sections 17-24 to gen_deep_learning.py (code1/code2/code3 required format)."""
import os

BASE = r"c:\Users\seany\Documents\All Codes\Data Science Study Path"
FILE = os.path.join(BASE, "gen_deep_learning.py")

def ct(code, indent="            "):
    lines = code.split('\n')
    parts = []
    for line in lines:
        escaped = line.replace('\\', '\\\\').replace('"', '\\"')
        parts.append(f'{indent}"{escaped}\\n"')
    return "(\n" + "\n".join(parts) + "\n        )"

def ec(s):
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace("'", "\\'")

def make_section(num, title, desc, c1t, c1, c2t, c2, c3t, c3,
                 rw_scenario="", rw_code="", pt="", pd_text="", ps=""):
    s  = f'    {{\n'
    s += f'        "title": "{num}. {title}",\n'
    s += f'        "desc": "{ec(desc)}",\n'
    s += f'        "code1_title": "{c1t}",\n'
    s += f'        "code1": {ct(c1)},\n'
    s += f'        "code2_title": "{c2t}",\n'
    s += f'        "code2": {ct(c2)},\n'
    s += f'        "code3_title": "{c3t}",\n'
    s += f'        "code3": {ct(c3)},\n'
    s += f'        "rw_scenario": "{ec(rw_scenario)}",\n'
    s += f'        "rw_code": {ct(rw_code)},\n'
    s += f'        "practice": {{\n'
    s += f'            "title": "{ec(pt)}",\n'
    s += f'            "desc": "{ec(pd_text)}",\n'
    s += f'            "starter": {ct(ps)},\n'
    s += f'        }},\n'
    s += f'    }},\n'
    return s

def insert_before_make_html(filepath, new_sections_str):
    content = open(filepath, encoding='utf-8').read()
    marker = '\n]\n\n\ndef make_html'
    idx = content.rfind(marker)
    if idx == -1:
        print(f"ERROR: marker not found in {filepath}")
        return False
    before = content[:idx].rstrip()
    if before.endswith('}') and not before.endswith('},'):
        content = before + ',\n\n' + new_sections_str + content[idx:]
    else:
        content = content[:idx] + '\n' + new_sections_str + content[idx:]
    open(filepath, 'w', encoding='utf-8').write(content)
    print(f"OK: inserted sections into {filepath}")
    return True

# ── Section 17: LSTM & GRU ────────────────────────────────────────────────────
s17 = make_section(17, "LSTM & GRU for Sequence Modeling",
    "LSTMs and GRUs solve the vanishing gradient problem for long sequences using gating mechanisms. LSTMs have separate cell/hidden states; GRUs merge them into a single hidden state for fewer parameters.",
    c1t="LSTM Time Series Forecasting",
    c1="""
import torch
import torch.nn as nn
import numpy as np

torch.manual_seed(42); np.random.seed(42)

t = np.linspace(0, 8*np.pi, 500)
signal = np.sin(t) + 0.1*np.random.randn(len(t))

def make_sequences(data, seq_len=20):
    X, y = [], []
    for i in range(len(data) - seq_len):
        X.append(data[i:i+seq_len])
        y.append(data[i+seq_len])
    return np.array(X, dtype=np.float32), np.array(y, dtype=np.float32)

X, y = make_sequences(signal)
split = int(len(X)*0.8)
X_tr = torch.tensor(X[:split]).unsqueeze(-1)
X_te = torch.tensor(X[split:]).unsqueeze(-1)
y_tr = torch.tensor(y[:split]).unsqueeze(-1)
y_te = torch.tensor(y[split:]).unsqueeze(-1)

class LSTMForecaster(nn.Module):
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(1, 32, 2, batch_first=True, dropout=0.2)
        self.fc = nn.Linear(32, 1)
    def forward(self, x):
        out, _ = self.lstm(x)
        return self.fc(out[:, -1, :])

model = LSTMForecaster()
opt = torch.optim.Adam(model.parameters(), lr=1e-3)
crit = nn.MSELoss()
for epoch in range(50):
    model.train()
    loss = crit(model(X_tr), y_tr)
    opt.zero_grad(); loss.backward(); opt.step()
    if (epoch+1) % 10 == 0:
        model.eval()
        with torch.no_grad():
            vl = crit(model(X_te), y_te).item()
        print(f"Epoch {epoch+1}: train={loss.item():.4f}, val={vl:.4f}")
""".strip(),
    c2t="GRU Sentiment Classifier",
    c2="""
import torch
import torch.nn as nn

torch.manual_seed(42)
VOCAB = list("abcdefghijklmnopqrstuvwxyz ")
char2idx = {c: i+1 for i, c in enumerate(VOCAB)}
MAX = 40

def encode(text):
    enc = [char2idx.get(c, 0) for c in text.lower()[:MAX]]
    return enc + [0]*(MAX-len(enc))

texts = ["great product love it", "terrible quality broke",
         "amazing fast shipping", "waste of money poor",
         "highly recommend excellent", "disappointed does not work"]
labels = [1, 0, 1, 0, 1, 0]

X = torch.tensor([encode(t) for t in texts], dtype=torch.long)
y = torch.tensor(labels, dtype=torch.float)

class GRUClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.embed = nn.Embedding(len(VOCAB)+2, 16, padding_idx=0)
        self.gru = nn.GRU(16, 32, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(64, 1)
    def forward(self, x):
        x = self.embed(x)
        _, h = self.gru(x)
        h = torch.cat([h[-2], h[-1]], dim=-1)
        return torch.sigmoid(self.fc(h)).squeeze()

model = GRUClassifier()
opt = torch.optim.Adam(model.parameters(), lr=1e-3)
crit = nn.BCELoss()
for _ in range(100):
    loss = crit(model(X), y)
    opt.zero_grad(); loss.backward(); opt.step()

model.eval()
with torch.no_grad():
    preds = (model(X) > 0.5).int().tolist()
acc = sum(p==l for p,l in zip(preds, labels))/len(labels)
print(f"GRU Accuracy: {acc:.2f}")
for t, p, l in zip(texts, preds, labels):
    print(f"  [{'OK' if p==l else 'X'}] {t}: pred={p}")
""".strip(),
    c3t="LSTM vs GRU Performance Comparison",
    c3="""
import torch
import torch.nn as nn
import time
import numpy as np

torch.manual_seed(42)

# Compare LSTM vs GRU on same task
X = torch.randn(64, 50, 10)  # batch=64, seq=50, features=10
y = torch.randint(0, 2, (64,)).float()

class RNNModel(nn.Module):
    def __init__(self, cell='lstm', hidden=64):
        super().__init__()
        if cell == 'lstm':
            self.rnn = nn.LSTM(10, hidden, 2, batch_first=True)
        else:
            self.rnn = nn.GRU(10, hidden, 2, batch_first=True)
        self.fc = nn.Linear(hidden, 1)
    def forward(self, x):
        out, _ = self.rnn(x)
        return torch.sigmoid(self.fc(out[:, -1])).squeeze()

results = {}
for cell in ['lstm', 'gru']:
    model = RNNModel(cell=cell)
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    crit = nn.BCELoss()
    n_params = sum(p.numel() for p in model.parameters())
    start = time.time()
    for _ in range(100):
        loss = crit(model(X), y)
        opt.zero_grad(); loss.backward(); opt.step()
    elapsed = time.time() - start
    acc = ((model(X) > 0.5).float() == y).float().mean().item()
    results[cell] = {'params': n_params, 'time': elapsed, 'acc': acc, 'loss': loss.item()}

print("LSTM vs GRU Comparison:")
for cell, r in results.items():
    print(f"  {cell.upper()}: params={r['params']:,}, time={r['time']:.2f}s, "
          f"acc={r['acc']:.4f}, loss={r['loss']:.4f}")
print("\\nConclusion: GRU has fewer params and is faster; LSTM often better for long deps")
""".strip(),
    rw_scenario="Build a stock price direction predictor using LSTM. Use 60-day windows of normalized closing prices to predict next-day direction (up/down). Report validation accuracy and compare with a GRU baseline.",
    rw_code="""
import torch, torch.nn as nn, numpy as np

torch.manual_seed(42); np.random.seed(42)
n = 500
prices = np.cumsum(np.random.randn(n)*0.5) + 100
prices = (prices - prices.mean()) / prices.std()

def make_data(prices, seq=60):
    X, y = [], []
    for i in range(len(prices)-seq-1):
        X.append(prices[i:i+seq])
        y.append(1 if prices[i+seq] > prices[i+seq-1] else 0)
    return (torch.tensor(np.array(X), dtype=torch.float32).unsqueeze(-1),
            torch.tensor(y, dtype=torch.float32))

X, y = make_data(prices)
sp = int(len(X)*0.8)
X_tr, X_te, y_tr, y_te = X[:sp], X[sp:], y[:sp], y[sp:]

for cell, RNN in [('LSTM', nn.LSTM), ('GRU', nn.GRU)]:
    class Model(nn.Module):
        def __init__(self):
            super().__init__()
            self.rnn = RNN(1, 64, 2, batch_first=True, dropout=0.2)
            self.fc = nn.Sequential(nn.Linear(64, 16), nn.ReLU(), nn.Linear(16, 1))
        def forward(self, x):
            out, _ = self.rnn(x)
            return torch.sigmoid(self.fc(out[:, -1])).squeeze()
    model = Model()
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    crit = nn.BCELoss()
    for epoch in range(60):
        model.train()
        loss = crit(model(X_tr), y_tr)
        opt.zero_grad(); loss.backward(); opt.step()
    model.eval()
    with torch.no_grad():
        acc = ((model(X_te)>0.5).float()==y_te).float().mean().item()
    print(f"{cell}: val_acc={acc:.4f}")
""".strip(),
    pt="Sequence Direction Predictor",
    pd_text="Build a GRU model with 30-day windows for direction prediction. Compare bidirectional vs unidirectional GRU and report validation accuracy.",
    ps="""
import torch, torch.nn as nn, numpy as np
torch.manual_seed(42); np.random.seed(42)
# 1. Generate 400-day synthetic price series (random walk)
# 2. Create 30-day windows with direction labels (up=1, down=0)
# 3. Build bidirectional GRU classifier
# 4. Build standard GRU classifier
# 5. Train both 50 epochs, compare val_acc
""".strip()
)

# ── Section 18: Transfer Learning ─────────────────────────────────────────────
s18 = make_section(18, "Transfer Learning & Fine-tuning",
    "Transfer learning reuses pretrained model weights, dramatically reducing training time and data requirements. Strategies include feature extraction (frozen backbone), gradual unfreezing, and layer-wise learning rates.",
    c1t="Feature Extraction with Frozen Backbone",
    c1="""
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader

torch.manual_seed(42)

class PretrainedBackbone(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Linear(128, 64), nn.ReLU(),
            nn.Linear(64, 32), nn.ReLU(),
        )
        for p in self.parameters():
            p.requires_grad = False  # Freeze
    def forward(self, x): return self.features(x)

class TransferModel(nn.Module):
    def __init__(self, n_classes=4):
        super().__init__()
        self.backbone = PretrainedBackbone()
        self.head = nn.Sequential(
            nn.Linear(32, 16), nn.ReLU(), nn.Dropout(0.3),
            nn.Linear(16, n_classes)
        )
    def forward(self, x): return self.head(self.backbone(x))

model = TransferModel()
trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
total = sum(p.numel() for p in model.parameters())
print(f"Trainable: {trainable}/{total} ({trainable/total*100:.1f}%)")

X = torch.randn(200, 128); y = torch.randint(0, 4, (200,))
loader = DataLoader(TensorDataset(X, y), batch_size=32, shuffle=True)
opt = torch.optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=1e-3)
crit = nn.CrossEntropyLoss()

for epoch in range(15):
    for xb, yb in loader:
        loss = crit(model(xb), yb)
        opt.zero_grad(); loss.backward(); opt.step()
    if (epoch+1) % 5 == 0:
        model.eval()
        with torch.no_grad():
            acc = (model(X).argmax(1)==y).float().mean().item()
        model.train()
        print(f"Epoch {epoch+1}: loss={loss.item():.4f}, acc={acc:.4f}")
""".strip(),
    c2t="Gradual Unfreezing with Layer-wise LRs",
    c2="""
import torch
import torch.nn as nn

torch.manual_seed(42)

class PretrainedModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Linear(64, 32)
        self.layer2 = nn.Linear(32, 16)
        self.head = nn.Linear(16, 3)
        self.relu = nn.ReLU()
        for layer in [self.layer1, self.layer2]:
            for p in layer.parameters():
                p.requires_grad = False

    def forward(self, x):
        return self.head(self.relu(self.layer2(self.relu(self.layer1(x)))))

X = torch.randn(200, 64); y = torch.randint(0, 3, (200,))
crit = nn.CrossEntropyLoss()
model = PretrainedModel()

# Phase 1: head only
opt = torch.optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=1e-3)
for _ in range(20):
    loss = crit(model(X), y); opt.zero_grad(); loss.backward(); opt.step()
print(f"Phase 1 (head only): {loss.item():.4f}")

# Phase 2: unfreeze layer2 with smaller LR
for p in model.layer2.parameters(): p.requires_grad = True
opt = torch.optim.Adam([
    {"params": model.layer2.parameters(), "lr": 1e-4},
    {"params": model.head.parameters(), "lr": 1e-3},
])
for _ in range(20):
    loss = crit(model(X), y); opt.zero_grad(); loss.backward(); opt.step()
print(f"Phase 2 (+layer2): {loss.item():.4f}")

# Phase 3: unfreeze all
for p in model.layer1.parameters(): p.requires_grad = True
opt = torch.optim.Adam([
    {"params": model.layer1.parameters(), "lr": 1e-5},
    {"params": model.layer2.parameters(), "lr": 1e-4},
    {"params": model.head.parameters(), "lr": 1e-3},
])
for _ in range(30):
    loss = crit(model(X), y); opt.zero_grad(); loss.backward(); opt.step()
acc = (model(X).argmax(1)==y).float().mean().item()
print(f"Phase 3 (all): loss={loss.item():.4f}, acc={acc:.4f}")
""".strip(),
    c3t="Transfer Learning Diagnostics",
    c3="""
import torch, torch.nn as nn, numpy as np

torch.manual_seed(42)

class Encoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(50, 32)
        self.fc2 = nn.Linear(32, 16)
        self.relu = nn.ReLU()
    def forward(self, x): return self.relu(self.fc2(self.relu(self.fc1(x))))

class TargetModel(nn.Module):
    def __init__(self, freeze=True):
        super().__init__()
        self.encoder = Encoder()
        self.head = nn.Linear(16, 2)
        if freeze:
            for p in self.encoder.parameters(): p.requires_grad = False
    def forward(self, x): return self.head(self.encoder(x))

X_src = torch.randn(500, 50); y_src = torch.randint(0, 2, (500,))
X_tgt = torch.randn(50, 50); y_tgt = torch.randint(0, 2, (50,))  # small target

crit = nn.CrossEntropyLoss()
for mode in ["frozen", "full_finetune"]:
    model = TargetModel(freeze=(mode=="frozen"))
    opt = torch.optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=1e-3)
    for _ in range(50):
        loss = crit(model(X_tgt), y_tgt); opt.zero_grad(); loss.backward(); opt.step()
    model.eval()
    with torch.no_grad():
        src_acc = (model(X_src).argmax(1)==y_src).float().mean().item()
        tgt_acc = (model(X_tgt).argmax(1)==y_tgt).float().mean().item()
    print(f"{mode:>16}: target_acc={tgt_acc:.4f}, source_acc={src_acc:.4f}")

print("\\nTip: Frozen backbone works best with limited target data (< 500 samples)")
print("Tip: Full fine-tuning risks catastrophic forgetting on small datasets")
""".strip(),
    rw_scenario="You have a pretrained feature extractor trained on 1M samples. Your new task has only 300 labeled examples. Use transfer learning with frozen backbone first, then gradually unfreeze layers.",
    rw_code="""
import torch, torch.nn as nn, numpy as np

torch.manual_seed(42); np.random.seed(42)

class Encoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(100, 64), nn.ReLU(), nn.Linear(64, 32), nn.ReLU())
    def forward(self, x): return self.layers(x)

class MedModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = Encoder()
        self.head = nn.Sequential(nn.Linear(32, 8), nn.ReLU(), nn.Linear(8, 1))
        for p in self.encoder.parameters(): p.requires_grad = False
    def forward(self, x): return torch.sigmoid(self.head(self.encoder(x))).squeeze()

X = torch.randn(300, 100); y = torch.randint(0, 2, (300,)).float()
Xv = torch.randn(100, 100); yv = torch.randint(0, 2, (100,)).float()
crit = nn.BCELoss()

model = MedModel()
for phase, lr_enc, lr_head, unfreeze in [
    ("Phase 1: head only", None, 1e-3, False),
    ("Phase 2: full tune", 1e-5, 1e-4, True),
]:
    if unfreeze:
        for p in model.encoder.parameters(): p.requires_grad = True
        opt = torch.optim.Adam([
            {"params": model.encoder.parameters(), "lr": lr_enc},
            {"params": model.head.parameters(), "lr": lr_head},
        ])
    else:
        opt = torch.optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=lr_head)
    for _ in range(40):
        loss = crit(model(X), y); opt.zero_grad(); loss.backward(); opt.step()
    model.eval()
    with torch.no_grad():
        va = ((model(Xv)>0.5).float()==yv).float().mean().item()
    model.train()
    print(f"{phase}: val_acc={va:.4f}")
""".strip(),
    pt="Two-Phase Transfer Learning",
    pd_text="Implement transfer learning on a pretrained encoder: Phase 1 trains only the new head, Phase 2 unfreezes all layers with layer-wise LRs (1e-5 for encoder, 1e-3 for head).",
    ps="""
import torch, torch.nn as nn
torch.manual_seed(42)
# 1. Build PretrainedEncoder (freeze all layers)
# 2. Add new classification head
# 3. Phase 1: train head only for 20 epochs
# 4. Phase 2: unfreeze encoder, use lr=1e-5 for encoder, lr=1e-3 for head
# 5. Report val_acc after each phase
X = torch.randn(100, 32); y = torch.randint(0, 3, (100,))
""".strip()
)

# ── Section 19: Attention Mechanisms ─────────────────────────────────────────
s19 = make_section(19, "Attention Mechanisms",
    "Attention allows models to focus on relevant parts of input. Scaled dot-product attention computes query-key similarity, softmax-normalizes scores, then aggregates values. Multi-head attention runs this in parallel across multiple representation subspaces.",
    c1t="Scaled Dot-Product Attention",
    c1="""
import torch
import torch.nn as nn

torch.manual_seed(42)

def sdp_attention(Q, K, V, mask=None):
    d_k = Q.size(-1)
    scores = torch.matmul(Q, K.transpose(-2, -1)) / (d_k**0.5)
    if mask is not None:
        scores = scores.masked_fill(mask==0, float('-inf'))
    weights = torch.softmax(scores, dim=-1)
    return torch.matmul(weights, V), weights

class MultiHeadAttention(nn.Module):
    def __init__(self, d_model=64, n_heads=4):
        super().__init__()
        self.d_k = d_model // n_heads
        self.n_heads = n_heads
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)

    def split(self, x):
        B, T, D = x.size()
        return x.view(B, T, self.n_heads, self.d_k).transpose(1, 2)

    def forward(self, Q, K, V):
        B = Q.size(0)
        Q, K, V = self.split(self.W_q(Q)), self.split(self.W_k(K)), self.split(self.W_v(V))
        out, attn = sdp_attention(Q, K, V)
        out = out.transpose(1,2).contiguous().view(B, -1, self.n_heads*self.d_k)
        return self.W_o(out), attn

B, T, D = 2, 10, 64
x = torch.randn(B, T, D)
mha = MultiHeadAttention(d_model=64, n_heads=4)
out, attn = mha(x, x, x)
print(f"Input: {x.shape} -> Output: {out.shape}")
print(f"Attention weights: {attn.shape}")
print(f"Attention sums to 1: {attn[0,0,0].sum().item():.4f}")
""".strip(),
    c2t="Transformer Encoder Block",
    c2="""
import torch, torch.nn as nn, math

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=1000):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        pos = torch.arange(0, max_len).unsqueeze(1).float()
        div = torch.exp(torch.arange(0, d_model, 2).float()*(-math.log(10000.0)/d_model))
        pe[:, 0::2] = torch.sin(pos*div)
        pe[:, 1::2] = torch.cos(pos*div)
        self.register_buffer('pe', pe.unsqueeze(0))
    def forward(self, x): return x + self.pe[:, :x.size(1)]

class TransformerBlock(nn.Module):
    def __init__(self, d=64, n_heads=4, ff=256, drop=0.1):
        super().__init__()
        self.attn = nn.MultiheadAttention(d, n_heads, dropout=drop, batch_first=True)
        self.ff = nn.Sequential(nn.Linear(d, ff), nn.GELU(), nn.Dropout(drop), nn.Linear(ff, d))
        self.n1, self.n2 = nn.LayerNorm(d), nn.LayerNorm(d)
        self.drop = nn.Dropout(drop)
    def forward(self, x):
        a, _ = self.attn(x, x, x)
        x = self.n1(x + self.drop(a))
        return self.n2(x + self.drop(self.ff(x)))

class TransformerClassifier(nn.Module):
    def __init__(self, vocab=100, d=64, n_heads=4, n_layers=2, n_classes=3):
        super().__init__()
        self.embed = nn.Embedding(vocab, d, padding_idx=0)
        self.pos = PositionalEncoding(d)
        self.layers = nn.Sequential(*[TransformerBlock(d, n_heads) for _ in range(n_layers)])
        self.head = nn.Linear(d, n_classes)
    def forward(self, x): return self.head(self.layers(self.pos(self.embed(x))).mean(1))

torch.manual_seed(42)
model = TransformerClassifier()
x = torch.randint(1, 100, (4, 20)); y = torch.randint(0, 3, (4,))
opt = torch.optim.Adam(model.parameters(), lr=1e-3)
for i in range(30):
    loss = nn.CrossEntropyLoss()(model(x), y)
    opt.zero_grad(); loss.backward(); opt.step()
print(f"Transformer: {sum(p.numel() for p in model.parameters()):,} params")
print(f"After 30 steps: loss={loss.item():.4f}, preds={model(x).argmax(1).tolist()}")
""".strip(),
    c3t="Attention Visualization",
    c3="""
import torch, torch.nn as nn, numpy as np

torch.manual_seed(42)

def sdp_attention(Q, K, V):
    d_k = Q.size(-1)
    scores = torch.matmul(Q, K.transpose(-2,-1)) / (d_k**0.5)
    weights = torch.softmax(scores, dim=-1)
    return torch.matmul(weights, V), weights

# Simple sequence: "the cat sat on the mat"
tokens = ["the", "cat", "sat", "on", "the", "mat"]
d_model = 8
x = torch.randn(1, len(tokens), d_model)

# Single-head attention
W_q = nn.Linear(d_model, d_model, bias=False)
W_k = nn.Linear(d_model, d_model, bias=False)
W_v = nn.Linear(d_model, d_model, bias=False)

Q, K, V = W_q(x), W_k(x), W_v(x)
out, attn = sdp_attention(Q, K, V)
attn_matrix = attn[0].detach().numpy()

print("Attention weights matrix (rows=query, cols=key):")
print("Tokens:", tokens)
header = "      " + "".join(f"{t:>6}" for t in tokens)
print(header)
for i, row in enumerate(attn_matrix):
    row_str = f"{tokens[i]:>6}" + "".join(f"{v:>6.3f}" for v in row)
    print(row_str)

# Check: each row sums to 1
print(f"\\nRow sums: {attn_matrix.sum(axis=1).round(4)}")
print(f"Diagonal (self-attention strength): {attn_matrix.diagonal().round(4)}")
""".strip(),
    rw_scenario="Build a 2-layer Transformer encoder for document classification with 4 categories. Visualize attention weights to explain which words drive predictions.",
    rw_code="""
import torch, torch.nn as nn, numpy as np, math

torch.manual_seed(42)

class TFEncoder(nn.Module):
    def __init__(self, vocab=50, d=32, heads=4, layers=2, classes=4):
        super().__init__()
        self.embed = nn.Embedding(vocab, d, padding_idx=0)
        self.enc = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d, heads, dim_feedforward=64, dropout=0.1, batch_first=True),
            num_layers=layers)
        self.head = nn.Linear(d, classes)
    def forward(self, x): return self.head(self.enc(self.embed(x)).mean(1))

X = torch.randint(1, 50, (64, 20))
y = torch.randint(0, 4, (64,))
model = TFEncoder()
opt = torch.optim.Adam(model.parameters(), lr=1e-3)
crit = nn.CrossEntropyLoss()
for epoch in range(50):
    loss = crit(model(X), y); opt.zero_grad(); loss.backward(); opt.step()
    if (epoch+1) % 10 == 0:
        acc = (model(X).argmax(1)==y).float().mean().item()
        print(f"Epoch {epoch+1}: loss={loss.item():.4f}, acc={acc:.4f}")
""".strip(),
    pt="Self-Attention from Scratch",
    pd_text="Implement scaled dot-product attention and test with batch_size=4, seq_len=8, d_model=16. Verify attention weights sum to 1 along the last dimension.",
    ps="""
import torch, torch.nn as nn

def sdp_attention(Q, K, V, mask=None):
    # 1. Compute attention scores: Q @ K.T / sqrt(d_k)
    # 2. Apply mask if provided
    # 3. Softmax over last dimension
    # 4. Return weighted sum of V, and the attention weights
    pass

B, T, D = 4, 8, 16
x = torch.randn(B, T, D)
out, weights = sdp_attention(x, x, x)
# Assert: weights.sum(dim=-1).allclose(torch.ones(B, T))
""".strip()
)

# ── Section 20: Batch Normalization & Regularization ─────────────────────────
s20 = make_section(20, "Batch Normalization & Regularization",
    "BatchNorm stabilizes training by normalizing layer inputs per batch. Dropout randomly zeroes activations during training. Weight decay (L2) penalizes large weights. LayerNorm is preferred in Transformers.",
    c1t="BatchNorm, Dropout & Weight Decay Comparison",
    c1="""
import torch, torch.nn as nn, numpy as np

torch.manual_seed(42); np.random.seed(42)

class PlainNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(40, 128), nn.ReLU(),
                                  nn.Linear(128, 64), nn.ReLU(), nn.Linear(64, 1))
    def forward(self, x): return self.net(x).squeeze()

class RegNet(nn.Module):
    def __init__(self, dropout=0.3):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(40, 128), nn.BatchNorm1d(128), nn.ReLU(), nn.Dropout(dropout),
            nn.Linear(128, 64), nn.BatchNorm1d(64), nn.ReLU(), nn.Dropout(dropout),
            nn.Linear(64, 1))
    def forward(self, x): return self.net(x).squeeze()

X_tr = torch.randn(100, 40); y_tr = (X_tr[:, 0] > 0).float()
X_va = torch.randn(500, 40); y_va = (X_va[:, 0] > 0).float()
crit = nn.BCEWithLogitsLoss()

def train(model, n=100, wd=0.0):
    opt = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=wd)
    for _ in range(n):
        model.train()
        loss = crit(model(X_tr), y_tr); opt.zero_grad(); loss.backward(); opt.step()
    model.eval()
    with torch.no_grad():
        tr_acc = ((model(X_tr)>0).float()==y_tr).float().mean().item()
        va_acc = ((model(X_va)>0).float()==y_va).float().mean().item()
    return tr_acc, va_acc

for name, model, wd in [
    ("No regularization", PlainNet(), 0),
    ("BN + Dropout(0.3)", RegNet(0.3), 0),
    ("BN + Drop + L2", RegNet(0.3), 1e-4),
]:
    tr, va = train(model, n=100, wd=wd)
    print(f"{name:<22}: train={tr:.4f}, val={va:.4f}, overfit={tr-va:.4f}")
""".strip(),
    c2t="LayerNorm vs BatchNorm",
    c2="""
import torch, torch.nn as nn

torch.manual_seed(42)
B, T, D = 4, 10, 32
x = torch.randn(B, T, D)

# BatchNorm (normalizes over N,L per channel D)
bn = nn.BatchNorm1d(D)
x2d = x.view(-1, D)
out_bn = bn(x2d).view(B, T, D)

# LayerNorm (normalizes over D per token position)
ln = nn.LayerNorm(D)
out_ln = ln(x)

print(f"Input:     mean={x.mean():.4f}, std={x.std():.4f}")
print(f"BatchNorm: mean={out_bn.mean():.6f}, std={out_bn.std():.4f}")
print(f"LayerNorm: mean={out_ln.mean():.6f}, std={out_ln.std():.4f}")

# Verify LayerNorm normalizes per token
for pos in [0, 3, 7]:
    m = out_ln[0, pos].mean().item()
    s = out_ln[0, pos].std().item()
    print(f"  LayerNorm pos {pos}: mean={m:.6f}, std={s:.4f}")

guide = {
    "BatchNorm":  "CNNs, fixed-length, large batches (N >= 16)",
    "LayerNorm":  "Transformers, NLP, variable-length sequences",
    "GroupNorm":  "Small batches (N < 8), object detection",
    "InstanceNorm": "Style transfer, per-sample normalization",
}
print("\\nNormalization Guide:")
for k, v in guide.items():
    print(f"  {k:<14}: {v}")
""".strip(),
    c3t="Dropout Modes & Inference",
    c3="""
import torch, torch.nn as nn, numpy as np

torch.manual_seed(42)

# Critical: model.eval() disables dropout and uses running BN stats
class NetWithDropout(nn.Module):
    def __init__(self, dropout=0.5):
        super().__init__()
        self.fc1 = nn.Linear(20, 64)
        self.bn = nn.BatchNorm1d(64)
        self.drop = nn.Dropout(dropout)
        self.fc2 = nn.Linear(64, 1)
    def forward(self, x):
        return self.fc2(self.drop(torch.relu(self.bn(self.fc1(x))))).squeeze()

model = NetWithDropout(dropout=0.5)
x = torch.randn(10, 20)

# Demonstrate train vs eval mode difference
model.train()
out_train1 = model(x).detach()
out_train2 = model(x).detach()

model.eval()
out_eval1 = model(x).detach()
out_eval2 = model(x).detach()

print("Train mode outputs (different each call due to dropout):")
print(f"  Call 1: {out_train1[:5].numpy().round(3)}")
print(f"  Call 2: {out_train2[:5].numpy().round(3)}")
print(f"  Same:   {torch.allclose(out_train1, out_train2)}")

print("\\nEval mode outputs (deterministic):")
print(f"  Call 1: {out_eval1[:5].numpy().round(3)}")
print(f"  Call 2: {out_eval2[:5].numpy().round(3)}")
print(f"  Same:   {torch.allclose(out_eval1, out_eval2)}")

print("\\nKey rule: ALWAYS call model.eval() before inference!")
""".strip(),
    rw_scenario="Your deep network training diverges at epoch 3 due to exploding activations. Add BatchNorm after every hidden layer, Dropout (p=0.4), and L2 regularization (1e-4) to stabilize training.",
    rw_code="""
import torch, torch.nn as nn, numpy as np

torch.manual_seed(42); np.random.seed(42)

class UnstableNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(50, 256), nn.ReLU(), nn.Linear(256, 128), nn.ReLU(), nn.Linear(128, 1))
    def forward(self, x): return self.net(x).squeeze()

class StableNet(nn.Module):
    def __init__(self, dropout=0.4):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(50, 256), nn.BatchNorm1d(256), nn.ReLU(), nn.Dropout(dropout),
            nn.Linear(256, 128), nn.BatchNorm1d(128), nn.ReLU(), nn.Dropout(dropout),
            nn.Linear(128, 1))
    def forward(self, x): return self.net(x).squeeze()

X = torch.randn(200, 50)*5; y = (X[:,0] > 0).float()
crit = nn.BCEWithLogitsLoss()

for name, model, wd in [("Unstable", UnstableNet(), 0), ("Stable", StableNet(0.4), 1e-4)]:
    opt = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=wd)
    losses = []
    for epoch in range(50):
        model.train()
        pred = model(X)
        loss = crit(pred, y)
        if torch.isnan(loss): losses.append(float('nan')); break
        opt.zero_grad(); loss.backward(); opt.step()
        losses.append(round(loss.item(), 4))
    valid = [l for l in losses if l==l]
    print(f"{name}: final={valid[-1]:.4f}, epochs={len(valid)}, diverged={len(valid)<50}")
""".strip(),
    pt="Regularized Classifier",
    pd_text="Build a 3-layer MLP with BatchNorm + Dropout (p=0.3) for binary classification. Compare train vs val accuracy with and without regularization.",
    ps="""
import torch, torch.nn as nn
torch.manual_seed(42)
X_tr = torch.randn(100, 20); y_tr = (X_tr[:,0]>0).float()
X_va = torch.randn(300, 20); y_va = (X_va[:,0]>0).float()
# 1. Build UnregularizedNet (3 layers, no BN/Dropout)
# 2. Build RegularizedNet (3 layers, BN + Dropout p=0.3)
# 3. Train both 100 epochs with Adam, BCEWithLogitsLoss
# 4. Print train_acc and val_acc for both
""".strip()
)

# ── Section 21: Learning Rate Scheduling ─────────────────────────────────────
s21 = make_section(21, "Learning Rate Scheduling",
    "Learning rate schedules adapt LR during training. Step decay, cosine annealing, and warmup+cosine are common strategies. ReduceLROnPlateau automatically reduces LR when validation metrics stagnate.",
    c1t="Common LR Schedulers",
    c1="""
import torch, torch.nn as nn

torch.manual_seed(42)

def run_scheduler(sched_name, n_epochs=60, base_lr=0.1):
    model = nn.Linear(10, 1)
    opt = torch.optim.SGD(model.parameters(), lr=base_lr)
    if sched_name == "StepLR":
        sched = torch.optim.lr_scheduler.StepLR(opt, step_size=15, gamma=0.5)
    elif sched_name == "CosineAnnealing":
        sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=n_epochs)
    elif sched_name == "ExponentialLR":
        sched = torch.optim.lr_scheduler.ExponentialLR(opt, gamma=0.95)
    else:
        sched = torch.optim.lr_scheduler.OneCycleLR(
            opt, max_lr=base_lr, total_steps=n_epochs)

    lrs = [opt.param_groups[0]['lr']]
    for _ in range(n_epochs):
        sched.step()
        lrs.append(opt.param_groups[0]['lr'])
    return lrs

schedules = ["StepLR", "CosineAnnealing", "ExponentialLR", "OneCycleLR"]
checkpoints = [0, 15, 30, 45, 60]

for name in schedules:
    lrs = run_scheduler(name)
    vals = [f"{lrs[i]:.5f}" for i in checkpoints]
    print(f"{name:<20}: {' -> '.join(vals)}")
""".strip(),
    c2t="Warmup + Cosine Decay",
    c2="""
import torch, torch.nn as nn, math

class WarmupCosine:
    def __init__(self, opt, warmup, total, min_lr=1e-6):
        self.opt = opt
        self.warmup = warmup
        self.total = total
        self.min_lr = min_lr
        self.base_lr = opt.param_groups[0]['lr']
        self.step_n = 0

    def step(self):
        self.step_n += 1
        if self.step_n <= self.warmup:
            lr = self.base_lr * self.step_n / self.warmup
        else:
            p = (self.step_n - self.warmup) / (self.total - self.warmup)
            lr = self.min_lr + 0.5*(self.base_lr-self.min_lr)*(1+math.cos(math.pi*p))
        for g in self.opt.param_groups: g['lr'] = lr
        return lr

torch.manual_seed(42)
model = nn.Linear(10, 1)
opt = torch.optim.AdamW(model.parameters(), lr=1e-3)
sched = WarmupCosine(opt, warmup=10, total=100)

lrs = [sched.step() for _ in range(100)]
print("Warmup + Cosine LR at key steps:")
for s in [1, 5, 10, 25, 50, 75, 100]:
    print(f"  Step {s:>3}: {lrs[s-1]:.6f}")

# Simulate training
X = torch.randn(100, 10); y = torch.randn(100, 1)
opt2 = torch.optim.AdamW(model.parameters(), lr=1e-3)
sched2 = WarmupCosine(opt2, warmup=10, total=100)
for step in range(100):
    loss = nn.MSELoss()(model(X), y)
    opt2.zero_grad(); loss.backward(); opt2.step()
    sched2.step()
    if (step+1) % 25 == 0:
        print(f"  Step {step+1}: loss={loss.item():.4f}, lr={opt2.param_groups[0]['lr']:.6f}")
""".strip(),
    c3t="ReduceLROnPlateau & LR Finder",
    c3="""
import torch, torch.nn as nn, numpy as np

torch.manual_seed(42)

# ReduceLROnPlateau: auto-reduces LR when metric stagnates
model = nn.Sequential(nn.Linear(20, 64), nn.ReLU(), nn.Linear(64, 1))
opt = torch.optim.Adam(model.parameters(), lr=1e-2)
plateau_sched = torch.optim.lr_scheduler.ReduceLROnPlateau(
    opt, mode='min', factor=0.5, patience=5, min_lr=1e-6, verbose=False)

X = torch.randn(200, 20); y = X[:, :1]
X_val = torch.randn(50, 20); y_val = X_val[:, :1]
crit = nn.MSELoss()

lr_history = []
for epoch in range(60):
    model.train()
    loss = crit(model(X), y)
    opt.zero_grad(); loss.backward(); opt.step()
    model.eval()
    with torch.no_grad():
        val_loss = crit(model(X_val), y_val).item()
    plateau_sched.step(val_loss)
    lr_history.append(opt.param_groups[0]['lr'])
    if (epoch+1) % 10 == 0:
        print(f"Epoch {epoch+1}: val_loss={val_loss:.4f}, lr={opt.param_groups[0]['lr']:.6f}")

# Simple LR range test (find optimal LR)
print("\\nLR Range Test (exponential sweep):")
model2 = nn.Linear(20, 1)
opt2 = torch.optim.SGD(model2.parameters(), lr=1e-6)
min_lr, max_lr, n_steps = 1e-6, 1e-1, 20
lr_mult = (max_lr/min_lr)**(1/n_steps)
for step in range(n_steps):
    lr = min_lr * (lr_mult**step)
    for g in opt2.param_groups: g['lr'] = lr
    loss = crit(model2(X[:32]), y[:32])
    opt2.zero_grad(); loss.backward(); opt2.step()
    if step % 5 == 0:
        print(f"  lr={lr:.2e}: loss={loss.item():.4f}")
""".strip(),
    rw_scenario="Your LM training diverges in the first 500 steps. Apply linear warmup for 500 steps, then cosine decay over 5000 total steps. Compare convergence vs a fixed LR.",
    rw_code="""
import torch, torch.nn as nn, math, numpy as np

torch.manual_seed(42)

def lr_fn(step, warmup=500, total=5000, base=1e-3, min_lr=1e-6):
    if step < warmup: return base * step / max(1, warmup)
    p = (step - warmup) / (total - warmup)
    return min_lr + 0.5*(base-min_lr)*(1+math.cos(math.pi*p))

model1 = nn.Sequential(nn.Linear(32, 64), nn.ReLU(), nn.Linear(64, 1))
model2 = nn.Sequential(nn.Linear(32, 64), nn.ReLU(), nn.Linear(64, 1))
opt1 = torch.optim.AdamW(model1.parameters(), lr=1e-3)  # fixed
opt2 = torch.optim.AdamW(model2.parameters(), lr=1e-3)  # warmup+cosine

X = torch.randn(200, 32); y = torch.randn(200, 1)
crit = nn.MSELoss()

for step in range(5001):
    for g in opt2.param_groups: g['lr'] = lr_fn(step)
    l1 = crit(model1(X), y)
    l2 = crit(model2(X), y)
    for m, l, o in [(model1, l1, opt1), (model2, l2, opt2)]:
        o.zero_grad(); l.backward(); o.step()
    if step % 1000 == 0:
        print(f"Step {step}: fixed_lr={l1.item():.4f}, warmup_cosine={l2.item():.4f}, lr={lr_fn(step):.6f}")
""".strip(),
    pt="Warmup + Cosine LR Scheduler",
    pd_text="Implement a warmup+cosine LR scheduler from scratch. Apply it to a regression model and print LR at steps [0, 50, 100, 200, 500].",
    ps="""
import torch, torch.nn as nn, math

def get_lr(step, warmup=100, total=500, base_lr=1e-3):
    # Phase 1: linear warmup
    # Phase 2: cosine decay
    pass

model = nn.Linear(10, 1)
opt = torch.optim.Adam(model.parameters(), lr=1e-3)
X = torch.randn(100, 10); y = torch.randn(100, 1)
# Apply scheduler over 500 steps, print LR at key checkpoints
""".strip()
)

# ── Section 22: Model Checkpointing & Early Stopping ─────────────────────────
s22 = make_section(22, "Model Checkpointing & Early Stopping",
    "Checkpointing saves model state during training to recover from crashes and resume. Early stopping halts training when validation loss stops improving, preventing overfitting automatically.",
    c1t="Model Checkpointing",
    c1="""
import torch, torch.nn as nn, os

torch.manual_seed(42)

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(20,64), nn.ReLU(), nn.Linear(64,1))
    def forward(self, x): return self.net(x).squeeze()

def save_ckpt(model, opt, epoch, val_loss, path):
    torch.save({'epoch': epoch, 'model': model.state_dict(),
                'optimizer': opt.state_dict(), 'val_loss': val_loss}, path)
    print(f"  Saved: epoch={epoch}, val_loss={val_loss:.4f}")

def load_ckpt(model, opt, path):
    if not os.path.exists(path): return 0, float('inf')
    ckpt = torch.load(path, weights_only=True)
    model.load_state_dict(ckpt['model'])
    opt.load_state_dict(ckpt['optimizer'])
    print(f"  Resumed from epoch {ckpt['epoch']}")
    return ckpt['epoch'], ckpt['val_loss']

model = Net()
opt = torch.optim.Adam(model.parameters(), lr=1e-3)
crit = nn.MSELoss()
X_tr = torch.randn(200,20); y_tr = X_tr[:,0]
X_va = torch.randn(50,20); y_va = X_va[:,0]
best_val, ckpt_path = float('inf'), "/tmp/best.pt"

for epoch in range(30):
    model.train()
    loss = crit(model(X_tr), y_tr); opt.zero_grad(); loss.backward(); opt.step()
    model.eval()
    with torch.no_grad():
        vl = crit(model(X_va), y_va).item()
    if vl < best_val:
        best_val = vl; save_ckpt(model, opt, epoch+1, vl, ckpt_path)

# Reload best
model2 = Net(); opt2 = torch.optim.Adam(model2.parameters())
load_ckpt(model2, opt2, ckpt_path)
model2.eval()
with torch.no_grad():
    print(f"Loaded model val_loss: {crit(model2(X_va), y_va).item():.4f}")
""".strip(),
    c2t="Early Stopping with Patience",
    c2="""
import torch, torch.nn as nn, copy

class EarlyStopping:
    def __init__(self, patience=10, min_delta=1e-4):
        self.patience = patience
        self.min_delta = min_delta
        self.best_loss = float('inf')
        self.best_weights = None
        self.counter = 0

    def __call__(self, model, val_loss):
        if val_loss < self.best_loss - self.min_delta:
            self.best_loss = val_loss
            self.best_weights = copy.deepcopy(model.state_dict())
            self.counter = 0
        else:
            self.counter += 1
        if self.counter >= self.patience:
            model.load_state_dict(self.best_weights)
            return True
        return False

torch.manual_seed(42)
model = nn.Sequential(nn.Linear(10,32), nn.ReLU(), nn.Linear(32,1))
opt = torch.optim.Adam(model.parameters(), lr=1e-2)
crit = nn.MSELoss()
es = EarlyStopping(patience=8, min_delta=1e-3)

X = torch.randn(100,10); y = X[:,0:1]
Xv = torch.randn(50,10); yv = Xv[:,0:1]

for epoch in range(200):
    model.train()
    loss = crit(model(X), y); opt.zero_grad(); loss.backward(); opt.step()
    model.eval()
    with torch.no_grad():
        vl = crit(model(Xv), yv).item()
    if (epoch+1)%20==0:
        print(f"Epoch {epoch+1}: val={vl:.4f}, patience_ctr={es.counter}")
    if es(model, vl):
        print(f"Early stop at epoch {epoch+1}, best_val={es.best_loss:.4f}")
        break
""".strip(),
    c3t="Training Manager (Checkpoint + Early Stop)",
    c3="""
import torch, torch.nn as nn, copy, os

class TrainingManager:
    def __init__(self, model, optimizer, patience=10, ckpt_every=5, save_dir="/tmp"):
        self.model = model; self.opt = optimizer
        self.patience = patience; self.ckpt_every = ckpt_every
        self.save_dir = save_dir; self.best_loss = float('inf')
        self.best_state = None; self.counter = 0; self.history = []

    def update(self, epoch, train_loss, val_loss):
        self.history.append({'epoch': epoch, 'train': train_loss, 'val': val_loss})
        if (epoch+1) % self.ckpt_every == 0:
            path = os.path.join(self.save_dir, f"ckpt_ep{epoch+1}.pt")
            torch.save({'epoch': epoch+1, 'model': self.model.state_dict(), 'val': val_loss}, path)
            print(f"  [ckpt] ep{epoch+1} saved")
        if val_loss < self.best_loss - 1e-4:
            self.best_loss = val_loss
            self.best_state = copy.deepcopy(self.model.state_dict())
            self.counter = 0
        else:
            self.counter += 1
        if self.counter >= self.patience:
            self.model.load_state_dict(self.best_state)
            print(f"  Early stop ep {epoch+1}, best={self.best_loss:.4f}")
            return True
        return False

torch.manual_seed(42)
model = nn.Sequential(nn.Linear(20,64), nn.ReLU(), nn.Linear(64,1))
opt = torch.optim.Adam(model.parameters(), lr=5e-3)
mgr = TrainingManager(model, opt, patience=10, ckpt_every=5)
X = torch.randn(200,20); y = X[:,:1]; Xv = torch.randn(50,20); yv = Xv[:,:1]
crit = nn.MSELoss()

for epoch in range(80):
    model.train()
    l = crit(model(X), y); opt.zero_grad(); l.backward(); opt.step()
    model.eval()
    with torch.no_grad():
        vl = crit(model(Xv), yv).item()
    if (epoch+1)%20==0:
        print(f"Epoch {epoch+1}: train={l.item():.4f}, val={vl:.4f}")
    if mgr.update(epoch, l.item(), vl): break
""".strip(),
    rw_scenario="Your 6-hour-per-epoch training must support crash recovery. Implement checkpointing every 5 epochs, save the best model separately, and early stop with patience=15.",
    rw_code="""
import torch, torch.nn as nn, copy, os

torch.manual_seed(42)

class TrainingSystem:
    def __init__(self, model, opt, patience=15, ckpt_every=5, save_dir="/tmp"):
        self.model = model; self.opt = opt
        self.patience = patience; self.ckpt_every = ckpt_every; self.save_dir = save_dir
        self.best_loss = float('inf'); self.best_state = None; self.counter = 0

    def step(self, epoch, train_loss, val_loss):
        if (epoch+1) % self.ckpt_every == 0:
            torch.save({'epoch': epoch+1, 'val': val_loss, 'model': self.model.state_dict()},
                       f"{self.save_dir}/ckpt_ep{epoch+1}.pt")
            print(f"  Checkpoint saved: epoch {epoch+1}")
        if val_loss < self.best_loss - 1e-4:
            self.best_loss = val_loss; self.counter = 0
            self.best_state = copy.deepcopy(self.model.state_dict())
            torch.save(self.best_state, f"{self.save_dir}/best.pt")
        else:
            self.counter += 1
        if self.counter >= self.patience:
            self.model.load_state_dict(self.best_state)
            print(f"  Early stop at {epoch+1}, best_val={self.best_loss:.4f}")
            return True
        return False

model = nn.Sequential(nn.Linear(20,64), nn.ReLU(), nn.Linear(64,1))
opt = torch.optim.Adam(model.parameters(), lr=5e-3)
sys = TrainingSystem(model, opt, patience=15, ckpt_every=5)
X = torch.randn(200,20); y = X[:,:1]; Xv = torch.randn(50,20); yv = Xv[:,:1]
crit = nn.MSELoss()
for epoch in range(100):
    model.train()
    l = crit(model(X), y); opt.zero_grad(); l.backward(); opt.step()
    model.eval()
    with torch.no_grad(): vl = crit(model(Xv), yv).item()
    if (epoch+1)%20==0: print(f"Epoch {epoch+1}: train={l.item():.4f}, val={vl:.4f}")
    if sys.step(epoch, l.item(), vl): break
""".strip(),
    pt="Early Stopping Implementation",
    pd_text="Write an EarlyStopping class with patience=10 and min_delta=1e-3 that restores best weights on trigger. Verify it stops training and the loaded model has the best val_loss.",
    ps="""
import torch, torch.nn as nn, copy

class EarlyStopping:
    def __init__(self, patience=10, min_delta=1e-3):
        self.patience = patience
        self.min_delta = min_delta
        # TODO: add best_loss, best_weights, counter
        pass

    def __call__(self, model, val_loss):
        # TODO: update counter, save best weights, return True to stop
        pass

model = nn.Sequential(nn.Linear(10,32), nn.ReLU(), nn.Linear(32,1))
opt = torch.optim.Adam(model.parameters(), lr=1e-2)
X = torch.randn(100,10); y = X[:,0:1]
Xv = torch.randn(50,10); yv = Xv[:,0:1]
""".strip()
)

# ── Section 23: Gradient Clipping & Mixed Precision ──────────────────────────
s23 = make_section(23, "Gradient Clipping & Mixed Precision",
    "Gradient clipping prevents exploding gradients in deep RNNs and Transformers. Mixed precision (FP16/BF16) training halves memory usage and speeds up training on modern GPUs using GradScaler.",
    c1t="Gradient Clipping",
    c1="""
import torch, torch.nn as nn, numpy as np

torch.manual_seed(42)

class DeepRNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.rnn = nn.RNN(10, 64, 4, batch_first=True)
        self.fc = nn.Linear(64, 1)
    def forward(self, x):
        out, _ = self.rnn(x)
        return self.fc(out[:, -1]).squeeze()

def grad_norm(model):
    return sum(p.grad.data.norm(2).item()**2 for p in model.parameters()
               if p.grad is not None)**0.5

X = torch.randn(16, 50, 10); y = torch.randn(16)
model = DeepRNN()
opt = torch.optim.SGD(model.parameters(), lr=0.1)
crit = nn.MSELoss()

print("Gradient norms (before/after clip):")
for step in range(10):
    loss = crit(model(X), y)
    opt.zero_grad(); loss.backward()
    gn_before = grad_norm(model)
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
    gn_after = grad_norm(model)
    opt.step()
    if step < 5:
        print(f"  Step {step+1}: before={gn_before:.2f}, after={gn_after:.2f} (clipped={gn_before>1.0})")
""".strip(),
    c2t="Mixed Precision Training Pattern",
    c2="""
import torch, torch.nn as nn, time

torch.manual_seed(42)

class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(128, 256), nn.ReLU(), nn.Linear(256, 128), nn.ReLU(), nn.Linear(128, 10))
    def forward(self, x): return self.net(x)

X = torch.randn(256, 128); y = torch.randint(0, 10, (256,))
crit = nn.CrossEntropyLoss()

# Standard FP32
model1 = Model()
opt1 = torch.optim.AdamW(model1.parameters(), lr=1e-3)
t0 = time.time()
for _ in range(200):
    l = crit(model1(X), y); opt1.zero_grad(); l.backward(); opt1.step()
fp32_t = time.time()-t0

# AMP pattern (works on CPU too, GPU gets real speedup)
model2 = Model()
opt2 = torch.optim.AdamW(model2.parameters(), lr=1e-3)
scaler = torch.amp.GradScaler('cpu', enabled=False)
t0 = time.time()
for _ in range(200):
    with torch.amp.autocast('cpu', dtype=torch.float32):
        l = crit(model2(X), y)
    scaler.scale(l).backward()
    scaler.unscale_(opt2)
    torch.nn.utils.clip_grad_norm_(model2.parameters(), 1.0)
    scaler.step(opt2); scaler.update(); opt2.zero_grad()
amp_t = time.time()-t0

print(f"FP32 time: {fp32_t:.2f}s, AMP pattern time: {amp_t:.2f}s")
print(f"FP32 loss: {crit(model1(X),y).item():.4f}")
print(f"AMP  loss: {crit(model2(X),y).item():.4f}")
print("\\nAMP Best Practices:")
for tip in ["Use autocast for forward pass only",
            "Use GradScaler to prevent FP16 underflow",
            "Clip gradients AFTER scaler.unscale_()",
            "BF16 more stable than FP16 (Ampere+ GPUs only)"]:
    print(f"  - {tip}")
""".strip(),
    c3t="Gradient Monitoring & Debugging",
    c3="""
import torch, torch.nn as nn, numpy as np

torch.manual_seed(42)

class MultiLayerNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.ModuleList([
            nn.Linear(20, 64), nn.Linear(64, 32), nn.Linear(32, 16), nn.Linear(16, 1)])
        self.relu = nn.ReLU()
    def forward(self, x):
        for layer in self.layers[:-1]:
            x = self.relu(layer(x))
        return self.layers[-1](x).squeeze()

model = MultiLayerNet()
opt = torch.optim.Adam(model.parameters(), lr=1e-3)
crit = nn.MSELoss()
X = torch.randn(64, 20); y = torch.randn(64)

print("Gradient statistics per layer:")
for epoch in [1, 10, 50]:
    for _ in range(epoch if epoch==1 else 9):
        loss = crit(model(X), y); opt.zero_grad(); loss.backward(); opt.step()
    print(f"\\nEpoch {epoch}:")
    for name, p in model.named_parameters():
        if p.grad is not None:
            gn = p.grad.norm().item()
            wn = p.data.norm().item()
            print(f"  {name:<25}: grad_norm={gn:.4f}, weight_norm={wn:.4f}, ratio={gn/wn:.4f}")

# Detect vanishing/exploding gradients
print("\\nGradient health check:")
for name, p in model.named_parameters():
    if p.grad is not None:
        gn = p.grad.norm().item()
        status = "EXPLODING" if gn > 10 else ("VANISHING" if gn < 1e-5 else "OK")
        print(f"  {name:<25}: {status} (norm={gn:.6f})")
""".strip(),
    rw_scenario="Your stacked LSTM diverges after 10 epochs. Apply gradient clipping (max_norm=0.5), monitor per-layer gradient norms, and add mixed precision training pattern for GPU efficiency.",
    rw_code="""
import torch, torch.nn as nn, numpy as np

torch.manual_seed(42)

class StackedLSTM(nn.Module):
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(10, 128, 4, batch_first=True, dropout=0.2)
        self.fc = nn.Linear(128, 1)
    def forward(self, x):
        out, _ = self.lstm(x)
        return self.fc(out[:, -1]).squeeze()

model = StackedLSTM()
opt = torch.optim.Adam(model.parameters(), lr=5e-3)
crit = nn.MSELoss()
X = torch.randn(32, 40, 10); y = torch.randn(32)
scaler = torch.amp.GradScaler('cpu', enabled=False)

print("Training with gradient clipping:")
for epoch in range(30):
    with torch.amp.autocast('cpu', dtype=torch.float32):
        pred = model(X); loss = crit(pred, y)
    scaler.scale(loss).backward()
    scaler.unscale_(opt)
    gn_before = sum(p.grad.norm()**2 for p in model.parameters() if p.grad is not None)**0.5
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=0.5)
    gn_after = sum(p.grad.norm()**2 for p in model.parameters() if p.grad is not None)**0.5
    scaler.step(opt); scaler.update(); opt.zero_grad()
    if (epoch+1) % 10 == 0:
        print(f"Epoch {epoch+1}: loss={loss.item():.4f}, grad={gn_before.item():.3f}->{gn_after.item():.3f}")
""".strip(),
    pt="Gradient Clipping + Monitoring",
    pd_text="Train a 3-layer RNN and clip gradients with max_norm=1.0. Print gradient norm before and after clipping every 10 epochs.",
    ps="""
import torch, torch.nn as nn

model = nn.RNN(10, 64, 3, batch_first=True)
fc = nn.Linear(64, 1)
params = list(model.parameters()) + list(fc.parameters())
opt = torch.optim.Adam(params, lr=1e-2)
X = torch.randn(16, 30, 10); y = torch.randn(16)
# 1. Forward: out, _ = model(X); pred = fc(out[:,-1]).squeeze()
# 2. MSELoss backward
# 3. Print grad norm BEFORE clip_grad_norm_
# 4. Apply clip_grad_norm_ max_norm=1.0
# 5. Print grad norm AFTER
# 6. optimizer.step()
""".strip()
)

# ── Section 24: Model Export & Deployment ─────────────────────────────────────
s24 = make_section(24, "Model Export & Deployment",
    "Export PyTorch models via TorchScript for language-agnostic C++/mobile deployment, ONNX for cross-framework serving, or pickle for sklearn models. Production deployment requires consistent preprocessing and health checks.",
    c1t="TorchScript Export",
    c1="""
import torch, torch.nn as nn, os

torch.manual_seed(42)

class Classifier(nn.Module):
    def __init__(self, n_in=20, n_classes=3):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_in, 64), nn.ReLU(), nn.Dropout(0.2),
            nn.Linear(64, 32), nn.ReLU(), nn.Linear(32, n_classes))
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return torch.softmax(self.net(x), dim=-1)

model = Classifier(); model.eval()
x = torch.randn(5, 20)
original_out = model(x)

# trace: for fixed control flow
traced = torch.jit.trace(model, x)

# script: for dynamic control flow
scripted = torch.jit.script(model)
scripted.save("/tmp/classifier.pt")

loaded = torch.jit.load("/tmp/classifier.pt"); loaded.eval()
loaded_out = loaded(x)

print(f"TorchScript size: {os.path.getsize('/tmp/classifier.pt')/1024:.1f} KB")
print(f"Outputs match: {torch.allclose(original_out, loaded_out, atol=1e-5)}")
print(f"Batch preds: {loaded(torch.randn(8,20)).argmax(1).tolist()}")
""".strip(),
    c2t="ONNX Export",
    c2="""
import torch, torch.nn as nn, os

torch.manual_seed(42)

class Regressor(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(10,32), nn.ReLU(), nn.Linear(32,1))
    def forward(self, x): return self.net(x)

model = Regressor(); model.eval()
dummy = torch.randn(1, 10)

torch.onnx.export(
    model, dummy, "/tmp/regressor.onnx",
    input_names=["features"], output_names=["prediction"],
    dynamic_axes={"features": {0: "batch"}, "prediction": {0: "batch"}},
    opset_version=17)

print(f"ONNX file: {os.path.getsize('/tmp/regressor.onnx')/1024:.1f} KB")

try:
    import onnx
    m = onnx.load("/tmp/regressor.onnx")
    onnx.checker.check_model(m)
    print("ONNX check: PASSED")
    print(f"  Inputs:  {[i.name for i in m.graph.input]}")
    print(f"  Outputs: {[o.name for o in m.graph.output]}")
except ImportError:
    print("Install onnx: pip install onnx")

# Deployment comparison
print("\\nDeployment Format Comparison:")
for fmt, use_case in [
    ("TorchScript", "C++ microservice, mobile (TorchMobile)"),
    ("ONNX",        "Cross-framework, ONNX Runtime, mobile"),
    ("Pickle",      "Python-only, sklearn, quick prototyping"),
    ("TF SavedModel","TensorFlow Serving, TFLite mobile"),
]:
    print(f"  {fmt:<15}: {use_case}")
""".strip(),
    c3t="Production Deployment Checklist",
    c3="""
import torch, torch.nn as nn, pickle, json, time, os

torch.manual_seed(42)

# Full deployment pipeline: train -> validate -> export -> health check
class ProductionModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(10,32), nn.ReLU(), nn.Linear(32,3))
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return torch.softmax(self.net(x), dim=-1)

# Train
model = ProductionModel()
X = torch.randn(200, 10); y = torch.randint(0, 3, (200,))
opt = torch.optim.Adam(model.parameters(), lr=1e-3)
for _ in range(100):
    l = nn.CrossEntropyLoss()(model(X), y); opt.zero_grad(); l.backward(); opt.step()

model.eval()
test_acc = (model(X).argmax(1)==y).float().mean().item()
print(f"Model accuracy: {test_acc:.4f}")

# Export
scripted = torch.jit.script(model)
scripted.save("/tmp/prod_model.pt")
scripted_size = os.path.getsize("/tmp/prod_model.pt")/1024

# Health check function
def health_check(model_path, test_input_shape=(1, 10)):
    loaded = torch.jit.load(model_path); loaded.eval()
    x_test = torch.randn(*test_input_shape)
    t0 = time.time()
    with torch.no_grad():
        out = loaded(x_test)
    latency_ms = (time.time()-t0)*1000
    return {
        "status": "healthy",
        "output_shape": list(out.shape),
        "output_sum_to_1": bool(abs(out.sum().item()-1) < 1e-4),
        "latency_ms": round(latency_ms, 3),
        "model_size_kb": round(scripted_size, 1),
    }

health = health_check("/tmp/prod_model.pt")
print("\\nHealth Check:", json.dumps(health, indent=2))

# Deployment manifest
manifest = {
    "model_path": "/tmp/prod_model.pt",
    "format": "TorchScript",
    "input": {"name": "features", "shape": [-1, 10], "dtype": "float32"},
    "output": {"name": "probabilities", "shape": [-1, 3]},
    "accuracy": round(test_acc, 4),
}
print("\\nDeployment Manifest:", json.dumps(manifest, indent=2))
""".strip(),
    rw_scenario="Deploy a PyTorch model to a REST microservice AND a mobile app. Export as TorchScript for the microservice and ONNX for mobile. Verify identical predictions across formats.",
    rw_code="""
import torch, torch.nn as nn, os

torch.manual_seed(42)

class MultiOutputModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(15,64), nn.ReLU(), nn.Linear(64,32), nn.ReLU(), nn.Linear(32,4))
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return torch.softmax(self.net(x), dim=-1)

# Train
model = MultiOutputModel()
X = torch.randn(200, 15); y = torch.randint(0, 4, (200,))
for _ in range(100):
    l = nn.CrossEntropyLoss()(model(X), y)
    l.backward(); torch.optim.Adam(model.parameters()).step()
model.eval()

test = torch.randn(5, 15)
orig_out = model(test).detach()

# Export TorchScript
scripted = torch.jit.script(model)
scripted.save("/tmp/multi.pt")
ts_out = torch.jit.load("/tmp/multi.pt")(test).detach()

# Export ONNX
torch.onnx.export(model, torch.randn(1,15), "/tmp/multi.onnx",
                  input_names=["x"], output_names=["probs"],
                  dynamic_axes={"x":{0:"batch"},"probs":{0:"batch"}}, opset_version=17)

print(f"TorchScript match: {torch.allclose(orig_out, ts_out, atol=1e-5)}")
print(f"ONNX size: {os.path.getsize('/tmp/multi.onnx')/1024:.1f} KB")
print(f"Predictions: {orig_out[:3].numpy().round(4)}")
""".strip(),
    pt="Export and Verify a Model",
    pd_text="Train a simple classifier, export it via TorchScript (script), save to disk, reload, and verify predictions match with torch.allclose.",
    ps="""
import torch, torch.nn as nn

class Net(nn.Module):
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # TODO: add layers
        pass

model = Net(); model.eval()
# 1. torch.jit.script(model) -> scripted
# 2. scripted.save("/tmp/net.pt")
# 3. loaded = torch.jit.load("/tmp/net.pt")
# 4. x = torch.randn(4, 10)
# 5. Assert torch.allclose(model(x), loaded(x))
""".strip()
)

# ── Assemble ──────────────────────────────────────────────────────────────────
all_sections = s17 + s18 + s19 + s20 + s21 + s22 + s23 + s24
result = insert_before_make_html(FILE, all_sections)
print("SUCCESS" if result else "FAILED")
