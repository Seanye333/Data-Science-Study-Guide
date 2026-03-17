"""Add 3 sections each to gen_deep_learning.py and gen_streamlit.py (code1/code2/code3/code4 format)."""
import os

BASE = r"c:\Users\seany\Documents\All Codes\Data Science Study Path"

def ec(s):
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace("'", "\\'")

def ct(code, indent="            "):
    """Convert multi-line code to tuple-concatenation format with escaping."""
    lines = code.split('\n')
    parts = []
    for line in lines:
        escaped = line.replace('\\', '\\\\').replace('"', '\\"')
        parts.append(f'{indent}"{escaped}\\n"')
    return "(\n" + "\n".join(parts) + "\n        )"

def make_section4(num, title, desc,
                  c1t, c1, c2t, c2, c3t=None, c3=None, c4t=None, c4=None,
                  rw_scenario="", rw_code="",
                  pt="", pd="", ps=""):
    s = f'    {{\n'
    s += f'        "title": "{num}. {title}",\n'
    s += f'        "desc": "{ec(desc)}",\n'
    s += f'        "code1_title": "{c1t}",\n'
    s += f'        "code1": {ct(c1)},\n'
    s += f'        "code2_title": "{c2t}",\n'
    s += f'        "code2": {ct(c2)},\n'
    if c3t and c3:
        s += f'        "code3_title": "{c3t}",\n'
        s += f'        "code3": {ct(c3)},\n'
    if c4t and c4:
        s += f'        "code4_title": "{c4t}",\n'
        s += f'        "code4": {ct(c4)},\n'
    s += f'        "rw_scenario": "{ec(rw_scenario)}",\n'
    s += f'        "rw_code": {ct(rw_code)},\n'
    s += f'        "practice": {{\n'
    s += f'            "title": "{pt}",\n'
    s += f'            "desc": "{ec(pd)}",\n'
    s += f'            "starter": {ct(ps)},\n'
    s += f'        }},\n'
    s += f'    }},\n'
    return s

def insert_code4(filepath, new_sections_str):
    content = open(filepath, encoding='utf-8').read()
    marker = '\n]\n\n\ndef make_html'
    idx = content.find(marker)
    if idx == -1:
        print(f"ERROR: marker not found in {filepath}")
        return False
    insert_str = content[:idx] + '\n' + new_sections_str + content[idx:]
    open(filepath, 'w', encoding='utf-8').write(insert_str)
    print(f"OK: inserted sections into {filepath}")
    return True

# ═══════════════════════════════════════════════════════════════════
#  DEEP LEARNING SECTIONS
# ═══════════════════════════════════════════════════════════════════

dl14_c1 = """import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np

np.random.seed(42); torch.manual_seed(42)
# Simulate image-like data
X = torch.randn(1000, 1, 28, 28)
y = torch.randint(0, 10, (1000,))

class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.pool  = nn.MaxPool2d(2, 2)
        self.relu  = nn.ReLU()
        self.fc1   = nn.Linear(32 * 7 * 7, 128)
        self.fc2   = nn.Linear(128, 10)
        self.dropout = nn.Dropout(0.3)

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))  # -> (16, 14, 14)
        x = self.pool(self.relu(self.conv2(x)))  # -> (32, 7, 7)
        x = x.view(x.size(0), -1)
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        return self.fc2(x)

model = SimpleCNN()
print(f"Parameters: {sum(p.numel() for p in model.parameters()):,}")
loader = DataLoader(TensorDataset(X, y), batch_size=32)
x_batch, _ = next(iter(loader))
out = model(x_batch)
print(f"Output shape: {out.shape}")"""

dl14_c2 = """import torch
import torch.nn as nn
import numpy as np

class ResidualBlock(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.conv1 = nn.Conv2d(channels, channels, 3, padding=1)
        self.bn1   = nn.BatchNorm2d(channels)
        self.conv2 = nn.Conv2d(channels, channels, 3, padding=1)
        self.bn2   = nn.BatchNorm2d(channels)
        self.relu  = nn.ReLU()

    def forward(self, x):
        identity = x
        out = self.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        return self.relu(out + identity)  # skip connection

class MiniResNet(nn.Module):
    def __init__(self, n_classes=10):
        super().__init__()
        self.stem   = nn.Conv2d(1, 32, 3, padding=1)
        self.res1   = ResidualBlock(32)
        self.pool   = nn.AdaptiveAvgPool2d(4)
        self.fc     = nn.Linear(32 * 4 * 4, n_classes)

    def forward(self, x):
        x = torch.relu(self.stem(x))
        x = self.res1(x)
        x = self.pool(x)
        return self.fc(x.flatten(1))

model = MiniResNet()
x = torch.randn(8, 1, 28, 28)
print(f"Output shape: {model(x).shape}")
print(f"Params: {sum(p.numel() for p in model.parameters()):,}")"""

dl14_c3 = """import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np

torch.manual_seed(0); np.random.seed(0)
# Multi-class classification
X = torch.randn(2000, 3, 32, 32)
y = torch.randint(0, 5, (2000,))

class CNN3(nn.Module):
    def __init__(self, n_classes=5):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1), nn.BatchNorm2d(32), nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.BatchNorm2d(64), nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1), nn.ReLU(),
            nn.AdaptiveAvgPool2d(2),
            nn.Flatten(),
            nn.Linear(128*4, 256), nn.ReLU(), nn.Dropout(0.4),
            nn.Linear(256, n_classes)
        )
    def forward(self, x): return self.net(x)

model = CNN3()
loader = DataLoader(TensorDataset(X[:200], y[:200]), batch_size=32, shuffle=True)
opt  = optim.Adam(model.parameters(), lr=1e-3)
loss_fn = nn.CrossEntropyLoss()
for epoch in range(3):
    total_loss = 0
    for xb, yb in loader:
        opt.zero_grad()
        loss = loss_fn(model(xb), yb)
        loss.backward(); opt.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1}: loss={total_loss/len(loader):.4f}")"""

