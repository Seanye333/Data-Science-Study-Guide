"""Add sections 25-32 to gen_numpy.py."""
import sys
sys.path.insert(0, r"c:\Users\seany\Documents\All Codes\Data Science Study Path")
from _inserter import insert_sections

FILE   = r"c:\Users\seany\Documents\All Codes\Data Science Study Path\gen_numpy.py"
MARKER = "]  # end SECTIONS"

def ec(code):
    return (code.replace('\\', '\\\\')
                .replace('"', '\\"')
                .replace('\n', '\\n')
                .replace("'", "\\'"))

def make_np(num, title, desc, examples, rw_title, rw_scenario, rw_code, pt, pd_text, ps):
    ex_lines = []
    for i, ex in enumerate(examples):
        comma = ',' if i < len(examples) - 1 else ''
        ex_lines.append(
            f'        {{"label": "{ec(ex["label"])}", "code": "{ec(ex["code"])}"}}{comma}'
        )
    ex_block = '\n'.join(ex_lines)
    return (
        f'    {{\n'
        f'    "title": "{num}. {title}",\n'
        f'    "desc": "{ec(desc)}",\n'
        f'    "examples": [\n{ex_block}\n    ],\n'
        f'    "rw": {{\n'
        f'        "title": "{ec(rw_title)}",\n'
        f'        "scenario": "{ec(rw_scenario)}",\n'
        f'        "code": "{ec(rw_code)}"\n'
        f'    }},\n'
        f'    "practice": {{\n'
        f'        "title": "{ec(pt)}",\n'
        f'        "desc": "{ec(pd_text)}",\n'
        f'        "starter": "{ec(ps)}"\n'
        f'    }}\n'
        f'    }},\n\n'
    )

# ── Section 25: Meshgrid & Grid Operations ───────────────────────────────────
s25 = make_np(25, "Meshgrid & Grid Operations",
    "np.meshgrid, np.ogrid, and np.mgrid create coordinate grids for evaluating functions over 2D/3D spaces — essential for plotting, distance fields, and convolutions.",
    [
        {"label": "np.meshgrid for 2D function evaluation",
         "code":
"""import numpy as np

# meshgrid creates coordinate matrices
x = np.linspace(-2, 2, 5)
y = np.linspace(-1, 1, 4)
X, Y = np.meshgrid(x, y)

print("x:", x)
print("y:", y)
print("X shape:", X.shape, "  Y shape:", Y.shape)
print("X:\\n", X)
print("Y:\\n", Y)

# Evaluate a 2D function over the grid
Z = np.sin(X) * np.exp(-Y**2)
print("Z shape:", Z.shape)
print("Z max:", Z.max().round(4))

# Find point closest to (1.0, 0.5)
target_x, target_y = 1.0, 0.5
dist = np.sqrt((X - target_x)**2 + (Y - target_y)**2)
iy, ix = np.unravel_index(dist.argmin(), dist.shape)
print(f"Closest grid point to ({target_x}, {target_y}): ({X[iy,ix]:.1f}, {Y[iy,ix]:.1f})")

# 'ij' indexing (matrix-style, transposed from default)
X_ij, Y_ij = np.meshgrid(x, y, indexing='ij')
print("With indexing='ij': X shape:", X_ij.shape)"""},
        {"label": "ogrid and mgrid for memory-efficient grids",
         "code":
"""import numpy as np

# ogrid: open grid — returns 1D arrays that broadcast
oy, ox = np.ogrid[-3:3:7j, -3:3:7j]   # 7 points from -3 to 3
print("ogrid ox shape:", ox.shape, " oy shape:", oy.shape)  # (1,7) and (7,1)

# Broadcasting creates the 2D result without full grid in memory
Z = ox**2 + oy**2  # broadcasts to (7,7)
print("Z shape:", Z.shape)
print("Radial distance from origin:\\n", np.sqrt(Z).round(2))

# mgrid: closed grid — returns full arrays
y_grid, x_grid = np.mgrid[0:4, 0:5]  # like meshgrid but shorter syntax
print("mgrid shapes:", x_grid.shape, y_grid.shape)
print("x_grid:\\n", x_grid)

# Useful: create coordinate pairs for all pixels
H, W = 8, 8
rows, cols = np.mgrid[0:H, 0:W]
center = np.array([H/2, W/2])
dist_from_center = np.sqrt((rows - center[0])**2 + (cols - center[1])**2)
circle_mask = dist_from_center <= 3
print(f"Pixels within radius 3 of center: {circle_mask.sum()}")

# All coordinate pairs as (N, 2) array
coords = np.column_stack([rows.ravel(), cols.ravel()])
print(f"All {H}x{W} pixel coordinates shape: {coords.shape}")"""},
        {"label": "Distance fields and spatial operations",
         "code":
"""import numpy as np

# Create a distance field from a set of source points
H, W = 20, 20
rows, cols = np.mgrid[0:H, 0:W]

source_points = np.array([[3, 3], [10, 15], [17, 5]])

# Distance to nearest source point
dist_field = np.full((H, W), np.inf)
for pt in source_points:
    d = np.sqrt((rows - pt[0])**2 + (cols - pt[1])**2)
    dist_field = np.minimum(dist_field, d)

print(f"Distance field shape: {dist_field.shape}")
print(f"Max distance: {dist_field.max():.2f}")
print(f"Pixels within 5 units of any source: {(dist_field <= 5).sum()}")

# Voronoi diagram: which source is closest to each pixel?
labels = np.zeros((H, W), dtype=int)
for k, pt in enumerate(source_points):
    d = np.sqrt((rows - pt[0])**2 + (cols - pt[1])**2)
    mask = d < dist_field  # strictly closer than current min
    labels[mask] = k
    dist_field = np.minimum(dist_field, d)

for k in range(len(source_points)):
    print(f"Region {k}: {(labels == k).sum()} pixels")

# Gaussian RBF kernel centered at each source
sigma = 3.0
rbf = sum(np.exp(-(((rows-pt[0])**2+(cols-pt[1])**2)/(2*sigma**2)))
          for pt in source_points)
print(f"RBF max: {rbf.max():.3f}, sum: {rbf.sum():.1f}")"""}
    ],
    rw_title="Heat Map Generator",
    rw_scenario="A geographic data team generates a density heat map from GPS coordinates by evaluating a Gaussian kernel density estimate over a grid covering the study area.",
    rw_code=
"""import numpy as np

rng = np.random.default_rng(42)
# Simulate GPS points (lat/lon in some area)
n_points = 500
lat = rng.normal(40.7, 0.05, n_points)   # NYC-like
lon = rng.normal(-74.0, 0.08, n_points)

# Create grid
lat_grid, lon_grid = np.mgrid[
    lat.min()-0.02 : lat.max()+0.02 : 50j,
    lon.min()-0.02 : lon.max()+0.02 : 60j
]

# Gaussian KDE
def kde_density(lat_g, lon_g, lat_pts, lon_pts, bw=0.01):
    density = np.zeros_like(lat_g)
    for la, lo in zip(lat_pts, lon_pts):
        d2 = (lat_g - la)**2 + (lon_g - lo)**2
        density += np.exp(-d2 / (2 * bw**2))
    return density / (len(lat_pts) * 2 * np.pi * bw**2)

density = kde_density(lat_grid, lon_grid, lat, lon)
print(f"Grid shape: {density.shape}")
print(f"Density range: [{density.min():.4f}, {density.max():.4f}]")
print(f"Peak density at: lat={lat_grid.ravel()[density.argmax()]:.4f}, "
      f"lon={lon_grid.ravel()[density.argmax()]:.4f}")

# Hot spots: top 10% density cells
threshold = np.percentile(density, 90)
hot_spots  = density > threshold
print(f"Hot spot cells: {hot_spots.sum()} ({hot_spots.mean():.1%} of grid)")""",
    pt="Bivariate Gaussian",
    pd_text="Write a function bivariate_gaussian(X, Y, mu_x, mu_y, sigma_x, sigma_y, rho) that evaluates the bivariate normal PDF at grid points (X, Y). Parameters: mu = means, sigma = std devs, rho = correlation. Use meshgrid to create a 50x50 grid over [-3, 3] x [-3, 3] and plot (print stats). Verify the PDF integrates to ~1.",
    ps=
"""import numpy as np

def bivariate_gaussian(X, Y, mu_x=0, mu_y=0, sigma_x=1, sigma_y=1, rho=0):
    z = ((X - mu_x)**2 / sigma_x**2
         - 2*rho*(X - mu_x)*(Y - mu_y) / (sigma_x*sigma_y)
         + (Y - mu_y)**2 / sigma_y**2)
    coeff = 1 / (2 * np.pi * sigma_x * sigma_y * np.sqrt(1 - rho**2))
    return coeff * np.exp(-z / (2 * (1 - rho**2)))

x = np.linspace(-3, 3, 50)
y = np.linspace(-3, 3, 50)
X, Y = np.meshgrid(x, y)
dx = x[1] - x[0]
dy = y[1] - y[0]

# Standard normal (rho=0)
Z1 = bivariate_gaussian(X, Y)
print(f"Standard: max={Z1.max():.4f}, integral={Z1.sum()*dx*dy:.4f}")

# Correlated (rho=0.7)
Z2 = bivariate_gaussian(X, Y, mu_x=0.5, mu_y=-0.5, sigma_x=1.2, sigma_y=0.8, rho=0.7)
print(f"Correlated: max={Z2.max():.4f}, integral={Z2.sum()*dx*dy:.4f}")
print(f"Peak at: ({X.ravel()[Z2.argmax()]:.2f}, {Y.ravel()[Z2.argmax()]:.2f})")
"""
)

