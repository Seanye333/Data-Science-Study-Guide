import os, json, textwrap

OUT = r"c:\Users\seany\Documents\All Codes\Data Science Study Path\06_sklearn"
ACCENT = "#34d399"

SECTIONS = [
    {
        "title": "Setup & Data Loading",
        "desc": "Import scikit-learn, load built-in datasets, split data into train/test sets.",
        "code1_title": "Loading Datasets & Train/Test Split",
        "code1": (
            "from sklearn.datasets import load_iris, load_boston, make_classification\n"
            "from sklearn.model_selection import train_test_split\n"
            "import pandas as pd\n\n"
            "# Load Iris dataset\n"
            "iris = load_iris()\n"
            "X, y = iris.data, iris.target\n"
            "print('Features:', iris.feature_names)\n"
            "print('Classes:', iris.target_names)\n"
            "print('Shape:', X.shape)\n\n"
            "# Split 80/20\n"
            "X_train, X_test, y_train, y_test = train_test_split(\n"
            "    X, y, test_size=0.2, random_state=42, stratify=y\n"
            ")\n"
            "print(f'Train: {X_train.shape}, Test: {X_test.shape}')"
        ),
        "code2_title": "Synthetic Dataset with make_classification",
        "code2": (
            "from sklearn.datasets import make_classification, make_regression\n"
            "import numpy as np\n\n"
            "# Synthetic classification data\n"
            "X, y = make_classification(\n"
            "    n_samples=1000, n_features=10,\n"
            "    n_informative=5, n_redundant=2,\n"
            "    random_state=42\n"
            ")\n"
            "print('X shape:', X.shape, '| Classes:', np.unique(y))\n\n"
            "# Synthetic regression data\n"
            "X_r, y_r = make_regression(\n"
            "    n_samples=500, n_features=5, noise=0.1, random_state=42\n"
            ")\n"
            "print('Regression X:', X_r.shape, '| y range:', y_r.min().round(1), '-', y_r.max().round(1))"
        ),
        "rw_scenario": "Healthcare: Load patient vitals dataset, split into train/test while preserving class balance (stratify) for disease prediction.",
        "rw_code": (
            "import pandas as pd\n"
            "from sklearn.model_selection import train_test_split\n\n"
            "# Simulate patient vitals\n"
            "import numpy as np\n"
            "np.random.seed(42)\n"
            "df = pd.DataFrame({\n"
            "    'age': np.random.randint(20, 80, 200),\n"
            "    'bp': np.random.randint(60, 140, 200),\n"
            "    'cholesterol': np.random.randint(150, 300, 200),\n"
            "    'glucose': np.random.randint(70, 200, 200),\n"
            "    'disease': np.random.choice([0, 1], 200, p=[0.7, 0.3])\n"
            "})\n"
            "X = df.drop('disease', axis=1)\n"
            "y = df['disease']\n"
            "X_train, X_test, y_train, y_test = train_test_split(\n"
            "    X, y, test_size=0.2, stratify=y, random_state=42\n"
            ")\n"
            "print(f'Train positives: {y_train.mean():.1%} | Test positives: {y_test.mean():.1%}')"
        ),
        "code3_title": "Stratified K-Fold Cross-Validation",
        "code3": (
            "from sklearn.model_selection import StratifiedKFold, cross_val_score\n"
            "from sklearn.datasets import load_iris\n"
            "from sklearn.ensemble import RandomForestClassifier\n"
            "import numpy as np\n\n"
            "iris = load_iris()\n"
            "X, y = iris.data, iris.target\n\n"
            "skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)\n"
            "model = RandomForestClassifier(n_estimators=50, random_state=42)\n\n"
            "scores = cross_val_score(model, X, y, cv=skf, scoring='accuracy')\n"
            "print('Per-fold accuracy:', scores.round(4))\n"
            "print(f'Mean: {scores.mean():.4f}  Std: {scores.std():.4f}')\n\n"
            "# Check class balance per fold\n"
            "for fold, (train_idx, val_idx) in enumerate(skf.split(X, y)):\n"
            "    counts = np.bincount(y[val_idx])\n"
            "    print(f'Fold {fold+1} val class counts: {counts}')"
        ),
        "code4_title": "StratifiedShuffleSplit & make_regression for Continuous Targets",
        "code4": (
            "from sklearn.model_selection import StratifiedShuffleSplit\n"
            "from sklearn.datasets import make_classification, make_regression\n"
            "import numpy as np\n\n"
            "# StratifiedShuffleSplit: multiple random stratified splits\n"
            "X_c, y_c = make_classification(\n"
            "    n_samples=500, n_features=6, n_classes=3,\n"
            "    n_informative=4, random_state=42\n"
            ")\n"
            "sss = StratifiedShuffleSplit(n_splits=3, test_size=0.2, random_state=42)\n"
            "for fold, (train_idx, test_idx) in enumerate(sss.split(X_c, y_c)):\n"
            "    train_dist = np.bincount(y_c[train_idx]) / len(train_idx)\n"
            "    test_dist  = np.bincount(y_c[test_idx])  / len(test_idx)\n"
            "    print(f'Split {fold+1} train dist: {train_dist.round(3)} | test dist: {test_dist.round(3)}')\n\n"
            "# make_regression: multi-output continuous targets\n"
            "X_r, y_r = make_regression(\n"
            "    n_samples=400, n_features=8, n_informative=5,\n"
            "    n_targets=2, noise=5.0, random_state=42\n"
            ")\n"
            "print(f'Regression X: {X_r.shape} | y: {y_r.shape}')\n"
            "print(f'y col0 range: [{y_r[:,0].min():.1f}, {y_r[:,0].max():.1f}]')\n"
            "print(f'y col1 range: [{y_r[:,1].min():.1f}, {y_r[:,1].max():.1f}]')"
        ),
        "practice": {
            "title": "Stratified K-Fold CV Practice",
            "desc": "Using make_classification (1000 samples, 8 features, 3 classes), perform 10-fold stratified cross-validation with a LogisticRegression. Print each fold's accuracy, the mean, and std. Then compare to a simple train/test split — does CV give a more reliable estimate?",
            "starter": (
                "from sklearn.datasets import make_classification\n"
                "from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split\n"
                "from sklearn.linear_model import LogisticRegression\n"
                "import numpy as np\n\n"
                "X, y = make_classification(\n"
                "    n_samples=1000, n_features=8, n_classes=3,\n"
                "    n_informative=6, n_redundant=1, random_state=42\n"
                ")\n\n"
                "# TODO: Create StratifiedKFold with 10 splits, shuffle=True\n"
                "# skf = StratifiedKFold(???)\n\n"
                "# TODO: Run cross_val_score with LogisticRegression(max_iter=500)\n"
                "# scores = cross_val_score(???)\n"
                "# print('CV scores:', scores.round(4))\n"
                "# print(f'Mean: {scores.mean():.4f}  Std: {scores.std():.4f}')\n\n"
                "# TODO: Compare with a single train/test split\n"
                "# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n"
                "# model = LogisticRegression(max_iter=500)\n"
                "# model.fit(X_train, y_train)\n"
                "# print('Single split accuracy:', model.score(X_test, y_test).round(4))"
            ),
        },
    },
    {
        "title": "Linear & Logistic Regression",
        "desc": "LinearRegression for continuous targets; LogisticRegression for binary/multiclass classification.",
        "code1_title": "Linear Regression",
        "code1": (
            "from sklearn.linear_model import LinearRegression\n"
            "from sklearn.datasets import make_regression\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.metrics import mean_squared_error, r2_score\n"
            "import numpy as np\n\n"
            "X, y = make_regression(n_samples=200, n_features=3, noise=10, random_state=42)\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\n"
            "model = LinearRegression()\n"
            "model.fit(X_train, y_train)\n"
            "y_pred = model.predict(X_test)\n\n"
            "print('Coefficients:', model.coef_.round(2))\n"
            "print('Intercept:', round(model.intercept_, 2))\n"
            "print('R2 Score:', round(r2_score(y_test, y_pred), 4))\n"
            "print('RMSE:', round(np.sqrt(mean_squared_error(y_test, y_pred)), 2))"
        ),
        "code2_title": "Logistic Regression (Classification)",
        "code2": (
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.datasets import load_iris\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.metrics import accuracy_score, classification_report\n\n"
            "iris = load_iris()\n"
            "X_train, X_test, y_train, y_test = train_test_split(\n"
            "    iris.data, iris.target, test_size=0.2, random_state=42, stratify=iris.target\n"
            ")\n\n"
            "lr = LogisticRegression(max_iter=200)\n"
            "lr.fit(X_train, y_train)\n"
            "y_pred = lr.predict(X_test)\n\n"
            "print('Accuracy:', accuracy_score(y_test, y_pred))\n"
            "print(classification_report(y_test, y_pred, target_names=iris.target_names))"
        ),
        "rw_scenario": "Finance: Predict house prices (Linear Regression) and loan default probability (Logistic Regression).",
        "rw_code": (
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.metrics import classification_report\n"
            "from sklearn.model_selection import train_test_split\n"
            "import numpy as np\n\n"
            "# Simulate loan applicant data\n"
            "np.random.seed(42)\n"
            "n = 500\n"
            "income = np.random.normal(50000, 15000, n)\n"
            "debt = np.random.normal(20000, 8000, n)\n"
            "credit_score = np.random.randint(300, 850, n)\n"
            "X = np.column_stack([income, debt, credit_score])\n"
            "# Default if debt/income > 0.6 or credit < 550\n"
            "y = ((debt / income > 0.6) | (credit_score < 550)).astype(int)\n\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n"
            "model = LogisticRegression()\n"
            "model.fit(X_train, y_train)\n"
            "print('Loan Default Prediction:')\n"
            "print(classification_report(y_test, model.predict(X_test)))"
        ),
        "code3_title": "Ridge & Lasso Regularization",
        "code3": (
            "from sklearn.linear_model import Ridge, Lasso, LinearRegression\n"
            "from sklearn.datasets import make_regression\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.metrics import r2_score\n"
            "import numpy as np\n\n"
            "X, y = make_regression(n_samples=200, n_features=20, noise=15, random_state=42)\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\n"
            "models = [\n"
            "    ('LinearRegression', LinearRegression()),\n"
            "    ('Ridge(alpha=1)', Ridge(alpha=1.0)),\n"
            "    ('Ridge(alpha=10)', Ridge(alpha=10.0)),\n"
            "    ('Lasso(alpha=1)', Lasso(alpha=1.0)),\n"
            "]\n"
            "for name, model in models:\n"
            "    model.fit(X_train, y_train)\n"
            "    r2 = r2_score(y_test, model.predict(X_test))\n"
            "    n_zero = np.sum(np.abs(model.coef_) < 1e-4)\n"
            "    print(f'{name:25s} R2={r2:.4f}  zero_coefs={n_zero}')"
        ),
        "code4_title": "Alpha Tuning & ElasticNet",
        "code4": (
            "from sklearn.linear_model import Ridge, Lasso, ElasticNet\n"
            "from sklearn.datasets import make_regression\n"
            "from sklearn.model_selection import cross_val_score\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "from sklearn.pipeline import Pipeline\n"
            "import numpy as np\n\n"
            "X, y = make_regression(n_samples=300, n_features=15, n_informative=5,\n"
            "                       noise=20, random_state=42)\n\n"
            "# Alpha sweep for Ridge and Lasso\n"
            "alphas = [0.01, 0.1, 1, 10, 100]\n"
            "print(f'{'Alpha':>8} | {'Ridge R2':>10} | {'Lasso R2':>10}')\n"
            "print('-' * 35)\n"
            "for a in alphas:\n"
            "    r_pipe = Pipeline([('sc', StandardScaler()), ('m', Ridge(alpha=a))])\n"
            "    l_pipe = Pipeline([('sc', StandardScaler()), ('m', Lasso(alpha=a, max_iter=5000))])\n"
            "    r2_r = cross_val_score(r_pipe, X, y, cv=5, scoring='r2').mean()\n"
            "    r2_l = cross_val_score(l_pipe, X, y, cv=5, scoring='r2').mean()\n"
            "    print(f'{a:>8.2f} | {r2_r:>10.4f} | {r2_l:>10.4f}')\n\n"
            "# ElasticNet: blends L1 + L2\n"
            "for l1r in [0.1, 0.5, 0.9]:\n"
            "    en = Pipeline([('sc', StandardScaler()),\n"
            "                   ('m', ElasticNet(alpha=1.0, l1_ratio=l1r, max_iter=5000))])\n"
            "    r2 = cross_val_score(en, X, y, cv=5, scoring='r2').mean()\n"
            "    print(f'ElasticNet l1_ratio={l1r:.1f}  CV R2={r2:.4f}')"
        ),
        "practice": {
            "title": "Feature Selection via Coefficients",
            "desc": "Generate regression data with 15 features (only 5 informative). Train LinearRegression and Lasso(alpha=0.5). Compare: which features does Lasso zero out? Print feature coefficients sorted by absolute value for both models. Verify Lasso selects approximately the 5 informative features.",
            "starter": (
                "from sklearn.linear_model import LinearRegression, Lasso\n"
                "from sklearn.datasets import make_regression\n"
                "from sklearn.model_selection import train_test_split\n"
                "from sklearn.metrics import r2_score\n"
                "import numpy as np\n\n"
                "X, y, true_coef = make_regression(\n"
                "    n_samples=300, n_features=15, n_informative=5,\n"
                "    noise=10, coef=True, random_state=42\n"
                ")\n"
                "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\n"
                "# TODO: Train LinearRegression and compute R2\n"
                "# lr = LinearRegression()\n"
                "# lr.fit(X_train, y_train)\n"
                "# print('LinearRegression R2:', r2_score(y_test, lr.predict(X_test)).round(4))\n\n"
                "# TODO: Train Lasso(alpha=0.5) and compute R2\n"
                "# lasso = Lasso(alpha=0.5)\n"
                "# lasso.fit(X_train, y_train)\n"
                "# print('Lasso R2:', r2_score(y_test, lasso.predict(X_test)).round(4))\n\n"
                "# TODO: Count zero coefficients in Lasso\n"
                "# n_zero = np.sum(np.abs(lasso.coef_) < 1e-4)\n"
                "# print(f'Lasso zero coefs: {n_zero} / 15 (expect ~10)')\n\n"
                "# TODO: Print top-5 features by |coef| for both models\n"
                "# for name, coef in [('LR', lr.coef_), ('Lasso', lasso.coef_)]:\n"
                "#     top5 = np.argsort(np.abs(coef))[::-1][:5]\n"
                "#     print(f'{name} top features: {top5}')"
            ),
        },
    },
    {
        "title": "Decision Trees & Random Forest",
        "desc": "Tree-based models: interpretable Decision Trees and powerful ensemble Random Forests.",
        "code1_title": "Decision Tree Classifier",
        "code1": (
            "from sklearn.tree import DecisionTreeClassifier, export_text\n"
            "from sklearn.datasets import load_iris\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.metrics import accuracy_score\n\n"
            "iris = load_iris()\n"
            "X_train, X_test, y_train, y_test = train_test_split(\n"
            "    iris.data, iris.target, test_size=0.2, random_state=42\n"
            ")\n\n"
            "dt = DecisionTreeClassifier(max_depth=3, random_state=42)\n"
            "dt.fit(X_train, y_train)\n"
            "print('Accuracy:', accuracy_score(y_test, dt.predict(X_test)))\n"
            "print('Feature importances:')\n"
            "for name, imp in zip(iris.feature_names, dt.feature_importances_):\n"
            "    print(f'  {name}: {imp:.3f}')\n"
            "print(export_text(dt, feature_names=iris.feature_names))"
        ),
        "code2_title": "Random Forest & Feature Importance",
        "code2": (
            "from sklearn.ensemble import RandomForestClassifier\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.metrics import accuracy_score\n"
            "import numpy as np\n\n"
            "X, y = make_classification(n_samples=1000, n_features=10, random_state=42)\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\n"
            "rf = RandomForestClassifier(n_estimators=100, random_state=42)\n"
            "rf.fit(X_train, y_train)\n"
            "print('RF Accuracy:', accuracy_score(y_test, rf.predict(X_test)))\n\n"
            "# Top 5 features\n"
            "idx = np.argsort(rf.feature_importances_)[::-1][:5]\n"
            "for i in idx:\n"
            "    print(f'  Feature {i}: {rf.feature_importances_[i]:.4f}')"
        ),
        "rw_scenario": "Retail: Predict customer churn using Random Forest — who is likely to stop buying?",
        "rw_code": (
            "from sklearn.ensemble import RandomForestClassifier\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.metrics import classification_report\n"
            "import numpy as np, pandas as pd\n\n"
            "np.random.seed(42)\n"
            "n = 1000\n"
            "df = pd.DataFrame({\n"
            "    'recency_days': np.random.randint(1, 365, n),\n"
            "    'frequency': np.random.randint(1, 50, n),\n"
            "    'monetary': np.random.exponential(200, n),\n"
            "    'tenure_months': np.random.randint(1, 60, n),\n"
            "    'support_calls': np.random.poisson(2, n)\n"
            "})\n"
            "# Churn if high recency, low frequency\n"
            "df['churn'] = ((df['recency_days'] > 200) & (df['frequency'] < 5)).astype(int)\n\n"
            "X = df.drop('churn', axis=1)\n"
            "y = df['churn']\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n"
            "rf = RandomForestClassifier(n_estimators=100, random_state=42)\n"
            "rf.fit(X_train, y_train)\n"
            "print('Customer Churn Prediction:')\n"
            "print(classification_report(y_test, rf.predict(X_test)))"
        ),
        "code3_title": "Gradient Boosting Classifier",
        "code3": (
            "from sklearn.ensemble import GradientBoostingClassifier\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.metrics import accuracy_score\n"
            "import numpy as np\n\n"
            "X, y = make_classification(n_samples=1000, n_features=10, random_state=42)\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\n"
            "gb = GradientBoostingClassifier(\n"
            "    n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42\n"
            ")\n"
            "gb.fit(X_train, y_train)\n"
            "print('GBM Accuracy:', accuracy_score(y_test, gb.predict(X_test)).round(4))\n\n"
            "# Feature importances — top 5\n"
            "idx = np.argsort(gb.feature_importances_)[::-1][:5]\n"
            "print('Top 5 features by importance:')\n"
            "for rank, i in enumerate(idx, 1):\n"
            "    print(f'  {rank}. Feature {i}: {gb.feature_importances_[i]:.4f}')"
        ),
        "code4_title": "ExtraTreesClassifier & Feature Importance Bar Chart (Text)",
        "code4": (
            "from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier\n"
            "from sklearn.datasets import load_iris\n"
            "from sklearn.model_selection import train_test_split, cross_val_score\n"
            "from sklearn.metrics import accuracy_score\n"
            "import numpy as np\n\n"
            "iris = load_iris()\n"
            "X, y = iris.data, iris.target\n"
            "feat_names = iris.feature_names\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\n"
            "# ExtraTrees vs RandomForest comparison\n"
            "for name, clf in [('RandomForest ', RandomForestClassifier(n_estimators=100, random_state=42)),\n"
            "                   ('ExtraTrees   ', ExtraTreesClassifier(n_estimators=100, random_state=42))]:\n"
            "    clf.fit(X_train, y_train)\n"
            "    cv = cross_val_score(clf, X, y, cv=5).mean()\n"
            "    print(f'{name} test={accuracy_score(y_test, clf.predict(X_test)):.4f}  CV={cv:.4f}')\n\n"
            "# Text-based feature importance bar chart\n"
            "et = ExtraTreesClassifier(n_estimators=100, random_state=42).fit(X_train, y_train)\n"
            "imps = et.feature_importances_\n"
            "print('\\nFeature Importance Bar Chart:')\n"
            "max_imp = imps.max()\n"
            "bar_width = 30\n"
            "for name, imp in sorted(zip(feat_names, imps), key=lambda x: -x[1]):\n"
            "    bar = int(imp / max_imp * bar_width) * '#'\n"
            "    print(f'  {name:28s} |{bar:<30}| {imp:.4f}')"
        ),
        "practice": {
            "title": "Tree Depth vs Accuracy",
            "desc": "Using load_iris, train DecisionTreeClassifier with max_depth from 1 to 10. For each depth, record training accuracy and 5-fold CV accuracy. Print results as a table and identify the depth that minimises overfitting (smallest gap between train and CV). Which depth generalises best?",
            "starter": (
                "from sklearn.tree import DecisionTreeClassifier\n"
                "from sklearn.datasets import load_iris\n"
                "from sklearn.model_selection import cross_val_score\n"
                "import numpy as np\n\n"
                "iris = load_iris()\n"
                "X, y = iris.data, iris.target\n\n"
                "print(f'{'Depth':>6} | {'Train Acc':>10} | {'CV Acc':>10} | {'Gap':>8}')\n"
                "print('-' * 44)\n\n"
                "best_depth, best_cv = 1, 0.0\n"
                "for depth in range(1, 11):\n"
                "    # TODO: dt = DecisionTreeClassifier(max_depth=depth, random_state=42)\n"
                "    # TODO: dt.fit(X, y)\n"
                "    # TODO: train_acc = dt.score(X, y)\n"
                "    # TODO: cv_acc = cross_val_score(dt, X, y, cv=5).mean()\n"
                "    # TODO: gap = train_acc - cv_acc\n"
                "    # TODO: print(f'{depth:>6} | {train_acc:>10.4f} | {cv_acc:>10.4f} | {gap:>8.4f}')\n"
                "    # TODO: if cv_acc > best_cv: best_depth, best_cv = depth, cv_acc\n"
                "    pass\n\n"
                "# TODO: print(f'Best depth: {best_depth} with CV accuracy {best_cv:.4f}')"
            ),
        },
    },
    {
        "title": "Support Vector Machines",
        "desc": "SVM finds the maximum-margin hyperplane. Works for classification (SVC) and regression (SVR).",
        "code1_title": "SVC with Kernel Trick",
        "code1": (
            "from sklearn.svm import SVC\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "from sklearn.metrics import accuracy_score\n\n"
            "X, y = make_classification(n_samples=500, n_features=5, random_state=42)\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\n"
            "# SVM needs scaled features\n"
            "scaler = StandardScaler()\n"
            "X_train_s = scaler.fit_transform(X_train)\n"
            "X_test_s = scaler.transform(X_test)\n\n"
            "for kernel in ['linear', 'rbf', 'poly']:\n"
            "    svm = SVC(kernel=kernel, C=1.0)\n"
            "    svm.fit(X_train_s, y_train)\n"
            "    acc = accuracy_score(y_test, svm.predict(X_test_s))\n"
            "    print(f'{kernel:8s} kernel accuracy: {acc:.4f}')"
        ),
        "code2_title": "SVR for Regression",
        "code2": (
            "from sklearn.svm import SVR\n"
            "from sklearn.datasets import make_regression\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.metrics import r2_score\n\n"
            "X, y = make_regression(n_samples=300, n_features=3, noise=15, random_state=42)\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\n"
            "scaler = StandardScaler()\n"
            "X_train_s = scaler.fit_transform(X_train)\n"
            "X_test_s = scaler.transform(X_test)\n\n"
            "for kernel in ['linear', 'rbf']:\n"
            "    svr = SVR(kernel=kernel, C=10)\n"
            "    svr.fit(X_train_s, y_train)\n"
            "    r2 = r2_score(y_test, svr.predict(X_test_s))\n"
            "    print(f'SVR ({kernel}) R2: {r2:.4f}')"
        ),
        "rw_scenario": "NLP: SVM for text sentiment classification — positive vs negative product reviews.",
        "rw_code": (
            "from sklearn.svm import SVC\n"
            "from sklearn.feature_extraction.text import TfidfVectorizer\n"
            "from sklearn.pipeline import Pipeline\n"
            "from sklearn.metrics import accuracy_score\n\n"
            "# Simulated reviews\n"
            "reviews = [\n"
            "    'great product love it', 'terrible waste of money',\n"
            "    'amazing quality highly recommend', 'broken arrived damaged',\n"
            "    'best purchase ever', 'awful customer service never again',\n"
            "    'works perfectly fast shipping', 'poor quality disappointed',\n"
            "]\n"
            "labels = [1, 0, 1, 0, 1, 0, 1, 0]  # 1=positive, 0=negative\n\n"
            "pipe = Pipeline([\n"
            "    ('tfidf', TfidfVectorizer()),\n"
            "    ('svm', SVC(kernel='linear', C=1.0))\n"
            "])\n"
            "pipe.fit(reviews[:6], labels[:6])\n"
            "preds = pipe.predict(reviews[6:])\n"
            "print('Predictions:', ['Positive' if p else 'Negative' for p in preds])\n"
            "print('True labels:', ['Positive' if l else 'Negative' for l in labels[6:]])"
        ),
        "code3_title": "SVM with C-Parameter Tuning",
        "code3": (
            "from sklearn.svm import SVC\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.model_selection import train_test_split, cross_val_score\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "import numpy as np\n\n"
            "X, y = make_classification(n_samples=500, n_features=5, random_state=42)\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\n"
            "scaler = StandardScaler()\n"
            "X_train_s = scaler.fit_transform(X_train)\n"
            "X_test_s  = scaler.transform(X_test)\n\n"
            "print('C value | CV Accuracy')\n"
            "print('-' * 25)\n"
            "for C in [0.01, 0.1, 1, 10, 100]:\n"
            "    svm = SVC(kernel='rbf', C=C)\n"
            "    cv_scores = cross_val_score(svm, X_train_s, y_train, cv=5)\n"
            "    print(f'C={C:6.2f}  | {cv_scores.mean():.4f} +/- {cv_scores.std():.4f}')"
        ),
        "code4_title": "NuSVC & SVM with class_weight='balanced'",
        "code4": (
            "from sklearn.svm import NuSVC, SVC\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "from sklearn.metrics import classification_report, f1_score\n"
            "import numpy as np\n\n"
            "# Imbalanced binary classification\n"
            "X, y = make_classification(\n"
            "    n_samples=600, n_features=6, weights=[0.85, 0.15], random_state=42\n"
            ")\n"
            "X_train, X_test, y_train, y_test = train_test_split(\n"
            "    X, y, test_size=0.2, stratify=y, random_state=42\n"
            ")\n"
            "scaler = StandardScaler()\n"
            "X_tr = scaler.fit_transform(X_train)\n"
            "X_te = scaler.transform(X_test)\n\n"
            "# NuSVC: nu controls upper bound on training errors\n"
            "print('NuSVC nu sweep:')\n"
            "for nu in [0.1, 0.3, 0.5]:\n"
            "    try:\n"
            "        m = NuSVC(nu=nu, kernel='rbf').fit(X_tr, y_train)\n"
            "        f1 = f1_score(y_test, m.predict(X_te))\n"
            "        print(f'  nu={nu}  F1={f1:.4f}')\n"
            "    except Exception as e:\n"
            "        print(f'  nu={nu}  infeasible: {e}')\n\n"
            "# SVC with class_weight='balanced' handles imbalance\n"
            "print('\\nSVC class_weight comparison:')\n"
            "for cw in [None, 'balanced']:\n"
            "    svc = SVC(kernel='rbf', C=10, class_weight=cw).fit(X_tr, y_train)\n"
            "    f1 = f1_score(y_test, svc.predict(X_te))\n"
            "    print(f'  class_weight={str(cw):10s}  F1={f1:.4f}')\n"
            "print(classification_report(y_test, svc.predict(X_te)))"
        ),
        "practice": {
            "title": "SVM Kernel Comparison",
            "desc": "Use make_classification (500 samples, 6 features). Scale features with StandardScaler. Train SVC with linear, rbf, poly, and sigmoid kernels, each with C=1.0. For each: record 5-fold CV accuracy. Print a summary table. Which kernel wins? Now try rbf with C values [0.1, 1, 10, 100] and find the best C.",
            "starter": (
                "from sklearn.svm import SVC\n"
                "from sklearn.datasets import make_classification\n"
                "from sklearn.model_selection import cross_val_score\n"
                "from sklearn.preprocessing import StandardScaler\n"
                "import numpy as np\n\n"
                "X, y = make_classification(n_samples=500, n_features=6, random_state=0)\n"
                "# TODO: Scale X with StandardScaler\n"
                "# scaler = StandardScaler()\n"
                "# X_s = scaler.fit_transform(X)\n\n"
                "# TODO: Compare kernels\n"
                "kernels = ['linear', 'rbf', 'poly', 'sigmoid']\n"
                "print('Kernel   | CV Accuracy')\n"
                "print('-' * 28)\n"
                "for kernel in kernels:\n"
                "    # TODO: svm = SVC(kernel=kernel, C=1.0)\n"
                "    # TODO: scores = cross_val_score(svm, X_s, y, cv=5)\n"
                "    # TODO: print(f'{kernel:8s} | {scores.mean():.4f} +/- {scores.std():.4f}')\n"
                "    pass\n\n"
                "# TODO: Tune C for rbf kernel\n"
                "print('\\nRBF kernel C tuning:')\n"
                "for C in [0.1, 1, 10, 100]:\n"
                "    # TODO: svm = SVC(kernel='rbf', C=C)\n"
                "    # TODO: scores = cross_val_score(svm, X_s, y, cv=5)\n"
                "    # TODO: print(f'C={C:6.1f} | {scores.mean():.4f}')\n"
                "    pass"
            ),
        },
    },
    {
        "title": "K-Nearest Neighbors & Naive Bayes",
        "desc": "KNN classifies by majority vote of k neighbors. Naive Bayes uses Bayes' theorem with feature independence assumption.",
        "code1_title": "K-Nearest Neighbors",
        "code1": (
            "from sklearn.neighbors import KNeighborsClassifier\n"
            "from sklearn.datasets import load_iris\n"
            "from sklearn.model_selection import train_test_split, cross_val_score\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "import numpy as np\n\n"
            "iris = load_iris()\n"
            "X_train, X_test, y_train, y_test = train_test_split(\n"
            "    iris.data, iris.target, test_size=0.2, random_state=42\n"
            ")\n\n"
            "scaler = StandardScaler()\n"
            "X_train_s = scaler.fit_transform(X_train)\n"
            "X_test_s = scaler.transform(X_test)\n\n"
            "# Find best k\n"
            "for k in [1, 3, 5, 7, 11]:\n"
            "    knn = KNeighborsClassifier(n_neighbors=k)\n"
            "    scores = cross_val_score(knn, X_train_s, y_train, cv=5)\n"
            "    print(f'k={k:2d}: CV accuracy = {scores.mean():.4f} (+/- {scores.std():.4f})')"
        ),
        "code2_title": "Naive Bayes for Text Classification",
        "code2": (
            "from sklearn.naive_bayes import MultinomialNB, GaussianNB\n"
            "from sklearn.feature_extraction.text import CountVectorizer\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.metrics import accuracy_score\n\n"
            "# Email spam detection\n"
            "emails = [\n"
            "    'win money now free prize', 'meeting tomorrow at 10am',\n"
            "    'congratulations you won cash', 'project update attached',\n"
            "    'free viagra cheap pills', 'please review the report',\n"
            "    'claim your reward today', 'lunch at noon works for me',\n"
            "]\n"
            "labels = [1, 0, 1, 0, 1, 0, 1, 0]  # 1=spam\n\n"
            "vec = CountVectorizer()\n"
            "X = vec.fit_transform(emails)\n"
            "nb = MultinomialNB()\n"
            "nb.fit(X, labels)\n"
            "test = vec.transform(['free money win now', 'schedule a meeting'])\n"
            "preds = nb.predict(test)\n"
            "print('Predictions:', ['SPAM' if p else 'HAM' for p in preds])"
        ),
        "rw_scenario": "E-commerce: Recommend similar products using KNN — find the 5 most similar items based on features.",
        "rw_code": (
            "from sklearn.neighbors import NearestNeighbors\n"
            "import numpy as np, pandas as pd\n\n"
            "# Product feature vectors (price, rating, sales, weight)\n"
            "np.random.seed(42)\n"
            "products = pd.DataFrame({\n"
            "    'name': [f'Product_{i}' for i in range(20)],\n"
            "    'price': np.random.uniform(10, 200, 20),\n"
            "    'rating': np.random.uniform(1, 5, 20),\n"
            "    'sales': np.random.randint(100, 10000, 20),\n"
            "    'weight_kg': np.random.uniform(0.1, 5, 20)\n"
            "})\n\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "X = StandardScaler().fit_transform(products[['price','rating','sales','weight_kg']])\n\n"
            "nn = NearestNeighbors(n_neighbors=4, metric='euclidean')\n"
            "nn.fit(X)\n"
            "# Find similar products to Product_0\n"
            "distances, indices = nn.kneighbors([X[0]])\n"
            "print('Products similar to', products.iloc[0]['name'])\n"
            "for i, d in zip(indices[0][1:], distances[0][1:]):\n"
            "    print(f'  {products.iloc[i][\"name\"]} (dist={d:.2f})')"
        ),
        "code3_title": "GaussianNB with Prior Probability",
        "code3": (
            "from sklearn.naive_bayes import GaussianNB\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.metrics import accuracy_score, classification_report\n"
            "import numpy as np\n\n"
            "# Imbalanced dataset (80% class 0, 20% class 1)\n"
            "X, y = make_classification(\n"
            "    n_samples=1000, n_features=6, weights=[0.8, 0.2], random_state=42\n"
            ")\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\n"
            "# Default priors (learned from training data)\n"
            "gnb_default = GaussianNB()\n"
            "gnb_default.fit(X_train, y_train)\n\n"
            "# Custom priors (force equal class probability)\n"
            "gnb_equal = GaussianNB(priors=[0.5, 0.5])\n"
            "gnb_equal.fit(X_train, y_train)\n\n"
            "for name, m in [('Default priors', gnb_default), ('Equal priors', gnb_equal)]:\n"
            "    acc = accuracy_score(y_test, m.predict(X_test))\n"
            "    print(f'{name}: accuracy={acc:.4f}')\n"
            "print('Class priors (default):', gnb_default.class_prior_.round(3))"
        ),
        "code4_title": "RadiusNeighborsClassifier & GaussianNB Calibration",
        "code4": (
            "from sklearn.neighbors import RadiusNeighborsClassifier\n"
            "from sklearn.naive_bayes import GaussianNB\n"
            "from sklearn.calibration import CalibratedClassifierCV\n"
            "from sklearn.datasets import load_iris\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "from sklearn.metrics import accuracy_score, log_loss\n"
            "import numpy as np\n\n"
            "iris = load_iris()\n"
            "X_train, X_test, y_train, y_test = train_test_split(\n"
            "    iris.data, iris.target, test_size=0.2, stratify=iris.target, random_state=42\n"
            ")\n"
            "scaler = StandardScaler()\n"
            "X_tr = scaler.fit_transform(X_train)\n"
            "X_te = scaler.transform(X_test)\n\n"
            "# RadiusNeighborsClassifier: classify within a fixed radius\n"
            "print('RadiusNeighborsClassifier radius sweep:')\n"
            "for r in [0.5, 1.0, 1.5, 2.0]:\n"
            "    rnc = RadiusNeighborsClassifier(radius=r, outlier_label='most_frequent')\n"
            "    rnc.fit(X_tr, y_train)\n"
            "    acc = accuracy_score(y_test, rnc.predict(X_te))\n"
            "    print(f'  radius={r:.1f}  accuracy={acc:.4f}')\n\n"
            "# GaussianNB calibration: improve probability estimates\n"
            "gnb_raw  = GaussianNB()\n"
            "gnb_cal  = CalibratedClassifierCV(GaussianNB(), method='isotonic', cv=5)\n"
            "gnb_raw.fit(X_tr, y_train)\n"
            "gnb_cal.fit(X_tr, y_train)\n"
            "for name, m in [('GaussianNB (raw) ', gnb_raw), ('GaussianNB (cal) ', gnb_cal)]:\n"
            "    proba = m.predict_proba(X_te)\n"
            "    ll = log_loss(y_test, proba)\n"
            "    acc = accuracy_score(y_test, m.predict(X_te))\n"
            "    print(f'{name}  accuracy={acc:.4f}  log_loss={ll:.4f}')"
        ),
        "practice": {
            "title": "KNN: Distance Metric Comparison",
            "desc": "Using load_iris (scaled with StandardScaler), compare KNeighborsClassifier with k=5 using euclidean, manhattan, and chebyshev distance metrics. Use 5-fold CV for each. Print accuracy for each metric. Then find the best k (1-15) for the winning metric using CV. Report the optimal k.",
            "starter": (
                "from sklearn.neighbors import KNeighborsClassifier\n"
                "from sklearn.datasets import load_iris\n"
                "from sklearn.model_selection import cross_val_score\n"
                "from sklearn.preprocessing import StandardScaler\n"
                "import numpy as np\n\n"
                "iris = load_iris()\n"
                "# TODO: Scale features\n"
                "# scaler = StandardScaler()\n"
                "# X_s = scaler.fit_transform(iris.data)\n"
                "y = iris.target\n\n"
                "# TODO: Compare distance metrics at k=5\n"
                "metrics = ['euclidean', 'manhattan', 'chebyshev']\n"
                "print('Metric      | CV Accuracy')\n"
                "print('-' * 30)\n"
                "best_metric, best_score = '', 0.0\n"
                "for metric in metrics:\n"
                "    # TODO: knn = KNeighborsClassifier(n_neighbors=5, metric=metric)\n"
                "    # TODO: scores = cross_val_score(knn, X_s, y, cv=5)\n"
                "    # TODO: print(f'{metric:11s} | {scores.mean():.4f}')\n"
                "    # TODO: if scores.mean() > best_score: best_metric, best_score = metric, scores.mean()\n"
                "    pass\n\n"
                "# TODO: Find best k for the winning metric\n"
                "# print(f'\\nTuning k for best metric: {best_metric}')\n"
                "# for k in range(1, 16):\n"
                "#     knn = KNeighborsClassifier(n_neighbors=k, metric=best_metric)\n"
                "#     s = cross_val_score(knn, X_s, y, cv=5).mean()\n"
                "#     print(f'  k={k:2d}: {s:.4f}')"
            ),
        },
    },
    {
        "title": "Clustering: KMeans & DBSCAN",
        "desc": "Unsupervised learning: group similar data points without labels.",
        "code1_title": "KMeans Clustering",
        "code1": (
            "from sklearn.cluster import KMeans\n"
            "from sklearn.datasets import make_blobs\n"
            "from sklearn.metrics import silhouette_score\n"
            "import numpy as np\n\n"
            "X, _ = make_blobs(n_samples=300, centers=4, random_state=42)\n\n"
            "# Elbow method to find optimal k\n"
            "inertias = []\n"
            "for k in range(2, 9):\n"
            "    km = KMeans(n_clusters=k, random_state=42, n_init=10)\n"
            "    km.fit(X)\n"
            "    inertias.append(km.inertia_)\n"
            "    sil = silhouette_score(X, km.labels_)\n"
            "    print(f'k={k}: inertia={km.inertia_:.1f}, silhouette={sil:.3f}')\n\n"
            "# Best k=4\n"
            "best = KMeans(n_clusters=4, random_state=42, n_init=10)\n"
            "best.fit(X)\n"
            "print('Cluster sizes:', {i: (best.labels_==i).sum() for i in range(4)})"
        ),
        "code2_title": "DBSCAN for Density-Based Clustering",
        "code2": (
            "from sklearn.cluster import DBSCAN\n"
            "from sklearn.datasets import make_moons\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "import numpy as np\n\n"
            "# make_moons: non-convex shapes KMeans can't handle\n"
            "X, _ = make_moons(n_samples=200, noise=0.1, random_state=42)\n"
            "X = StandardScaler().fit_transform(X)\n\n"
            "db = DBSCAN(eps=0.3, min_samples=5)\n"
            "db.fit(X)\n\n"
            "labels = db.labels_\n"
            "n_clusters = len(set(labels)) - (1 if -1 in labels else 0)\n"
            "n_noise = (labels == -1).sum()\n"
            "print(f'Clusters found: {n_clusters}')\n"
            "print(f'Noise points: {n_noise}')\n"
            "print(f'Cluster sizes: {[(labels==i).sum() for i in range(n_clusters)]}')"
        ),
                "code4_title": "AgglomerativeClustering & Silhouette Score Comparison",
        "code4": (
            "from sklearn.cluster import AgglomerativeClustering, KMeans\n"
            "from sklearn.metrics import silhouette_score\n"
            "from sklearn.datasets import make_blobs\n"
            "import numpy as np\n"
            "\n"
            "X, _ = make_blobs(n_samples=300, centers=4, cluster_std=0.8, random_state=42)\n"
            "\n"
            "# Compare silhouette scores for k = 2..6\n"
            "print('KMeans silhouette scores:')\n"
            "for k in range(2, 7):\n"
            "    labels = KMeans(n_clusters=k, random_state=42, n_init=10).fit_predict(X)\n"
            "    score  = silhouette_score(X, labels)\n"
            "    print(f'  k={k}: {score:.4f}')\n"
            "\n"
            "# AgglomerativeClustering with different linkages\n"
            "print('\\nAgglomerative linkage comparison (k=4):')\n"
            "for linkage in ['ward', 'complete', 'average', 'single']:\n"
            "    agg    = AgglomerativeClustering(n_clusters=4, linkage=linkage)\n"
            "    labels = agg.fit_predict(X)\n"
            "    score  = silhouette_score(X, labels)\n"
            "    print(f'  {linkage:8s}: {score:.4f}')"
        ),
        "rw_scenario": "Marketing: Segment customers into groups (KMeans) based on RFM (Recency, Frequency, Monetary) for targeted campaigns.",
        "rw_code": (
            "from sklearn.cluster import KMeans\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "import numpy as np, pandas as pd\n\n"
            "np.random.seed(42)\n"
            "n = 500\n"
            "df = pd.DataFrame({\n"
            "    'recency': np.random.randint(1, 365, n),\n"
            "    'frequency': np.random.randint(1, 100, n),\n"
            "    'monetary': np.random.exponential(300, n)\n"
            "})\n\n"
            "X = StandardScaler().fit_transform(df)\n"
            "km = KMeans(n_clusters=4, random_state=42, n_init=10)\n"
            "df['segment'] = km.fit_predict(X)\n\n"
            "segment_names = {0: 'Champions', 1: 'At Risk', 2: 'New Customers', 3: 'Lost'}\n"
            "summary = df.groupby('segment').agg({'recency':'mean','frequency':'mean','monetary':'mean','segment':'count'})\n"
            "summary.columns = ['Avg Recency', 'Avg Frequency', 'Avg Monetary', 'Count']\n"
            "print('Customer Segments:')\n"
            "print(summary.round(1))"
        ),
        "code3_title": "Agglomerative Hierarchical Clustering",
        "code3": (
            "from sklearn.cluster import AgglomerativeClustering\n"
            "from sklearn.datasets import make_blobs\n"
            "from sklearn.metrics import silhouette_score\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "import numpy as np\n\n"
            "X, _ = make_blobs(n_samples=200, centers=3, random_state=42)\n"
            "X = StandardScaler().fit_transform(X)\n\n"
            "for linkage in ['ward', 'complete', 'average', 'single']:\n"
            "    agg = AgglomerativeClustering(n_clusters=3, linkage=linkage)\n"
            "    labels = agg.fit_predict(X)\n"
            "    sil = silhouette_score(X, labels)\n"
            "    print(f'Linkage={linkage:8s}  silhouette={sil:.4f}')"
        ),
        "practice": {
            "title": "Elbow Method for Optimal K",
            "desc": "Generate blobs with 5 centers (make_blobs, 400 samples). Run KMeans for k=2 to 10. For each k, record inertia and silhouette score. Print a table. Identify the elbow point visually from the inertia values — at which k does the decrease in inertia slow down? Confirm with silhouette score.",
            "starter": (
                "from sklearn.cluster import KMeans\n"
                "from sklearn.datasets import make_blobs\n"
                "from sklearn.metrics import silhouette_score\n"
                "from sklearn.preprocessing import StandardScaler\n"
                "import numpy as np\n\n"
                "X, true_labels = make_blobs(n_samples=400, centers=5, random_state=42)\n"
                "X = StandardScaler().fit_transform(X)\n\n"
                "print(f'{'k':>3} | {'Inertia':>12} | {'Silhouette':>12}')\n"
                "print('-' * 35)\n\n"
                "inertias = []\n"
                "sil_scores = []\n"
                "for k in range(2, 11):\n"
                "    # TODO: km = KMeans(n_clusters=k, random_state=42, n_init=10)\n"
                "    # TODO: km.fit(X)\n"
                "    # TODO: inertias.append(km.inertia_)\n"
                "    # TODO: sil = silhouette_score(X, km.labels_)\n"
                "    # TODO: sil_scores.append(sil)\n"
                "    # TODO: print(f'{k:>3} | {km.inertia_:>12.2f} | {sil:>12.4f}')\n"
                "    pass\n\n"
                "# TODO: best_k = range(2, 11)[np.argmax(sil_scores)]\n"
                "# print(f'Best k by silhouette: {best_k}')"
            ),
        },
    },
    {
        "title": "Model Evaluation & Metrics",
        "desc": "Measure model performance: confusion matrix, ROC-AUC, precision-recall, cross-validation.",
        "code1_title": "Classification Metrics",
        "code1": (
            "from sklearn.metrics import (\n"
            "    confusion_matrix, classification_report,\n"
            "    roc_auc_score, roc_curve, accuracy_score\n"
            ")\n"
            "from sklearn.ensemble import RandomForestClassifier\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.model_selection import train_test_split\n\n"
            "X, y = make_classification(n_samples=500, n_features=8, random_state=42)\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\n"
            "rf = RandomForestClassifier(n_estimators=50, random_state=42)\n"
            "rf.fit(X_train, y_train)\n"
            "y_pred = rf.predict(X_test)\n"
            "y_prob = rf.predict_proba(X_test)[:, 1]\n\n"
            "print('Accuracy:', accuracy_score(y_test, y_pred))\n"
            "print('ROC-AUC:', roc_auc_score(y_test, y_prob).round(4))\n"
            "print('Confusion Matrix:')\n"
            "print(confusion_matrix(y_test, y_pred))\n"
            "print(classification_report(y_test, y_pred))"
        ),
        "code2_title": "Cross-Validation & Regression Metrics",
        "code2": (
            "from sklearn.model_selection import cross_val_score, KFold\n"
            "from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score\n"
            "from sklearn.ensemble import RandomForestRegressor\n"
            "from sklearn.datasets import make_regression\n"
            "import numpy as np\n\n"
            "X, y = make_regression(n_samples=300, n_features=5, noise=20, random_state=42)\n\n"
            "rf = RandomForestRegressor(n_estimators=50, random_state=42)\n"
            "\n"
            "# 5-fold cross-validation\n"
            "cv = KFold(n_splits=5, shuffle=True, random_state=42)\n"
            "scores = cross_val_score(rf, X, y, cv=cv, scoring='r2')\n"
            "print(f'CV R2: {scores.mean():.4f} +/- {scores.std():.4f}')\n\n"
            "# Also report MAE, RMSE on test set\n"
            "from sklearn.model_selection import train_test_split\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n"
            "rf.fit(X_train, y_train)\n"
            "yp = rf.predict(X_test)\n"
            "print(f'MAE: {mean_absolute_error(y_test, yp):.2f}')\n"
            "print(f'RMSE: {np.sqrt(mean_squared_error(y_test, yp)):.2f}')\n"
            "print(f'R2: {r2_score(y_test, yp):.4f}')"
        ),
                "code4_title": "Learning Curve, Validation Curve & Precision-Recall",
        "code4": (
            "from sklearn.model_selection import learning_curve, validation_curve\n"
            "from sklearn.ensemble import RandomForestClassifier\n"
            "from sklearn.datasets import make_classification\n"
            "import numpy as np\n"
            "\n"
            "X, y = make_classification(n_samples=1000, n_features=10, random_state=42)\n"
            "\n"
            "# Learning curve — how accuracy changes with more training data\n"
            "train_sizes, train_scores, val_scores = learning_curve(\n"
            "    RandomForestClassifier(n_estimators=50, random_state=42),\n"
            "    X, y, cv=5, train_sizes=np.linspace(0.1, 1.0, 8), scoring='accuracy'\n"
            ")\n"
            "print('Learning curve (train size → val accuracy):')\n"
            "for sz, vs in zip(train_sizes, val_scores.mean(axis=1)):\n"
            "    print(f'  n={int(sz):4d}: {vs:.4f}')\n"
            "\n"
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
        "rw_scenario": "Medical: Evaluate a cancer detection model — minimize false negatives (missed cancers) using recall + AUC.",
        "rw_code": (
            "from sklearn.metrics import classification_report, roc_auc_score, recall_score\n"
            "from sklearn.ensemble import GradientBoostingClassifier\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.datasets import make_classification\n\n"
            "# Simulate imbalanced cancer screening data (10% positive)\n"
            "X, y = make_classification(\n"
            "    n_samples=1000, weights=[0.9, 0.1],\n"
            "    n_features=8, random_state=42\n"
            ")\n"
            "X_train, X_test, y_train, y_test = train_test_split(\n"
            "    X, y, test_size=0.2, stratify=y, random_state=42\n"
            ")\n\n"
            "model = GradientBoostingClassifier(random_state=42)\n"
            "model.fit(X_train, y_train)\n"
            "y_pred = model.predict(X_test)\n"
            "y_prob = model.predict_proba(X_test)[:, 1]\n\n"
            "print('Cancer Detection Model Evaluation:')\n"
            "print(f'Recall (sensitivity): {recall_score(y_test, y_pred):.4f}')\n"
            "print(f'ROC-AUC: {roc_auc_score(y_test, y_prob):.4f}')\n"
            "print(classification_report(y_test, y_pred, target_names=['Healthy','Cancer']))"
        ),
        "code3_title": "Precision-Recall Curve & Threshold Tuning",
        "code3": (
            "from sklearn.metrics import precision_recall_curve, average_precision_score\n"
            "from sklearn.metrics import f1_score, precision_score, recall_score\n"
            "from sklearn.ensemble import RandomForestClassifier\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.model_selection import train_test_split\n"
            "import numpy as np\n\n"
            "X, y = make_classification(n_samples=1000, weights=[0.85, 0.15], random_state=42)\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)\n\n"
            "rf = RandomForestClassifier(n_estimators=50, random_state=42)\n"
            "rf.fit(X_train, y_train)\n"
            "y_prob = rf.predict_proba(X_test)[:, 1]\n\n"
            "print(f'Avg Precision Score: {average_precision_score(y_test, y_prob):.4f}')\n\n"
            "# Find threshold that maximises F1\n"
            "thresholds = np.arange(0.1, 0.9, 0.05)\n"
            "best_f1, best_thresh = 0, 0.5\n"
            "for t in thresholds:\n"
            "    y_pred_t = (y_prob >= t).astype(int)\n"
            "    f1 = f1_score(y_test, y_pred_t, zero_division=0)\n"
            "    if f1 > best_f1:\n"
            "        best_f1, best_thresh = f1, t\n"
            "print(f'Best threshold={best_thresh:.2f}  F1={best_f1:.4f}')\n"
            "y_best = (y_prob >= best_thresh).astype(int)\n"
            "print(f'Precision={precision_score(y_test, y_best):.4f}  Recall={recall_score(y_test, y_best):.4f}')"
        ),
        "practice": {
            "title": "Threshold Tuning for Imbalanced Data",
            "desc": "Generate imbalanced data (weights=[0.9, 0.1], 800 samples). Train a RandomForestClassifier. At the default 0.5 threshold, compute precision, recall, F1. Then sweep thresholds from 0.1 to 0.9 in steps of 0.05. For each threshold compute F1. Print the threshold that maximises F1. Also compute ROC-AUC.",
            "starter": (
                "from sklearn.ensemble import RandomForestClassifier\n"
                "from sklearn.datasets import make_classification\n"
                "from sklearn.model_selection import train_test_split\n"
                "from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score\n"
                "import numpy as np\n\n"
                "X, y = make_classification(\n"
                "    n_samples=800, weights=[0.9, 0.1], n_features=8, random_state=1\n"
                ")\n"
                "X_train, X_test, y_train, y_test = train_test_split(\n"
                "    X, y, test_size=0.2, stratify=y, random_state=1\n"
                ")\n\n"
                "# TODO: Train RandomForestClassifier and get predict_proba\n"
                "# rf = RandomForestClassifier(n_estimators=100, random_state=1)\n"
                "# rf.fit(X_train, y_train)\n"
                "# y_prob = rf.predict_proba(X_test)[:, 1]\n\n"
                "# TODO: Default threshold (0.5) metrics\n"
                "# y_pred = (y_prob >= 0.5).astype(int)\n"
                "# print(f'Default: P={precision_score(y_test, y_pred):.4f}  R={recall_score(y_test, y_pred):.4f}  F1={f1_score(y_test, y_pred):.4f}')\n\n"
                "# TODO: Threshold sweep\n"
                "# best_f1, best_t = 0, 0.5\n"
                "# for t in np.arange(0.1, 0.9, 0.05):\n"
                "#     yp = (y_prob >= t).astype(int)\n"
                "#     f1 = f1_score(y_test, yp, zero_division=0)\n"
                "#     if f1 > best_f1: best_f1, best_t = f1, t\n"
                "# print(f'Best threshold={best_t:.2f}  F1={best_f1:.4f}')\n\n"
                "# TODO: ROC-AUC\n"
                "# print('ROC-AUC:', roc_auc_score(y_test, y_prob).round(4))"
            ),
        },
    },
    {
        "title": "Pipelines & Preprocessing",
        "desc": "Chain preprocessing + model into a single Pipeline. Prevent data leakage and simplify deployment.",
        "code1_title": "Building a Pipeline",
        "code1": (
            "from sklearn.pipeline import Pipeline\n"
            "from sklearn.preprocessing import StandardScaler, LabelEncoder\n"
            "from sklearn.impute import SimpleImputer\n"
            "from sklearn.ensemble import RandomForestClassifier\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.datasets import make_classification\n"
            "import numpy as np\n\n"
            "X, y = make_classification(n_samples=500, n_features=6, random_state=42)\n"
            "# Inject missing values\n"
            "X_missing = X.copy()\n"
            "X_missing[np.random.choice(500, 50), np.random.choice(6, 50)] = np.nan\n\n"
            "X_train, X_test, y_train, y_test = train_test_split(X_missing, y, test_size=0.2, random_state=42)\n\n"
            "pipe = Pipeline([\n"
            "    ('imputer', SimpleImputer(strategy='mean')),\n"
            "    ('scaler', StandardScaler()),\n"
            "    ('clf', RandomForestClassifier(n_estimators=50, random_state=42))\n"
            "])\n"
            "pipe.fit(X_train, y_train)\n"
            "print('Pipeline accuracy:', pipe.score(X_test, y_test).round(4))"
        ),
        "code2_title": "ColumnTransformer for Mixed Data",
        "code2": (
            "from sklearn.compose import ColumnTransformer\n"
            "from sklearn.preprocessing import StandardScaler, OneHotEncoder\n"
            "from sklearn.pipeline import Pipeline\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "import pandas as pd, numpy as np\n\n"
            "# Mixed data: numeric + categorical\n"
            "np.random.seed(42)\n"
            "df = pd.DataFrame({\n"
            "    'age': np.random.randint(18, 70, 200),\n"
            "    'income': np.random.normal(50000, 20000, 200),\n"
            "    'city': np.random.choice(['NYC', 'LA', 'Chicago'], 200),\n"
            "    'plan': np.random.choice(['basic', 'premium'], 200)\n"
            "})\n"
            "y = (df['income'] > 55000).astype(int)\n\n"
            "num_cols = ['age', 'income']\n"
            "cat_cols = ['city', 'plan']\n\n"
            "preprocessor = ColumnTransformer([\n"
            "    ('num', StandardScaler(), num_cols),\n"
            "    ('cat', OneHotEncoder(drop='first'), cat_cols)\n"
            "])\n"
            "pipe = Pipeline([('prep', preprocessor), ('clf', LogisticRegression())])\n\n"
            "from sklearn.model_selection import cross_val_score\n"
            "scores = cross_val_score(pipe, df, y, cv=5)\n"
            "print('CV Accuracy:', scores.mean().round(4))"
        ),
                "code4_title": "Pipeline with SelectKBest & FunctionTransformer",
        "code4": (
            "from sklearn.pipeline import Pipeline\n"
            "from sklearn.feature_selection import SelectKBest, f_classif\n"
            "from sklearn.preprocessing import FunctionTransformer, StandardScaler\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.model_selection import cross_val_score\n"
            "import numpy as np\n"
            "\n"
            "X, y = make_classification(n_samples=500, n_features=20,\n"
            "                           n_informative=8, random_state=42)\n"
            "\n"
            "# Custom log1p transform as a FunctionTransformer\n"
            "log_transform = FunctionTransformer(np.log1p, validate=True)\n"
            "\n"
            "pipe = Pipeline([\n"
            "    ('log',    FunctionTransformer(np.abs)),   # make all positive first\n"
            "    ('scaler', StandardScaler()),\n"
            "    ('select', SelectKBest(f_classif, k=8)),   # keep top 8 features\n"
            "    ('clf',    LogisticRegression(max_iter=500))\n"
            "])\n"
            "\n"
            "scores = cross_val_score(pipe, X, y, cv=5, scoring='accuracy')\n"
            "print('Pipeline with SelectKBest(k=8):')\n"
            "print(f'  CV accuracy: {scores.mean():.4f} ± {scores.std():.4f}')\n"
            "\n"
            "# Compare: all 20 features vs top 8\n"
            "pipe_all = Pipeline([('scaler', StandardScaler()), ('clf', LogisticRegression(max_iter=500))])\n"
            "scores_all = cross_val_score(pipe_all, X, y, cv=5)\n"
            "print(f'  All 20 features: {scores_all.mean():.4f} ± {scores_all.std():.4f}')"
        ),
        "rw_scenario": "HR Analytics: Build a complete pipeline to predict employee attrition from mixed numeric/categorical HR data.",
        "rw_code": (
            "from sklearn.pipeline import Pipeline\n"
            "from sklearn.compose import ColumnTransformer\n"
            "from sklearn.preprocessing import StandardScaler, OneHotEncoder\n"
            "from sklearn.ensemble import GradientBoostingClassifier\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.metrics import classification_report\n"
            "import pandas as pd, numpy as np\n\n"
            "np.random.seed(42)\n"
            "n = 500\n"
            "df = pd.DataFrame({\n"
            "    'age': np.random.randint(22, 60, n),\n"
            "    'salary': np.random.normal(60000, 20000, n),\n"
            "    'years_at_co': np.random.randint(1, 20, n),\n"
            "    'dept': np.random.choice(['Eng', 'Sales', 'HR', 'Finance'], n),\n"
            "    'satisfaction': np.random.choice(['low', 'med', 'high'], n)\n"
            "})\n"
            "df['attrition'] = ((df['salary'] < 45000) | (df['satisfaction'] == 'low')).astype(int)\n\n"
            "X = df.drop('attrition', axis=1)\n"
            "y = df['attrition']\n\n"
            "pre = ColumnTransformer([\n"
            "    ('num', StandardScaler(), ['age', 'salary', 'years_at_co']),\n"
            "    ('cat', OneHotEncoder(drop='first', sparse_output=False), ['dept', 'satisfaction'])\n"
            "])\n"
            "pipe = Pipeline([('prep', pre), ('clf', GradientBoostingClassifier(random_state=42))])\n\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n"
            "pipe.fit(X_train, y_train)\n"
            "print('Employee Attrition Pipeline:')\n"
            "print(classification_report(y_test, pipe.predict(X_test)))"
        ),
        "code3_title": "Pipeline with Polynomial Features",
        "code3": (
            "from sklearn.pipeline import Pipeline\n"
            "from sklearn.preprocessing import StandardScaler, PolynomialFeatures\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.model_selection import train_test_split\n\n"
            "X, y = make_classification(n_samples=500, n_features=4, random_state=42)\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\n"
            "pipe = Pipeline([\n"
            "    ('scaler', StandardScaler()),\n"
            "    ('poly', PolynomialFeatures(degree=2, include_bias=False)),\n"
            "    ('clf', LogisticRegression(max_iter=1000))\n"
            "])\n"
            "pipe.fit(X_train, y_train)\n"
            "print('Pipeline steps:', [name for name, _ in pipe.steps])\n"
            "print(f'Train accuracy: {pipe.score(X_train, y_train):.4f}')\n"
            "print(f'Test accuracy:  {pipe.score(X_test, y_test):.4f}')\n"
            "print(f'Features after poly: {pipe.named_steps[\"poly\"].n_output_features_}')"
        ),
        "practice": {
            "title": "Build an End-to-End Pipeline",
            "desc": "Create a full sklearn Pipeline for a mixed-type DataFrame: numeric columns need imputation + scaling, categorical columns need imputation + one-hot encoding. Chain everything into a RandomForest and run 5-fold CV.",
            "starter": (
                "from sklearn.pipeline import Pipeline\n"
                "from sklearn.compose import ColumnTransformer\n"
                "from sklearn.preprocessing import StandardScaler, OneHotEncoder\n"
                "from sklearn.impute import SimpleImputer\n"
                "from sklearn.ensemble import RandomForestClassifier\n"
                "from sklearn.model_selection import cross_val_score\n"
                "import pandas as pd, numpy as np\n\n"
                "np.random.seed(42)\n"
                "n = 400\n"
                "df = pd.DataFrame({\n"
                "    'age': np.random.randint(18, 65, n).astype(float),\n"
                "    'salary': np.random.normal(50000, 15000, n),\n"
                "    'dept': np.random.choice(['Tech', 'HR', 'Sales'], n),\n"
                "    'remote': np.random.choice(['yes', 'no'], n),\n"
                "})\n"
                "df.loc[np.random.choice(n, 30), 'age'] = np.nan\n"
                "y = (df['salary'] > 55000).astype(int)\n\n"
                "# TODO: Define numeric_features and categorical_features\n"
                "numeric_features = []  # age, salary\n"
                "categorical_features = []  # dept, remote\n\n"
                "# TODO: Build numeric_transformer Pipeline: SimpleImputer(strategy='median') -> StandardScaler\n"
                "numeric_transformer = None\n\n"
                "# TODO: Build categorical_transformer Pipeline: SimpleImputer(strategy='most_frequent') -> OneHotEncoder(drop='first')\n"
                "categorical_transformer = None\n\n"
                "# TODO: Build ColumnTransformer with numeric and categorical transformers\n"
                "preprocessor = None\n\n"
                "# TODO: Build full Pipeline: preprocessor -> RandomForestClassifier(n_estimators=50, random_state=42)\n"
                "pipe = None\n\n"
                "# TODO: Run cross_val_score and print mean accuracy\n"
                "# scores = cross_val_score(pipe, df, y, cv=5)\n"
                "# print('CV Accuracy:', scores.mean().round(4))"
            ),
        },
    },
    {
        "title": "Hyperparameter Tuning",
        "desc": "Find the best model parameters using GridSearchCV and RandomizedSearchCV.",
        "code1_title": "GridSearchCV",
        "code1": (
            "from sklearn.model_selection import GridSearchCV\n"
            "from sklearn.ensemble import RandomForestClassifier\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.model_selection import train_test_split\n\n"
            "X, y = make_classification(n_samples=600, n_features=8, random_state=42)\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\n"
            "param_grid = {\n"
            "    'n_estimators': [50, 100, 200],\n"
            "    'max_depth': [None, 5, 10],\n"
            "    'min_samples_split': [2, 5]\n"
            "}\n\n"
            "grid = GridSearchCV(\n"
            "    RandomForestClassifier(random_state=42),\n"
            "    param_grid, cv=5, scoring='accuracy', n_jobs=-1\n"
            ")\n"
            "grid.fit(X_train, y_train)\n"
            "print('Best params:', grid.best_params_)\n"
            "print('Best CV score:', round(grid.best_score_, 4))\n"
            "print('Test score:', round(grid.score(X_test, y_test), 4))"
        ),
        "code2_title": "RandomizedSearchCV (Faster)",
        "code2": (
            "from sklearn.model_selection import RandomizedSearchCV\n"
            "from sklearn.ensemble import GradientBoostingClassifier\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.model_selection import train_test_split\n"
            "from scipy.stats import randint, uniform\n\n"
            "X, y = make_classification(n_samples=600, n_features=8, random_state=42)\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\n"
            "param_dist = {\n"
            "    'n_estimators': randint(50, 300),\n"
            "    'max_depth': randint(2, 10),\n"
            "    'learning_rate': uniform(0.01, 0.3),\n"
            "    'subsample': uniform(0.6, 0.4)\n"
            "}\n\n"
            "rscv = RandomizedSearchCV(\n"
            "    GradientBoostingClassifier(random_state=42),\n"
            "    param_dist, n_iter=20, cv=5, scoring='accuracy',\n"
            "    random_state=42, n_jobs=-1\n"
            ")\n"
            "rscv.fit(X_train, y_train)\n"
            "print('Best params:', rscv.best_params_)\n"
            "print('Best CV score:', round(rscv.best_score_, 4))\n"
            "print('Test score:', round(rscv.score(X_test, y_test), 4))"
        ),
                "code4_title": "cross_validate with Multiple Scoring Metrics",
        "code4": (
            "from sklearn.model_selection import cross_validate\n"
            "from sklearn.ensemble import GradientBoostingClassifier\n"
            "from sklearn.datasets import make_classification\n"
            "import numpy as np\n"
            "\n"
            "X, y = make_classification(n_samples=800, n_features=10,\n"
            "                           weights=[0.7, 0.3], random_state=42)\n"
            "\n"
            "# Evaluate with multiple metrics at once\n"
            "scoring = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']\n"
            "results = cross_validate(\n"
            "    GradientBoostingClassifier(n_estimators=100, random_state=42),\n"
            "    X, y, cv=5, scoring=scoring, return_train_score=True\n"
            ")\n"
            "\n"
            "print('5-fold CV results (mean ± std):')\n"
            "for metric in scoring:\n"
            "    test_mean  = results[f'test_{metric}'].mean()\n"
            "    test_std   = results[f'test_{metric}'].std()\n"
            "    train_mean = results[f'train_{metric}'].mean()\n"
            "    gap = train_mean - test_mean\n"
            "    print(f'  {metric:12s}: {test_mean:.4f} ± {test_std:.4f}  (train={train_mean:.4f}, gap={gap:.4f})')\n"
            "print(f'\\nFit time: {results[\"fit_time\"].mean():.3f}s avg')"
        ),
        "rw_scenario": "Ad Tech: Tune a click-through-rate (CTR) prediction model to maximize ROC-AUC for an ad targeting system.",
        "rw_code": (
            "from sklearn.model_selection import RandomizedSearchCV\n"
            "from sklearn.ensemble import GradientBoostingClassifier\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.model_selection import train_test_split\n"
            "from scipy.stats import randint, uniform\n\n"
            "# Simulate CTR data (heavily imbalanced: ~2% click rate)\n"
            "X, y = make_classification(\n"
            "    n_samples=2000, weights=[0.98, 0.02],\n"
            "    n_features=10, n_informative=6, random_state=42\n"
            ")\n"
            "X_train, X_test, y_train, y_test = train_test_split(\n"
            "    X, y, stratify=y, test_size=0.2, random_state=42\n"
            ")\n\n"
            "param_dist = {\n"
            "    'n_estimators': randint(100, 400),\n"
            "    'learning_rate': uniform(0.01, 0.2),\n"
            "    'max_depth': randint(2, 6)\n"
            "}\n"
            "rscv = RandomizedSearchCV(\n"
            "    GradientBoostingClassifier(random_state=42),\n"
            "    param_dist, n_iter=15, cv=3, scoring='roc_auc',\n"
            "    random_state=42, n_jobs=-1\n"
            ")\n"
            "rscv.fit(X_train, y_train)\n"
            "from sklearn.metrics import roc_auc_score\n"
            "y_prob = rscv.predict_proba(X_test)[:, 1]\n"
            "print('CTR Model Tuning:')\n"
            "print('Best AUC:', round(rscv.best_score_, 4))\n"
            "print('Test AUC:', round(roc_auc_score(y_test, y_prob), 4))"
        ),
        "code3_title": "HalvingGridSearchCV (Successive Halving)",
        "code3": (
            "from sklearn.experimental import enable_halving_search_cv\n"
            "from sklearn.model_selection import HalvingGridSearchCV\n"
            "from sklearn.ensemble import RandomForestClassifier\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.model_selection import train_test_split\n\n"
            "X, y = make_classification(n_samples=2000, n_features=10, random_state=42)\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\n"
            "param_grid = {\n"
            "    'n_estimators': [50, 100, 200, 300],\n"
            "    'max_depth': [None, 5, 10],\n"
            "    'min_samples_split': [2, 5]\n"
            "}\n\n"
            "search = HalvingGridSearchCV(\n"
            "    RandomForestClassifier(random_state=42),\n"
            "    param_grid, factor=3, cv=3, scoring='accuracy',\n"
            "    random_state=42, n_jobs=-1\n"
            ")\n"
            "search.fit(X_train, y_train)\n"
            "print('Best params:', search.best_params_)\n"
            "print('Best CV score:', round(search.best_score_, 4))\n"
            "print('Test accuracy:', round(search.score(X_test, y_test), 4))\n"
            "print(f'Configs evaluated: {len(search.cv_results_[\"mean_test_score\"])}')"
        ),
        "practice": {
            "title": "Tune an SVM Classifier",
            "desc": "Build a Pipeline(StandardScaler + SVC) and use GridSearchCV to tune C, kernel, and gamma. Then compare with RandomizedSearchCV using n_iter=10. Which finds a better score and runs faster?",
            "starter": (
                "from sklearn.model_selection import GridSearchCV, RandomizedSearchCV\n"
                "from sklearn.svm import SVC\n"
                "from sklearn.datasets import make_classification\n"
                "from sklearn.model_selection import train_test_split\n"
                "from sklearn.preprocessing import StandardScaler\n"
                "from sklearn.pipeline import Pipeline\n"
                "import numpy as np\n\n"
                "X, y = make_classification(n_samples=800, n_features=8, random_state=42)\n"
                "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\n"
                "# TODO: Build Pipeline with StandardScaler and SVC\n"
                "# pipe = Pipeline([('scaler', StandardScaler()), ('svm', SVC())])\n\n"
                "# TODO: Define param_grid for SVC:\n"
                "# 'svm__C': [0.1, 1, 10, 100], 'svm__kernel': ['rbf', 'linear']\n"
                "param_grid = {}\n\n"
                "# TODO: Run GridSearchCV with cv=5, scoring='accuracy'\n"
                "# grid = GridSearchCV(pipe, param_grid, cv=5, scoring='accuracy', n_jobs=-1)\n"
                "# grid.fit(X_train, y_train)\n"
                "# print('Best params:', grid.best_params_)\n"
                "# print('Test accuracy:', round(grid.score(X_test, y_test), 4))\n\n"
                "# BONUS: Try RandomizedSearchCV with n_iter=10\n"
                "# from scipy.stats import loguniform\n"
                "# param_dist = {'svm__C': loguniform(0.01, 100), 'svm__kernel': ['rbf', 'linear']}\n"
                "# rscv = RandomizedSearchCV(pipe, param_dist, n_iter=10, cv=5, random_state=42)\n"
                "# rscv.fit(X_train, y_train)\n"
                "# print('RandomizedSearch best:', rscv.best_params_)"
            ),
        },
    },
    {
        "title": "Dimensionality Reduction: PCA & t-SNE",
        "desc": "Reduce high-dimensional data for visualization, noise reduction, and speeding up training.",
        "code1_title": "PCA — Principal Component Analysis",
        "code1": (
            "from sklearn.decomposition import PCA\n"
            "from sklearn.datasets import load_digits\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "import numpy as np\n\n"
            "digits = load_digits()\n"
            "X = StandardScaler().fit_transform(digits.data)\n"
            "print('Original shape:', X.shape)  # 1797 x 64\n\n"
            "# Keep 95% of variance\n"
            "pca = PCA(n_components=0.95)\n"
            "X_pca = pca.fit_transform(X)\n"
            "print('Reduced shape:', X_pca.shape)\n"
            "print(f'Explained variance: {pca.explained_variance_ratio_.sum():.3f}')\n\n"
            "# 2D for visualization\n"
            "pca2 = PCA(n_components=2)\n"
            "X_2d = pca2.fit_transform(X)\n"
            "print('2D shape:', X_2d.shape)\n"
            "print('Variance explained by 2 PCs:', pca2.explained_variance_ratio_.sum().round(3))"
        ),
        "code2_title": "t-SNE for Visualization",
        "code2": (
            "from sklearn.manifold import TSNE\n"
            "from sklearn.datasets import load_iris\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "import numpy as np\n\n"
            "iris = load_iris()\n"
            "X = StandardScaler().fit_transform(iris.data)\n\n"
            "# t-SNE: great for visualization, non-linear\n"
            "tsne = TSNE(n_components=2, random_state=42, perplexity=30, max_iter=1000)\n"
            "X_tsne = tsne.fit_transform(X)\n"
            "print('t-SNE output shape:', X_tsne.shape)\n\n"
            "# Confirm clusters align with true labels\n"
            "for cls in range(3):\n"
            "    mask = iris.target == cls\n"
            "    center = X_tsne[mask].mean(axis=0)\n"
            "    print(f'{iris.target_names[cls]}: center=({center[0]:.1f}, {center[1]:.1f})')"
        ),
                "code4_title": "NMF & Isomap for Non-Linear Reduction",
        "code4": (
            "from sklearn.decomposition import NMF\n"
            "from sklearn.manifold import Isomap\n"
            "from sklearn.preprocessing import MinMaxScaler\n"
            "from sklearn.datasets import load_digits\n"
            "import numpy as np\n"
            "\n"
            "digits = load_digits()\n"
            "X      = MinMaxScaler().fit_transform(digits.data)  # NMF needs non-negative\n"
            "y      = digits.target\n"
            "\n"
            "# NMF: learns parts-based representation\n"
            "nmf = NMF(n_components=20, max_iter=500, random_state=42)\n"
            "X_nmf = nmf.fit_transform(X)\n"
            "print(f'NMF: {X.shape} → {X_nmf.shape}')\n"
            "print(f'Reconstruction error: {nmf.reconstruction_err_:.4f}')\n"
            "\n"
            "# Isomap: non-linear manifold learning (preserves geodesic distances)\n"
            "iso = Isomap(n_components=2, n_neighbors=10)\n"
            "X_iso = iso.fit_transform(X)\n"
            "print(f'\\nIsomap: {X.shape} → {X_iso.shape}')\n"
            "\n"
            "# Check cluster quality: std of 2D coordinates per digit class\n"
            "print('Per-digit cluster spread (lower = tighter cluster):')\n"
            "for cls in range(10):\n"
            "    spread = X_iso[y == cls].std()\n"
            "    print(f'  Digit {cls}: {spread:.3f}')"
        ),
        "rw_scenario": "NLP: Reduce TF-IDF document vectors from 5000 dims to 50 with PCA before training a classifier — 10x speedup.",
        "rw_code": (
            "from sklearn.decomposition import PCA, TruncatedSVD\n"
            "from sklearn.feature_extraction.text import TfidfVectorizer\n"
            "from sklearn.pipeline import Pipeline\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.model_selection import cross_val_score\n\n"
            "# Simulated news headlines\n"
            "docs = [\n"
            "    'stock market rises sharply', 'fed raises interest rates',\n"
            "    'tech giants report earnings', 'inflation data released',\n"
            "    'new iphone model announced', 'oil prices fall today',\n"
            "    'housing market cools down', 'crypto prices volatile',\n"
            "    'gdp growth beats forecast', 'layoffs hit tech sector'\n"
            "]\n"
            "labels = [1, 1, 1, 1, 1, 0, 0, 0, 1, 0]  # 1=finance/tech, 0=other\n\n"
            "# TF-IDF -> LSA (Truncated SVD) -> Logistic Regression\n"
            "pipe = Pipeline([\n"
            "    ('tfidf', TfidfVectorizer(max_features=50)),\n"
            "    ('svd', TruncatedSVD(n_components=5, random_state=42)),\n"
            "    ('clf', LogisticRegression())\n"
            "])\n"
            "pipe.fit(docs, labels)\n"
            "print('Test predictions:', pipe.predict(docs[-3:]))\n"
            "print('True labels:     ', labels[-3:])"
        ),
        "code3_title": "Explained Variance Curve with PCA",
        "code3": (
            "from sklearn.decomposition import PCA\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "from sklearn.datasets import load_digits\n"
            "import numpy as np\n\n"
            "digits = load_digits()\n"
            "X = StandardScaler().fit_transform(digits.data)\n\n"
            "pca_full = PCA()\n"
            "pca_full.fit(X)\n"
            "cumvar = np.cumsum(pca_full.explained_variance_ratio_)\n\n"
            "n90 = np.argmax(cumvar >= 0.90) + 1\n"
            "n95 = np.argmax(cumvar >= 0.95) + 1\n"
            "n99 = np.argmax(cumvar >= 0.99) + 1\n\n"
            "print(f'Total features: {X.shape[1]}')\n"
            "print(f'Components for 90% variance: {n90}  ({X.shape[1]/n90:.1f}x compression)')\n"
            "print(f'Components for 95% variance: {n95}  ({X.shape[1]/n95:.1f}x compression)')\n"
            "print(f'Components for 99% variance: {n99}  ({X.shape[1]/n99:.1f}x compression)')\n\n"
            "print('Top 5 PC variance explained:')\n"
            "for i, (var, cum) in enumerate(zip(pca_full.explained_variance_ratio_[:5], cumvar[:5])):\n"
            "    print(f'  PC{i+1}: {var:.4f} (cumulative: {cum:.4f})')"
        ),
        "practice": {
            "title": "PCA + KNN: Compress and Classify",
            "desc": "Load the digits dataset, apply PCA to retain 90% variance, then compare KNN accuracy before and after reduction using 5-fold CV. Also try 2D PCA and print the cluster centers per digit class.",
            "starter": (
                "from sklearn.decomposition import PCA\n"
                "from sklearn.preprocessing import StandardScaler\n"
                "from sklearn.neighbors import KNeighborsClassifier\n"
                "from sklearn.model_selection import cross_val_score\n"
                "from sklearn.datasets import load_digits\n"
                "import numpy as np\n\n"
                "digits = load_digits()\n"
                "X = StandardScaler().fit_transform(digits.data)\n"
                "y = digits.target\n"
                "print('Original shape:', X.shape)  # (1797, 64)\n\n"
                "# TODO: Apply PCA keeping 90% of variance\n"
                "# pca = PCA(n_components=???)\n"
                "# X_pca = pca.fit_transform(X)\n"
                "# print('Reduced shape:', X_pca.shape)\n\n"
                "# TODO: 5-fold CV on ORIGINAL data with KNN(n_neighbors=5)\n"
                "# scores_orig = cross_val_score(KNeighborsClassifier(n_neighbors=5), X, y, cv=5)\n"
                "# print(f'KNN on original: {scores_orig.mean():.4f}')\n\n"
                "# TODO: 5-fold CV on PCA-reduced data\n"
                "# scores_pca = cross_val_score(KNeighborsClassifier(n_neighbors=5), X_pca, y, cv=5)\n"
                "# print(f'KNN on PCA:      {scores_pca.mean():.4f}')\n\n"
                "# BONUS: Reduce to 2D and print class centers\n"
                "# pca2 = PCA(n_components=2)\n"
                "# X_2d = pca2.fit_transform(X)\n"
                "# for cls in range(10):\n"
                "#     center = X_2d[y == cls].mean(axis=0)\n"
                "#     print(f'Digit {cls} center: ({center[0]:.2f}, {center[1]:.2f})')"
            ),
        },
    },
    {
        "title": "Imbalanced Data Handling",
        "desc": "Handle class imbalance using resampling (oversampling minority, undersampling majority), class weights, and threshold tuning to improve recall on rare classes.",
        "code1_title": "Class Weights & Threshold Tuning",
        "code1": (
            "import numpy as np\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.metrics import classification_report, f1_score\n\n"
            "np.random.seed(42)\n"
            "X, y = make_classification(\n"
            "    n_samples=5000, weights=[0.95, 0.05], random_state=42\n"
            ")\n"
            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)\n\n"
            "# Without class weight\n"
            "lr_base = LogisticRegression(random_state=0).fit(X_tr, y_tr)\n"
            "print('Default class_weight:')\n"
            "print(classification_report(y_te, lr_base.predict(X_te), target_names=['maj','min']))\n\n"
            "# With class_weight='balanced'\n"
            "lr_bal = LogisticRegression(class_weight='balanced', random_state=0).fit(X_tr, y_tr)\n"
            "proba = lr_bal.predict_proba(X_te)[:, 1]\n"
            "best_thresh, best_f1 = 0.5, 0.0\n"
            "for t in np.arange(0.1, 0.9, 0.05):\n"
            "    f1 = f1_score(y_te, (proba > t).astype(int))\n"
            "    if f1 > best_f1: best_f1, best_thresh = f1, t\n"
            "print(f'Balanced model: best threshold={best_thresh:.2f}, minority F1={best_f1:.3f}')"
        ),
        "code2_title": "Manual Oversampling (Random + SMOTE-style)",
        "code2": (
            "import numpy as np\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.metrics import f1_score\n\n"
            "np.random.seed(42)\n"
            "X, y = make_classification(n_samples=2000, weights=[0.9, 0.1], random_state=42)\n"
            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)\n\n"
            "def random_oversample(X, y, random_state=42):\n"
            "    rng = np.random.RandomState(random_state)\n"
            "    classes, counts = np.unique(y, return_counts=True)\n"
            "    max_count = max(counts)\n"
            "    X_bal, y_bal = [X], [y]\n"
            "    for cls, cnt in zip(classes, counts):\n"
            "        if cnt < max_count:\n"
            "            idx = np.where(y == cls)[0]\n"
            "            extra = rng.choice(idx, max_count - cnt, replace=True)\n"
            "            X_bal.append(X[extra])\n"
            "            y_bal.append(y[extra])\n"
            "    return np.vstack(X_bal), np.concatenate(y_bal)\n\n"
            "X_res, y_res = random_oversample(X_tr, y_tr)\n"
            "print(f'Before: {np.bincount(y_tr)}')\n"
            "print(f'After:  {np.bincount(y_res)}')\n"
            "base_f1 = f1_score(y_te, LogisticRegression(random_state=0).fit(X_tr, y_tr).predict(X_te))\n"
            "over_f1 = f1_score(y_te, LogisticRegression(random_state=0).fit(X_res, y_res).predict(X_te))\n"
            "print(f'Base minority F1: {base_f1:.3f} | Oversampled F1: {over_f1:.3f}')"
        ),
        "code3_title": "SMOTE with imbalanced-learn",
        "code3": (
            "try:\n"
            "    from imblearn.over_sampling import SMOTE\n"
            "    from imblearn.pipeline import Pipeline as ImbPipeline\n"
            "    from sklearn.ensemble import RandomForestClassifier\n"
            "    from sklearn.datasets import make_classification\n"
            "    from sklearn.model_selection import cross_val_score\n"
            "    import numpy as np\n\n"
            "    np.random.seed(42)\n"
            "    X, y = make_classification(n_samples=2000, weights=[0.9, 0.1], random_state=42)\n\n"
            "    pipe = ImbPipeline([\n"
            "        ('smote', SMOTE(random_state=42)),\n"
            "        ('rf', RandomForestClassifier(n_estimators=50, random_state=0))\n"
            "    ])\n"
            "    scores = cross_val_score(pipe, X, y, cv=5, scoring='f1')\n"
            "    print(f'SMOTE+RF F1: {scores.mean():.3f} +/- {scores.std():.3f}')\n\n"
            "    base_scores = cross_val_score(\n"
            "        RandomForestClassifier(class_weight='balanced', n_estimators=50, random_state=0),\n"
            "        X, y, cv=5, scoring='f1'\n"
            "    )\n"
            "    print(f'Balanced RF F1: {base_scores.mean():.3f} +/- {base_scores.std():.3f}')\n"
            "except ImportError:\n"
            "    print('pip install imbalanced-learn')\n"
            "    print('SMOTE: synthetic minority oversampling.')\n"
            "    print('For each minority sample, create synthetic points along lines to k-nearest neighbors.')"
        ),
        "code4_title": "Precision-Recall Curve & AUC-PR",
        "code4": (
            "import numpy as np\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.metrics import precision_recall_curve, average_precision_score, roc_auc_score\n"
            "import matplotlib\n"
            "matplotlib.use('Agg')\n"
            "import matplotlib.pyplot as plt\n\n"
            "np.random.seed(42)\n"
            "X, y = make_classification(n_samples=3000, weights=[0.9, 0.1], random_state=42)\n"
            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)\n\n"
            "lr = LogisticRegression(class_weight='balanced', random_state=0).fit(X_tr, y_tr)\n"
            "proba = lr.predict_proba(X_te)[:, 1]\n"
            "prec, rec, thresh = precision_recall_curve(y_te, proba)\n"
            "ap = average_precision_score(y_te, proba)\n"
            "auc = roc_auc_score(y_te, proba)\n\n"
            "print(f'ROC-AUC: {auc:.4f}')\n"
            "print(f'Average Precision (AUC-PR): {ap:.4f}')\n"
            "print('Use AUC-PR for imbalanced data (ROC can be misleadingly high!)')\n\n"
            "fig, ax = plt.subplots(figsize=(6, 5))\n"
            "ax.plot(rec, prec, lw=2, label=f'AP={ap:.3f}')\n"
            "ax.axhline(y_te.mean(), linestyle='--', color='gray', label=f'Baseline ({y_te.mean():.3f})')\n"
            "ax.set_xlabel('Recall'); ax.set_ylabel('Precision')\n"
            "ax.set_title('Precision-Recall Curve'); ax.legend()\n"
            "plt.tight_layout(); plt.savefig('pr_curve.png', dpi=80); plt.close()\n"
            "print('Saved pr_curve.png')"
        ),
        "rw_scenario": "Fraud detection: only 0.5% of transactions are fraudulent. Train a model that maximizes recall (catch most frauds) while keeping precision above 40% to avoid alert fatigue.",
        "rw_code": (
            "import numpy as np\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.metrics import classification_report, average_precision_score\n\n"
            "np.random.seed(7)\n"
            "X, y = make_classification(n_samples=10000, weights=[0.995, 0.005], random_state=7,\n"
            "                           n_features=15, n_informative=8)\n"
            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)\n\n"
            "model = LogisticRegression(class_weight='balanced', max_iter=500, random_state=0)\n"
            "model.fit(X_tr, y_tr)\n"
            "proba = model.predict_proba(X_te)[:, 1]\n\n"
            "# Find threshold where precision >= 0.40\n"
            "from sklearn.metrics import precision_recall_curve\n"
            "prec, rec, thresh = precision_recall_curve(y_te, proba)\n"
            "valid = np.where(prec[:-1] >= 0.40)[0]\n"
            "if len(valid):\n"
            "    best_t = thresh[valid[np.argmax(rec[valid])]]\n"
            "    pred = (proba >= best_t).astype(int)\n"
            "    print(f'Threshold: {best_t:.3f}')\n"
            "    print(classification_report(y_te, pred, target_names=['legit', 'fraud']))\n"
            "print(f'AUC-PR: {average_precision_score(y_te, proba):.4f}')"
        ),
        "practice": {
            "title": "Imbalanced Credit Default Prediction",
            "desc": "With 5% positive rate, compare: (1) default LR, (2) balanced LR, (3) LR + random oversampling. Report minority F1 and AUC-PR for each. Find the optimal decision threshold for balanced LR to maximize minority F1.",
            "starter": (
                "import numpy as np\n"
                "from sklearn.datasets import make_classification\n"
                "from sklearn.linear_model import LogisticRegression\n"
                "from sklearn.model_selection import train_test_split\n"
                "from sklearn.metrics import f1_score, average_precision_score\n\n"
                "np.random.seed(42)\n"
                "X, y = make_classification(n_samples=3000, weights=[0.95, 0.05], random_state=42)\n"
                "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=0)\n\n"
                "# TODO: (1) Default LR - compute minority F1 and AUC-PR\n"
                "# TODO: (2) Balanced LR (class_weight='balanced') - same metrics\n"
                "# TODO: (3) LR + random oversampling - same metrics\n"
                "# TODO: For balanced LR, find threshold maximizing minority F1\n"
            ),
        },
    },
    {
        "title": "Custom Estimators",
        "desc": "Build sklearn-compatible custom transformers and estimators using BaseEstimator, TransformerMixin, and ClassifierMixin to integrate into pipelines.",
        "code1_title": "Custom Transformer with TransformerMixin",
        "code1": (
            "import numpy as np\n"
            "from sklearn.base import BaseEstimator, TransformerMixin\n"
            "from sklearn.pipeline import Pipeline\n"
            "from sklearn.linear_model import LinearRegression\n"
            "from sklearn.datasets import make_regression\n\n"
            "class WinsorizeTransformer(BaseEstimator, TransformerMixin):\n"
            "    '''Clip values to [lower_q, upper_q] quantiles per feature.'''\n"
            "    def __init__(self, lower=0.01, upper=0.99):\n"
            "        self.lower = lower\n"
            "        self.upper = upper\n\n"
            "    def fit(self, X, y=None):\n"
            "        self.lower_ = np.quantile(X, self.lower, axis=0)\n"
            "        self.upper_ = np.quantile(X, self.upper, axis=0)\n"
            "        return self\n\n"
            "    def transform(self, X):\n"
            "        return np.clip(X, self.lower_, self.upper_)\n\n"
            "np.random.seed(42)\n"
            "X, y = make_regression(n_samples=300, n_features=5, noise=5, random_state=42)\n"
            "X[:10, 0] = 1000  # outliers\n\n"
            "pipe = Pipeline([\n"
            "    ('winsor', WinsorizeTransformer(lower=0.05, upper=0.95)),\n"
            "    ('lr', LinearRegression())\n"
            "])\n"
            "from sklearn.model_selection import cross_val_score\n"
            "scores = cross_val_score(pipe, X, y, cv=5, scoring='r2')\n"
            "print(f'Winsorized pipeline R2: {scores.mean():.4f} +/- {scores.std():.4f}')\n"
            "print(f'Params: {pipe.get_params()}')"
        ),
        "code2_title": "Custom Classifier with ClassifierMixin",
        "code2": (
            "import numpy as np\n"
            "from sklearn.base import BaseEstimator, ClassifierMixin\n"
            "from sklearn.utils.validation import check_X_y, check_array, check_is_fitted\n"
            "from sklearn.utils.multiclass import unique_labels\n"
            "from sklearn.metrics import accuracy_score\n\n"
            "class MajorityVoteClassifier(BaseEstimator, ClassifierMixin):\n"
            "    '''Predicts the most common class in the neighborhood (baseline).'''\n"
            "    def __init__(self, window=10):\n"
            "        self.window = window\n\n"
            "    def fit(self, X, y):\n"
            "        X, y = check_X_y(X, y)\n"
            "        self.classes_ = unique_labels(y)\n"
            "        self.X_train_ = X\n"
            "        self.y_train_ = y\n"
            "        return self\n\n"
            "    def predict(self, X):\n"
            "        check_is_fitted(self)\n"
            "        X = check_array(X)\n"
            "        preds = []\n"
            "        for x in X:\n"
            "            dists = np.sum((self.X_train_ - x)**2, axis=1)\n"
            "            nn_idx = np.argsort(dists)[:self.window]\n"
            "            vals, cnts = np.unique(self.y_train_[nn_idx], return_counts=True)\n"
            "            preds.append(vals[np.argmax(cnts)])\n"
            "        return np.array(preds)\n\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.model_selection import cross_val_score\n"
            "np.random.seed(42)\n"
            "X, y = make_classification(n_samples=500, n_features=10, random_state=42)\n"
            "clf = MajorityVoteClassifier(window=15)\n"
            "scores = cross_val_score(clf, X, y, cv=5)\n"
            "print(f'MajorityVote CV accuracy: {scores.mean():.4f}')"
        ),
        "code3_title": "Custom Selector: SelectByCorrelation",
        "code3": (
            "import numpy as np\n"
            "from sklearn.base import BaseEstimator, TransformerMixin\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.pipeline import Pipeline\n"
            "from sklearn.model_selection import cross_val_score\n\n"
            "class SelectByCorrelation(BaseEstimator, TransformerMixin):\n"
            "    '''Keep features with |Pearson corr| > threshold with target.'''\n"
            "    def __init__(self, threshold=0.1):\n"
            "        self.threshold = threshold\n\n"
            "    def fit(self, X, y):\n"
            "        corrs = np.array([\n"
            "            abs(np.corrcoef(X[:, j], y)[0, 1])\n"
            "            for j in range(X.shape[1])\n"
            "        ])\n"
            "        self.selected_ = np.where(corrs >= self.threshold)[0]\n"
            "        self.n_features_in_ = X.shape[1]\n"
            "        return self\n\n"
            "    def transform(self, X):\n"
            "        return X[:, self.selected_]\n\n"
            "np.random.seed(42)\n"
            "X, y = make_classification(n_samples=600, n_features=20, n_informative=5, random_state=42)\n\n"
            "pipe = Pipeline([\n"
            "    ('select', SelectByCorrelation(threshold=0.05)),\n"
            "    ('lr', LogisticRegression(max_iter=200, random_state=0))\n"
            "])\n"
            "from sklearn.model_selection import GridSearchCV\n"
            "gs = GridSearchCV(pipe, {'select__threshold': [0.02, 0.05, 0.1, 0.15]}, cv=5)\n"
            "gs.fit(X, y)\n"
            "print(f'Best threshold: {gs.best_params_[\"select__threshold\"]}')\n"
            "print(f'Best CV accuracy: {gs.best_score_:.4f}')\n"
            "pipe.fit(X, y)\n"
            "print(f'Features selected: {pipe.named_steps[\"select\"].selected_.tolist()}')"
        ),
        "code4_title": "set_output API & check_estimator",
        "code4": (
            "import numpy as np\n"
            "import pandas as pd\n"
            "from sklearn.base import BaseEstimator, TransformerMixin\n"
            "from sklearn.utils.estimator_checks import parametrize_with_checks\n\n"
            "class RobustScaler(BaseEstimator, TransformerMixin):\n"
            "    '''Scale by median and IQR for robustness to outliers.'''\n"
            "    def __init__(self):\n"
            "        pass\n\n"
            "    def fit(self, X, y=None):\n"
            "        self.median_ = np.median(X, axis=0)\n"
            "        q75, q25 = np.percentile(X, [75, 25], axis=0)\n"
            "        self.iqr_ = q75 - q25\n"
            "        self.iqr_[self.iqr_ == 0] = 1.0\n"
            "        return self\n\n"
            "    def transform(self, X):\n"
            "        return (X - self.median_) / self.iqr_\n\n"
            "np.random.seed(42)\n"
            "X = np.random.randn(100, 4)\n"
            "X[[0,1,2], 0] = 100  # outliers\n\n"
            "rs = RobustScaler()\n"
            "X_scaled = rs.fit_transform(X)\n"
            "print('Original col0 stats: mean={:.1f}, std={:.1f}'.format(X[:,0].mean(), X[:,0].std()))\n"
            "print('Scaled  col0 stats: mean={:.3f}, std={:.3f}'.format(X_scaled[:,0].mean(), X_scaled[:,0].std()))\n"
            "print('set_output API (pandas):')\n"
            "rs2 = RobustScaler().set_output(transform='pandas')\n"
            "df = pd.DataFrame(X[:5], columns=['a','b','c','d'])\n"
            "print(rs2.fit_transform(df))"
        ),
        "rw_scenario": "Build a production feature engineering pipeline with custom outlier winsorization, correlation-based feature selection, and a custom log transformer that handles zero and negative values gracefully.",
        "rw_code": (
            "import numpy as np\n"
            "from sklearn.base import BaseEstimator, TransformerMixin\n"
            "from sklearn.pipeline import Pipeline\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.model_selection import cross_val_score\n"
            "from sklearn.datasets import make_classification\n\n"
            "class SafeLogTransformer(BaseEstimator, TransformerMixin):\n"
            "    def __init__(self, offset=1.0): self.offset = offset\n"
            "    def fit(self, X, y=None): return self\n"
            "    def transform(self, X): return np.log1p(np.abs(X)) * np.sign(X)\n\n"
            "class WinsorizeTransformer(BaseEstimator, TransformerMixin):\n"
            "    def __init__(self, q=0.05): self.q = q\n"
            "    def fit(self, X, y=None):\n"
            "        self.lo_ = np.quantile(X, self.q, axis=0)\n"
            "        self.hi_ = np.quantile(X, 1-self.q, axis=0)\n"
            "        return self\n"
            "    def transform(self, X): return np.clip(X, self.lo_, self.hi_)\n\n"
            "np.random.seed(42)\n"
            "X, y = make_classification(n_samples=800, n_features=12, n_informative=6, random_state=42)\n"
            "X[:20, :3] *= 100\n\n"
            "pipe = Pipeline([\n"
            "    ('winsor', WinsorizeTransformer(q=0.05)),\n"
            "    ('log',    SafeLogTransformer()),\n"
            "    ('lr',     LogisticRegression(max_iter=300, random_state=0))\n"
            "])\n"
            "scores = cross_val_score(pipe, X, y, cv=5)\n"
            "print(f'Custom pipeline CV: {scores.mean():.4f} +/- {scores.std():.4f}')"
        ),
        "practice": {
            "title": "Build a ClipTransformer",
            "desc": "Implement a ClipTransformer that clips each feature to [mean - k*std, mean + k*std] where k is a hyperparameter (default=3). It must be sklearn-compatible (BaseEstimator + TransformerMixin). Use it in a Pipeline with LogisticRegression. Grid search over k in [1.5, 2, 2.5, 3] on data with injected outliers.",
            "starter": (
                "import numpy as np\n"
                "from sklearn.base import BaseEstimator, TransformerMixin\n"
                "from sklearn.pipeline import Pipeline\n"
                "from sklearn.linear_model import LogisticRegression\n"
                "from sklearn.model_selection import cross_val_score, GridSearchCV\n"
                "from sklearn.datasets import make_classification\n\n"
                "class ClipTransformer(BaseEstimator, TransformerMixin):\n"
                "    def __init__(self, k=3.0):\n"
                "        self.k = k\n"
                "    def fit(self, X, y=None):\n"
                "        # TODO: store mean_ and std_ for each feature\n"
                "        return self\n"
                "    def transform(self, X):\n"
                "        # TODO: clip to [mean_ - k*std_, mean_ + k*std_]\n"
                "        pass\n\n"
                "np.random.seed(42)\n"
                "X, y = make_classification(n_samples=600, n_features=10, random_state=42)\n"
                "X[:10, :3] *= 50  # inject outliers\n\n"
                "pipe = Pipeline([('clip', ClipTransformer()), ('lr', LogisticRegression(max_iter=200))])\n"
                "# TODO: GridSearchCV over clip__k in [1.5, 2.0, 2.5, 3.0]\n"
                "# TODO: Print best k and best CV score\n"
            ),
        },
    },
    {
        "title": "Model Calibration",
        "desc": "Calibrate classifier probabilities so that a predicted 0.7 means 70% of samples are positive. Use Platt scaling and isotonic regression with reliability diagrams.",
        "code1_title": "Calibration Curve (Reliability Diagram)",
        "code1": (
            "import numpy as np\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.calibration import calibration_curve\n"
            "import matplotlib\n"
            "matplotlib.use('Agg')\n"
            "import matplotlib.pyplot as plt\n\n"
            "np.random.seed(42)\n"
            "X, y = make_classification(n_samples=3000, n_features=20, random_state=42)\n"
            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=42)\n\n"
            "models = {\n"
            "    'Random Forest': RandomForestClassifier(n_estimators=50, random_state=0),\n"
            "    'Logistic Reg':  LogisticRegression(max_iter=200, random_state=0),\n"
            "}\n"
            "fig, ax = plt.subplots(figsize=(6, 6))\n"
            "ax.plot([0,1], [0,1], 'k--', label='Perfect')\n"
            "for name, clf in models.items():\n"
            "    clf.fit(X_tr, y_tr)\n"
            "    prob_pos = clf.predict_proba(X_te)[:, 1]\n"
            "    frac_pos, mean_pred = calibration_curve(y_te, prob_pos, n_bins=10)\n"
            "    ax.plot(mean_pred, frac_pos, 's-', label=name)\n"
            "ax.set_xlabel('Mean predicted probability')\n"
            "ax.set_ylabel('Fraction of positives')\n"
            "ax.set_title('Reliability Diagram'); ax.legend()\n"
            "plt.tight_layout(); plt.savefig('calibration.png', dpi=80); plt.close()\n"
            "print('Saved calibration.png')\n"
            "print('RF is typically overconfident; LR is generally better calibrated.')"
        ),
        "code2_title": "Platt Scaling (Sigmoid Calibration)",
        "code2": (
            "import numpy as np\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.ensemble import RandomForestClassifier\n"
            "from sklearn.calibration import CalibratedClassifierCV\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.metrics import brier_score_loss, log_loss\n\n"
            "np.random.seed(42)\n"
            "X, y = make_classification(n_samples=2000, n_features=20, random_state=42)\n"
            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=42)\n\n"
            "rf = RandomForestClassifier(n_estimators=50, random_state=0)\n"
            "rf.fit(X_tr, y_tr)\n\n"
            "# Platt scaling = sigmoid calibration\n"
            "platt = CalibratedClassifierCV(RandomForestClassifier(n_estimators=50, random_state=0),\n"
            "                               method='sigmoid', cv=5)\n"
            "platt.fit(X_tr, y_tr)\n\n"
            "# Isotonic regression calibration\n"
            "isoton = CalibratedClassifierCV(RandomForestClassifier(n_estimators=50, random_state=0),\n"
            "                                method='isotonic', cv=5)\n"
            "isoton.fit(X_tr, y_tr)\n\n"
            "for name, clf in [('RF (raw)', rf), ('Platt', platt), ('Isotonic', isoton)]:\n"
            "    prob = clf.predict_proba(X_te)[:, 1]\n"
            "    print(f'{name:<15} Brier={brier_score_loss(y_te, prob):.4f} LogLoss={log_loss(y_te, prob):.4f}')"
        ),
        "code3_title": "Expected Calibration Error (ECE)",
        "code3": (
            "import numpy as np\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.ensemble import GradientBoostingClassifier\n"
            "from sklearn.calibration import CalibratedClassifierCV\n"
            "from sklearn.model_selection import train_test_split\n\n"
            "def expected_calibration_error(y_true, y_prob, n_bins=10):\n"
            "    bins = np.linspace(0, 1, n_bins + 1)\n"
            "    ece  = 0.0\n"
            "    for lo, hi in zip(bins[:-1], bins[1:]):\n"
            "        mask = (y_prob >= lo) & (y_prob < hi)\n"
            "        if not mask.any(): continue\n"
            "        frac_pos = y_true[mask].mean()\n"
            "        mean_conf = y_prob[mask].mean()\n"
            "        ece += mask.mean() * abs(frac_pos - mean_conf)\n"
            "    return ece\n\n"
            "np.random.seed(42)\n"
            "X, y = make_classification(n_samples=2000, n_features=20, random_state=42)\n"
            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=42)\n\n"
            "gbm = GradientBoostingClassifier(n_estimators=100, random_state=0).fit(X_tr, y_tr)\n"
            "gbm_cal = CalibratedClassifierCV(\n"
            "    GradientBoostingClassifier(n_estimators=100, random_state=0), method='isotonic', cv=5\n"
            ").fit(X_tr, y_tr)\n\n"
            "for name, clf in [('GBM raw', gbm), ('GBM calibrated', gbm_cal)]:\n"
            "    prob = clf.predict_proba(X_te)[:, 1]\n"
            "    ece  = expected_calibration_error(y_te, prob)\n"
            "    print(f'{name:<18} ECE={ece:.4f}')"
        ),
        "code4_title": "Temperature Scaling (post-hoc calibration)",
        "code4": (
            "import numpy as np\n"
            "from scipy.optimize import minimize_scalar\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.ensemble import GradientBoostingClassifier\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.metrics import log_loss\n\n"
            "def sigmoid(z): return 1 / (1 + np.exp(-z))\n\n"
            "def temperature_scale(logits, T):\n"
            "    return sigmoid(logits / T)\n\n"
            "np.random.seed(42)\n"
            "X, y = make_classification(n_samples=3000, n_features=20, random_state=42)\n"
            "X_tr, X_val, X_te = X[:1500], X[1500:2000], X[2000:]\n"
            "y_tr, y_val, y_te = y[:1500], y[1500:2000], y[2000:]\n\n"
            "gbm = GradientBoostingClassifier(n_estimators=50, random_state=0).fit(X_tr, y_tr)\n\n"
            "# Get raw log-odds on validation set\n"
            "proba_val = gbm.predict_proba(X_val)[:, 1]\n"
            "logits_val = np.log(proba_val + 1e-10) - np.log(1 - proba_val + 1e-10)\n\n"
            "# Optimize temperature on validation set\n"
            "result = minimize_scalar(\n"
            "    lambda T: log_loss(y_val, temperature_scale(logits_val, T)),\n"
            "    bounds=(0.1, 10.0), method='bounded'\n"
            ")\n"
            "T_opt = result.x\n"
            "print(f'Optimal temperature: {T_opt:.3f}')\n\n"
            "proba_te = gbm.predict_proba(X_te)[:, 1]\n"
            "logits_te = np.log(proba_te + 1e-10) - np.log(1 - proba_te + 1e-10)\n"
            "cal_proba = temperature_scale(logits_te, T_opt)\n"
            "print(f'Original  log-loss: {log_loss(y_te, proba_te):.4f}')\n"
            "print(f'Calibrated log-loss: {log_loss(y_te, cal_proba):.4f}')"
        ),
        "rw_scenario": "Risk scoring for loan defaults: the model outputs probabilities, and the business uses score >= 0.3 as the approval threshold. Calibrate so that predicted 0.3 truly means 30% default rate, enabling better risk-adjusted pricing.",
        "rw_code": (
            "import numpy as np\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.ensemble import GradientBoostingClassifier\n"
            "from sklearn.calibration import CalibratedClassifierCV, calibration_curve\n"
            "from sklearn.model_selection import train_test_split\n"
            "from sklearn.metrics import brier_score_loss\n\n"
            "np.random.seed(1)\n"
            "X, y = make_classification(n_samples=5000, n_features=15, weights=[0.8, 0.2], random_state=1)\n"
            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)\n\n"
            "raw = GradientBoostingClassifier(n_estimators=100, random_state=0).fit(X_tr, y_tr)\n"
            "cal = CalibratedClassifierCV(\n"
            "    GradientBoostingClassifier(n_estimators=100, random_state=0),\n"
            "    method='isotonic', cv=5\n"
            ").fit(X_tr, y_tr)\n\n"
            "for name, clf in [('Raw GBM', raw), ('Calibrated', cal)]:\n"
            "    prob = clf.predict_proba(X_te)[:, 1]\n"
            "    frac, mean_pred = calibration_curve(y_te, prob, n_bins=5)\n"
            "    print(f'{name} Brier: {brier_score_loss(y_te, prob):.4f}')\n"
            "    for mp, fp in zip(mean_pred, frac):\n"
            "        print(f'  pred={mp:.2f} -> actual={fp:.2f} (err={abs(fp-mp):.2f})')"
        ),
        "practice": {
            "title": "Calibrate a Random Forest for Insurance Pricing",
            "desc": "Train a Random Forest on imbalanced classification data (10% positive). Compare reliability diagrams (calibration curves) for: (1) raw RF, (2) Platt-calibrated RF, (3) isotonic-calibrated RF. Compute Brier score and ECE for each. Identify which performs best.",
            "starter": (
                "import numpy as np\n"
                "from sklearn.datasets import make_classification\n"
                "from sklearn.ensemble import RandomForestClassifier\n"
                "from sklearn.calibration import CalibratedClassifierCV, calibration_curve\n"
                "from sklearn.model_selection import train_test_split\n"
                "from sklearn.metrics import brier_score_loss\n\n"
                "np.random.seed(42)\n"
                "X, y = make_classification(n_samples=3000, n_features=15, weights=[0.9,0.1], random_state=42)\n"
                "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=0)\n\n"
                "# TODO: Train raw RF\n"
                "# TODO: Calibrate with 'sigmoid' (Platt)\n"
                "# TODO: Calibrate with 'isotonic'\n"
                "# TODO: For each, compute Brier score and print calibration curve values\n"
            ),
        },
    },
    {
        "title": "14. Ensemble Methods: Stacking & Blending",
        "desc": "Combine multiple base learners to build a stronger meta-model. Stacking uses out-of-fold predictions as features for a meta-learner; blending uses a single held-out set. Both reduce variance and capture complementary model strengths.",
        "code1_title": "Stacking with OOF Predictions",
        "code1": (
            "import numpy as np\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.model_selection import cross_val_predict, StratifiedKFold\n"
            "from sklearn.metrics import roc_auc_score\n"
            "\n"
            "X, y = make_classification(n_samples=1000, n_features=20, random_state=42)\n"
            "cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)\n"
            "\n"
            "# Base learners: get out-of-fold predictions\n"
            "rf   = RandomForestClassifier(n_estimators=100, random_state=0)\n"
            "gbm  = GradientBoostingClassifier(n_estimators=100, random_state=1)\n"
            "rf_oof  = cross_val_predict(rf,  X, y, cv=cv, method='predict_proba')[:, 1]\n"
            "gbm_oof = cross_val_predict(gbm, X, y, cv=cv, method='predict_proba')[:, 1]\n"
            "\n"
            "# Stack: meta-learner on OOF predictions\n"
            "import numpy as np\n"
            "X_meta = np.column_stack([rf_oof, gbm_oof])\n"
            "meta = LogisticRegression()\n"
            "meta_oof = cross_val_predict(meta, X_meta, y, cv=cv, method='predict_proba')[:, 1]\n"
            "\n"
            "print(f\"RF AUC:   {roc_auc_score(y, rf_oof):.4f}\")\n"
            "print(f\"GBM AUC:  {roc_auc_score(y, gbm_oof):.4f}\")\n"
            "print(f\"Stack AUC:{roc_auc_score(y, meta_oof):.4f}\")\n"
        ),
        "code2_title": "Blending with Weight Search",
        "code2": (
            "import numpy as np\n"
            "from sklearn.datasets import make_regression\n"
            "from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor\n"
            "from sklearn.linear_model import Ridge\n"
            "from sklearn.model_selection import KFold\n"
            "from sklearn.metrics import mean_squared_error\n"
            "\n"
            "X, y = make_regression(n_samples=800, n_features=15, noise=20, random_state=42)\n"
            "kf = KFold(n_splits=5, shuffle=True, random_state=0)\n"
            "\n"
            "# Blending: single hold-out blend set\n"
            "blend_idx = int(0.8 * len(X))\n"
            "X_tr, X_bl = X[:blend_idx], X[blend_idx:]\n"
            "y_tr, y_bl = y[:blend_idx], y[blend_idx:]\n"
            "\n"
            "rf   = RandomForestRegressor(n_estimators=100, random_state=0).fit(X_tr, y_tr)\n"
            "gbm  = GradientBoostingRegressor(n_estimators=100, random_state=1).fit(X_tr, y_tr)\n"
            "rf_bl  = rf.predict(X_bl)\n"
            "gbm_bl = gbm.predict(X_bl)\n"
            "\n"
            "# Grid search blending weights\n"
            "best_w, best_rmse = 0.5, float('inf')\n"
            "for w in np.arange(0, 1.05, 0.05):\n"
            "    blend = w * rf_bl + (1-w) * gbm_bl\n"
            "    rmse = np.sqrt(mean_squared_error(y_bl, blend))\n"
            "    if rmse < best_rmse:\n"
            "        best_rmse, best_w = rmse, w\n"
            "\n"
            "print(f\"RF   RMSE: {np.sqrt(mean_squared_error(y_bl, rf_bl)):.4f}\")\n"
            "print(f\"GBM  RMSE: {np.sqrt(mean_squared_error(y_bl, gbm_bl)):.4f}\")\n"
            "print(f\"Best blend (w_rf={best_w:.2f}): RMSE={best_rmse:.4f}\")\n"
        ),
        "code3_title": "sklearn StackingClassifier",
        "code3": (
            "import numpy as np\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.ensemble import (RandomForestClassifier, GradientBoostingClassifier,\n"
            "                               ExtraTreesClassifier, StackingClassifier)\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.svm import SVC\n"
            "from sklearn.model_selection import cross_val_score\n"
            "\n"
            "X, y = make_classification(n_samples=1000, n_features=20,\n"
            "                            n_informative=12, random_state=42)\n"
            "estimators = [\n"
            "    ('rf',  RandomForestClassifier(n_estimators=100, random_state=0)),\n"
            "    ('gbm', GradientBoostingClassifier(n_estimators=100, random_state=1)),\n"
            "    ('et',  ExtraTreesClassifier(n_estimators=100, random_state=2)),\n"
            "]\n"
            "stack = StackingClassifier(\n"
            "    estimators=estimators,\n"
            "    final_estimator=LogisticRegression(),\n"
            "    cv=5, passthrough=False\n"
            ")\n"
            "scores = cross_val_score(stack, X, y, cv=5, scoring='roc_auc')\n"
            "print(f\"Stacking AUC: {scores.mean():.4f} +/- {scores.std():.4f}\")\n"
        ),
        "code4_title": "Ensemble Comparison",
        "code4": (
            "import numpy as np\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, BaggingClassifier\n"
            "from sklearn.tree import DecisionTreeClassifier\n"
            "from sklearn.model_selection import cross_val_score\n"
            "from sklearn.metrics import roc_auc_score\n"
            "\n"
            "X, y = make_classification(n_samples=1000, n_features=20, random_state=7)\n"
            "\n"
            "models = {\n"
            "    \"Single Tree\":  DecisionTreeClassifier(max_depth=5),\n"
            "    \"Bagging\":      BaggingClassifier(DecisionTreeClassifier(max_depth=5),\n"
            "                                       n_estimators=50, random_state=0),\n"
            "    \"AdaBoost\":     AdaBoostClassifier(n_estimators=100, random_state=1),\n"
            "    \"Random Forest\":RandomForestClassifier(n_estimators=100, random_state=2),\n"
            "}\n"
            "print(f\"{'Model':<20} {'AUC':>8} {'Std':>6}\")\n"
            "for name, model in models.items():\n"
            "    scores = cross_val_score(model, X, y, cv=5, scoring='roc_auc')\n"
            "    print(f\"{name:<20} {scores.mean():.4f}  {scores.std():.4f}\")\n"
        ),
        "rw_scenario": "Insurance claim prediction: blend Random Forest, GBM, and Logistic Regression using OOF stacking to achieve better AUC than any single model for claims approval.",
        "rw_code": (
            "import numpy as np\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, StackingClassifier\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.model_selection import cross_val_score, StratifiedKFold\n"
            "from sklearn.metrics import roc_auc_score\n"
            "np.random.seed(42)\n"
            "X, y = make_classification(n_samples=2000, n_features=25, n_informative=15, random_state=0)\n"
            "estimators = [\n"
            "    (\"rf\",  RandomForestClassifier(n_estimators=100, random_state=0)),\n"
            "    (\"gbm\", GradientBoostingClassifier(n_estimators=100, random_state=1)),\n"
            "]\n"
            "stack = StackingClassifier(estimators=estimators, final_estimator=LogisticRegression(), cv=5)\n"
            "for name, clf in estimators + [(\"stack\", stack)]:\n"
            "    scores = cross_val_score(clf, X, y, cv=5, scoring=\"roc_auc\")\n"
            "    print(f\"{name:<8}: AUC={scores.mean():.4f} +/- {scores.std():.4f}\")\n"
        ),
        "practice": {
            "title": "Breast Cancer Ensemble",
            "desc": "Build a 3-model stacking classifier on the breast cancer dataset. Compare individual model AUC vs stacking AUC with and without feature passthrough. Also try a weighted average blend and optimize weights by grid search. Report which combination gives the best result.",
            "starter": (
            "import numpy as np\n"
            "from sklearn.datasets import load_breast_cancer\n"
            "from sklearn.ensemble import (RandomForestClassifier, GradientBoostingClassifier,\n"
            "                               StackingClassifier)\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.model_selection import cross_val_predict, StratifiedKFold, cross_val_score\n"
            "from sklearn.metrics import roc_auc_score\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "from sklearn.pipeline import Pipeline\n"
            "\n"
            "X, y = load_breast_cancer(return_X_y=True)\n"
            "# TODO: Build a 3-model stacking ensemble (RF, GBM, SVM or LR)\n"
            "# TODO: Use StratifiedKFold(5) for OOF generation\n"
            "# TODO: Meta-learner: LogisticRegression\n"
            "# TODO: Compare: base models AUC vs stacking AUC\n"
            "# TODO: Add feature passthrough=True and compare again\n"
            "\n"
        ),
        },
    },
    {
        "title": "15. Time-Based Cross-Validation & Walk-Forward Validation",
        "desc": "Use TimeSeriesSplit for realistic CV that respects temporal ordering. Expanding-window and sliding-window strategies prevent future data leakage and simulate production deployment conditions.",
        "code1_title": "Expanding Window CV from Scratch",
        "code1": (
            "import numpy as np\n"
            "import pandas as pd\n"
            "from sklearn.linear_model import Ridge\n"
            "from sklearn.metrics import mean_squared_error\n"
            "\n"
            "np.random.seed(42)\n"
            "n = 500\n"
            "dates = pd.date_range(\"2020-01-01\", periods=n, freq=\"D\")\n"
            "trend  = np.arange(n) * 0.05\n"
            "season = 2 * np.sin(2 * np.pi * np.arange(n) / 7)\n"
            "noise  = np.random.normal(0, 0.5, n)\n"
            "y = trend + season + noise\n"
            "\n"
            "# Time-Series Split: expanding window\n"
            "n_splits = 5\n"
            "split_size = n // (n_splits + 1)\n"
            "results = []\n"
            "for fold in range(n_splits):\n"
            "    train_end = split_size * (fold + 2)\n"
            "    test_end  = train_end + split_size\n"
            "    X_tr = np.column_stack([np.arange(train_end), np.sin(2*np.pi*np.arange(train_end)/7)])\n"
            "    X_te = np.column_stack([np.arange(train_end, test_end),\n"
            "                             np.sin(2*np.pi*np.arange(train_end, test_end)/7)])\n"
            "    m = Ridge().fit(X_tr, y[:train_end])\n"
            "    pred = m.predict(X_te)\n"
            "    rmse = np.sqrt(mean_squared_error(y[train_end:test_end], pred))\n"
            "    results.append(rmse)\n"
            "    print(f\"Fold {fold+1}: train={train_end}, test RMSE={rmse:.4f}\")\n"
            "print(f\"Mean RMSE: {np.mean(results):.4f}\")\n"
        ),
        "code2_title": "TimeSeriesSplit with sklearn Pipeline",
        "code2": (
            "import numpy as np\n"
            "from sklearn.model_selection import TimeSeriesSplit\n"
            "from sklearn.pipeline import Pipeline\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "from sklearn.linear_model import Ridge\n"
            "from sklearn.metrics import mean_squared_error\n"
            "\n"
            "np.random.seed(1)\n"
            "n = 400\n"
            "t = np.arange(n)\n"
            "y = 3*np.sin(2*np.pi*t/30) + 0.02*t + np.random.normal(0, 0.3, n)\n"
            "\n"
            "# Feature engineering: lag features + time features\n"
            "def make_features(t_arr, y_arr, lag=5):\n"
            "    X = np.column_stack([\n"
            "        t_arr,\n"
            "        np.sin(2*np.pi*t_arr/7),\n"
            "        np.sin(2*np.pi*t_arr/30),\n"
            "    ] + [np.roll(y_arr, l) for l in range(1, lag+1)])\n"
            "    return X[lag:]\n"
            "\n"
            "lag = 5\n"
            "X = make_features(t, y, lag)\n"
            "y_lagged = y[lag:]\n"
            "tscv = TimeSeriesSplit(n_splits=5)\n"
            "pipe = Pipeline([(\"scaler\", StandardScaler()), (\"ridge\", Ridge(alpha=1.0))])\n"
            "rmses = []\n"
            "for tr, te in tscv.split(X):\n"
            "    pipe.fit(X[tr], y_lagged[tr])\n"
            "    pred = pipe.predict(X[te])\n"
            "    rmses.append(np.sqrt(mean_squared_error(y_lagged[te], pred)))\n"
            "    print(f\"  RMSE: {rmses[-1]:.4f}\")\n"
            "print(f\"TimeSeriesSplit CV RMSE: {np.mean(rmses):.4f} +/- {np.std(rmses):.4f}\")\n"
        ),
        "code3_title": "Walk-Forward with Gap (prevents leakage)",
        "code3": (
            "import numpy as np\n"
            "from sklearn.model_selection import TimeSeriesSplit\n"
            "from sklearn.ensemble import GradientBoostingRegressor\n"
            "from sklearn.preprocessing import StandardScaler\n"
            "from sklearn.pipeline import Pipeline\n"
            "from sklearn.metrics import mean_squared_error\n"
            "\n"
            "np.random.seed(5)\n"
            "n = 600\n"
            "t = np.arange(n)\n"
            "# Piecewise trend with seasonality\n"
            "y = np.where(t < 300, 0.03*t, 0.01*t + 6) + 2*np.sin(2*np.pi*t/52) + np.random.normal(0, 0.5, n)\n"
            "\n"
            "def make_X(t_arr, y_arr, lag=10):\n"
            "    features = [t_arr % 7, t_arr % 52]  # day-of-week, week-of-year\n"
            "    for l in range(1, lag+1):\n"
            "        features.append(np.roll(y_arr, l))\n"
            "    X = np.column_stack(features)[lag:]\n"
            "    return X\n"
            "\n"
            "X = make_X(t, y, lag=10)\n"
            "y_f = y[10:]\n"
            "tscv = TimeSeriesSplit(n_splits=5, gap=10)\n"
            "results = []\n"
            "for fold, (tr, te) in enumerate(tscv.split(X)):\n"
            "    m = GradientBoostingRegressor(n_estimators=100, max_depth=4, random_state=0)\n"
            "    m.fit(X[tr], y_f[tr])\n"
            "    pred = m.predict(X[te])\n"
            "    rmse = np.sqrt(mean_squared_error(y_f[te], pred))\n"
            "    results.append(rmse)\n"
            "    print(f\"Fold {fold+1} (gap=10): RMSE={rmse:.4f}\")\n"
            "print(f\"Mean RMSE: {np.mean(results):.4f}\")\n"
        ),
        "rw_scenario": "Stock return prediction: use TimeSeriesSplit(n_splits=5, gap=5) to evaluate a GBM model on 3 years of daily data. Prevent look-ahead bias by ensuring a 5-day gap between train and test sets.",
        "rw_code": (
            "import numpy as np\n"
            "from sklearn.model_selection import TimeSeriesSplit\n"
            "from sklearn.ensemble import GradientBoostingRegressor\n"
            "from sklearn.metrics import mean_squared_error\n"
            "np.random.seed(7)\n"
            "n = 750\n"
            "t = np.arange(n)\n"
            "returns = np.random.normal(0.001, 0.02, n)\n"
            "# Lag features\n"
            "X = np.column_stack([np.roll(returns, l) for l in range(1, 11)])[10:]\n"
            "y = returns[10:]\n"
            "tscv = TimeSeriesSplit(n_splits=5, gap=5)\n"
            "results = []\n"
            "for fold, (tr, te) in enumerate(tscv.split(X)):\n"
            "    m = GradientBoostingRegressor(n_estimators=100, max_depth=3, random_state=0)\n"
            "    m.fit(X[tr], y[tr])\n"
            "    pred = m.predict(X[te])\n"
            "    rmse = np.sqrt(mean_squared_error(y[te], pred))\n"
            "    results.append(rmse)\n"
            "    print(f\"Fold {fold+1}: test_size={len(te)}, RMSE={rmse:.6f}\")\n"
            "print(f\"Mean RMSE: {np.mean(results):.6f}\")\n"
        ),
        "practice": {
            "title": "Demand Forecasting Walk-Forward",
            "desc": "Build a walk-forward validation pipeline for 730 days of demand data with weekly and annual seasonality. Compare Ridge, Random Forest, and GBM using TimeSeriesSplit(n_splits=5, gap=7). Report per-fold RMSE and select the best model. Use lag features (1-14 days) plus day-of-week and month features.",
            "starter": (
            "import numpy as np\n"
            "import pandas as pd\n"
            "from sklearn.model_selection import TimeSeriesSplit\n"
            "from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor\n"
            "from sklearn.linear_model import Ridge\n"
            "from sklearn.metrics import mean_squared_error\n"
            "np.random.seed(0)\n"
            "n = 730\n"
            "t = np.arange(n)\n"
            "# Daily demand with weekly + annual seasonality + upward trend\n"
            "demand = (100 + 0.1*t + 20*np.sin(2*np.pi*t/7) +\n"
            "          10*np.sin(2*np.pi*t/365) + np.random.normal(0, 5, n))\n"
            "# TODO: Create lag features (lag 1..14) + time features (dow, month)\n"
            "# TODO: TimeSeriesSplit(n_splits=5, gap=7) walk-forward validation\n"
            "# TODO: Compare Ridge, RF, GBM with CV RMSE\n"
            "# TODO: Report per-fold RMSE and total mean RMSE for each model\n"
            "\n"
        ),
        },
    },
    {
        "title": "16. Interpretable ML: SHAP Values",
        "desc": "SHAP (SHapley Additive exPlanations) provides consistent, theoretically grounded feature attributions for any model. Use TreeExplainer for tree-based models for fast exact SHAP values.",
        "code1_title": "Global Feature Importance with SHAP",
        "code1": (
            "import numpy as np\n"
            "from sklearn.datasets import make_classification\n"
            "from sklearn.ensemble import RandomForestClassifier\n"
            "import shap\n"
            "\n"
            "X, y = make_classification(n_samples=500, n_features=10,\n"
            "                            n_informative=6, random_state=42)\n"
            "feature_names = [f\"feat_{i}\" for i in range(10)]\n"
            "model = RandomForestClassifier(n_estimators=100, random_state=0).fit(X, y)\n"
            "\n"
            "explainer = shap.TreeExplainer(model)\n"
            "shap_values = explainer.shap_values(X[:100])\n"
            "# shap_values[1] = SHAP for class 1\n"
            "print(\"Global feature importance (mean |SHAP|):\")\n"
            "mean_shap = np.abs(shap_values[1]).mean(axis=0)\n"
            "for i in np.argsort(mean_shap)[::-1]:\n"
            "    bar = \"#\" * int(mean_shap[i] * 100)\n"
            "    print(f\"  {feature_names[i]:<12} {mean_shap[i]:.4f}  {bar}\")\n"
        ),
        "code2_title": "Individual Prediction Explanation",
        "code2": (
            "import numpy as np\n"
            "from sklearn.datasets import make_regression\n"
            "from sklearn.ensemble import GradientBoostingRegressor\n"
            "import shap\n"
            "\n"
            "X, y = make_regression(n_samples=400, n_features=8, noise=10, random_state=0)\n"
            "feature_names = [\"age\",\"income\",\"tenure\",\"spend\",\"logins\",\"products\",\"region\",\"segment\"]\n"
            "model = GradientBoostingRegressor(n_estimators=200, random_state=0).fit(X, y)\n"
            "explainer = shap.TreeExplainer(model)\n"
            "shap_values = explainer(X[:50])\n"
            "\n"
            "print(\"Individual explanation for sample 0:\")\n"
            "print(f\"  Base value (expected prediction): {shap_values.base_values[0]:.3f}\")\n"
            "print(f\"  Model output for sample 0:        {model.predict(X[:1])[0]:.3f}\")\n"
            "print(\"  Feature contributions:\")\n"
            "for feat, val in sorted(zip(feature_names, shap_values.values[0]),\n"
            "                         key=lambda x: abs(x[1]), reverse=True):\n"
            "    direction = \"++\" if val > 0 else \"--\"\n"
            "    print(f\"    {direction} {feat:<12}: {val:+.4f}\")\n"
        ),
        "code3_title": "SHAP on Breast Cancer Dataset",
        "code3": (
            "import numpy as np\n"
            "from sklearn.datasets import load_breast_cancer\n"
            "from sklearn.ensemble import GradientBoostingClassifier\n"
            "from sklearn.model_selection import train_test_split\n"
            "import shap\n"
            "\n"
            "X, y = load_breast_cancer(return_X_y=True, as_frame=True)\n"
            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=0)\n"
            "model = GradientBoostingClassifier(n_estimators=100, random_state=0).fit(X_tr, y_tr)\n"
            "\n"
            "explainer = shap.TreeExplainer(model)\n"
            "shap_values = explainer.shap_values(X_te.values)\n"
            "\n"
            "# Summary: top 5 most impactful features globally\n"
            "mean_abs = np.abs(shap_values).mean(axis=0)\n"
            "top5_idx = np.argsort(mean_abs)[::-1][:5]\n"
            "print(\"Top 5 features by mean |SHAP| on test set:\")\n"
            "for i in top5_idx:\n"
            "    feat = X.columns[i]\n"
            "    print(f\"  {feat:<35} mean|SHAP|={mean_abs[i]:.4f}\")\n"
        ),
        "rw_scenario": "Credit scoring: use SHAP to explain individual loan approval/rejection decisions to regulators and customers, identifying the top 3 features driving each decision.",
        "rw_code": (
            "import numpy as np\n"
            "from sklearn.ensemble import GradientBoostingClassifier\n"
            "from sklearn.model_selection import train_test_split\n"
            "import shap\n"
            "np.random.seed(0)\n"
            "n = 1000\n"
            "X = np.random.randn(n, 8)\n"
            "feature_names = [\"credit_score\",\"income\",\"debt_ratio\",\"employment_yrs\",\n"
            "                 \"loan_amount\",\"num_accounts\",\"late_payments\",\"collateral\"]\n"
            "# Simulate default probability\n"
            "prob = 1 / (1 + np.exp(-(X[:,0]*0.8 - X[:,2]*0.6 + X[:,4]*0.4)))\n"
            "y = np.random.binomial(1, prob)\n"
            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=0)\n"
            "model = GradientBoostingClassifier(n_estimators=100, random_state=0).fit(X_tr, y_tr)\n"
            "explainer = shap.TreeExplainer(model)\n"
            "sv = explainer.shap_values(X_te)\n"
            "print(\"Global importance (credit model):\")\n"
            "mean_abs = np.abs(sv).mean(axis=0)\n"
            "for i in np.argsort(mean_abs)[::-1][:5]:\n"
            "    print(f\"  {feature_names[i]:<20}: {mean_abs[i]:.4f}\")\n"
            "print(\"\\nSample 0 explanation:\")\n"
            "for feat, val in sorted(zip(feature_names, sv[0]), key=lambda x: abs(x[1]), reverse=True)[:3]:\n"
            "    print(f\"  {feat}: {val:+.4f}\")\n"
        ),
        "practice": {
            "title": "California Housing SHAP Analysis",
            "desc": "Train a GBM on the California housing dataset and compute SHAP values for 200 test samples. Report global feature importance, explain the 3 highest and 3 lowest predicted houses, and verify SHAP additivity (SHAP values should sum to prediction - expected value).",
            "starter": (
            "import numpy as np\n"
            "import pandas as pd\n"
            "from sklearn.datasets import fetch_california_housing\n"
            "from sklearn.ensemble import GradientBoostingRegressor\n"
            "from sklearn.model_selection import train_test_split\n"
            "import shap\n"
            "\n"
            "housing = fetch_california_housing(as_frame=True)\n"
            "X, y = housing.data, housing.target\n"
            "X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)\n"
            "model = GradientBoostingRegressor(n_estimators=200, max_depth=4, random_state=0)\n"
            "model.fit(X_tr, y_tr)\n"
            "# TODO: Create SHAP TreeExplainer and compute shap_values for X_te[:200]\n"
            "# TODO: Print global feature importance ranking (mean |SHAP|)\n"
            "# TODO: Explain the 3 highest and 3 lowest predicted houses individually\n"
            "# TODO: Check if SHAP values sum to model output - expected value (verify additivity)\n"
            "\n"
        ),
        },
    },

]