dl14_c4 = """import torch
import torch.nn as nn
import numpy as np

# Transfer learning simulation with pretrained-like frozen backbone
class FrozenBackbone(nn.Module):
    def __init__(self):
        super().__init__()
        # Simulated frozen backbone (fixed weights)
        self.backbone = nn.Sequential(
            nn.Conv2d(3, 64, 3, padding=1), nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1), nn.ReLU(),
            nn.AdaptiveAvgPool2d(4),
        )
        # Freeze backbone
        for p in self.backbone.parameters():
            p.requires_grad = False
        # Trainable head
        self.head = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128*16, 256), nn.ReLU(), nn.Dropout(0.3),
            nn.Linear(256, 3)   # 3 classes
        )
    def forward(self, x):
        with torch.no_grad():
            features = self.backbone(x)
        return self.head(features)

model = FrozenBackbone()
frozen = sum(p.numel() for p in model.parameters() if not p.requires_grad)
trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"Frozen params:    {frozen:,}")
print(f"Trainable params: {trainable:,}")
x = torch.randn(4, 3, 64, 64)
print(f"Output: {model(x).shape}")"""

dl14_rw_code = """import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np

torch.manual_seed(7); np.random.seed(7)
# Simulate chest X-ray binary classification (pneumonia vs normal)
n_train, n_val = 800, 200
X_tr = torch.randn(n_train, 1, 64, 64)
y_tr = torch.randint(0, 2, (n_train,))
X_va = torch.randn(n_val,   1, 64, 64)
y_va = torch.randint(0, 2, (n_val,))

class ChestCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=1), nn.BatchNorm2d(32), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.BatchNorm2d(64), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1), nn.ReLU(), nn.AdaptiveAvgPool2d(4),
            nn.Flatten(), nn.Linear(128*16, 256), nn.ReLU(), nn.Dropout(0.5),
            nn.Linear(256, 2)
        )
    def forward(self, x): return self.net(x)

model = ChestCNN()
opt = optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)
loss_fn = nn.CrossEntropyLoss()
tr_loader = DataLoader(TensorDataset(X_tr, y_tr), batch_size=32, shuffle=True)
for epoch in range(3):
    model.train(); tr_loss = 0
    for xb, yb in tr_loader:
        opt.zero_grad(); loss = loss_fn(model(xb), yb)
        loss.backward(); opt.step(); tr_loss += loss.item()
    model.eval()
    with torch.no_grad():
        val_pred = model(X_va).argmax(1)
        val_acc = (val_pred == y_va).float().mean()
    print(f"Epoch {epoch+1}: loss={tr_loss/len(tr_loader):.4f}, val_acc={val_acc:.4f}")"""

dl14_ps = """import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
torch.manual_seed(0); np.random.seed(0)
# CIFAR-10 like: 3-channel 32x32, 10 classes
X = torch.randn(1000, 3, 32, 32)
y = torch.randint(0, 10, (1000,))
X_val = torch.randn(200, 3, 32, 32)
y_val = torch.randint(0, 10, (200,))
# TODO: Build CNN with at least 3 conv layers + batch norm + dropout
# TODO: Add a residual skip connection in one of the layers
# TODO: Train for 5 epochs, log train loss + val accuracy
# TODO: Report param count (frozen vs trainable)
# TODO: Try learning rate 1e-3 vs 1e-4 and compare convergence
"""

dl14 = make_section4(
    "14", "Convolutional Neural Networks (CNNs)",
    "CNNs use learnable filters to detect spatial patterns in images. Conv layers extract local features, pooling reduces dimensionality, and residual connections enable training very deep networks by solving the vanishing gradient problem.",
    "Simple CNN Classifier", dl14_c1,
    "Residual Block & Skip Connections", dl14_c2,
    "3-Channel CNN with BatchNorm", dl14_c3,
    "Transfer Learning: Frozen Backbone", dl14_c4,
    rw_scenario="Medical imaging: classify chest X-rays (pneumonia vs normal) using a CNN with BatchNorm + Dropout. Freeze a pretrained backbone and only train the classification head to maximize data efficiency.",
    rw_code=dl14_rw_code,
    pt="CIFAR-10 Style CNN",
    pd="Build a CNN for 10-class image classification on 1000 simulated 32x32 RGB images. Include at least 3 conv layers with BatchNorm, one residual connection, and Dropout. Train for 5 epochs. Compare 1e-3 vs 1e-4 learning rates and report train loss + val accuracy.",
    ps=dl14_ps
)

dl15_c1 = """import torch
import torch.nn as nn
import numpy as np

class TransformerBlock(nn.Module):
    def __init__(self, d_model, n_heads, d_ff, dropout=0.1):
        super().__init__()
        self.attn  = nn.MultiheadAttention(d_model, n_heads, batch_first=True, dropout=dropout)
        self.ff    = nn.Sequential(
            nn.Linear(d_model, d_ff), nn.GELU(), nn.Linear(d_ff, d_model)
        )
        self.ln1 = nn.LayerNorm(d_model)
        self.ln2 = nn.LayerNorm(d_model)
        self.drop = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        # Pre-norm formulation
        attn_out, weights = self.attn(self.ln1(x), self.ln1(x), self.ln1(x))
        x = x + self.drop(attn_out)
        x = x + self.drop(self.ff(self.ln2(x)))
        return x, weights

d_model, n_heads, d_ff = 64, 4, 256
block = TransformerBlock(d_model, n_heads, d_ff)
x = torch.randn(8, 20, d_model)  # batch=8, seq_len=20
out, weights = block(x)
print(f"Output shape:  {out.shape}")
print(f"Attn weights:  {weights.shape}")"""

dl15_c2 = """import torch
import torch.nn as nn
import numpy as np

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=512, dropout=0.1):
        super().__init__()
        self.dropout = nn.Dropout(dropout)
        pe = torch.zeros(max_len, d_model)
        pos = torch.arange(max_len).unsqueeze(1)
        div = torch.exp(torch.arange(0, d_model, 2) * (-torch.log(torch.tensor(10000.0)) / d_model))
        pe[:, 0::2] = torch.sin(pos * div)
        pe[:, 1::2] = torch.cos(pos * div)
        self.register_buffer("pe", pe.unsqueeze(0))

    def forward(self, x):
        return self.dropout(x + self.pe[:, :x.size(1)])

class TextTransformer(nn.Module):
    def __init__(self, vocab_size=1000, d_model=64, n_heads=4, n_layers=2, n_classes=3):
        super().__init__()
        self.embed   = nn.Embedding(vocab_size, d_model, padding_idx=0)
        self.pos_enc = PositionalEncoding(d_model)
        encoder_layer = nn.TransformerEncoderLayer(d_model, n_heads, dim_feedforward=256,
                                                    batch_first=True, norm_first=True)
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=n_layers)
        self.classifier = nn.Linear(d_model, n_classes)

    def forward(self, x, src_key_padding_mask=None):
        x = self.pos_enc(self.embed(x))
        x = self.encoder(x, src_key_padding_mask=src_key_padding_mask)
        return self.classifier(x.mean(dim=1))  # mean pooling

model = TextTransformer()
tokens = torch.randint(1, 1000, (4, 30))  # batch=4, seq_len=30
out = model(tokens)
print(f"Output: {out.shape}, params: {sum(p.numel() for p in model.parameters()):,}")"""

