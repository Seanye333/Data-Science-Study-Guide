"""
Script to add code4_title + code4 to sections missing them in
gen_sklearn.py, gen_polars.py, gen_deep_learning.py, gen_streamlit.py
"""
import re

BASE = r"c:/Users/seany/Documents/All Codes/Data Science Study Path/"

# ─── Content for missing sections ────────────────────────────────────────────

SKLEARN_CODE4 = {
    # key = section title fragment, value = (code4_title, code4 string)
    "Clustering": (
        "AgglomerativeClustering & Silhouette Score Comparison",
        (
            "from sklearn.cluster import AgglomerativeClustering, KMeans\n"
            "from sklearn.metrics import silhouette_score\n"
            "from sklearn.datasets import make_blobs\n"
            "import numpy as np\n\n"
            "X, _ = make_blobs(n_samples=300, centers=4, cluster_std=0.8, random_state=42)\n\n"
            "# Compare silhouette scores for k = 2..6\n"
            "print('KMeans silhouette scores:')\n"
            "for k in range(2, 7):\n"
            "    labels = KMeans(n_clusters=k, random_state=42, n_init=10).fit_predict(X)\n"
            "    score  = silhouette_score(X, labels)\n"
            "    print(f'  k={k}: {score:.4f}')\n\n"
            "# AgglomerativeClustering with different linkages\n"
            "print('\\nAgglomerative linkage comparison (k=4):')\n"
            "for linkage in ['ward', 'complete', 'average', 'single']:\n"
            "    agg    = AgglomerativeClustering(n_clusters=4, linkage=linkage)\n"
            "    labels = agg.fit_predict(X)\n"
            "    score  = silhouette_score(X, labels)\n"
            "    print(f'  {linkage:8s}: {score:.4f}')"
        ),
    ),
    "Model Evaluation": (
        "Learning Curve, Validation Curve & Precision-Recall",
        (
            "from sklearn.model_selection import learning_curve, validation_curve\n"
            "from sklearn.ensemble import RandomForestClassifier\n"
            "from sklearn.datasets import make_classification\n"
            "import numpy as np\n\n"
            "X, y = make_classification(n_samples=1000, n_features=10, random_state=42)\n\n"
            "# Learning curve — how accuracy changes with more training data\n"
            "train_sizes, train_scores, val_scores = learning_curve(\n"
            "    RandomForestClassifier(n_estimators=50, random_state=42),\n"
            "    X, y, cv=5, train_sizes=np.linspace(0.1, 1.0, 8), scoring='accuracy'\n"
            ")\n"
            "print('Learning curve (train size → val accuracy):')\n"
            "for sz, vs in zip(train_sizes, val_scores.mean(axis=1)):\n"
            "    print(f'  n={int(sz):4d}: {vs:.4f}')\n\n"
            "# Validation curve — how accuracy changes with a hyperparameter\n"
            "param_range = [10, 50, 100, 200, 300]\n"
            "train_s, val_s = validation_curve(\n"
            "    RandomForestClassifier(random_state=42),\n"
            "    X, y, param_name='n_estimators', param_range=param_range,\n"
            "    cv=5, scoring='accuracy'\n"
            ")\n"
            "print('\\nValidation curve (n_estimators → val accuracy):')\n"
            "for n, vs in zip(param_range, val_s.mean(axis=1)):\n"
            "    print(f'  n={n:3d}: {vs:.4f}')"
        ),
    ),
    "Pipelines": (
        "Pipeline with SelectKBest & FunctionTransformer",
        (
            "from sklearn.pipeline import Pipeline\n"
            "from sklearn.feature_selection import SelectKBest, f_classif\n"
            "from sklearn.preprocessing import FunctionTransformer, StandardScaler\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.model_selection import cross_val_score\n"
            "import numpy as np\n\n"
            "X, y = make_classification(n_samples=500, n_features=20,\n"
            "                           n_informative=8, random_state=42)\n\n"
            "# Custom log1p transform as a FunctionTransformer\n"
            "log_transform = FunctionTransformer(np.log1p, validate=True)\n\n"
            "pipe = Pipeline([\n"
            "    ('log',    FunctionTransformer(np.abs)),   # make all positive first\n"
            "    ('scaler', StandardScaler()),\n"
            "    ('select', SelectKBest(f_classif, k=8)),   # keep top 8 features\n"
            "    ('clf',    LogisticRegression(max_iter=500))\n"
            "])\n\n"
            "scores = cross_val_score(pipe, X, y, cv=5, scoring='accuracy')\n"
            "print('Pipeline with SelectKBest(k=8):')\n"
            "print(f'  CV accuracy: {scores.mean():.4f} ± {scores.std():.4f}')\n\n"
            "# Compare: all 20 features vs top 8\n"
            "pipe_all = Pipeline([('scaler', StandardScaler()), ('clf', LogisticRegression(max_iter=500))])\n"
            "scores_all = cross_val_score(pipe_all, X, y, cv=5)\n"
            "print(f'  All 20 features: {scores_all.mean():.4f} ± {scores_all.std():.4f}')"
        ),
    ),
    "Hyperparameter": (
        "cross_validate with Multiple Scoring Metrics",
        (
            "from sklearn.model_selection import cross_validate\n"
            "from sklearn.ensemble import GradientBoostingClassifier\n"
            "from sklearn.datasets import make_classification\n"
            "import numpy as np\n\n"
            "X, y = make_classification(n_samples=800, n_features=10,\n"
            "                           weights=[0.7, 0.3], random_state=42)\n\n"
            "# Evaluate with multiple metrics at once\n"
            "scoring = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']\n"
            "results = cross_validate(\n"
            "    GradientBoostingClassifier(n_estimators=100, random_state=42),\n"
            "    X, y, cv=5, scoring=scoring, return_train_score=True\n"
            ")\n\n"
            "print('5-fold CV results (mean ± std):')\n"
            "for metric in scoring:\n"
            "    test_mean  = results[f'test_{metric}'].mean()\n"
            "    test_std   = results[f'test_{metric}'].std()\n"
            "    train_mean = results[f'train_{metric}'].mean()\n"
            "    gap = train_mean - test_mean\n"
            "    print(f'  {metric:12s}: {test_mean:.4f} ± {test_std:.4f}  (train={train_mean:.4f}, gap={gap:.4f})')\n"
            "print(f'\\nFit time: {results[\"fit_time\"].mean():.3f}s avg')"
        ),
    ),
    "Dimensionality": (
        "NMF & Isomap for Non-Linear Reduction",
        (
            "from sklearn.decomposition import NMF\n"
            "from sklearn.manifold import Isomap\n"
            "from sklearn.preprocessing import MinMaxScaler\n"
            "from sklearn.datasets import load_digits\n"
            "import numpy as np\n\n"
            "digits = load_digits()\n"
            "X      = MinMaxScaler().fit_transform(digits.data)  # NMF needs non-negative\n"
            "y      = digits.target\n\n"
            "# NMF: learns parts-based representation\n"
            "nmf = NMF(n_components=20, max_iter=500, random_state=42)\n"
            "X_nmf = nmf.fit_transform(X)\n"
            "print(f'NMF: {X.shape} → {X_nmf.shape}')\n"
            "print(f'Reconstruction error: {nmf.reconstruction_err_:.4f}')\n\n"
            "# Isomap: non-linear manifold learning (preserves geodesic distances)\n"
            "iso = Isomap(n_components=2, n_neighbors=10)\n"
            "X_iso = iso.fit_transform(X)\n"
            "print(f'\\nIsomap: {X.shape} → {X_iso.shape}')\n\n"
            "# Check cluster quality: std of 2D coordinates per digit class\n"
            "print('Per-digit cluster spread (lower = tighter cluster):')\n"
            "for cls in range(10):\n"
            "    spread = X_iso[y == cls].std()\n"
            "    print(f'  Digit {cls}: {spread:.3f}')"
        ),
    ),
}