def make_html(sections):
    cards = ""
    nav_links = ""
    for i, s in enumerate(sections):
        sid = f"s{i}"
        nav_links += f'<a href="#{sid}">{s["title"]}</a>\n'

        code3_block = ""
        if s.get("code3_title") and s.get("code3"):
            code3_block = f"""    <h4>{s["code3_title"]}</h4>
    <div class="code-wrap"><button class="copy-btn" onclick="copyCode(this)">Copy</button>
    <pre><code class="language-python">{s["code3"]}</code></pre></div>"""

        code4_block = ""
        if s.get("code4_title") and s.get("code4"):
            code4_block = f"""    <h4>{s["code4_title"]}</h4>
    <div class="code-wrap"><button class="copy-btn" onclick="copyCode(this)">Copy</button>
    <pre><code class="language-python">{s["code4"]}</code></pre></div>"""

        practice = s.get("practice", {})
        practice_block = ""
        if practice:
            pid = f"prac-{sid}"
            practice_block = f"""<div class="practice">
      <div class="ph">&#x1F3CB;&#xFE0F; Practice: {practice["title"]}</div>
      <div class="pd">{practice["desc"]}</div>
      <div class="code-wrap"><button class="copy-btn" onclick="copyCode(this)">Copy</button>
      <pre><code id="{pid}" class="language-python">{practice["starter"]}</code></pre></div>
    </div>"""

        cards += f"""
<div class="card" id="{sid}">
  <div class="card-header" onclick="toggle('{sid}')">
    <span>{i+1}. {s["title"]}</span>
    <span class="arrow" id="arr-{sid}">&#9654;</span>
  </div>
  <div class="card-body" id="body-{sid}" style="display:none">
    <p class="desc">{s["desc"]}</p>
    <h4>{s["code1_title"]}</h4>
    <div class="code-wrap"><button class="copy-btn" onclick="copyCode(this)">Copy</button>
    <pre><code class="language-python">{s["code1"]}</code></pre></div>
    <h4>{s["code2_title"]}</h4>
    <div class="code-wrap"><button class="copy-btn" onclick="copyCode(this)">Copy</button>
    <pre><code class="language-python">{s["code2"]}</code></pre></div>
    {code3_block}
    {code4_block}
    <div class="rw">
      <div class="rh">Real-World Use Case</div>
      <div class="rd">{s["rw_scenario"]}</div>
      <div class="code-wrap"><button class="copy-btn" onclick="copyCode(this)">Copy</button>
      <pre><code class="language-python">{s["rw_code"]}</code></pre></div>
    </div>
    {practice_block}
  </div>
</div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Scikit-learn Study Guide</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<style>
:root{{--accent:{ACCENT};--bg:#0d1117;--card:#161b22;--border:#30363d;--text:#e6edf3;--muted:#8b949e;}}
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;display:flex;min-height:100vh;}}
nav{{width:240px;min-height:100vh;background:var(--card);border-right:1px solid var(--border);padding:20px 0;position:sticky;top:0;overflow-y:auto;flex-shrink:0;}}
nav h2{{padding:0 16px 12px;font-size:.85rem;color:var(--accent);text-transform:uppercase;letter-spacing:.08em;}}
nav input{{width:calc(100% - 32px);margin:0 16px 12px;padding:6px 10px;background:#0d1117;border:1px solid var(--border);border-radius:6px;color:var(--text);font-size:.8rem;}}
nav a{{display:block;padding:6px 16px;color:var(--muted);text-decoration:none;font-size:.82rem;border-left:2px solid transparent;transition:.2s;}}
nav a:hover{{color:var(--accent);border-left-color:var(--accent);background:rgba(52,211,153,.05);}}
main{{flex:1;padding:32px;max-width:900px;}}
header{{margin-bottom:32px;}}
header h1{{font-size:2rem;font-weight:700;}}
header h1 span{{color:var(--accent);}}
header p{{color:var(--muted);margin-top:6px;}}
.badge{{display:inline-block;padding:3px 10px;border-radius:20px;font-size:.75rem;font-weight:600;background:rgba(52,211,153,.15);color:var(--accent);border:1px solid rgba(52,211,153,.3);margin-top:8px;}}
.card{{border:1px solid var(--border);border-radius:10px;margin-bottom:16px;overflow:hidden;}}
.card-header{{padding:14px 18px;cursor:pointer;display:flex;justify-content:space-between;align-items:center;background:var(--card);font-weight:600;transition:.2s;}}
.card-header:hover{{background:#1c2128;color:var(--accent);}}
.arrow{{transition:transform .25s;color:var(--accent);}}
.card-body{{padding:18px;background:#0d1117;border-top:1px solid var(--border);}}
.desc{{color:var(--muted);margin-bottom:14px;line-height:1.6;}}
h4{{font-size:.85rem;color:var(--accent);margin:14px 0 6px;text-transform:uppercase;letter-spacing:.06em;}}
.code-wrap{{position:relative;border-radius:8px;overflow:hidden;margin-bottom:12px;}}
pre{{margin:0;overflow-x:auto;}}
pre code{{font-size:.82rem;padding:14px!important;}}
.copy-btn{{position:absolute;top:6px;right:6px;padding:3px 10px;background:#30363d;color:#e6edf3;border:none;border-radius:5px;font-size:.72rem;cursor:pointer;z-index:10;}}
.copy-btn:hover{{background:var(--accent);color:#000;}}
.rw{{background:rgba(52,211,153,.05);border:1px solid rgba(52,211,153,.2);border-radius:8px;padding:14px;margin-top:16px;}}
.rh{{font-weight:700;color:var(--accent);margin-bottom:6px;font-size:.85rem;}}
.rd{{color:var(--muted);margin-bottom:10px;font-size:.85rem;line-height:1.5;}}
.practice{{background:#0d1b2a;border:1px solid #388bfd;border-radius:8px;padding:14px;margin-top:16px;}}
.ph{{font-weight:700;color:#58a6ff;margin-bottom:6px;font-size:.85rem;}}
.pd{{color:#79c0ff;font-size:.85rem;margin-bottom:10px;line-height:1.5;}}
@media(max-width:700px){{nav{{display:none;}}main{{padding:16px;}}}}
</style>
</head>
<body>
<nav>
  <h2>Scikit-learn</h2>
  <input type="text" id="search" placeholder="Search topics..." oninput="filterNav(this.value)">
  {nav_links}
</nav>
<main>
<header>
  <h1>Scikit-<span>learn</span> Study Guide</h1>
  <p>Machine Learning in Python — from data loading to model deployment.</p>
  <span class="badge">10 Topics &bull; Real-World ML</span>
</header>
{cards}
</main>
<script>
hljs.highlightAll();
function toggle(id){{
  var b=document.getElementById('body-'+id),a=document.getElementById('arr-'+id);
  if(b.style.display==='none'){{b.style.display='block';a.style.transform='rotate(90deg)';}}
  else{{b.style.display='none';a.style.transform='';}}
}}
function copyCode(btn){{
  var code=btn.nextElementSibling.querySelector('code');
  navigator.clipboard.writeText(code.innerText).then(function(){{
    btn.textContent='Copied!';setTimeout(function(){{btn.textContent='Copy';}},1500);
  }});
}}
function filterNav(q){{
  document.querySelectorAll('nav a').forEach(function(a){{
    a.style.display=a.textContent.toLowerCase().includes(q.toLowerCase())?'block':'none';
  }});
}}
</script>
</body>
</html>"""