dl15_c3 = """import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

torch.manual_seed(0)
# Text classification with Transformer
vocab_size, d_model, n_classes = 500, 32, 4
class MiniTransformer(nn.Module):
    def __init__(self):
        super().__init__()
        self.embed   = nn.Embedding(vocab_size, d_model, padding_idx=0)
        layer = nn.TransformerEncoderLayer(d_model, 4, 128, batch_first=True, norm_first=True)
        self.encoder = nn.TransformerEncoder(layer, num_layers=2)
        self.head    = nn.Linear(d_model, n_classes)
    def forward(self, x):
        mask = (x == 0)
        return self.head(self.encoder(self.embed(x), src_key_padding_mask=mask).mean(1))

model = MiniTransformer()
X = torch.randint(0, vocab_size, (200, 20))
X[:, 15:] = 0  # padding
y = torch.randint(0, n_classes, (200,))
loader = torch.utils.data.DataLoader(
    torch.utils.data.TensorDataset(X, y), batch_size=32, shuffle=True)
opt = optim.Adam(model.parameters(), lr=3e-4)
for epoch in range(5):
    total = 0
    for xb, yb in loader:
        opt.zero_grad(); loss = nn.CrossEntropyLoss()(model(xb), yb)
        loss.backward(); opt.step(); total += loss.item()
    print(f"Epoch {epoch+1}: loss={total/len(loader):.4f}")"""

dl15_rw_code = """import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

torch.manual_seed(42)
# Sentiment analysis with Transformer on simulated review data
vocab_size = 2000
class SentimentTransformer(nn.Module):
    def __init__(self, d=64, h=4, layers=2):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, d, padding_idx=0)
        enc_layer  = nn.TransformerEncoderLayer(d, h, d*4, batch_first=True, norm_first=True, dropout=0.1)
        self.encoder = nn.TransformerEncoder(enc_layer, num_layers=layers)
        self.head = nn.Sequential(nn.Linear(d, 32), nn.ReLU(), nn.Linear(32, 2))

    def forward(self, x):
        pad_mask = (x == 0)
        z = self.encoder(self.embed(x), src_key_padding_mask=pad_mask)
        return self.head(z.mean(dim=1))

model = SentimentTransformer()
n = 500
X = torch.randint(1, vocab_size, (n, 40))
X[:, 35:] = 0  # simulate padding
y = torch.randint(0, 2, (n,))
X_val, y_val = X[:100], y[:100]
X_tr,  y_tr  = X[100:], y[100:]
loader = torch.utils.data.DataLoader(
    torch.utils.data.TensorDataset(X_tr, y_tr), batch_size=32, shuffle=True)
opt = optim.AdamW(model.parameters(), lr=3e-4, weight_decay=1e-4)
for epoch in range(5):
    model.train(); tr_loss = 0
    for xb, yb in loader:
        opt.zero_grad(); loss = nn.CrossEntropyLoss()(model(xb), yb)
        loss.backward(); opt.step(); tr_loss += loss.item()
    model.eval()
    with torch.no_grad():
        val_acc = (model(X_val).argmax(1) == y_val).float().mean()
    print(f"Epoch {epoch+1}: loss={tr_loss/len(loader):.4f}, val_acc={val_acc:.4f}")"""

dl15_ps = """import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

torch.manual_seed(3)
vocab_size = 1000
# Simulated multi-class text classification (4 categories)
X = torch.randint(1, vocab_size, (600, 50))
X[:, 45:] = 0  # padding
y = torch.randint(0, 4, (600,))
X_val, y_val = X[:100], y[:100]
X_tr,  y_tr  = X[100:], y[100:]
# TODO: Build TransformerEncoder with 3 layers, d_model=64, n_heads=4
# TODO: Add positional encoding (sinusoidal)
# TODO: Use mean pooling over sequence before classification head
# TODO: Train with AdamW + cosine LR schedule for 8 epochs
# TODO: Report train loss and val accuracy each epoch
# TODO: Print total parameter count
"""

dl15 = make_section4(
    "15", "Transformer Architecture & Attention Mechanisms",
    "Transformers use self-attention to relate every position to every other position in a sequence. Multi-head attention, positional encoding, and residual connections make them the foundation of modern NLP and vision models.",
    "Transformer Block with Multi-Head Attention", dl15_c1,
    "Text Classification Transformer", dl15_c2,
    "Training a Mini-Transformer on Text", dl15_c3,
    rw_scenario="Customer review sentiment: train a 2-layer Transformer encoder on tokenized product reviews (padded to 40 tokens) to classify positive vs negative sentiment with AdamW optimizer.",
    rw_code=dl15_rw_code,
    pt="News Category Transformer",
    pd="Build a 3-layer Transformer encoder with sinusoidal positional encoding for 4-class news categorization. Use AdamW with cosine LR scheduling. Train for 8 epochs on 500 simulated sequences (length 50, vocab 1000) with padding. Report val accuracy and param count.",
    ps=dl15_ps
)