POLARS_CODE4 = {
    "String & Date": (
        "str.extract with Regex, str.split_exact & dt.truncate",
        (
            "import polars as pl\n"
            "from datetime import date\n\n"
            "# String regex extraction\n"
            "df = pl.DataFrame({'log': [\n"
            "    '2024-01-15 ERROR db_pool Connection timeout after 30s',\n"
            "    '2024-01-16 INFO  auth_svc User alice logged in',\n"
            "    '2024-01-17 WARN  api_gw  Rate limit at 95%',\n"
            "]})\n\n"
            "result = df.with_columns([\n"
            "    pl.col('log').str.extract(r'(\\d{4}-\\d{2}-\\d{2})', 1).alias('date'),\n"
            "    pl.col('log').str.extract(r'\\d{4}-\\d{2}-\\d{2} (\\w+)', 1).alias('level'),\n"
            "    pl.col('log').str.extract(r'\\w+ \\w+\\s+(\\w+)\\s', 1).alias('service'),\n"
            "])\n"
            "print('Regex extraction:')\n"
            "print(result)\n\n"
            "# str.split_exact — fixed number of parts\n"
            "df2 = pl.DataFrame({'ts': ['2024-01-15', '2024-06-30', '2024-12-01']})\n"
            "split = df2.with_columns(\n"
            "    pl.col('ts').str.split_exact('-', 2).alias('parts')\n"
            ").unnest('parts').rename({'field_0':'year','field_1':'month','field_2':'day'})\n"
            "print('\\nSplit date parts:')\n"
            "print(split)\n\n"
            "# dt.truncate — round dates to month/week\n"
            "df3 = pl.DataFrame({'dt': pl.date_range(\n"
            "    pl.date(2024, 1, 1), pl.date(2024, 3, 31), interval='11d', eager=True\n"
            ")})\n"
            "df3 = df3.with_columns([\n"
            "    pl.col('dt').dt.truncate('1mo').alias('month_start'),\n"
            "    pl.col('dt').dt.truncate('1w').alias('week_start'),\n"
            "])\n"
            "print('\\nDate truncation:')\n"
            "print(df3.head(6))"
        ),
    ),
    "Lazy API": (
        "Streaming Mode & LazyFrame Schema Inspection",
        (
            "import polars as pl\n"
            "import numpy as np\n"
            "import tempfile, os\n\n"
            "np.random.seed(42)\n"
            "n = 500_000\n"
            "df = pl.DataFrame({\n"
            "    'id':       range(n),\n"
            "    'amount':   np.random.exponential(100, n).round(2),\n"
            "    'category': np.random.choice(['A','B','C','D'], n),\n"
            "    'flag':     np.random.choice([True, False], n),\n"
            "})\n"
            "pq_path = os.path.join(tempfile.gettempdir(), 'streaming_demo.parquet')\n"
            "df.write_parquet(pq_path)\n\n"
            "# LazyFrame schema inspection — no data loaded yet\n"
            "lf = pl.scan_parquet(pq_path)\n"
            "print('Schema (no data loaded):')\n"
            "print(lf.schema)\n"
            "print('Columns:', lf.columns)\n\n"
            "# Build a lazy query\n"
            "query = (\n"
            "    lf.filter(pl.col('flag') & (pl.col('amount') > 50))\n"
            "      .group_by('category')\n"
            "      .agg([\n"
            "          pl.col('amount').mean().round(2).alias('avg'),\n"
            "          pl.len().alias('count')\n"
            "      ])\n"
            "      .sort('avg', descending=True)\n"
            ")\n\n"
            "# Show the optimized query plan\n"
            "print('\\nOptimized plan:')\n"
            "query.explain(optimized=True)\n\n"
            "# Execute\n"
            "result = query.collect()\n"
            "print('\\nResult:')\n"
            "print(result)"
        ),
    ),
    "Reading & Writing": (
        "scan_csv with Schema Override & In-Memory Parquet",
        (
            "import polars as pl\n"
            "import io\n\n"
            "# scan_csv with explicit schema override\n"
            "csv_data = 'id,score,grade,active\\n1,92.5,A,true\\n2,78.0,B,false\\n3,85.5,A,true\\n'\n"
            "schema_override = {\n"
            "    'id':     pl.Int32,\n"
            "    'score':  pl.Float32,\n"
            "    'grade':  pl.Categorical,\n"
            "    'active': pl.Boolean,\n"
            "}\n"
            "df = pl.read_csv(io.StringIO(csv_data), schema_overrides=schema_override)\n"
            "print('With schema override:')\n"
            "print(df)\n"
            "print('Dtypes:', df.dtypes)\n\n"
            "# In-memory Parquet (BytesIO — no file system needed)\n"
            "import numpy as np\n"
            "np.random.seed(0)\n"
            "df2 = pl.DataFrame({\n"
            "    'x': np.random.randn(1000).astype('float32'),\n"
            "    'y': np.random.randint(0, 10, 1000),\n"
            "})\n"
            "buf = io.BytesIO()\n"
            "df2.write_parquet(buf, compression='zstd')\n"
            "buf.seek(0)\n"
            "size_kb = buf.getbuffer().nbytes / 1024\n"
            "df3 = pl.read_parquet(buf)\n"
            "print(f'\\nIn-memory Parquet: {df2.shape} → {size_kb:.1f} KB')\n"
            "print('Read back:', df3.shape)"
        ),
    ),
    "Window": (
        "ewm_mean (Exponential Weighted), rolling_quantile & map_elements",
        (
            "import polars as pl\n"
            "import numpy as np\n\n"
            "np.random.seed(42)\n"
            "df = pl.DataFrame({\n"
            "    'day':   range(1, 31),\n"
            "    'price': np.random.uniform(95, 105, 30).round(2),\n"
            "    'vol':   np.random.randint(1000, 5000, 30),\n"
            "})\n\n"
            "result = df.with_columns([\n"
            "    # Exponential weighted mean (recent values get more weight)\n"
            "    pl.col('price').ewm_mean(span=5).round(3).alias('ewm_5'),\n"
            "    # Rolling 7-day median (robust to outliers)\n"
            "    pl.col('price').rolling_median(window_size=7).round(3).alias('rolling_med_7'),\n"
            "    # Rolling 75th percentile\n"
            "    pl.col('vol').rolling_quantile(quantile=0.75, window_size=7).alias('vol_q75'),\n"
            "])\n"
            "print(result.head(10))\n\n"
            "# map_elements for custom per-element logic\n"
            "df2 = pl.DataFrame({'scores': [[85, 90, 78], [60, 70], [95, 88, 92, 80]]})\n"
            "result2 = df2.with_columns(\n"
            "    pl.col('scores').map_elements(\n"
            "        lambda lst: round(sum(lst) / len(lst), 2),\n"
            "        return_dtype=pl.Float64\n"
            "    ).alias('avg_score')\n"
            ")\n"
            "print('\\nCustom avg via map_elements:')\n"
            "print(result2)"
        ),
    ),
    "Polars vs Pandas": (
        "Arrow Zero-Copy Interchange & Categorical dtype",
        (
            "import polars as pl\n"
            "import pandas as pd\n"
            "import numpy as np\n\n"
            "# Categorical dtype in Polars (much more efficient than object)\n"
            "np.random.seed(42)\n"
            "n = 100_000\n"
            "df_pl = pl.DataFrame({\n"
            "    'product':  pl.Series(np.random.choice(['Widget','Gadget','Doohickey'], n)).cast(pl.Categorical),\n"
            "    'region':   pl.Series(np.random.choice(['North','South','East','West'], n)).cast(pl.Categorical),\n"
            "    'revenue':  np.random.exponential(200, n).round(2),\n"
            "})\n"
            "print('Categorical memory usage:')\n"
            "print(f'  estimated size: {df_pl.estimated_size(\"mb\"):.2f} MB')\n"
            "print(f'  product unique values: {df_pl[\"product\"].n_unique()}')\n\n"
            "# Zero-copy to pandas via Arrow\n"
            "df_pd = df_pl.to_pandas(use_pyarrow_extension_array=True)\n"
            "print('\\nArrow-backed pandas dtypes:')\n"
            "print(df_pd.dtypes)\n\n"
            "# from_pandas preserving categorical\n"
            "df_pd2 = pd.DataFrame({\n"
            "    'color': pd.Categorical(['red','blue','red','green','blue']),\n"
            "    'val':   [1, 2, 3, 4, 5]\n"
            "})\n"
            "df_pl2 = pl.from_pandas(df_pd2)\n"
            "print('\\nFrom pandas Categorical:')\n"
            "print(df_pl2)\n"
            "print('dtype:', df_pl2['color'].dtype)"
        ),
    ),
}