# ── Section 26: Advanced Broadcasting & Pairwise Operations ──────────────────
s26 = make_np(26, "Advanced Broadcasting & Pairwise Operations",
    "Broadcasting rules let NumPy operate on arrays of different shapes without copying data. Master broadcasting for pairwise distances, outer products, and vectorized scoring.",
    [
        {"label": "Broadcasting rules and shape alignment",
         "code":
"""import numpy as np

# Broadcasting rule: align shapes from the right,
# size-1 dimensions are stretched to match

# Example 1: add row vector to each row of a matrix
m = np.ones((4, 3))
v = np.array([10, 20, 30])         # shape (3,)
print("m + v:", m + v)             # (4,3) + (3,) -> (4,3)

# Example 2: add column vector to each column
col = np.array([[1], [2], [3], [4]])   # shape (4, 1)
print("m + col:\\n", m + col)          # (4,3) + (4,1) -> (4,3)

# Example 3: outer product via broadcasting
a = np.array([1, 2, 3])     # shape (3,)
b = np.array([10, 20])      # shape (2,)
outer = a[:, np.newaxis] * b[np.newaxis, :]  # (3,1) * (1,2) -> (3,2)
print("Outer product:\\n", outer)
print("Same as np.outer:", np.array_equal(outer, np.outer(a, b)))

# Shape check
shapes = [(3, 4, 5), (4, 5), (5,), (1,)]
base = np.zeros((3, 4, 5))
for s in shapes:
    arr = np.ones(s)
    print(f"(3,4,5) + {s} = {(base + arr).shape}")"""},
        {"label": "Pairwise distances (no loops)",
         "code":
"""import numpy as np

rng = np.random.default_rng(42)

# Euclidean distance matrix: D[i,j] = dist(A[i], B[j])
def pairwise_euclidean(A, B):
    # A: (m, d), B: (n, d) -> (m, n)
    # ||a - b||^2 = ||a||^2 + ||b||^2 - 2 a.b
    sq_A = (A**2).sum(axis=1, keepdims=True)  # (m, 1)
    sq_B = (B**2).sum(axis=1, keepdims=True)  # (n, 1)
    dot  = A @ B.T                            # (m, n)
    return np.sqrt(np.maximum(sq_A + sq_B.T - 2*dot, 0))

A = rng.standard_normal((50, 3))   # 50 query points
B = rng.standard_normal((100, 3))  # 100 database points

D = pairwise_euclidean(A, B)
print(f"Distance matrix: {D.shape}")
print(f"Min dist: {D.min():.3f}, Max dist: {D.max():.3f}")

# Nearest neighbor for each query
nn_idx = D.argmin(axis=1)
nn_dist = D.min(axis=1)
print(f"Query 0: nearest is B[{nn_idx[0]}] at distance {nn_dist[0]:.3f}")

# k-NN: top-k closest
k = 3
knn_idx = np.argpartition(D, k, axis=1)[:, :k]
print(f"3-NN indices for query 0: {knn_idx[0]}")

# Cosine similarity matrix
def cosine_sim(A, B):
    A_norm = A / (np.linalg.norm(A, axis=1, keepdims=True) + 1e-9)
    B_norm = B / (np.linalg.norm(B, axis=1, keepdims=True) + 1e-9)
    return A_norm @ B_norm.T

C = cosine_sim(A, B)
print(f"Cosine sim range: [{C.min():.3f}, {C.max():.3f}]")"""},
        {"label": "Vectorized scoring and ranking",
         "code":
"""import numpy as np

rng = np.random.default_rng(42)

# Multi-criteria scoring: score[i,j] = dot(weights, features[i,j])
# items: (N, F) features, weights: (F,) -> scores: (N,)
n_items, n_features = 1000, 10
features = rng.uniform(0, 1, (n_items, n_features))
weights  = np.array([0.3, 0.2, 0.15, 0.1, 0.1, 0.05, 0.04, 0.03, 0.02, 0.01])

scores = features @ weights   # (N,F) @ (F,) -> (N,)
print(f"Scores shape: {scores.shape}, range: [{scores.min():.3f}, {scores.max():.3f}]")

# Rank items (descending score)
ranks = np.argsort(scores)[::-1]
print("Top 5 items:", ranks[:5], "scores:", scores[ranks[:5]].round(3))

# Broadcasting for threshold matrix: flag (user, item) pairs
n_users = 20
user_thresholds = rng.uniform(0.4, 0.7, n_users)     # (20,)
# recommended[i,j] = True if scores[j] >= thresholds[i]
recommended = scores[np.newaxis, :] >= user_thresholds[:, np.newaxis]  # (20, 1000)
print(f"Recommendation matrix: {recommended.shape}")
print(f"Avg recommendations per user: {recommended.sum(axis=1).mean():.1f}")

# Pairwise similarity between items (feature dot products)
item_sim = features @ features.T  # (N, N)
print(f"Item similarity matrix: {item_sim.shape}")
print(f"Self-similarity range: [{np.diag(item_sim).min():.3f}, {np.diag(item_sim).max():.3f}]")"""}
    ],
    rw_title="Embedding Search Engine",
    rw_scenario="A semantic search system finds the top-5 most similar documents to a query by computing cosine similarity between query embedding and 50,000 document embeddings using broadcasting.",
    rw_code=
"""import numpy as np

rng = np.random.default_rng(42)

# Simulate document embeddings and a query
n_docs, dim = 50_000, 128
docs  = rng.standard_normal((n_docs, dim))
docs /= np.linalg.norm(docs, axis=1, keepdims=True)  # L2 normalize

query = rng.standard_normal(dim)
query /= np.linalg.norm(query)

# Cosine similarity: since both normalized, just dot product
sims = docs @ query   # (50000,)

# Top-5 results
top5_idx = np.argpartition(sims, -5)[-5:]
top5_idx = top5_idx[np.argsort(sims[top5_idx])[::-1]]

print("Top 5 similar documents:")
for rank, idx in enumerate(top5_idx, 1):
    print(f"  Rank {rank}: doc_id={idx:5d}, similarity={sims[idx]:.4f}")

# Retrieval metrics: how many docs above threshold?
threshold = 0.1
n_relevant = (sims >= threshold).sum()
print(f"Docs with similarity >= {threshold}: {n_relevant} ({n_relevant/n_docs:.2%})")

# Batch queries
n_queries = 100
queries = rng.standard_normal((n_queries, dim))
queries /= np.linalg.norm(queries, axis=1, keepdims=True)
batch_sims = queries @ docs.T   # (100, 50000)
batch_top1 = batch_sims.argmax(axis=1)
print(f"Batch top-1 for {n_queries} queries: mean sim={batch_sims.max(axis=1).mean():.4f}")""",
    pt="Attention Scores",
    pd_text="Implement scaled_dot_product_attention(Q, K, V) where Q, K have shape (seq_len, d_k) and V has shape (seq_len, d_v). Compute scores = softmax(Q @ K.T / sqrt(d_k)) @ V using only NumPy. Also implement multi_head_attention(Q, K, V, n_heads) that splits into n_heads, applies attention, and concatenates.",
    ps=
"""import numpy as np

def softmax(x, axis=-1):
    e = np.exp(x - x.max(axis=axis, keepdims=True))
    return e / e.sum(axis=axis, keepdims=True)

def scaled_dot_product_attention(Q, K, V):
    # Q: (seq, d_k), K: (seq, d_k), V: (seq, d_v)
    d_k = Q.shape[-1]
    # TODO: scores = softmax(Q @ K.T / sqrt(d_k))
    # TODO: return scores @ V
    pass

def multi_head_attention(Q, K, V, n_heads):
    seq, d = Q.shape
    d_k = d // n_heads
    heads = []
    for h in range(n_heads):
        # TODO: slice Q[:,h*d_k:(h+1)*d_k], K, V similarly
        # TODO: apply scaled_dot_product_attention, collect output
        pass
    # TODO: concatenate heads along last axis
    pass

rng = np.random.default_rng(42)
seq, d = 10, 64
Q = rng.standard_normal((seq, d))
K = rng.standard_normal((seq, d))
V = rng.standard_normal((seq, d))

out1 = scaled_dot_product_attention(Q, K, V)
print("Single-head output shape:", out1.shape)  # (10, 64)

out2 = multi_head_attention(Q, K, V, n_heads=8)
print("Multi-head output shape:", out2.shape)   # (10, 64)
"""
)