def make_nb(sections):
    cells = []

    def md(src):
        return {"cell_type": "markdown", "metadata": {}, "source": [src]}

    def code(src):
        return {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [src],
        }

    cells.append(md("# Scikit-learn Study Guide\n\nMachine Learning in Python — from data loading to model deployment.\n\n**Topics:** Setup & Data Loading, Linear & Logistic Regression, Decision Trees & Random Forest, SVM, KNN & Naive Bayes, Clustering, Metrics, Pipelines, Hyperparameter Tuning, PCA & t-SNE"))

    for s in sections:
        cells.append(md(f"## {s['title']}\n\n{s['desc']}"))
        cells.append(md(f"### {s['code1_title']}"))
        cells.append(code(s["code1"]))
        cells.append(md(f"### {s['code2_title']}"))
        cells.append(code(s["code2"]))
        if s.get("code3_title") and s.get("code3"):
            cells.append(md(f"### {s['code3_title']}"))
            cells.append(code(s["code3"]))
        if s.get("code4_title") and s.get("code4"):
            cells.append(md(f"### {s['code4_title']}"))
            cells.append(code(s["code4"]))
        cells.append(md(f"### Real-World Use Case\n\n**Scenario:** {s['rw_scenario']}"))
        cells.append(code(s["rw_code"]))
        practice = s.get("practice")
        if practice:
            cells.append(md(f"### Practice: {practice['title']}\n\n{practice['desc']}"))
            cells.append(code(practice["starter"]))

    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.10.0"},
        },
        "cells": cells,
    }


os.makedirs(OUT, exist_ok=True)
html_path = os.path.join(OUT, "index.html")
nb_path = os.path.join(OUT, "study_guide.ipynb")

html = make_html(SECTIONS)
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

nb = make_nb(SECTIONS)
with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

nb_cells = len(nb["cells"])
html_kb = os.path.getsize(html_path) / 1024
print(f"Sklearn guide created: {OUT}")
print(f"  index.html:        {html_kb:.1f} KB")
print(f"  study_guide.ipynb: {nb_cells} cells")