dl16_c1 = """import torch
import torch.nn as nn
import numpy as np

# Variational Autoencoder (VAE)
class VAE(nn.Module):
    def __init__(self, input_dim=784, hidden=256, latent=16):
        super().__init__()
        self.encoder = nn.Sequential(nn.Linear(input_dim, hidden), nn.ReLU())
        self.mu_layer  = nn.Linear(hidden, latent)
        self.log_var_layer = nn.Linear(hidden, latent)
        self.decoder = nn.Sequential(
            nn.Linear(latent, hidden), nn.ReLU(),
            nn.Linear(hidden, input_dim), nn.Sigmoid()
        )
    def encode(self, x):
        h = self.encoder(x)
        return self.mu_layer(h), self.log_var_layer(h)
    def reparameterize(self, mu, log_var):
        std = torch.exp(0.5 * log_var)
        eps = torch.randn_like(std)
        return mu + eps * std
    def forward(self, x):
        mu, log_var = self.encode(x)
        z = self.reparameterize(mu, log_var)
        return self.decoder(z), mu, log_var

vae = VAE()
x = torch.randn(32, 784).clamp(0, 1)
recon, mu, log_var = vae(x)
recon_loss = nn.functional.binary_cross_entropy(recon, x, reduction="sum")
kl_loss = -0.5 * torch.sum(1 + log_var - mu.pow(2) - log_var.exp())
loss = recon_loss + kl_loss
print(f"Recon loss: {recon_loss.item():.2f}, KL loss: {kl_loss.item():.2f}")
print(f"Latent shape: {mu.shape}")"""

dl16_c2 = """import torch
import torch.nn as nn
import numpy as np

# Simple GAN for 1D distribution
class Generator(nn.Module):
    def __init__(self, z_dim=8, out_dim=1):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(z_dim, 32), nn.LeakyReLU(0.2),
            nn.Linear(32, 64), nn.LeakyReLU(0.2),
            nn.Linear(64, out_dim)
        )
    def forward(self, z): return self.net(z)

class Discriminator(nn.Module):
    def __init__(self, in_dim=1):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, 64), nn.LeakyReLU(0.2),
            nn.Linear(64, 32), nn.LeakyReLU(0.2),
            nn.Linear(32, 1), nn.Sigmoid()
        )
    def forward(self, x): return self.net(x)

torch.manual_seed(0)
G, D = Generator(), Discriminator()
G_opt = torch.optim.Adam(G.parameters(), lr=2e-4, betas=(0.5, 0.999))
D_opt = torch.optim.Adam(D.parameters(), lr=2e-4, betas=(0.5, 0.999))
bce = nn.BCELoss()
# Target: N(3, 0.5) distribution
for step in range(300):
    real = torch.randn(64, 1) * 0.5 + 3.0
    z = torch.randn(64, 8)
    fake = G(z)
    d_loss = bce(D(real), torch.ones(64,1)) + bce(D(fake.detach()), torch.zeros(64,1))
    D_opt.zero_grad(); d_loss.backward(); D_opt.step()
    g_loss = bce(D(G(torch.randn(64,8))), torch.ones(64,1))
    G_opt.zero_grad(); g_loss.backward(); G_opt.step()
with torch.no_grad():
    samples = G(torch.randn(1000, 8)).squeeze()
print(f"Generated: mean={samples.mean():.3f}, std={samples.std():.3f}")
print(f"Target:    mean=3.000, std=0.500")"""

dl16_c3 = """import torch
import torch.nn as nn
import numpy as np

# Autoencoder for anomaly detection
class Autoencoder(nn.Module):
    def __init__(self, input_dim=20, bottleneck=4):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 12), nn.ReLU(),
            nn.Linear(12, bottleneck), nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(bottleneck, 12), nn.ReLU(),
            nn.Linear(12, input_dim)
        )
    def forward(self, x):
        return self.decoder(self.encoder(x))

torch.manual_seed(5)
ae = Autoencoder()
# Train on normal data
X_normal = torch.randn(500, 20)
opt = torch.optim.Adam(ae.parameters(), lr=1e-3)
loader = torch.utils.data.DataLoader(X_normal, batch_size=32, shuffle=True)
for epoch in range(20):
    for xb in loader:
        recon = ae(xb)
        loss = nn.MSELoss()(recon, xb)
        opt.zero_grad(); loss.backward(); opt.step()
# Anomaly detection
X_test_normal = torch.randn(50, 20)
X_test_anomaly = torch.randn(10, 20) * 3  # out-of-distribution
X_test = torch.cat([X_test_normal, X_test_anomaly])
labels = torch.cat([torch.zeros(50), torch.ones(10)])
with torch.no_grad():
    errors = ((ae(X_test) - X_test)**2).mean(dim=1)
threshold = errors[:50].mean() + 2*errors[:50].std()
preds = (errors > threshold).float()
accuracy = (preds == labels).float().mean()
print(f"Anomaly threshold: {threshold:.4f}")
print(f"Detection accuracy: {accuracy:.4f}")"""

dl16_rw_code = """import torch
import torch.nn as nn
import numpy as np

torch.manual_seed(42)
# VAE for anomaly detection in manufacturing sensor data
input_dim, latent_dim = 15, 4

class SensorVAE(nn.Module):
    def __init__(self):
        super().__init__()
        self.enc = nn.Sequential(nn.Linear(input_dim, 32), nn.ELU())
        self.mu  = nn.Linear(32, latent_dim)
        self.lv  = nn.Linear(32, latent_dim)
        self.dec = nn.Sequential(
            nn.Linear(latent_dim, 32), nn.ELU(),
            nn.Linear(32, input_dim)
        )
    def forward(self, x):
        h = self.enc(x)
        mu, lv = self.mu(h), self.lv(h)
        z = mu + torch.exp(0.5*lv) * torch.randn_like(mu)
        return self.dec(z), mu, lv

vae = SensorVAE()
X_normal = torch.randn(1000, input_dim)
loader = torch.utils.data.DataLoader(X_normal, batch_size=64, shuffle=True)
opt = torch.optim.Adam(vae.parameters(), lr=1e-3)
for epoch in range(15):
    total = 0
    for xb in loader:
        recon, mu, lv = vae(xb)
        recon_loss = nn.MSELoss(reduction="sum")(recon, xb)
        kl = -0.5 * torch.sum(1 + lv - mu.pow(2) - lv.exp())
        loss = recon_loss + 0.1 * kl
        opt.zero_grad(); loss.backward(); opt.step()
        total += loss.item()
    if epoch % 5 == 4:
        print(f"Epoch {epoch+1}: loss={total/len(loader):.2f}")
vae.eval()
X_test_norm = torch.randn(100, input_dim)
X_test_anom = torch.randn(20, input_dim) * 4
X_all = torch.cat([X_test_norm, X_test_anom])
true_labels = torch.cat([torch.zeros(100), torch.ones(20)])
with torch.no_grad():
    recon_all, _, _ = vae(X_all)
    errors = ((recon_all - X_all)**2).mean(dim=1)
threshold = errors[:100].mean() + 3*errors[:100].std()
pred = (errors > threshold).float()
precision = (pred * true_labels).sum() / pred.sum()
recall    = (pred * true_labels).sum() / true_labels.sum()
print(f"Precision: {precision:.3f}, Recall: {recall:.3f}")"""