# ── Section 27: Universal Functions (ufuncs) in Depth ────────────────────────
s27 = make_np(27, "Universal Functions (ufuncs) in Depth",
    "Ufuncs are vectorized functions that operate element-wise on arrays. They support reduce, accumulate, outer, and reduceat — and you can create custom ufuncs with np.frompyfunc or Numba.",
    [
        {"label": "Built-in ufunc methods: reduce, accumulate, outer",
         "code":
"""import numpy as np

arr = np.array([1, 2, 3, 4, 5])

# reduce: apply ufunc repeatedly to reduce array
print("np.add.reduce:", np.add.reduce(arr))         # 15 (sum)
print("np.multiply.reduce:", np.multiply.reduce(arr))  # 120 (product)
print("np.maximum.reduce:", np.maximum.reduce(arr))  # 5

# accumulate: like reduce but keeps intermediate results
print("np.add.accumulate:", np.add.accumulate(arr))        # cumsum
print("np.multiply.accumulate:", np.multiply.accumulate(arr))  # cumprod
print("np.maximum.accumulate:", np.maximum.accumulate(arr))

# outer: compute all pairs
a = np.array([1, 2, 3])
b = np.array([10, 20, 30])
print("np.add.outer:\\n", np.add.outer(a, b))
print("np.multiply.outer:\\n", np.multiply.outer(a, b))

# 2D reduce along axis
m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print("Row sums:", np.add.reduce(m, axis=1))       # [6, 15, 24]
print("Col products:", np.multiply.reduce(m, axis=0))  # [28, 80, 162]

# reduceat: reduce in segments
data = np.arange(10)
# Reduce segments: [0:3], [3:6], [6:10]
result = np.add.reduceat(data, [0, 3, 6])
print("Segment sums:", result)   # [0+1+2, 3+4+5, 6+7+8+9]"""},
        {"label": "Creating custom ufuncs",
         "code":
"""import numpy as np

# np.frompyfunc: wrap a Python function as a ufunc
def clip_and_scale(x, lo=0, hi=1):
    return min(max(x, lo), hi) * 100

# frompyfunc returns object dtype by default
ufunc_cas = np.frompyfunc(lambda x: clip_and_scale(x), 1, 1)
data = np.array([-0.5, 0.0, 0.3, 0.7, 1.0, 1.5])
print("clip_and_scale:", ufunc_cas(data).astype(float))

# vectorize: more user-friendly, supports output dtype
clip_pct = np.vectorize(clip_and_scale, otypes=[float])
print("vectorize:", clip_pct(data))

# Common ufuncs catalogue
x = np.linspace(0.1, 2.0, 5)
print("exp:", np.exp(x).round(3))
print("log:", np.log(x).round(3))
print("log2:", np.log2(x).round(3))
print("log10:", np.log10(x).round(3))
print("sqrt:", np.sqrt(x).round(3))
print("cbrt:", np.cbrt(x).round(3))

# Trigonometric
angles = np.array([0, np.pi/6, np.pi/4, np.pi/3, np.pi/2])
print("sin:", np.sin(angles).round(3))
print("arcsin:", np.arcsin(np.sin(angles)).round(3))"""},
        {"label": "Ufunc performance and where argument",
         "code":
"""import numpy as np
import timeit

# where argument: apply ufunc only to selected elements
rng = np.random.default_rng(42)
data = rng.uniform(-5, 5, 1_000_000)

# np.sqrt only where data > 0, else keep 0
result = np.zeros_like(data)
np.sqrt(data, out=result, where=data > 0)
print(f"sqrt(data) where > 0: {result[:5].round(3)}")

# np.log1p (log(1+x)) is more numerically stable for small x
small = np.array([1e-10, 1e-5, 0.001, 0.01, 0.1])
print("log(1+x):  ", np.log(1 + small))
print("log1p(x):  ", np.log1p(small))

# Ufunc with out argument (in-place, avoids allocation)
a = np.random.rand(1_000_000)
b = np.empty_like(a)

t1 = timeit.timeit(lambda: np.exp(a), number=10)
t2 = timeit.timeit(lambda: np.exp(a, out=b), number=10)
print(f"exp(a) without out: {t1:.3f}s")
print(f"exp(a, out=b):      {t2:.3f}s")

# at: unbuffered in-place operation (useful for scatter operations)
arr = np.zeros(5)
indices = np.array([0, 1, 0, 2, 1])
values  = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
np.add.at(arr, indices, values)
print("add.at result:", arr)  # handles duplicate indices correctly"""}
    ],
    rw_title="Vectorized Activation Functions",
    rw_scenario="A neural network training loop applies activation functions to millions of neurons — using ufuncs with out= buffers halves memory allocation overhead.",
    rw_code=
"""import numpy as np

# Pre-allocated buffers
rng  = np.random.default_rng(42)
N    = 1_000_000
x    = rng.standard_normal(N).astype(np.float32)
buf  = np.empty_like(x)

def relu(x, out=None):
    return np.maximum(x, 0, out=out)

def sigmoid(x, out=None):
    out = np.empty_like(x) if out is None else out
    np.negative(x, out=out)
    np.exp(out, out=out)
    out += 1
    np.reciprocal(out, out=out)
    return out

def gelu(x, out=None):
    # Approximate GELU: x * sigmoid(1.702 * x)
    s = sigmoid(1.702 * x)
    return np.multiply(x, s, out=out)

def swish(x, out=None):
    return np.multiply(x, sigmoid(x), out=out)

# Compute and compare
activations = {
    "ReLU":    relu(x, buf.copy()),
    "Sigmoid": sigmoid(x, buf.copy()),
    "GELU":    gelu(x, buf.copy()),
    "Swish":   swish(x, buf.copy()),
}

for name, act in activations.items():
    print(f"{name:8s}: mean={act.mean():.4f}, std={act.std():.4f}, "
          f"range=[{act.min():.3f}, {act.max():.3f}]")""",
    pt="Custom Ufunc",
    pd_text="Use np.frompyfunc to create a ufunc haversine_ufunc that computes the great-circle distance in km between a (lat1, lon1) and (lat2, lon2) point pair. Then use vectorize to wrap it into a function that accepts arrays of lat/lon pairs. Compute distances between New York and a grid of 100 cities.",
    ps=
"""import numpy as np

def haversine_scalar(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat/2)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon/2)**2
    return 2 * R * np.arcsin(np.sqrt(a))

# Vectorize to work on arrays
haversine = np.vectorize(haversine_scalar, otypes=[float])

# New York City
ny_lat, ny_lon = 40.7128, -74.0060

rng = np.random.default_rng(42)
n_cities = 100
city_lats = rng.uniform(-60, 70, n_cities)
city_lons = rng.uniform(-180, 180, n_cities)

distances = haversine(ny_lat, ny_lon, city_lats, city_lons)
print(f"Distances computed: {len(distances)}")
print(f"Nearest city: {distances.min():.0f} km")
print(f"Farthest city: {distances.max():.0f} km")
print(f"Average distance from NYC: {distances.mean():.0f} km")
"""
)