DEEP_CODE4 = {
    "Custom Datasets": (
        "Weighted Random Sampler for Imbalanced Data",
        (
            "import torch\n"
            "from torch.utils.data import Dataset, DataLoader, WeightedRandomSampler\n"
            "import numpy as np\n\n"
            "# Simulate imbalanced dataset: 90% class 0, 10% class 1\n"
            "np.random.seed(42)\n"
            "n = 1000\n"
            "X = torch.randn(n, 8)\n"
            "y = torch.tensor(np.random.choice([0, 1], n, p=[0.9, 0.1]), dtype=torch.long)\n"
            "print(f'Class distribution: 0={( y==0).sum()}, 1={(y==1).sum()}')\n\n"
            "class TabularDataset(Dataset):\n"
            "    def __init__(self, X, y): self.X, self.y = X, y\n"
            "    def __len__(self): return len(self.y)\n"
            "    def __getitem__(self, i): return self.X[i], self.y[i]\n\n"
            "dataset = TabularDataset(X, y)\n\n"
            "# WeightedRandomSampler: oversample minority class\n"
            "class_counts   = torch.bincount(y)\n"
            "class_weights  = 1.0 / class_counts.float()\n"
            "sample_weights = class_weights[y]\n"
            "sampler = WeightedRandomSampler(sample_weights, num_samples=500, replacement=True)\n\n"
            "loader = DataLoader(dataset, batch_size=32, sampler=sampler)\n"
            "# Verify balance in sampled batches\n"
            "all_labels = []\n"
            "for _, labels in loader:\n"
            "    all_labels.extend(labels.tolist())\n"
            "sampled_0 = all_labels.count(0)\n"
            "sampled_1 = all_labels.count(1)\n"
            "print(f'Sampled class distribution: 0={sampled_0}, 1={sampled_1}')\n"
            "print(f'Balance ratio: {sampled_1/max(sampled_0,1):.2f}')"
        ),
    ),
    "Regularization": (
        "Focal Loss, Label Smoothing & Weighted Cross-Entropy",
        (
            "import torch\n"
            "import torch.nn as nn\n"
            "import torch.nn.functional as F\n\n"
            "# Focal Loss — down-weights easy examples, focuses on hard ones\n"
            "class FocalLoss(nn.Module):\n"
            "    def __init__(self, alpha=1.0, gamma=2.0):\n"
            "        super().__init__()\n"
            "        self.alpha, self.gamma = alpha, gamma\n\n"
            "    def forward(self, logits, targets):\n"
            "        ce   = F.cross_entropy(logits, targets, reduction='none')\n"
            "        pt   = torch.exp(-ce)\n"
            "        loss = self.alpha * (1 - pt) ** self.gamma * ce\n"
            "        return loss.mean()\n\n"
            "# Label smoothing — prevents overconfident predictions\n"
            "class LabelSmoothingLoss(nn.Module):\n"
            "    def __init__(self, num_classes, smoothing=0.1):\n"
            "        super().__init__()\n"
            "        self.smoothing = smoothing\n"
            "        self.cls = num_classes\n\n"
            "    def forward(self, logits, targets):\n"
            "        log_probs = F.log_softmax(logits, dim=-1)\n"
            "        smooth    = self.smoothing / (self.cls - 1)\n"
            "        one_hot   = torch.full_like(log_probs, smooth)\n"
            "        one_hot.scatter_(1, targets.unsqueeze(1), 1 - self.smoothing)\n"
            "        return -(one_hot * log_probs).sum(dim=-1).mean()\n\n"
            "# Compare losses on synthetic predictions\n"
            "torch.manual_seed(42)\n"
            "logits  = torch.randn(8, 3)   # 8 samples, 3 classes\n"
            "targets = torch.randint(0, 3, (8,))\n\n"
            "ce_loss = nn.CrossEntropyLoss()(logits, targets)\n"
            "fl_loss = FocalLoss(gamma=2.0)(logits, targets)\n"
            "ls_loss = LabelSmoothingLoss(3, 0.1)(logits, targets)\n"
            "print(f'CrossEntropy:    {ce_loss.item():.4f}')\n"
            "print(f'FocalLoss:       {fl_loss.item():.4f}')\n"
            "print(f'LabelSmoothing:  {ls_loss.item():.4f}')\n\n"
            "# Weighted CrossEntropy for class imbalance\n"
            "weights = torch.tensor([1.0, 5.0, 3.0])  # class 1 is rare, upweighted\n"
            "wce = nn.CrossEntropyLoss(weight=weights)(logits, targets)\n"
            "print(f'WeightedCE:      {wce.item():.4f}')"
        ),
    ),
    "Saving": (
        "Model Versioning with State Dict & ONNX-like Summary",
        (
            "import torch\n"
            "import torch.nn as nn\n"
            "import io\n\n"
            "class MLP(nn.Module):\n"
            "    def __init__(self, in_f, hidden, out_f):\n"
            "        super().__init__()\n"
            "        self.net = nn.Sequential(\n"
            "            nn.Linear(in_f, hidden), nn.ReLU(),\n"
            "            nn.Linear(hidden, out_f)\n"
            "        )\n"
            "    def forward(self, x): return self.net(x)\n\n"
            "model = MLP(16, 64, 4)\n\n"
            "# Save/load state dict to buffer (no file system needed)\n"
            "buf = io.BytesIO()\n"
            "torch.save(model.state_dict(), buf)\n"
            "buf.seek(0)\n"
            "size_kb = buf.getbuffer().nbytes / 1024\n"
            "print(f'State dict size: {size_kb:.2f} KB')\n\n"
            "# Load into new model\n"
            "model2 = MLP(16, 64, 4)\n"
            "model2.load_state_dict(torch.load(buf, weights_only=True))\n"
            "model2.eval()\n\n"
            "# Verify identical outputs\n"
            "torch.manual_seed(0)\n"
            "x = torch.randn(4, 16)\n"
            "with torch.no_grad():\n"
            "    out1 = model(x)\n"
            "    out2 = model2(x)\n"
            "print(f'Outputs identical: {torch.allclose(out1, out2)}')\n\n"
            "# Parameter count per layer\n"
            "print('\\nModel parameter summary:')\n"
            "total = 0\n"
            "for name, p in model.named_parameters():\n"
            "    n = p.numel()\n"
            "    total += n\n"
            "    print(f'  {name:25s}: {list(p.shape)} = {n:,} params')\n"
            "print(f'  Total: {total:,} parameters')"
        ),
    ),
    "RNNs": (
        "Bidirectional LSTM & Packed Sequences",
        (
            "import torch\n"
            "import torch.nn as nn\n"
            "from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence, pad_sequence\n\n"
            "torch.manual_seed(42)\n\n"
            "# Bidirectional LSTM\n"
            "bi_lstm = nn.LSTM(input_size=16, hidden_size=32, num_layers=2,\n"
            "                  batch_first=True, bidirectional=True, dropout=0.2)\n\n"
            "x = torch.randn(8, 20, 16)  # batch=8, seq_len=20, features=16\n"
            "out, (h_n, c_n) = bi_lstm(x)\n"
            "print('Bidirectional LSTM:')\n"
            "print(f'  Input:  {list(x.shape)}')\n"
            "print(f'  Output: {list(out.shape)}  (hidden*2={32*2} for bidirectional)')\n"
            "print(f'  h_n:    {list(h_n.shape)}  (layers*2, batch, hidden)')\n\n"
            "# Packed sequences — handle variable-length inputs efficiently\n"
            "sequences = [torch.randn(length, 8) for length in [10, 7, 5, 3]]\n"
            "lengths   = torch.tensor([10, 7, 5, 3])\n"
            "padded    = pad_sequence(sequences, batch_first=True)  # (4, 10, 8)\n\n"
            "lstm = nn.LSTM(input_size=8, hidden_size=16, batch_first=True)\n"
            "packed = pack_padded_sequence(padded, lengths, batch_first=True, enforce_sorted=True)\n"
            "out_packed, _ = lstm(packed)\n"
            "out_padded, out_lengths = pad_packed_sequence(out_packed, batch_first=True)\n\n"
            "print('\\nPacked sequences:')\n"
            "print(f'  Padded input:  {list(padded.shape)}')\n"
            "print(f'  Output:        {list(out_padded.shape)}')\n"
            "print(f'  Out lengths:   {out_lengths.tolist()}')"
        ),
    ),
}