dl16_ps = """import torch
import torch.nn as nn
import numpy as np

torch.manual_seed(7)
input_dim = 10
# Generate: 80% normal data, 20% anomalies (higher variance)
X_normal = torch.randn(800, input_dim)
X_anomaly = torch.randn(200, input_dim) * 3
labels = torch.cat([torch.zeros(800), torch.ones(200)])
# Shuffle
perm = torch.randperm(1000)
X_all = torch.cat([X_normal, X_anomaly])[perm]
y_all = labels[perm]
X_tr = X_all[:700]  # train on mostly normal (won't know ground truth)
# TODO: Build VAE (encoder->mu/logvar, decoder) with bottleneck=3
# TODO: Train for 20 epochs on X_tr
# TODO: Compute reconstruction error on full dataset
# TODO: Choose threshold as mean + 2*std of training errors
# TODO: Report precision, recall, F1 for anomaly detection
"""

dl16 = make_section4(
    "16", "Generative Models: VAE & GAN",
    "Variational Autoencoders learn a compressed latent distribution and can generate new samples. GANs pit a generator against a discriminator in an adversarial game. Both are used for data augmentation, anomaly detection, and synthetic data generation.",
    "Variational Autoencoder (VAE)", dl16_c1,
    "Generative Adversarial Network (GAN)", dl16_c2,
    "Autoencoder for Anomaly Detection", dl16_c3,
    rw_scenario="Manufacturing quality control: train a VAE on 15 sensor readings from normal production runs, then use reconstruction error to detect faulty batches (anomalies) at inference time.",
    rw_code=dl16_rw_code,
    pt="Anomaly Detection VAE",
    pd="Train a VAE (bottleneck=3) on 700 samples from a 10-feature dataset where 80% are normal and 20% are anomalies (3x variance). Use reconstruction error as anomaly score. Choose threshold = mean + 2*std of training errors. Report precision, recall, and F1.",
    ps=dl16_ps
)

# ═══════════════════════════════════════════════════════════════════
#  STREAMLIT SECTIONS
# ═══════════════════════════════════════════════════════════════════

st14_c1 = """# app.py — run with: streamlit run app.py
import streamlit as st
import pandas as pd
import numpy as np

st.title("Interactive Data Explorer")
st.sidebar.header("Settings")
n_rows = st.sidebar.slider("Number of rows", 50, 1000, 200, step=50)
noise  = st.sidebar.slider("Noise level", 0.0, 5.0, 1.0, step=0.5)
chart  = st.sidebar.selectbox("Chart type", ["Line", "Bar", "Scatter"])

np.random.seed(42)
df = pd.DataFrame({
    "date":  pd.date_range("2024-01-01", periods=n_rows, freq="D"),
    "value": np.cumsum(np.random.normal(0, noise, n_rows)) + 100,
    "category": np.random.choice(["A","B","C"], n_rows),
})

st.write(f"Dataset: {len(df)} rows")
col1, col2 = st.columns(2)
col1.metric("Mean", f"{df['value'].mean():.2f}")
col2.metric("Std",  f"{df['value'].std():.2f}")

if chart == "Line":
    st.line_chart(df.set_index("date")["value"])
elif chart == "Bar":
    st.bar_chart(df.groupby("category")["value"].mean())
else:
    st.scatter_chart(df.rename(columns={"date":"x","value":"y"}), x="x", y="y")

if st.checkbox("Show raw data"):
    st.dataframe(df.head(20), use_container_width=True)"""

st14_c2 = """# Upload and analyze CSV files
import streamlit as st
import pandas as pd
import numpy as np

st.title("CSV Analyzer")
uploaded = st.file_uploader("Upload CSV", type="csv")
if uploaded:
    df = pd.read_csv(uploaded)
    st.success(f"Loaded {df.shape[0]} rows x {df.shape[1]} columns")
    st.dataframe(df.head(10))
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    if numeric_cols:
        col = st.selectbox("Analyze column:", numeric_cols)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Mean",   f"{df[col].mean():.3f}")
        c2.metric("Median", f"{df[col].median():.3f}")
        c3.metric("Std",    f"{df[col].std():.3f}")
        c4.metric("Nulls",  str(df[col].isna().sum()))
        st.subheader(f"Distribution of {col}")
        hist_data = np.histogram(df[col].dropna(), bins=30)
        hist_df = pd.DataFrame({"value": hist_data[1][:-1], "count": hist_data[0]})
        st.bar_chart(hist_df.set_index("value"))
else:
    st.info("Upload a CSV file to get started")
    # Demo data
    demo = pd.DataFrame({"x": np.arange(20), "y": np.random.randn(20)})
    st.line_chart(demo.set_index("x"))"""

st14_c3 = """# Multi-page app with session state
import streamlit as st
import pandas as pd
import numpy as np

if "data" not in st.session_state:
    st.session_state.data = None
if "filters" not in st.session_state:
    st.session_state.filters = {}

page = st.sidebar.radio("Navigate", ["Generate Data", "Filter & Explore", "Summary"])
if page == "Generate Data":
    st.header("Data Generator")
    n = st.number_input("Rows", 100, 10000, 500)
    seed = st.number_input("Random seed", 0, 999, 42)
    if st.button("Generate"):
        np.random.seed(seed)
        st.session_state.data = pd.DataFrame({
            "age":     np.random.randint(18, 80, n),
            "income":  np.random.lognormal(10, 0.5, n),
            "score":   np.random.beta(2, 5, n),
            "segment": np.random.choice(["A","B","C"], n),
        })
        st.success(f"Generated {n} rows!")
elif page == "Filter & Explore":
    if st.session_state.data is None:
        st.warning("Generate data first!")
    else:
        df = st.session_state.data
        min_age, max_age = st.slider("Age range", 18, 80, (25, 65))
        seg = st.multiselect("Segments", ["A","B","C"], default=["A","B","C"])
        filtered = df[(df.age.between(min_age, max_age)) & (df.segment.isin(seg))]
        st.write(f"Filtered: {len(filtered)} rows"); st.dataframe(filtered.head(20))
else:
    if st.session_state.data is not None:
        df = st.session_state.data
        st.header("Summary Statistics"); st.dataframe(df.describe())"""