# ── Section 28: Masked Arrays ────────────────────────────────────────────────
s28 = make_np(28, "Masked Arrays (np.ma)",
    "np.ma.MaskedArray transparently handles missing data by maintaining a boolean mask alongside values. Useful for sensor data with gaps or any dataset with invalid entries.",
    [
        {"label": "Creating and using masked arrays",
         "code":
"""import numpy as np

# Create masked array
data = np.array([1.0, 2.0, -999.0, 4.0, -999.0, 6.0])
mask = data == -999.0

ma = np.ma.array(data, mask=mask)
print("Data:  ", ma)
print("Mask:  ", ma.mask)
print("Filled:", ma.filled(fill_value=0))

# Operations automatically skip masked values
print("Mean (excludes masked):", ma.mean())   # (1+2+4+6)/4 = 3.25
print("Sum:", ma.sum())                        # 13
print("Std:", ma.std().round(4))

# np.ma.masked_where
arr = np.array([10, 25, -5, 0, 8, -1, 15])
ma2 = np.ma.masked_where(arr <= 0, arr)
print("Masked non-positive:", ma2)
print("Log (safe):", np.log(ma2))   # no error for masked values

# np.ma.masked_invalid: auto-mask NaN and Inf
dirty = np.array([1.0, np.nan, 3.0, np.inf, 5.0, -np.inf])
clean = np.ma.masked_invalid(dirty)
print("Masked invalid:", clean)
print("Safe mean:", clean.mean())"""},
        {"label": "Masked array operations and conversions",
         "code":
"""import numpy as np

# 2D masked array
temps = np.array([[15.2, 16.1, -999, 18.5],
                  [-999, 14.8, 15.9, 16.7],
                  [13.1, -999, -999, 15.3]])
m = np.ma.masked_equal(temps, -999)

print("Masked temps:\\n", m)
print("Row means (excl. missing):", m.mean(axis=1))
print("Col means (excl. missing):", m.mean(axis=0))

# Fill with column means
col_means = m.mean(axis=0)
filled = m.filled(fill_value=col_means)  # broadcasts col_means
print("Filled temps:\\n", filled.round(1))

# Stacking masked arrays
a = np.ma.array([1, 2, 3, 4], mask=[0, 1, 0, 0])
b = np.ma.array([5, 6, 7, 8], mask=[0, 0, 1, 0])
stacked = np.ma.vstack([a, b])
print("Stacked:\\n", stacked)
print("Column min (ignoring masks):", stacked.min(axis=0))

# Convert to/from regular arrays
arr = m.compressed()         # 1D array of valid values only
print("Compressed:", arr)
arr2 = np.ma.filled(m, -1)  # replace mask with -1
print("Filled(-1):\\n", arr2)"""},
        {"label": "Masked array with statistics and aggregations",
         "code":
"""import numpy as np

rng = np.random.default_rng(42)
N = 1000

# Simulate sensor readings with random dropouts
raw = rng.normal(20, 3, N)          # temperature readings
dropout_mask = rng.random(N) < 0.15  # 15% missing

sensor = np.ma.array(raw, mask=dropout_mask)
print(f"Total readings: {N}")
print(f"Valid readings: {sensor.count()} ({sensor.count()/N:.1%})")
print(f"Masked readings: {sensor.mask.sum()}")

# Robust statistics (automatically use only valid data)
print(f"Mean:   {sensor.mean():.3f}")
print(f"Median: {np.ma.median(sensor):.3f}")
print(f"Std:    {sensor.std():.3f}")
print(f"Min:    {sensor.min():.3f}")
print(f"Max:    {sensor.max():.3f}")

# Percentiles (need filled for np.percentile)
filled_for_pct = sensor.compressed()
print(f"P25/P75: {np.percentile(filled_for_pct, [25,75]).round(2)}")

# Anomaly detection: flag values > 3 sigma (on top of existing mask)
mean, std = sensor.mean(), sensor.std()
anomaly_mask = (sensor < mean - 3*std) | (sensor > mean + 3*std)
sensor_clean = np.ma.array(sensor.data, mask=sensor.mask | anomaly_mask.filled(False))
print(f"After anomaly removal: {sensor_clean.count()} valid readings")"""}
    ],
    rw_title="Oceanographic Data Cleaner",
    rw_scenario="A research station processes 5-year daily ocean temperature data with sensor failures (flagged as -9999) and physical impossibilities (<-2°C or >35°C), using masked arrays to compute clean statistics.",
    rw_code=
"""import numpy as np

rng = np.random.default_rng(42)
n_years = 5
n_days  = n_years * 365

# Simulate ocean temps with seasonal pattern
t = np.linspace(0, n_years * 2 * np.pi, n_days)
base_temp = 15 + 10 * np.sin(t - np.pi/2)  # seasonal cycle
temps = base_temp + rng.normal(0, 1.5, n_days)

# Inject data quality issues
sensor_fail   = rng.random(n_days) < 0.08    # 8% sensor failures
physical_anom = rng.random(n_days) < 0.02    # 2% physical anomalies
temps[sensor_fail]   = -9999.0
temps[physical_anom] = rng.choice([-5.0, 40.0], physical_anom.sum())

# Build mask: flag everything invalid
mask = ((temps == -9999.0) |
        (temps < -2.0) |
        (temps > 35.0))
clean = np.ma.array(temps, mask=mask)

print(f"Data coverage: {clean.count()/n_days:.1%} valid ({clean.count()} of {n_days} days)")
print(f"Mean temperature: {clean.mean():.2f}°C")
print(f"Seasonal range: [{clean.min():.2f}, {clean.max():.2f}]°C")

# Annual stats (reshape to years x 365)
annual = clean[:n_years*365].reshape(n_years, 365)
for y in range(n_years):
    row = annual[y]
    print(f"  Year {y+1}: mean={row.mean():.2f}°C, valid={row.count()} days")""",
    pt="Masked Correlation",
    pd_text="Write masked_corrcoef(X) that computes a pairwise correlation matrix for a 2D masked array X (shape n_obs x n_vars), where each pair of variables is correlated only using rows where BOTH are valid. Return a regular (n_vars x n_vars) ndarray. Test on a dataset where each column has independent random missing values.",
    ps=
"""import numpy as np

def masked_corrcoef(X):
    n_obs, n_vars = X.shape
    corr = np.eye(n_vars)
    for i in range(n_vars):
        for j in range(i+1, n_vars):
            # Rows valid for BOTH columns i and j
            valid = (~X[:, i].mask) & (~X[:, j].mask)
            if valid.sum() < 2:
                corr[i, j] = corr[j, i] = np.nan
                continue
            xi = X[valid, i].data
            xj = X[valid, j].data
            r  = np.corrcoef(xi, xj)[0, 1]
            corr[i, j] = corr[j, i] = r
    return corr

rng = np.random.default_rng(42)
n, p = 200, 4
data = rng.standard_normal((n, p))
# Create correlated structure
data[:, 1] = 0.7 * data[:, 0] + 0.3 * rng.standard_normal(n)

masks = rng.random((n, p)) < 0.2   # 20% missing per column
X = np.ma.array(data, mask=masks)

corr = masked_corrcoef(X)
print("Pairwise correlations (with per-pair valid observations):")
print(corr.round(3))
print("Expected corr(0,1) ~ 0.7:", corr[0, 1].round(2))
"""
)