STREAMLIT_CODE4 = {
    "Charts": (
        "st.pyplot, st.plotly_chart & st.altair_chart",
        (
            "# Run: streamlit run app.py\n"
            "import streamlit as st\n"
            "import matplotlib\n"
            "matplotlib.use('Agg')\n"
            "import matplotlib.pyplot as plt\n"
            "import plotly.express as px\n"
            "import altair as alt\n"
            "import pandas as pd\n"
            "import numpy as np\n\n"
            "st.title('Multi-Library Charts')\n\n"
            "np.random.seed(42)\n"
            "df = pd.DataFrame({'x': range(20), 'y': np.random.randn(20).cumsum(),\n"
            "                   'group': np.random.choice(['A','B'], 20)})\n\n"
            "# 1. Matplotlib via st.pyplot\n"
            "st.subheader('Matplotlib')\n"
            "fig, ax = plt.subplots(figsize=(7, 3))\n"
            "ax.plot(df['x'], df['y'], color='steelblue', linewidth=2)\n"
            "ax.set_title('Cumulative Random Walk')\n"
            "st.pyplot(fig)\n"
            "plt.close()\n\n"
            "# 2. Plotly via st.plotly_chart\n"
            "st.subheader('Plotly (Interactive)')\n"
            "fig2 = px.scatter(df, x='x', y='y', color='group', title='Scatter by Group')\n"
            "st.plotly_chart(fig2, use_container_width=True)\n\n"
            "# 3. Altair via st.altair_chart\n"
            "st.subheader('Altair (Declarative)')\n"
            "chart = alt.Chart(df).mark_line(point=True).encode(\n"
            "    x='x:Q', y='y:Q', color='group:N'\n"
            ").properties(title='Altair Line Chart', width=600)\n"
            "st.altair_chart(chart, use_container_width=True)"
        ),
    ),
    "Layout": (
        "st.container, st.empty for Dynamic Updates & st.status",
        (
            "# Run: streamlit run app.py\n"
            "import streamlit as st\n"
            "import time\n\n"
            "st.title('Dynamic Layout Demo')\n\n"
            "# st.container — group elements logically\n"
            "with st.container(border=True):\n"
            "    st.subheader('Metrics Panel')\n"
            "    c1, c2, c3 = st.columns(3)\n"
            "    c1.metric('Revenue', '$42,000', '+8%')\n"
            "    c2.metric('Users',    '1,234',   '+12%')\n"
            "    c3.metric('Errors',   '3',        '-2')\n\n"
            "# st.empty — placeholder that can be updated\n"
            "st.subheader('Countdown')\n"
            "placeholder = st.empty()\n"
            "if st.button('Start Countdown'):\n"
            "    for i in range(5, 0, -1):\n"
            "        placeholder.markdown(f'## ⏱ {i}...')\n"
            "        time.sleep(1)\n"
            "    placeholder.success('Done! 🎉')\n\n"
            "# st.status — progress display for long operations\n"
            "if st.button('Run Long Process'):\n"
            "    with st.status('Processing...', expanded=True) as status:\n"
            "        st.write('Step 1: Loading data...')\n"
            "        time.sleep(0.5)\n"
            "        st.write('Step 2: Running model...')\n"
            "        time.sleep(0.5)\n"
            "        st.write('Step 3: Generating report...')\n"
            "        time.sleep(0.3)\n"
            "        status.update(label='Complete!', state='complete')"
        ),
    ),
    "Sidebar": (
        "st.session_state with on_change Callbacks & st.rerun",
        (
            "# Run: streamlit run app.py\n"
            "import streamlit as st\n\n"
            "st.title('Session State with Callbacks')\n\n"
            "# Initialize state\n"
            "if 'theme' not in st.session_state:\n"
            "    st.session_state.theme = 'Light'\n"
            "if 'font_size' not in st.session_state:\n"
            "    st.session_state.font_size = 14\n"
            "if 'history' not in st.session_state:\n"
            "    st.session_state.history = []\n\n"
            "# Callback function — runs BEFORE the widget returns\n"
            "def on_theme_change():\n"
            "    st.session_state.history.append(\n"
            "        f'Theme changed to: {st.session_state.theme_select}'\n"
            "    )\n"
            "    st.session_state.theme = st.session_state.theme_select\n\n"
            "st.selectbox(\n"
            "    'Theme', ['Light', 'Dark', 'High Contrast'],\n"
            "    key='theme_select',\n"
            "    on_change=on_theme_change\n"
            ")\n"
            "st.slider('Font size', 10, 24, key='font_size')\n\n"
            "st.write(f'Active theme: **{st.session_state.theme}**')\n"
            "st.write(f'Font size: **{st.session_state.font_size}px**')\n\n"
            "if st.session_state.history:\n"
            "    st.subheader('Change History')\n"
            "    for item in st.session_state.history[-5:]:\n"
            "        st.write(f'• {item}')\n\n"
            "if st.button('Reset All'):\n"
            "    for key in ['theme', 'font_size', 'history', 'theme_select']:\n"
            "        st.session_state.pop(key, None)\n"
            "    st.rerun()  # immediately refresh the page"
        ),
    ),
    "File Upload": (
        "st.camera_input & st.download_button with CSV",
        (
            "# Run: streamlit run app.py\n"
            "import streamlit as st\n"
            "import pandas as pd\n"
            "import numpy as np\n"
            "import io\n\n"
            "st.title('File Operations')\n\n"
            "# Generate sample data for download\n"
            "np.random.seed(42)\n"
            "df = pd.DataFrame({\n"
            "    'id':      range(1, 21),\n"
            "    'name':    [f'Product_{i}' for i in range(1, 21)],\n"
            "    'price':   np.random.uniform(9.99, 99.99, 20).round(2),\n"
            "    'stock':   np.random.randint(0, 500, 20),\n"
            "})\n\n"
            "st.subheader('Download Sample Data')\n"
            "st.dataframe(df.head())\n\n"
            "# st.download_button — download as CSV\n"
            "csv_bytes = df.to_csv(index=False).encode('utf-8')\n"
            "st.download_button(\n"
            "    label='📥 Download as CSV',\n"
            "    data=csv_bytes,\n"
            "    file_name='products.csv',\n"
            "    mime='text/csv',\n"
            "    help='Download the full product list'\n"
            ")\n\n"
            "# Download as Excel (requires openpyxl)\n"
            "try:\n"
            "    excel_buf = io.BytesIO()\n"
            "    df.to_excel(excel_buf, index=False, engine='openpyxl')\n"
            "    st.download_button(\n"
            "        '📥 Download as Excel',\n"
            "        data=excel_buf.getvalue(),\n"
            "        file_name='products.xlsx',\n"
            "        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'\n"
            "    )\n"
            "except ImportError:\n"
            "    st.info('Install openpyxl for Excel download')\n\n"
            "# st.camera_input — capture photo from webcam\n"
            "st.subheader('Camera Input')\n"
            "photo = st.camera_input('Take a photo')\n"
            "if photo:\n"
            "    st.image(photo, caption='Captured photo', use_container_width=True)\n"
            "    st.write(f'File size: {len(photo.getvalue()) / 1024:.1f} KB')"
        ),
    ),
    "Forms": (
        "@st.cache_resource for Models & Connections",
        (
            "# Run: streamlit run app.py\n"
            "import streamlit as st\n"
            "import time\n\n"
            "# @st.cache_resource — for expensive global resources (models, DB connections)\n"
            "# Unlike @st.cache_data, resource is shared across all users/sessions\n\n"
            "@st.cache_resource\n"
            "def load_model(model_name: str):\n"
            "    \"\"\"Loads a model once per app lifetime — not per user session.\"\"\"\n"
            "    st.write(f'Loading {model_name}...')  # only shows on first load\n"
            "    time.sleep(2)  # simulate slow model load\n"
            "    return {'name': model_name, 'weights': list(range(100)), 'loaded_at': time.time()}\n\n"
            "@st.cache_data(ttl=60)  # expires every 60 seconds\n"
            "def fetch_live_data(endpoint: str):\n"
            "    \"\"\"Re-fetches data every 60s automatically.\"\"\"\n"
            "    time.sleep(0.5)  # simulate API call\n"
            "    import numpy as np\n"
            "    np.random.seed(int(time.time()) % 100)\n"
            "    return {'endpoint': endpoint, 'value': round(np.random.uniform(95, 105), 2)}\n\n"
            "st.title('Resource & Data Caching')\n\n"
            "model_name = st.selectbox('Select model', ['bert-base', 'gpt2', 'roberta'])\n"
            "model = load_model(model_name)\n"
            "st.success(f'Model \"{model[\"name\"]}\" ready (loaded at {model[\"loaded_at\"]:.0f})')\n\n"
            "st.subheader('Live Data (refreshes every 60s)')\n"
            "data = fetch_live_data('/api/sensor/temperature')\n"
            "st.metric('Temperature', f\"{data['value']}°C\")\n"
            "if st.button('Force refresh'):\n"
            "    st.cache_data.clear()\n"
            "    st.rerun()"
        ),
    ),
    "Multi-Page": (
        "st.navigation with st.Page & Page-Specific State",
        (
            "# Structure: create these files:\n"
            "# app.py (entry point), pages/home.py, pages/data.py, pages/settings.py\n\n"
            "# --- app.py ---\n"
            "import streamlit as st\n\n"
            "# New navigation API (Streamlit >= 1.36)\n"
            "home     = st.Page('pages/home.py',     title='Home',     icon='🏠', default=True)\n"
            "data     = st.Page('pages/data.py',     title='Data',     icon='📊')\n"
            "settings = st.Page('pages/settings.py', title='Settings', icon='⚙️')\n\n"
            "pg = st.navigation({'Main': [home, data], 'Config': [settings]})\n"
            "pg.run()\n\n"
            "# --- pages/home.py ---\n"
            "# import streamlit as st\n"
            "# st.title('Home 🏠')\n"
            "# st.write('Welcome! Use the sidebar to navigate.')\n"
            "# if 'visit_count' not in st.session_state:\n"
            "#     st.session_state.visit_count = 0\n"
            "# st.session_state.visit_count += 1\n"
            "# st.metric('Page visits this session', st.session_state.visit_count)\n\n"
            "# --- pages/data.py ---\n"
            "# import streamlit as st, pandas as pd, numpy as np\n"
            "# st.title('Data 📊')\n"
            "# @st.cache_data\n"
            "# def load(): return pd.DataFrame({'x': range(10), 'y': np.random.randn(10)})\n"
            "# st.dataframe(load())\n\n"
            "# --- pages/settings.py ---\n"
            "# import streamlit as st\n"
            "# st.title('Settings ⚙️')\n"
            "# theme = st.radio('Theme', ['Light', 'Dark'])\n"
            "# st.session_state['theme'] = theme\n"
            "# if st.button('Switch to Data page'):\n"
            "#     st.switch_page('pages/data.py')"
        ),
    ),
}