st14_rw_code = """# Sales Dashboard app
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("Sales Performance Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
months = st.sidebar.multiselect("Month", list(range(1,13)), default=list(range(1,13)))
region = st.sidebar.multiselect("Region", ["North","South","East","West"],
                                default=["North","South","East","West"])
min_rev = st.sidebar.number_input("Min Revenue", 0, 100000, 0, step=1000)

# Simulated sales data
np.random.seed(0)
n = 500
df = pd.DataFrame({
    "month":   np.random.randint(1, 13, n),
    "region":  np.random.choice(["North","South","East","West"], n),
    "product": np.random.choice(["A","B","C"], n),
    "revenue": np.random.lognormal(8, 1, n),
    "units":   np.random.poisson(50, n),
})
filtered = df[(df.month.isin(months)) & (df.region.isin(region)) & (df.revenue >= min_rev)]

# KPI row
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", f"${filtered.revenue.sum():,.0f}")
c2.metric("Avg Revenue",   f"${filtered.revenue.mean():.0f}")
c3.metric("Total Units",   f"{filtered.units.sum():,}")
c4.metric("Orders",        f"{len(filtered):,}")

# Charts
col_a, col_b = st.columns(2)
with col_a:
    st.subheader("Revenue by Region")
    st.bar_chart(filtered.groupby("region")["revenue"].sum())
with col_b:
    st.subheader("Revenue by Product")
    st.bar_chart(filtered.groupby("product")["revenue"].sum())
st.subheader("Data Table")
st.dataframe(filtered.head(50), use_container_width=True)"""

st14_ps = """# Build your own dashboard — run with: streamlit run app.py
import streamlit as st
import pandas as pd
import numpy as np

st.title("Customer Analytics Dashboard")
# TODO: Sidebar with sliders for date range, dropdowns for segment/product
# TODO: Generate or upload simulated customer data (age, LTV, segment, country)
# TODO: Show 4 KPI metrics (total customers, avg LTV, retention rate, churn rate)
# TODO: Two-column layout: bar chart by segment, line chart over time
# TODO: Filterable data table with search
# TODO: Add a session state counter for "number of queries run"
"""

st14 = make_section4(
    "14", "Dashboards & Interactive Widgets",
    "Streamlit makes it easy to build interactive dashboards with sliders, dropdowns, file uploaders, and multi-column layouts. Session state preserves data between user interactions. All Python, no JavaScript needed.",
    "Interactive Data Explorer with Sidebar", st14_c1,
    "CSV Upload & Analysis App", st14_c2,
    "Multi-Page App with Session State", st14_c3,
    rw_scenario="Sales team dashboard: build an interactive Streamlit app with sidebar filters (month, region, min revenue), KPI metrics row, and two-column charts (revenue by region, by product) with a filterable data table.",
    rw_code=st14_rw_code,
    pt="Customer Analytics Dashboard",
    pd="Build a Streamlit dashboard with: sidebar filters (segment, country), 4 KPI metrics (total customers, avg LTV, retention, churn rate), two-column layout (bar chart by segment, line chart over time), filterable data table, and a session state query counter.",
    ps=st14_ps
)

st15_c1 = """# ML prediction app with real-time scoring
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler

# Train model (in real app, load pre-trained model)
@st.cache_resource
def train_model():
    np.random.seed(0)
    X = np.random.randn(2000, 5)
    y = (X[:,0] + X[:,1] > 0).astype(int)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    model = GradientBoostingClassifier(n_estimators=50, random_state=0)
    model.fit(X_scaled, y)
    return model, scaler

model, scaler = train_model()
st.title("Loan Approval Predictor")
st.write("Enter applicant details to get an instant decision")
col1, col2 = st.columns(2)
with col1:
    income  = st.number_input("Annual Income ($)", 20000, 500000, 75000, 5000)
    credit  = st.slider("Credit Score", 300, 850, 680)
    debt    = st.slider("Debt-to-Income Ratio", 0.0, 1.0, 0.3, 0.05)
with col2:
    tenure  = st.number_input("Employment Years", 0, 40, 5)
    loan_amt= st.number_input("Loan Amount ($)", 5000, 1000000, 150000, 5000)
if st.button("Predict", type="primary"):
    X_input = scaler.transform([[income/100000, credit/1000, debt, tenure/40, loan_amt/1000000]])
    prob = model.predict_proba(X_input)[0][1]
    st.metric("Approval Probability", f"{prob:.1%}")
    if prob > 0.6:
        st.success("Decision: APPROVED")
    else:
        st.error("Decision: DECLINED")"""

st15_c2 = """# Batch prediction with file upload + download
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import io

@st.cache_resource
def get_model():
    np.random.seed(0)
    X = np.random.randn(500, 4); y = (X[:,0]>0).astype(int)
    return RandomForestClassifier(n_estimators=50, random_state=0).fit(X, y)

model = get_model()
st.title("Batch ML Predictions")
uploaded = st.file_uploader("Upload data CSV (4 numeric features)", type="csv")
if uploaded:
    df = pd.read_csv(uploaded)
    numeric_df = df.select_dtypes(include=np.number).iloc[:, :4]
    if len(numeric_df.columns) < 4:
        st.error("Need at least 4 numeric columns")
    else:
        df["prediction"] = model.predict(numeric_df.values)
        df["probability"] = model.predict_proba(numeric_df.values)[:, 1]
        col1, col2 = st.columns(2)
        col1.metric("Positive predictions", int(df.prediction.sum()))
        col2.metric("Avg probability", f"{df.probability.mean():.3f}")
        st.dataframe(df.head(20))
        csv_out = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download predictions", csv_out, "predictions.csv", "text/csv")
else:
    st.info("Upload a CSV to get batch predictions")"""