# ── Section 29: Memory Layout, Strides & Contiguity ─────────────────────────
s29 = make_np(29, "Memory Layout, Strides & Contiguity",
    "NumPy arrays store data in contiguous memory blocks. Understanding C/F order, strides, and views vs copies is critical for performance and interoperability with C/Fortran libraries.",
    [
        {"label": "C vs Fortran order, flags, and strides",
         "code":
"""import numpy as np

# C order (row-major): last axis varies fastest (default)
arr_c = np.array([[1, 2, 3], [4, 5, 6]], order='C')
print("C order strides:", arr_c.strides)   # (12, 4) for float32

# F order (column-major): first axis varies fastest
arr_f = np.array([[1, 2, 3], [4, 5, 6]], order='F')
print("F order strides:", arr_f.strides)   # (4, 8) for float32

# Check flags
print("C-contiguous:", arr_c.flags['C_CONTIGUOUS'])   # True
print("F-contiguous:", arr_c.flags['F_CONTIGUOUS'])   # False

# Transpose only changes strides, no data copy
T = arr_c.T
print("Transposed strides:", T.strides)
print("T is view:", T.base is arr_c)   # True

# ascontiguousarray: ensure C-contiguous copy
T_c = np.ascontiguousarray(T)
print("After ascontiguousarray:", T_c.flags['C_CONTIGUOUS'])

# Strides as bytes
arr = np.arange(24, dtype=np.float64).reshape(2, 3, 4)
print(f"Shape: {arr.shape}, Strides (bytes): {arr.strides}")
print(f"Itemsize: {arr.itemsize} bytes")
# stride[k] = itemsize * product(shape[k+1:])"""},
        {"label": "Views vs copies and memory sharing",
         "code":
"""import numpy as np

arr = np.arange(20, dtype=float)

# Slice creates a VIEW (shares memory)
view = arr[2:10:2]   # every 2nd element from 2 to 10
print("view:", view)
print("view.base is arr:", view.base is arr)

view[0] = 999        # modifies arr!
print("arr after view[0]=999:", arr[:12])

# copy() creates an independent copy
arr2 = arr.copy()
arr2[0] = -1
print("Original arr[0] unchanged:", arr[0])  # still 999 (from earlier)

# Fancy indexing always copies
fancy = arr[[0, 3, 7]]
print("fancy.base:", fancy.base)   # None = not a view

# reshape: usually a view if data is contiguous
arr3 = np.arange(12)
reshaped = arr3.reshape(3, 4)
print("reshape is view:", reshaped.base is arr3)
reshaped[0, 0] = -1
print("arr3[0] changed:", arr3[0])   # -1

# np.shares_memory: robust check
a = np.arange(10)
b = a[::2]
c = a.copy()
print("a and b share memory:", np.shares_memory(a, b))   # True
print("a and c share memory:", np.shares_memory(a, c))   # False"""},
        {"label": "Stride tricks for rolling windows",
         "code":
"""import numpy as np
from numpy.lib.stride_tricks import sliding_window_view, as_strided

arr = np.arange(10, dtype=float)

# sliding_window_view: safe way to get overlapping windows
windows = sliding_window_view(arr, window_shape=4)
print("Windows shape:", windows.shape)   # (7, 4)
print("First 3 windows:\\n", windows[:3])

# Each window is a VIEW — no data copy!
windows[0, 0] = 999
print("arr[0] changed:", arr[0])   # yes, 999

arr = np.arange(10, dtype=float)  # reset

# 2D rolling windows (for image patches)
img = np.arange(16, dtype=float).reshape(4, 4)
patches = sliding_window_view(img, window_shape=(2, 2))
print("2D patches shape:", patches.shape)   # (3, 3, 2, 2)
print("Patch at [0,0]:\\n", patches[0, 0])

# as_strided: manual stride tricks (use with care!)
# Rolling mean via strides
def rolling_mean_strided(arr, window):
    w = sliding_window_view(arr, window)
    return w.mean(axis=1)

rolling = rolling_mean_strided(np.arange(10, dtype=float), 3)
print("Rolling mean (window=3):", rolling)"""}
    ],
    rw_title="Cache-Friendly Matrix Multiply",
    rw_scenario="A performance-critical simulation avoids unnecessary transpositions and ensures arrays are contiguous before passing to BLAS-backed np.dot, cutting computation time significantly.",
    rw_code=
"""import numpy as np, timeit

rng = np.random.default_rng(42)

A = rng.standard_normal((500, 300))
B = rng.standard_normal((300, 400))

# C-contiguous vs non-contiguous performance
B_T_F = np.asfortranarray(B.T)       # F-order, non-contiguous for @
B_T_C = np.ascontiguousarray(B.T)    # C-contiguous copy

print("B.T C-contiguous:", B.T.flags['C_CONTIGUOUS'])      # False
print("B_T_C contiguous:", B_T_C.flags['C_CONTIGUOUS'])    # True

# GEMM: A @ B (B is 300x400 C-contiguous)
t1 = timeit.timeit(lambda: A @ B, number=100)
t2 = timeit.timeit(lambda: A @ B_T_F.T, number=100)
t3 = timeit.timeit(lambda: A @ B_T_C.T, number=100)

print(f"A @ B (contiguous):      {t1:.4f}s")
print(f"A @ B_T_F.T (F-order):   {t2:.4f}s")
print(f"A @ B_T_C.T (C-order):   {t3:.4f}s")

# Verify results are the same
C1 = A @ B
C2 = A @ B_T_F.T
print("Results match:", np.allclose(C1, C2))

# Memory usage check
import sys
print(f"B.T.copy() size: {sys.getsizeof(B.T.copy()):,} bytes")
print(f"B.T view size:   {sys.getsizeof(B.T):,} bytes (metadata only)")""",
    pt="Stride Inspector",
    pd_text="Write inspect_array(arr) that prints: shape, dtype, strides, itemsize, nbytes, is_C_contiguous, is_F_contiguous, is_view (arr.base is not None), total elements. Then write reshape_safe(arr, shape) that reshapes arr to shape, ensuring the result is C-contiguous (copy only if needed). Test with various slices and transpositions.",
    ps=
"""import numpy as np

def inspect_array(arr):
    print(f"Shape:           {arr.shape}")
    print(f"dtype:           {arr.dtype}")
    print(f"strides (bytes): {arr.strides}")
    print(f"itemsize:        {arr.itemsize}")
    print(f"nbytes:          {arr.nbytes:,}")
    print(f"C-contiguous:    {arr.flags['C_CONTIGUOUS']}")
    print(f"F-contiguous:    {arr.flags['F_CONTIGUOUS']}")
    print(f"Is view:         {arr.base is not None}")
    print(f"N elements:      {arr.size}")

def reshape_safe(arr, shape):
    if not arr.flags['C_CONTIGUOUS']:
        arr = np.ascontiguousarray(arr)
    return arr.reshape(shape)

base = np.arange(24, dtype=np.float32).reshape(4, 6)
print("=== Base array ===")
inspect_array(base)

print("\\n=== Transposed ===")
T = base.T
inspect_array(T)

print("\\n=== Slice (non-contiguous) ===")
s = base[::2, ::2]
inspect_array(s)

print("\\n=== Reshape safe (from transposed) ===")
r = reshape_safe(T, (24,))
inspect_array(r)
"""
)