def add_code4_to_file(filepath, section_matches):
    """Add code4_title and code4 to sections by finding rw_scenario markers."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    for title_fragment, (code4_title, code4_str) in section_matches.items():
        # Find the section by its rw_scenario (unique per section)
        # Strategy: find the section that has title_fragment, then find its closing },
        # and insert code4 before it

        # Look for: "rw_scenario": "..." then the section's closing },
        # We find the rw_code block end and insert code4 after it

        # Find all occurrences of title_fragment in section titles
        pattern = rf'"title":\s*"[^"]*{re.escape(title_fragment)}[^"]*"'
        matches = list(re.finditer(pattern, content))
        if not matches:
            print(f"  WARNING: Could not find section with title fragment: {title_fragment}")
            continue

        # Take the first match that is a top-level section (not inside rw or practice)
        for m in matches:
            # Check that this title is NOT nested inside rw_scenario or practice
            # (nested titles would be inside string values, preceded by quotes on that same line)
            line_start = content.rfind('\n', 0, m.start()) + 1
            line_text = content[line_start:m.start()]
            # If there's a quote before "title" on the same line, it's a value inside a string
            if '"' in line_text.strip() or "'" in line_text.strip():
                continue  # skip if nested inside a string value

            # Found the right section. Now find where to insert code4.
            # Insert before "rw_scenario": key
            rw_pos = content.find('"rw_scenario":', m.end())
            if rw_pos == -1:
                print(f"  WARNING: Could not find rw_scenario for: {title_fragment}")
                break

            # Check if code4 already exists between title and rw_scenario
            section_chunk = content[m.start():rw_pos]
            if '"code4_title"' in section_chunk:
                print(f"  SKIP: {title_fragment} already has code4")
                break

            # Format the insertion
            # Build the code4 string in the file's format (parenthesized string concat)
            lines = code4_str.split('\n')
            formatted_lines = []
            for j, line in enumerate(lines):
                escaped = line.replace('\\', '\\\\').replace('"', '\\"')
                if j < len(lines) - 1:
                    formatted_lines.append(f'            "{escaped}\\n"')
                else:
                    if escaped:
                        formatted_lines.append(f'            "{escaped}"')
            code4_formatted = '\n'.join(formatted_lines)

            insertion = (
                f'        "code4_title": "{code4_title}",\n'
                f'        "code4": (\n'
                f'{code4_formatted}\n'
                f'        ),\n'
                f'        '
            )

            # Insert before rw_scenario
            content = content[:rw_pos] + insertion + content[rw_pos:]
            print(f"  Added code4 to: {title_fragment}")
            break

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


# ─── Apply to each file ───────────────────────────────────────────────────────

print("=== gen_sklearn.py ===")
add_code4_to_file(BASE + "gen_sklearn.py", SKLEARN_CODE4)

print("=== gen_polars.py ===")
add_code4_to_file(BASE + "gen_polars.py", POLARS_CODE4)

print("=== gen_deep_learning.py ===")
add_code4_to_file(BASE + "gen_deep_learning.py", DEEP_CODE4)

print("=== gen_streamlit.py ===")
add_code4_to_file(BASE + "gen_streamlit.py", STREAMLIT_CODE4)

print("\nDone!")