st15_c3 = """# Real-time streaming simulation with st.empty
import streamlit as st
import numpy as np
import time

st.title("Live Data Stream Simulator")
placeholder = st.empty()
chart_placeholder = st.empty()
stop = st.button("Stop Streaming")
n_points = st.sidebar.slider("Points to stream", 20, 200, 50)
speed = st.sidebar.slider("Update speed (ms)", 100, 1000, 300)
data_history = []
if not stop:
    for i in range(n_points):
        new_val = np.sin(i * 0.3) + np.random.normal(0, 0.2)
        data_history.append(new_val)
        with placeholder.container():
            c1, c2, c3 = st.columns(3)
            c1.metric("Current",  f"{new_val:.3f}")
            c2.metric("Mean",     f"{np.mean(data_history):.3f}")
            c3.metric("Std Dev",  f"{np.std(data_history):.3f}")
        import pandas as pd
        chart_placeholder.line_chart(pd.DataFrame({"signal": data_history}))
        time.sleep(speed / 1000)
    st.success(f"Streamed {n_points} data points!")"""

st15_rw_code = """# Churn prediction app with explanations
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler

@st.cache_resource
def build_churn_model():
    np.random.seed(42)
    n = 3000
    X = np.column_stack([
        np.random.randint(1, 120, n),   # tenure_months
        np.random.lognormal(7, 0.5, n), # monthly_spend
        np.random.randint(1, 10, n),    # num_products
        np.random.randint(0, 5, n),     # support_calls
        np.random.randint(0, 2, n),     # is_premium
    ])
    prob = 1/(1+np.exp(-(- X[:,0]/60 + X[:,3]/3 - X[:,4]*0.5)))
    y = np.random.binomial(1, prob)
    sc = StandardScaler(); Xs = sc.fit_transform(X)
    model = GradientBoostingClassifier(n_estimators=100, random_state=0).fit(Xs, y)
    return model, sc

model, scaler = build_churn_model()
feature_names = ["tenure_months","monthly_spend","num_products","support_calls","is_premium"]
st.title("Customer Churn Predictor")
st.sidebar.header("Customer Profile")
tenure  = st.sidebar.slider("Tenure (months)", 1, 120, 24)
spend   = st.sidebar.number_input("Monthly Spend ($)", 10, 2000, 150)
products= st.sidebar.slider("Number of Products", 1, 9, 2)
calls   = st.sidebar.slider("Support Calls (6m)", 0, 10, 1)
premium = st.sidebar.checkbox("Is Premium Customer", value=False)
X_in = scaler.transform([[tenure, spend, products, calls, int(premium)]])
churn_prob = model.predict_proba(X_in)[0][1]
st.metric("Churn Probability", f"{churn_prob:.1%}",
          delta=f"{'HIGH RISK' if churn_prob > 0.5 else 'LOW RISK'}")
st.progress(churn_prob)
# Feature importances
fi = model.feature_importances_
st.subheader("Key Drivers")
fi_df = pd.DataFrame({"Feature":feature_names, "Importance":fi}).sort_values("Importance", ascending=False)
st.bar_chart(fi_df.set_index("Feature"))"""

st15_ps = """# Build an ML demo app — run with: streamlit run app.py
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import io

# TODO: Build and cache a RandomForest model on simulated credit data (5 features)
# TODO: Single prediction form: sliders for each feature, button to predict
# TODO: Show prediction + probability with st.metric and colored st.success/st.error
# TODO: File upload section for batch predictions (predict on all rows)
# TODO: Download button for results CSV
# TODO: Bar chart of feature importances
"""

st15 = make_section4(
    "15", "ML Model Deployment with Streamlit",
    "Deploy ML models as interactive web apps with real-time predictions, batch file upload, and downloadable results. Use @st.cache_resource to load models once. st.empty enables live streaming updates.",
    "Real-Time Loan Approval Predictor", st15_c1,
    "Batch Predictions with CSV Upload & Download", st15_c2,
    "Live Data Streaming with st.empty", st15_c3,
    rw_scenario="Churn prediction tool for customer success team: interactive app with sidebar inputs for customer profile, real-time churn probability with progress bar, and feature importance chart to explain the prediction.",
    rw_code=st15_rw_code,
    pt="Credit Risk ML App",
    pd="Build a Streamlit app with @st.cache_resource model, single prediction form (5 sliders), colored output (success/error), batch CSV upload with predictions download, and feature importance bar chart.",
    ps=st15_ps
)

st16_c1 = """# Plotly + Streamlit: interactive charts
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

st.title("Advanced Visualizations")
np.random.seed(0)
n = 200
df = pd.DataFrame({
    "x":        np.random.randn(n),
    "y":        np.random.randn(n),
    "size":     np.abs(np.random.randn(n)) * 10 + 5,
    "color":    np.random.choice(["A","B","C"], n),
    "revenue":  np.random.lognormal(8, 1, n),
})
tab1, tab2, tab3 = st.tabs(["Scatter", "Histogram", "3D"])
with tab1:
    fig = px.scatter(df, x="x", y="y", color="color", size="size",
                     hover_data=["revenue"], title="Interactive Scatter")
    st.plotly_chart(fig, use_container_width=True)
with tab2:
    col = st.selectbox("Column", ["x","y","revenue"])
    fig2 = px.histogram(df, x=col, color="color", nbins=30, barmode="overlay")
    st.plotly_chart(fig2, use_container_width=True)
with tab3:
    fig3 = px.scatter_3d(df, x="x", y="y", z="revenue", color="color")
    st.plotly_chart(fig3, use_container_width=True)"""

st16_c2 = """# Advanced state & forms
import streamlit as st
import pandas as pd
import numpy as np

st.title("Experiment Tracker")
if "experiments" not in st.session_state:
    st.session_state.experiments = []
if "exp_count" not in st.session_state:
    st.session_state.exp_count = 0

with st.form("new_experiment"):
    st.subheader("Log New Experiment")
    col1, col2 = st.columns(2)
    model_name = col1.selectbox("Model", ["Ridge","RF","GBM","XGBoost"])
    lr = col2.selectbox("Learning Rate", [0.001, 0.01, 0.1, 0.5])
    n_est = st.slider("Estimators", 10, 500, 100, step=10)
    notes = st.text_input("Notes", placeholder="Brief description...")
    submitted = st.form_submit_button("Run Experiment")
    if submitted:
        np.random.seed(st.session_state.exp_count)
        auc = min(0.99, 0.7 + np.random.exponential(0.08) + n_est/5000)
        st.session_state.experiments.append({
            "id": st.session_state.exp_count + 1,
            "model": model_name, "lr": lr,
            "n_est": n_est, "auc": round(auc, 4), "notes": notes
        })
        st.session_state.exp_count += 1
        st.success(f"Experiment logged! AUC={auc:.4f}")

if st.session_state.experiments:
    df = pd.DataFrame(st.session_state.experiments)
    best = df.loc[df.auc.idxmax()]
    st.metric("Best AUC", f"{best.auc:.4f}", f"Model: {best.model}")
    st.dataframe(df.sort_values("auc", ascending=False))"""