# ── Section 30: Matrix Operations & Kronecker Products ───────────────────────
s30 = make_np(30, "Advanced Linear Algebra Operations",
    "Beyond basic dot products: matrix decompositions (SVD, QR, Cholesky), determinants, null spaces, pseudo-inverse, and Kronecker products for systems of equations and dimensionality reduction.",
    [
        {"label": "QR decomposition and least squares",
         "code":
"""import numpy as np

rng = np.random.default_rng(42)

# QR decomposition: A = Q @ R
A = rng.standard_normal((6, 4))
Q, R = np.linalg.qr(A)
print(f"A: {A.shape}, Q: {Q.shape}, R: {R.shape}")
print("Q orthonormal:", np.allclose(Q.T @ Q, np.eye(4)))
print("A = Q@R:", np.allclose(A, Q @ R))

# Least squares: solve Ax = b for overdetermined system
m, n = 100, 5
A = rng.standard_normal((m, n))
true_x = rng.standard_normal(n)
b = A @ true_x + rng.normal(0, 0.1, m)   # noisy measurements

# lstsq: minimize ||Ax - b||^2
x, residuals, rank, sv = np.linalg.lstsq(A, b, rcond=None)
print(f"True x:   {true_x[:3].round(3)}")
print(f"Solved x: {x[:3].round(3)}")
print(f"Matrix rank: {rank}, condition number: {sv[0]/sv[-1]:.1f}")

# Via normal equations (less stable but educational)
x_normal = np.linalg.solve(A.T @ A, A.T @ b)
print("Normal eq error:", np.abs(x - x_normal).max())"""},
        {"label": "Cholesky, determinant, and null space",
         "code":
"""import numpy as np

rng = np.random.default_rng(42)

# Cholesky decomposition: A = L @ L.T (for positive definite A)
# Used for sampling multivariate normal and inverting covariance matrices
n = 5
A = rng.standard_normal((n, n))
S = A.T @ A + n * np.eye(n)  # make it positive definite

L = np.linalg.cholesky(S)
print("L shape:", L.shape)
print("L @ L.T == S:", np.allclose(L @ L.T, S))
print("L is lower triangular:", np.allclose(L, np.tril(L)))

# Sample from multivariate normal using Cholesky
mu  = np.zeros(n)
cov = S / S.max()   # scale to reasonable range
L   = np.linalg.cholesky(cov)
samples = mu + rng.standard_normal((1000, n)) @ L.T
print(f"Sample covariance matches target: {np.allclose(np.cov(samples.T), cov, atol=0.1)}")

# Determinant (log for numerical stability)
logdet_sign, logdet = np.linalg.slogdet(S)
print(f"logdet(S): {logdet:.3f}, sign: {logdet_sign}")
print(f"det(S) = exp({logdet:.1f}) ~ {np.exp(logdet):.2e}")

# Pseudo-inverse (Moore-Penrose)
m = np.array([[1, 2], [3, 4], [5, 6]])
pinv = np.linalg.pinv(m)
print("Pseudo-inverse shape:", pinv.shape)
print("m @ pinv @ m == m:", np.allclose(m @ pinv @ m, m))"""},
        {"label": "Eigendecomposition and PCA from scratch",
         "code":
"""import numpy as np

rng = np.random.default_rng(42)

# Eigendecomposition: A v = lambda v
A = np.array([[4, -2], [1,  1]])
eigenvalues, eigenvectors = np.linalg.eig(A)
print("Eigenvalues:", eigenvalues)
print("Eigenvectors:\\n", eigenvectors)

# Verify: A @ v = lambda * v
for i in range(len(eigenvalues)):
    v = eigenvectors[:, i]
    print(f"  A @ v{i} == {eigenvalues[i]:.1f} * v{i}: {np.allclose(A @ v, eigenvalues[i] * v)}")

# Symmetric matrix: use eigh (more stable, guaranteed real eigenvalues)
S = np.array([[3, 1], [1, 3]])
w, v = np.linalg.eigh(S)
print("Symmetric eigs:", w)

# PCA from scratch using SVD
n, d = 200, 5
X = rng.standard_normal((n, d))
X[:, 1] = 0.8 * X[:, 0] + 0.6 * X[:, 1]  # create correlation

# Center data
X_c = X - X.mean(axis=0)

# SVD of centered data
U, s, Vt = np.linalg.svd(X_c, full_matrices=False)
explained = s**2 / (s**2).sum()
print("Explained variance ratio:", explained.round(3))
print("Cumulative:", explained.cumsum().round(3))

# Project to 2 components
X_2d = X_c @ Vt[:2].T
print(f"PCA 2D shape: {X_2d.shape}")"""}
    ],
    rw_title="Recommender via Matrix Factorization",
    rw_scenario="A collaborative filtering system factorizes a user-item rating matrix using SVD to find latent factors and predict missing ratings.",
    rw_code=
"""import numpy as np

rng = np.random.default_rng(42)

n_users, n_items, n_factors = 100, 200, 10

# Simulate a low-rank rating matrix (most entries unknown)
U_true = rng.standard_normal((n_users, n_factors))
V_true = rng.standard_normal((n_items, n_factors))
R_true = U_true @ V_true.T + rng.normal(0, 0.5, (n_users, n_items))
R_true = np.clip(R_true, 1, 5)

# Only observe 20% of ratings
observed_mask = rng.random((n_users, n_items)) < 0.2
R_obs = np.where(observed_mask, R_true, 0.0)

# Truncated SVD on observed (imperfect but illustrative)
U, s, Vt = np.linalg.svd(R_obs, full_matrices=False)
k = n_factors
R_hat = U[:, :k] @ np.diag(s[:k]) @ Vt[:k, :]
R_hat = np.clip(R_hat, 1, 5)

# RMSE on observed entries
observed_pred = R_hat[observed_mask]
observed_true = R_true[observed_mask]
rmse = np.sqrt(np.mean((observed_pred - observed_true)**2))
print(f"RMSE on observed ratings: {rmse:.3f}")

# Top-5 recommendations for user 0
user0_scores = R_hat[0]
user0_unseen = ~observed_mask[0]
top5 = np.argsort(user0_scores * user0_unseen)[::-1][:5]
print(f"Top-5 recommendations for user 0: items {top5} with scores {user0_scores[top5].round(2)}")""",
    pt="System of Equations Solver",
    pd_text="Write solve_system(A, b) that checks if the system Ax=b is (1) well-determined (use rank), (2) overdetermined (least squares), or (3) underdetermined (minimum-norm solution via pinv), and solves accordingly with a label. Also write condition_number(A) and show how ill-conditioned matrices cause solution instability.",
    ps=
"""import numpy as np

def solve_system(A, b):
    m, n = A.shape
    rank = np.linalg.matrix_rank(A)
    if m == n and rank == n:
        label = "well-determined"
        x = np.linalg.solve(A, b)
    elif m > n:
        label = "overdetermined (least squares)"
        x, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
    else:
        label = "underdetermined (min-norm)"
        x = np.linalg.pinv(A) @ b
    return x, label

def condition_number(A):
    s = np.linalg.svd(A, compute_uv=False)
    return s[0] / s[-1] if s[-1] > 0 else np.inf

# Test cases
rng = np.random.default_rng(42)

# Well-determined 3x3
A1 = rng.standard_normal((3, 3))
b1 = rng.standard_normal(3)
x1, lbl1 = solve_system(A1, b1)
print(f"{lbl1}: cond={condition_number(A1):.1f}, error={np.linalg.norm(A1@x1-b1):.2e}")

# Overdetermined 10x3
A2 = rng.standard_normal((10, 3))
b2 = rng.standard_normal(10)
x2, lbl2 = solve_system(A2, b2)
print(f"{lbl2}: cond={condition_number(A2):.1f}, residual={np.linalg.norm(A2@x2-b2):.4f}")

# Ill-conditioned
A3 = np.array([[1, 1], [1, 1+1e-10]])
b3 = np.array([2.0, 2.0])
x3, lbl3 = solve_system(A3, b3)
print(f"{lbl3}: cond={condition_number(A3):.2e}")
"""
)

# ── Section 31: Numerical Differentiation ────────────────────────────────────
s31 = make_np(31, "Numerical Differentiation & Optimization",
    "Finite differences approximate gradients of black-box functions. Combined with np.gradient, they enable sensitivity analysis, gradient checking, and simple optimization without symbolic math.",
    [
        {"label": "Finite differences: forward, backward, central",
         "code":
"""import numpy as np

# First derivative via finite differences
def forward_diff(f, x, h=1e-5):
    return (f(x + h) - f(x)) / h

def backward_diff(f, x, h=1e-5):
    return (f(x) - f(x - h)) / h

def central_diff(f, x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2 * h)

def second_diff(f, x, h=1e-5):
    return (f(x + h) - 2*f(x) + f(x - h)) / h**2

# Test on f(x) = sin(x), f'(x) = cos(x)
f = np.sin
x = np.pi / 4
true_deriv = np.cos(x)

print(f"True f'(pi/4) = {true_deriv:.10f}")
print(f"Forward:   {forward_diff(f, x):.10f}  err={abs(forward_diff(f,x)-true_deriv):.2e}")
print(f"Backward:  {backward_diff(f, x):.10f}  err={abs(backward_diff(f,x)-true_deriv):.2e}")
print(f"Central:   {central_diff(f, x):.10f}  err={abs(central_diff(f,x)-true_deriv):.2e}")
print(f"Second:    {second_diff(f, x):.10f}  true=-sin(pi/4)={-np.sin(x):.10f}")

# Vectorized on array
x_arr = np.linspace(0, 2*np.pi, 100)
deriv_arr = central_diff(np.sin, x_arr)
error = np.abs(deriv_arr - np.cos(x_arr))
print(f"Max error over array: {error.max():.2e}")"""},
        {"label": "np.gradient for array derivatives",
         "code":
"""import numpy as np

# np.gradient: uses central differences internally, handles edges with one-sided
x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)

dydx = np.gradient(y, x)   # pass x for proper spacing
true  = np.cos(x)
print(f"Max error vs cos(x): {np.abs(dydx - true).max():.4e}")

# Partial derivatives of 2D function
nx, ny = 50, 60
x_1d = np.linspace(0, 2, nx)
y_1d = np.linspace(0, 3, ny)
X, Y = np.meshgrid(x_1d, y_1d)

Z = np.sin(X) * np.cos(Y)

# gradient returns [dZ/dy, dZ/dx] for 2D (row, col ordering)
dZ_dy, dZ_dx = np.gradient(Z, y_1d, x_1d)

true_dZ_dx = np.cos(X) * np.cos(Y)
true_dZ_dy = -np.sin(X) * np.sin(Y)

print(f"dZ/dx error: {np.abs(dZ_dx - true_dZ_dx).max():.4e}")
print(f"dZ/dy error: {np.abs(dZ_dy - true_dZ_dy).max():.4e}")

# Gradient magnitude (for edge detection in images)
mag = np.sqrt(dZ_dx**2 + dZ_dy**2)
print(f"Gradient magnitude: min={mag.min():.3f}, max={mag.max():.3f}")"""},
        {"label": "Gradient descent with NumPy",
         "code":
"""import numpy as np

rng = np.random.default_rng(42)

# Optimize f(x, y) = (x-3)^2 + 2*(y+1)^2 (minimum at (3, -1))
def f(params):
    x, y = params
    return (x - 3)**2 + 2*(y + 1)**2

def grad_f(params):
    x, y = params
    return np.array([2*(x - 3), 4*(y + 1)])

# Gradient descent
params  = np.array([0.0, 0.0])
lr      = 0.1
history = [params.copy()]

for i in range(50):
    g = grad_f(params)
    params = params - lr * g
    history.append(params.copy())
    if i % 10 == 9:
        print(f"  iter {i+1:3d}: f={f(params):.6f}, params=({params[0]:.3f}, {params[1]:.3f})")

print(f"True minimum: (3, -1), found: ({params[0]:.4f}, {params[1]:.4f})")

# Numerical gradient check (compare analytic vs finite diff)
test_pt = rng.standard_normal(2)
analytic = grad_f(test_pt)
h = 1e-6
numeric  = np.array([(f(test_pt + h*e) - f(test_pt - h*e)) / (2*h)
                      for e in np.eye(2)])
print(f"Gradient check: analytic={analytic.round(4)}, numeric={numeric.round(4)}")
print(f"Max error: {np.abs(analytic - numeric).max():.2e}")"""}
    ],
    rw_title="Gradient-Based Calibration",
    rw_scenario="A financial model calibrates parameters to match observed option prices by minimizing a loss function using gradient descent with numerical gradients.",
    rw_code=
"""import numpy as np

rng = np.random.default_rng(42)

# Simulate: find mu, sigma that best fit observed log returns
n_obs = 500
true_mu, true_sigma = 0.001, 0.02
observed = rng.normal(true_mu, true_sigma, n_obs)

def neg_log_likelihood(params, data):
    mu, log_sigma = params
    sigma = np.exp(log_sigma)  # log parameterization ensures sigma > 0
    return 0.5 * np.sum(np.log(2*np.pi*sigma**2) + ((data - mu)/sigma)**2)

def numerical_gradient(f, params, h=1e-6):
    grad = np.zeros_like(params)
    for i in range(len(params)):
        e = np.zeros_like(params)
        e[i] = h
        grad[i] = (f(params + e) - f(params - e)) / (2 * h)
    return grad

params = np.array([0.0, np.log(0.01)])  # initial guess
lr = 1e-4

for epoch in range(500):
    loss = neg_log_likelihood(params, observed)
    grad = numerical_gradient(lambda p: neg_log_likelihood(p, observed), params)
    params -= lr * grad

mu_hat    = params[0]
sigma_hat = np.exp(params[1])
print(f"True:      mu={true_mu:.4f}, sigma={true_sigma:.4f}")
print(f"Estimated: mu={mu_hat:.4f}, sigma={sigma_hat:.4f}")
print(f"Error:     mu={abs(mu_hat-true_mu):.2e}, sigma={abs(sigma_hat-true_sigma):.2e}")""",
    pt="Jacobian Checker",
    pd_text="Write jacobian(f, x, h=1e-6) that computes the Jacobian matrix of a vector-valued function f: R^n -> R^m using central differences. Then write gradient_check(f, grad_f, x) that compares the numerical Jacobian with the analytic gradient and reports the relative error. Test with f(x) = [sin(x0)*x1, x0^2 + exp(x1)].",
    ps=
"""import numpy as np

def jacobian(f, x, h=1e-6):
    x  = np.asarray(x, float)
    f0 = np.asarray(f(x), float)
    m  = f0.size
    n  = x.size
    J  = np.zeros((m, n))
    for j in range(n):
        dx    = np.zeros(n)
        dx[j] = h
        J[:, j] = (np.asarray(f(x + dx)) - np.asarray(f(x - dx))) / (2 * h)
    return J

def gradient_check(f, grad_f, x, h=1e-6):
    J_num = jacobian(f, x, h)
    J_ana = np.asarray(grad_f(x))
    err   = np.abs(J_num - J_ana)
    rel   = err / (np.abs(J_ana) + 1e-8)
    return {"max_abs_err": err.max(), "max_rel_err": rel.max(), "ok": rel.max() < 1e-4}

# Test function: f(x) = [sin(x0)*x1, x0^2 + exp(x1)]
def f_vec(x):
    return [np.sin(x[0])*x[1], x[0]**2 + np.exp(x[1])]

def df_vec(x):
    return np.array([
        [np.cos(x[0])*x[1], np.sin(x[0])],
        [2*x[0],              np.exp(x[1])],
    ])

x0 = np.array([0.5, 1.2])
result = gradient_check(f_vec, df_vec, x0)
print("Jacobian check:", result)
print("Numerical J:\\n", jacobian(f_vec, x0).round(6))
print("Analytic J:\\n",  df_vec(x0).round(6))
"""
)