st16_c3 = """# Streamlit with database-style caching + alerts
import streamlit as st
import pandas as pd
import numpy as np
import time

@st.cache_data(ttl=60)
def load_data(n_rows):
    np.random.seed(42)
    return pd.DataFrame({
        "timestamp":pd.date_range("2024-01-01", periods=n_rows, freq="h"),
        "cpu_pct":  np.clip(50 + np.cumsum(np.random.normal(0, 2, n_rows)), 5, 99),
        "memory":   np.clip(40 + np.cumsum(np.random.normal(0, 1, n_rows)), 10, 95),
        "requests": np.abs(np.random.poisson(1000, n_rows).astype(float)),
    })

st.title("System Monitoring Dashboard")
n = st.sidebar.slider("Hours of history", 24, 720, 168, step=24)
df = load_data(n)
latest = df.iloc[-1]
c1, c2, c3 = st.columns(3)
delta_cpu = latest.cpu_pct - df.cpu_pct.mean()
c1.metric("CPU%",     f"{latest.cpu_pct:.1f}%",    f"{delta_cpu:+.1f}% vs avg")
c2.metric("Memory%",  f"{latest.memory:.1f}%")
c3.metric("Req/h",    f"{latest.requests:.0f}")
if latest.cpu_pct > 80:
    st.error("HIGH CPU USAGE ALERT!")
elif latest.cpu_pct > 60:
    st.warning("CPU usage elevated")
else:
    st.success("All systems normal")
st.subheader("CPU & Memory over Time")
st.line_chart(df.set_index("timestamp")[["cpu_pct","memory"]])"""

st16_rw_code = """# Full-featured analytics platform
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Analytics Platform", layout="wide", page_icon="analytics")

@st.cache_data
def generate_data(seed=42):
    np.random.seed(seed)
    n = 1000
    return pd.DataFrame({
        "date":     pd.date_range("2023-01-01", periods=n, freq="D"),
        "revenue":  np.cumsum(np.random.normal(1000, 200, n)) + 50000,
        "users":    np.random.poisson(500, n),
        "region":   np.random.choice(["NA","EU","APAC","LATAM"], n),
        "product":  np.random.choice(["Basic","Pro","Enterprise"], n),
        "churn":    np.random.binomial(1, 0.05, n),
    })

df = generate_data()
st.sidebar.header("Filters")
regions = st.sidebar.multiselect("Region", df.region.unique().tolist(), default=df.region.unique().tolist())
products = st.sidebar.multiselect("Product", df.product.unique().tolist(), default=df.product.unique().tolist())
date_range = st.sidebar.date_input("Date range",
    [df.date.min(), df.date.max()], df.date.min(), df.date.max())
fdf = df[(df.region.isin(regions)) & (df.product.isin(products))]
if len(date_range) == 2:
    fdf = fdf[(fdf.date >= pd.Timestamp(date_range[0])) & (fdf.date <= pd.Timestamp(date_range[1]))]
st.title("Business Analytics Platform")
c1,c2,c3,c4 = st.columns(4)
c1.metric("Total Revenue", f"${fdf.revenue.sum():,.0f}")
c2.metric("Total Users",   f"{fdf.users.sum():,}")
c3.metric("Avg Daily Users",f"{fdf.users.mean():.0f}")
c4.metric("Churn Events",  f"{fdf.churn.sum()}")
tab1, tab2 = st.tabs(["Trends", "Breakdown"])
with tab1:
    st.plotly_chart(px.line(fdf, x="date", y="revenue", color="region"), use_container_width=True)
with tab2:
    col_a, col_b = st.columns(2)
    with col_a:
        st.plotly_chart(px.bar(fdf.groupby("product")["revenue"].sum().reset_index(),
                               x="product", y="revenue"), use_container_width=True)
    with col_b:
        st.plotly_chart(px.pie(fdf.groupby("region")["users"].sum().reset_index(),
                               values="users", names="region"), use_container_width=True)"""

st16_ps = """# Advanced Streamlit app — run with: streamlit run app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(layout="wide")
# TODO: @st.cache_data function to generate/load 500-row dataset (product, region, date, revenue, rating)
# TODO: Sidebar: multiselect for region, product; date range slider
# TODO: 4-column KPI row (total revenue, avg rating, orders, top product)
# TODO: 3 tabs: Trends (line chart), Map (bar by region), Ratings (histogram)
# TODO: Download button for filtered data as CSV
# TODO: Experiment logger form using st.form + session state (track 5 experiments max)
"""

st16 = make_section4(
    "16", "Advanced Streamlit: Plotly, Forms & Production Patterns",
    "Combine Plotly charts with Streamlit for pixel-perfect interactive visualizations. Use st.form for atomic multi-input submissions, st.cache_data with TTL for refreshable data sources, and st.tabs for clean multi-view layouts.",
    "Plotly Charts in Tabs", st16_c1,
    "Experiment Tracker with st.form", st16_c2,
    "System Monitoring with st.cache_data + Alerts", st16_c3,
    rw_scenario="Business intelligence platform: multi-filter dashboard with region/product/date filters, 4 KPI metrics, Plotly trend charts in tabs, and a CSV download button — all in under 100 lines.",
    rw_code=st16_rw_code,
    pt="Full Analytics Platform",
    pd="Build a Streamlit app with @st.cache_data data, sidebar multiselect filters (region, product + date range), 4 KPI metrics, 3 tabs with Plotly charts (line, bar, pie), CSV download button, and a session-state experiment logger using st.form (max 5 entries).",
    ps=st16_ps
)

# ─── INSERT ──────────────────────────────────────────────────────────────────

dl_sections = dl14 + dl15 + dl16
st_sections = st14 + st15 + st16

insert_code4(os.path.join(BASE, "gen_deep_learning.py"), dl_sections)
insert_code4(os.path.join(BASE, "gen_streamlit.py"),     st_sections)

print("Done!")