# ── Section 32: NumPy in Data Science Workflows ──────────────────────────────
s32 = make_np(32, "NumPy in Data Science Workflows",
    "NumPy integrates tightly with pandas, scikit-learn, PyTorch, and SciPy. Understanding these bridges — arrays, dtypes, memory sharing — makes you faster at the whole pipeline.",
    [
        {"label": "NumPy <-> Pandas integration",
         "code":
"""import numpy as np

# Simulate what pandas does under the hood
# A DataFrame is essentially a dict of 1D NumPy arrays

# From numpy to structured array (pandas-like)
n = 5
ids    = np.arange(1, n+1)
names  = np.array(['Alice', 'Bob', 'Carol', 'Dave', 'Eve'])
scores = np.array([92.5, 78.3, 88.1, 95.0, 70.2])
grades = np.where(scores >= 90, 'A', np.where(scores >= 80, 'B', 'C'))

# Operations you'd do in pandas, using only NumPy
mean_score = scores.mean()
top_scorers = names[scores >= 90]
passing     = names[scores >= 75]

print("Mean score:", mean_score.round(2))
print("Top scorers (A grade):", top_scorers)
print("Passing (>=75):", passing)

# Group by grade
for grade in np.unique(grades):
    mask = grades == grade
    print(f"Grade {grade}: {names[mask].tolist()}, avg={scores[mask].mean():.1f}")

# NumPy array -> pandas DataFrame conversion info
try:
    import pandas as pd
    df = pd.DataFrame({'id': ids, 'name': names, 'score': scores, 'grade': grades})
    # df.values returns numpy array (may copy depending on dtypes)
    arr = df[['id', 'score']].to_numpy()
    print("DataFrame to numpy:", arr.shape, arr.dtype)
except ImportError:
    print("(pandas not available, but the pattern works)")"""},
        {"label": "NumPy for feature engineering",
         "code":
"""import numpy as np

rng = np.random.default_rng(42)
n, d = 1000, 5

X = rng.standard_normal((n, d))

# 1. Normalization
def z_score(X):
    return (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-8)

def min_max(X):
    lo, hi = X.min(axis=0), X.max(axis=0)
    return (X - lo) / (hi - lo + 1e-8)

Xz = z_score(X)
Xm = min_max(X)
print(f"Z-score: mean={Xz.mean(axis=0).round(2)}, std={Xz.std(axis=0).round(2)}")
print(f"MinMax: [{Xm.min():.3f}, {Xm.max():.3f}]")

# 2. Polynomial features (degree 2, first 3 columns)
Xp = np.column_stack([X[:, :3], X[:, :3]**2,
                       X[:, 0:1]*X[:, 1:2], X[:, 1:2]*X[:, 2:3]])
print(f"Polynomial features: {X.shape} -> {Xp.shape}")

# 3. One-hot encoding
cats = rng.integers(0, 4, n)   # 4 categories
ohe  = (cats[:, np.newaxis] == np.arange(4)[np.newaxis, :]).astype(float)
print(f"OHE: shape={ohe.shape}, sum per row all 1: {np.all(ohe.sum(axis=1)==1)}")

# 4. Interaction features (outer product per row)
a = X[:, :3]   # 3 features
# Row-wise outer: shape (n, 3, 3) -> upper triangle -> (n, 6) interaction terms
combos = np.einsum('ni,nj->nij', a, a)
triu_idx = np.triu_indices(3, k=0)
interactions = combos[:, triu_idx[0], triu_idx[1]]
print(f"Interaction features shape: {interactions.shape}")"""},
        {"label": "NumPy in ML inference",
         "code":
"""import numpy as np

rng = np.random.default_rng(42)

# Manually implement a 2-layer neural network forward pass
def relu(x): return np.maximum(0, x)
def softmax(x):
    e = np.exp(x - x.max(axis=1, keepdims=True))
    return e / e.sum(axis=1, keepdims=True)

# Simulated trained weights (normally loaded from file)
n_in, n_hidden, n_out = 784, 256, 10
W1 = rng.standard_normal((n_in, n_hidden)) * 0.01
b1 = np.zeros(n_hidden)
W2 = rng.standard_normal((n_hidden, n_out)) * 0.01
b2 = np.zeros(n_out)

def forward(X):
    h1  = relu(X @ W1 + b1)
    out = softmax(X @ W1 @ W2 + b2)  # simplified
    return out

# Batch inference
batch_size = 64
X_batch = rng.standard_normal((batch_size, n_in)).astype(np.float32)
probs = forward(X_batch)
preds = probs.argmax(axis=1)
conf  = probs.max(axis=1)

print(f"Batch: {X_batch.shape} -> probs: {probs.shape}")
print(f"Predictions: {preds[:10]}")
print(f"Confidence: min={conf.min():.3f}, max={conf.max():.3f}, mean={conf.mean():.3f}")

# Top-3 predictions per sample
top3 = np.argsort(probs, axis=1)[:, -3:][:, ::-1]
print(f"Top-3 class indices for sample 0: {top3[0]}")"""}
    ],
    rw_title="End-to-End ML Pipeline",
    rw_scenario="A data scientist implements a complete train/eval cycle using only NumPy: feature normalization, train/val/test split, logistic regression with gradient descent, and evaluation metrics.",
    rw_code=
"""import numpy as np

rng = np.random.default_rng(42)
N, D = 1000, 10

# Synthetic binary classification data
X = rng.standard_normal((N, D))
true_w = rng.standard_normal(D)
y = (X @ true_w + rng.normal(0, 0.5, N) > 0).astype(float)

# Train/val/test split (70/15/15)
idx = rng.permutation(N)
n_train = int(0.7*N); n_val = int(0.15*N)
tr, va, te = idx[:n_train], idx[n_train:n_train+n_val], idx[n_train+n_val:]

def normalize(X_tr, X_te):
    mu, std = X_tr.mean(0), X_tr.std(0) + 1e-8
    return (X_tr-mu)/std, (X_te-mu)/std

X_tr, X_te = normalize(X[tr], X[te])
X_tr, X_va = normalize(X[tr], X[va])

# Logistic regression with SGD
def sigmoid(z): return 1 / (1 + np.exp(-np.clip(z, -100, 100)))

w = np.zeros(D)
lr, n_epochs, bs = 0.1, 20, 32
for epoch in range(n_epochs):
    perm = rng.permutation(len(tr))
    for i in range(0, len(tr), bs):
        xi = X_tr[perm[i:i+bs]]
        yi = y[tr][perm[i:i+bs]]
        pred = sigmoid(xi @ w)
        grad = xi.T @ (pred - yi) / len(yi)
        w -= lr * grad

def accuracy(X, y_true, w):
    return ((sigmoid(X @ w) >= 0.5) == y_true.astype(bool)).mean()

print(f"Train acc: {accuracy(X_tr, y[tr], w):.3f}")
print(f"Val   acc: {accuracy(X_va, y[va], w):.3f}")
print(f"Test  acc: {accuracy(X_te, y[te], w):.3f}")""",
    pt="Cross-Validation",
    pd_text="Implement k_fold_cv(X, y, model_fn, k=5, seed=42) where model_fn(X_train, y_train, X_val) returns predictions. Split data into k folds, train on k-1 folds, predict on the held-out fold, compute accuracy for each fold, and return mean and std. Test with a simple threshold classifier.",
    ps=
"""import numpy as np

def k_fold_cv(X, y, model_fn, k=5, seed=42):
    rng  = np.random.default_rng(seed)
    idx  = rng.permutation(len(y))
    fold_size = len(y) // k
    scores = []
    for fold in range(k):
        val_idx   = idx[fold*fold_size:(fold+1)*fold_size]
        train_idx = np.concatenate([idx[:fold*fold_size], idx[(fold+1)*fold_size:]])
        X_tr, y_tr = X[train_idx], y[train_idx]
        X_va, y_va = X[val_idx],   y[val_idx]
        preds = model_fn(X_tr, y_tr, X_va)
        scores.append((preds == y_va).mean())
    return {"mean": np.mean(scores), "std": np.std(scores), "folds": scores}

# Threshold classifier: predict 1 if feature 0 > median
def threshold_model(X_tr, y_tr, X_va):
    threshold = np.median(X_tr[:, 0])
    return (X_va[:, 0] > threshold).astype(int)

rng = np.random.default_rng(42)
N, D = 500, 5
X = rng.standard_normal((N, D))
y = (X[:, 0] + 0.5 * X[:, 1] > 0).astype(int)

result = k_fold_cv(X, y, threshold_model, k=5)
print(f"5-fold CV: {result['mean']:.3f} ± {result['std']:.3f}")
print(f"Per-fold: {[round(s,3) for s in result['folds']]}")
"""
)

# ── Assemble and insert ──────────────────────────────────────────────────────
all_sections = s25 + s26 + s27 + s28 + s29 + s30 + s31 + s32
result = insert_sections(FILE, MARKER, all_sections)
if result:
    print("SUCCESS: numpy sections 25-32 added")
else:
    print("FAILED")
