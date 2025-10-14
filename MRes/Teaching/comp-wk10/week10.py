#!/usr/bin/env python3
"""
COMP2200/COMP6200 Week 10 Practical
===================================

This file contains complete solutions for all parts of the Week 10 practical
on text vectorisation, UMAP visualisation, and logistic regression for spam detection.

Data: enron_practical_sample.csv (text, label columns)
Expected runtime: ~3-5 minutes for full execution
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_validate, StratifiedKFold
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, f1_score, confusion_matrix,
    classification_report, ConfusionMatrixDisplay
)
import umap
from sklearn.utils import Bunch
import warnings
warnings.filterwarnings('ignore')  # Suppress convergence warnings for cleaner output

# Set random seed for reproducibility
RANDOM_STATE = 2025

print("=" * 80)
print("WEEK 10 PRACTICAL - COMPLETE SOLUTIONS")
print("=" * 80)

# ==============================================================================
# DATA LOADING AND TRAIN/TEST SPLIT
# ==============================================================================
print("\n[STEP 0] Loading data and creating train/test split")
print("-" * 80)

# Creating a proper hold-out test set before any experimentation to
# avoid data leakage
emails = pd.read_csv("enron_practical_sample.csv")

print(f"Total emails loaded: {len(emails)}")
print(f"Class distribution:\n{emails['label'].value_counts()}")
print(f"Class proportions:\n{emails['label'].value_counts(normalize=True)}")

# We use stratify to maintain class balance in both sets This is
# crucial when dealing with potentially imbalanced datasets
train_df, test_df = train_test_split(
    emails,
    test_size=0.2,
    random_state=RANDOM_STATE,
    stratify=emails['label']
)

train_text = train_df['text']
train_labels = train_df['label']
test_text = test_df['text']
test_labels = test_df['label']

print(f"\nTrain set: {len(train_df)} emails")
print(f"Test set: {len(test_df)} emails")
print(f"Train class distribution:\n{train_labels.value_counts()}")


# ==============================================================================
# PART A: TOKENISATION TUNING LAB (20 min)
# ==============================================================================
print("\n" + "=" * 80)
print("PART A: TOKENISATION TUNING LAB")
print("=" * 80)

def analyze_vectoriser(vectoriser, X_train, config_name):
    """Helper function to analyze and display vectoriser characteristics.

    This encapsulation makes it easy to experiment with different
    configurations systematically.

    """
    print(f"\n--- Configuration: {config_name} ---")

    # Vocabulary size
    vocab_size = len(vectoriser.vocabulary_)
    print(f"Vocabulary size: {vocab_size:,}")

    # Top 10 weighted terms (highest IDF scores)
    if hasattr(vectoriser, 'idf_'):
        idf_series = pd.Series(
            vectoriser.idf_,
            index=vectoriser.get_feature_names_out()
        )
        top_10_terms = idf_series.nlargest(10)
        print(f"\nTop 10 weighted terms (highest IDF = rarest/most distinctive):")
        for term, idf in top_10_terms.items():
            print(f"  {term:30s} IDF: {idf:.4f}")
    else:
        # For CountVectorizer, show term frequencies instead
        term_frequencies = pd.Series(
            X_train.sum(axis=0).A1,
            index=vectoriser.get_feature_names_out()
        )
        top_10_terms = term_frequencies.nlargest(10)
        print(f"\nTop 10 most frequent terms:")
        for term, freq in top_10_terms.items():
            print(f"  {term:30s} Frequency: {int(freq)}")

    # Show a few example features to illustrate the configuration
    features = vectoriser.get_feature_names_out()
    print(f"\nSample features (first 10): {list(features[:10])}")
    if len(features) > 10:
        print(f"Sample features (last 10): {list(features[-10:])}")

    return vocab_size, top_10_terms


# Configuration 1: Baseline TF-IDF with word unigrams
print("\n[Config 1] BASELINE: TF-IDF with word unigrams")
vectoriser_baseline = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 1)
)
X_train_baseline = vectoriser_baseline.fit_transform(train_text)
analyze_vectoriser(vectoriser_baseline, X_train_baseline, "Baseline (word unigrams)")

# Notice that common English words are filtered out
# and the vocabulary contains many domain-specific terms


# Configuration 2: Character n-grams
print("\n[Config 2] CHARACTER N-GRAMS (3-5 characters)")
# Character n-grams can capture subword patterns and are robust
# to typos, useful for spam detection where spelling variations are common
vectoriser_char = TfidfVectorizer(
    analyzer="char_wb",  # char_wb includes word boundaries
    ngram_range=(3, 5),
    stop_words=None  # stop_words not relevant for character n-grams
)
X_train_char = vectoriser_char.fit_transform(train_text)
analyze_vectoriser(vectoriser_char, X_train_char, "Character n-grams (3-5)")

# Try analyzer="char" (without word boundaries)
# This would capture patterns across word boundaries, which might be less useful


# Configuration 3: Frequency trims
print("\n[Config 3] FREQUENCY TRIMS (min_df=2, max_df=0.8)")
# min_df removes very rare terms (might be typos or outliers)
# max_df removes very common terms (might be uninformative)
vectoriser_freq = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 1),
    min_df=2,      # Term must appear in at least 2 documents
    max_df=0.8     # Term must appear in at most 80% of documents
)
X_train_freq = vectoriser_freq.fit_transform(train_text)
analyze_vectoriser(vectoriser_freq, X_train_freq, "Frequency trims")

# Vocabulary should be significantly smaller than baseline
# This reduces overfitting and improves generalization


# Configuration 4: Bigrams
print("\n[Config 4] BIGRAMS (1-2 word n-grams)")
# Bigrams capture common phrases like "nigerian prince"
# or "click here" which might be strong spam indicators
vectoriser_bigrams = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2)  # Both unigrams and bigrams
)
X_train_bigrams = vectoriser_bigrams.fit_transform(train_text)
analyze_vectoriser(vectoriser_bigrams, X_train_bigrams, "Bigrams (1-2)")

# Try ngram_range=(2, 2) for bigrams only
# or ngram_range=(1, 3) for trigrams as well




# ==============================================================================
# PART B: UMAP VISUALISATION (20 min)
# ==============================================================================
print("\n" + "=" * 80)
print("PART B: UMAP VISUALISATION")
print("=" * 80)

# [TEACHING POINT] Visualization helps build intuition about data separability
# before jumping into classification

print("\n[STEP 1] Creating TF-IDF representation for visualization")

# Combine all text for visualization
all_text = pd.concat([train_text, test_text])
all_labels = pd.concat([train_labels, test_labels])

# Vectorize with moderate feature budget
# We use max_features to keep dimensionality manageable for UMAP
vectoriser_viz = TfidfVectorizer(max_features=1000, stop_words="english")
X_tfidf = vectoriser_viz.fit_transform(all_text)

print(f"TF-IDF matrix shape: {X_tfidf.shape}")
print(f"Number of features: {X_tfidf.shape[1]}")
print(f"Matrix sparsity: {(1 - X_tfidf.nnz / (X_tfidf.shape[0] * X_tfidf.shape[1])) * 100:.2f}%")

print("\n[STEP 2] Reducing to 2D with UMAP")
# UMAP preserves both local and global structure
# n_neighbors controls balance between local/global structure
reducer = umap.UMAP(
    n_components=2,
    random_state=RANDOM_STATE,
    n_neighbors=15,
    min_dist=0.1,
    metric='cosine'  # Appropriate for TF-IDF vectors
)
embedding = reducer.fit_transform(X_tfidf)

print(f"UMAP embedding shape: {embedding.shape}")
print(f"Embedding ranges: X=[{embedding[:, 0].min():.2f}, {embedding[:, 0].max():.2f}], "
      f"Y=[{embedding[:, 1].min():.2f}, {embedding[:, 1].max():.2f}]")

print("\n[STEP 3] Creating visualization")

plt.figure(figsize=(12, 10))

# Create scatter plot with color coding
# We use alpha for transparency to show density
scatter = sns.scatterplot(
    x=embedding[:, 0],
    y=embedding[:, 1],
    hue=all_labels,
    palette={"ham": "#2ecc71", "spam": "#e74c3c"},
    alpha=0.5,
    s=30,
    edgecolor=None
)

plt.title("UMAP Projection of Enron Emails (TF-IDF, 1000 features)", fontsize=14, pad=20)
plt.xlabel("UMAP Component 1", fontsize=12)
plt.ylabel("UMAP Component 2", fontsize=12)
plt.legend(title="Label", fontsize=11)
plt.tight_layout()

# Save figure for reference
plt.savefig("umap_visualization.png", dpi=150, bbox_inches='tight')
print("Visualization saved as: umap_visualization.png")
plt.close()

# Analysis of separability
print("\n[STEP 4] Analyzing class separability")

# Calculate centroids
spam_points = embedding[all_labels == 'spam']
ham_points = embedding[all_labels == 'ham']

spam_centroid = spam_points.mean(axis=0)
ham_centroid = ham_points.mean(axis=0)

centroid_distance = np.linalg.norm(spam_centroid - ham_centroid)

print(f"Spam centroid: ({spam_centroid[0]:.2f}, {spam_centroid[1]:.2f})")
print(f"Ham centroid: ({ham_centroid[0]:.2f}, {ham_centroid[1]:.2f})")
print(f"Distance between centroids: {centroid_distance:.2f}")

# Calculate within-class spread
spam_spread = np.linalg.norm(spam_points - spam_centroid, axis=1).mean()
ham_spread = np.linalg.norm(ham_points - ham_centroid, axis=1).mean()

print(f"Spam cluster spread (avg distance from centroid): {spam_spread:.2f}")
print(f"Ham cluster spread (avg distance from centroid): {ham_spread:.2f}")


# [VARIATION] Optional: Test different n_neighbors values
print("\n[OPTIONAL] Testing different n_neighbors values:")
for n_neighbors in [5, 15, 50]:
    reducer_test = umap.UMAP(
        n_components=2,
        random_state=RANDOM_STATE,
        n_neighbors=n_neighbors,
        min_dist=0.1,
        metric='cosine'
    )
    embedding_test = reducer_test.fit_transform(X_tfidf)

    # Calculate separation metric
    spam_test = embedding_test[all_labels == 'spam']
    ham_test = embedding_test[all_labels == 'ham']
    centroid_dist = np.linalg.norm(spam_test.mean(axis=0) - ham_test.mean(axis=0))

    print(f"  n_neighbors={n_neighbors:2d}: centroid distance = {centroid_dist:.2f}")


# ==============================================================================
# PART C: FEATURE BUDGET CHALLENGE (40 min)
# ==============================================================================
print("\n" + "=" * 80)
print("PART C: FEATURE BUDGET CHALLENGE (max 1000 features)")
print("=" * 80)

# This section demonstrates systematic hyperparameter exploration

print("\n[TESTING MULTIPLE CONFIGURATIONS]")

# Store results for comparison
results = []

def test_configuration(config_name, vectoriser_params):
    """
    Test a vectoriser configuration with cross-validation.

    Encapsulating this in a function prevents code duplication
    and makes it easier to test many configurations systematically.
    """
    pipeline = Pipeline([
        ("vectoriser", TfidfVectorizer(**vectoriser_params)),
        ("model", LogisticRegression(max_iter=500, random_state=RANDOM_STATE))
    ])

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

    # [TEACHING POINT] We use cross_validate to get both train and test scores
    # This helps detect overfitting (high train score, low test score)
    metrics = cross_validate(
        pipeline, train_text, train_labels,
        cv=cv,
        scoring=["accuracy", "f1_macro"],
        return_train_score=True
    )

    result = {
        'configuration': config_name,
        'params': vectoriser_params,
        'train_accuracy': metrics['train_accuracy'].mean(),
        'test_accuracy': metrics['test_accuracy'].mean(),
        'train_f1': metrics['train_f1_macro'].mean(),
        'test_f1': metrics['test_f1_macro'].mean(),
        'std_f1': metrics['test_f1_macro'].std()
    }

    results.append(result)

    print(f"\n{config_name}:")
    print(f"  Params: {vectoriser_params}")
    print(f"  Train Accuracy: {result['train_accuracy']:.4f}")
    print(f"  Test Accuracy:  {result['test_accuracy']:.4f}")
    print(f"  Train F1:       {result['train_f1']:.4f}")
    print(f"  Test F1:        {result['test_f1']:.4f} (+/- {result['std_f1']:.4f})")

    # Potential overfitting
    overfit_gap = result['train_f1'] - result['test_f1']
    if overfit_gap > 0.05:
        print(f"  ⚠ Overfitting detected (gap: {overfit_gap:.4f})")

    return result


# Test Configuration 1: Baseline
test_configuration(
    "Config 1: Baseline",
    {
        'max_features': 1000,
        'stop_words': 'english',
        'ngram_range': (1, 1)
    }
)

# Test Configuration 2: With bigrams
test_configuration(
    "Config 2: Unigrams + Bigrams",
    {
        'max_features': 1000,
        'stop_words': 'english',
        'ngram_range': (1, 2)
    }
)

# Test Configuration 3: With frequency filtering
test_configuration(
    "Config 3: Frequency filtering",
    {
        'max_features': 1000,
        'stop_words': 'english',
        'ngram_range': (1, 1),
        'min_df': 2,
        'max_df': 0.9
    }
)

# Test Configuration 4: Bigrams + frequency filtering
test_configuration(
    "Config 4: Bigrams + frequency filtering",
    {
        'max_features': 1000,
        'stop_words': 'english',
        'ngram_range': (1, 2),
        'min_df': 2,
        'max_df': 0.9
    }
)

# Test Configuration 5: Sublinear TF scaling
# Sublinear TF uses log(tf) instead of raw tf
# This reduces the impact of very frequent terms within a document
test_configuration(
    "Config 5: Sublinear TF + bigrams",
    {
        'max_features': 1000,
        'stop_words': 'english',
        'ngram_range': (1, 2),
        'sublinear_tf': True,
        'min_df': 2
    }
)

# Test Configuration 6: Character n-grams (for comparison)
test_configuration(
    "Config 6: Character n-grams",
    {
        'max_features': 1000,
        'analyzer': 'char_wb',
        'ngram_range': (3, 5)
    }
)

# Also try:
# - Different max_features values (500, 750, 1000)
# - Different ngram ranges (1-3, 2-3)
# - norm='l1' vs norm='l2'
# - Different min_df/max_df thresholds


# Select best configuration based on test F1 score
print("\n" + "-" * 80)
print("CONFIGURATION COMPARISON:")
print("-" * 80)

results_df = pd.DataFrame(results)
results_df = results_df.sort_values('test_f1', ascending=False)

print(results_df[['configuration', 'test_accuracy', 'test_f1', 'std_f1']].to_string(index=False))

best_config = results_df.iloc[0]
print(f"\n🏆 Best configuration: {best_config['configuration']}")
print(f"   Test F1: {best_config['test_f1']:.4f} (+/- {best_config['std_f1']:.4f})")

# The "best" configuration might vary with data
# What matters is the systematic process and understanding trade-offs


# Final evaluation on held-out test set
print("\n" + "-" * 80)
print("FINAL EVALUATION ON HELD-OUT TEST SET:")
print("-" * 80)

# Only now do we use the test set we held out at the beginning
# This gives us an unbiased estimate of real-world performance

best_params = best_config['params']
final_pipeline = Pipeline([
    ("vectoriser", TfidfVectorizer(**best_params)),
    ("model", LogisticRegression(max_iter=500, random_state=RANDOM_STATE))
])

final_pipeline.fit(train_text, train_labels)
test_predictions = final_pipeline.predict(test_text)
test_probabilities = final_pipeline.predict_proba(test_text)

# Calculate metrics
test_accuracy = accuracy_score(test_labels, test_predictions)
test_f1 = f1_score(test_labels, test_predictions, pos_label='spam', average='macro')

print(f"Test Accuracy: {test_accuracy:.4f}")
print(f"Test F1 (macro): {test_f1:.4f}")

# Macro F1 treats both classes equally This is important when classes
# might be imbalanced

print("\nClassification Report:")
print(classification_report(test_labels, test_predictions))

print("\nConfusion Matrix:")
cm = confusion_matrix(test_labels, test_predictions)
print(cm)

# Create visual confusion matrix
fig, ax = plt.subplots(figsize=(8, 6))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['ham', 'spam'])
disp.plot(ax=ax, cmap='Blues', values_format='d')
plt.title("Confusion Matrix - Final Model on Test Set")
plt.tight_layout()
plt.savefig("confusion_matrix.png", dpi=150, bbox_inches='tight')
print("Confusion matrix saved as: confusion_matrix.png")
plt.close()

print("\nConfusion Matrix Interpretation:")
tn, fp, fn, tp = cm.ravel()
print(f"  True Negatives (Ham correctly classified):  {tn}")
print(f"  False Positives (Ham incorrectly as Spam):  {fp}")
print(f"  False Negatives (Spam incorrectly as Ham):  {fn}")
print(f"  True Positives (Spam correctly classified): {tp}")
print(f"\n  [TEACHING POINT] Which error is worse?")
print(f"  → FP: Legitimate email goes to spam (user might miss important email)")
print(f"  → FN: Spam goes to inbox (user sees spam)")
print(f"  → Typically, FP is considered worse in email filtering!")


# ==============================================================================
# OPTIONAL: Smaller vocabulary challenge
# ==============================================================================
print("\n" + "-" * 80)
print("[OPTIONAL] HOW SMALL CAN WE GO?")
print("-" * 80)

# This shows the trade-off between model size and performance
# Useful for deployment scenarios with memory constraints

for n_features in [100, 250, 500, 1000]:
    pipeline_small = Pipeline([
        ("vectoriser", TfidfVectorizer(**{**best_params, 'max_features': n_features})),
        ("model", LogisticRegression(max_iter=500, random_state=RANDOM_STATE))
    ])

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    metrics = cross_validate(
        pipeline_small, train_text, train_labels,
        cv=cv, scoring=['f1_macro']
    )

    mean_f1 = metrics['test_f1_macro'].mean()
    std_f1 = metrics['test_f1_macro'].std()

    print(f"max_features={n_features:4d}: F1 = {mean_f1:.4f} (+/- {std_f1:.4f})")

print("\nDiminishing returns - going from 500→1000 features")
print("often provides minimal improvement but doubles memory/computation cost")


# ==============================================================================
# PART D: REGULARISATION AND COEFFICIENT STORYTELLING (30 min)
# ==============================================================================
print("\n" + "=" * 80)
print("PART D: REGULARISATION AND COEFFICIENT STORYTELLING")
print("=" * 80)

# This section connects model internals to interpretability

def train_with_c(C=1.0, penalty="l2") -> Bunch:
    """
    Train a model with specified regularization and return coefficients.

    [TEACHING POINT] C is the inverse of regularization strength:
    - Small C = strong regularization = smaller coefficients
    - Large C = weak regularization = larger coefficients
    """
    pipeline = Pipeline([
        ("vectoriser", TfidfVectorizer(**best_params)),
        ("model", LogisticRegression(
            max_iter=1000,
            C=C,
            penalty=penalty,
            solver="liblinear" if penalty == "l1" else "lbfgs",
            random_state=RANDOM_STATE
        ))
    ])

    pipeline.fit(train_text, train_labels)

    # Get predictions on test set
    test_preds = pipeline.predict(test_text)
    test_acc = accuracy_score(test_labels, test_preds)
    test_f1 = f1_score(test_labels, test_preds, pos_label='spam', average='macro')

    return Bunch(
        pipeline=pipeline,
        coefficients=pipeline.named_steps["model"].coef_[0],
        vocab=pipeline.named_steps["vectoriser"].get_feature_names_out(),
        C=C,
        penalty=penalty,
        test_accuracy=test_acc,
        test_f1=test_f1
    )


print("\n[TESTING DIFFERENT REGULARIZATION STRENGTHS]")

# Test different C values with L2 regularization
c_values = [0.1, 1.0, 10.0]
models_l2 = {}

for C in c_values:
    print(f"\nTraining with C={C} (L2 penalty)")
    model_result = train_with_c(C=C, penalty="l2")
    models_l2[C] = model_result

    # Calculate coefficient statistics
    coef_mean = np.abs(model_result.coefficients).mean()
    coef_max = np.abs(model_result.coefficients).max()
    coef_nonzero = np.sum(model_result.coefficients != 0)

    print(f"  Test Accuracy: {model_result.test_accuracy:.4f}")
    print(f"  Test F1: {model_result.test_f1:.4f}")
    print(f"  Mean |coefficient|: {coef_mean:.4f}")
    print(f"  Max |coefficient|: {coef_max:.4f}")
    print(f"  Non-zero coefficients: {coef_nonzero}/{len(model_result.coefficients)}")

# Smaller C should give smaller coefficients and potentially better generalization


# Test L1 regularization (for comparison)
print(f"\nTraining with C=1.0 (L1 penalty)")
model_l1 = train_with_c(C=1.0, penalty="l1")

coef_mean_l1 = np.abs(model_l1.coefficients).mean()
coef_max_l1 = np.abs(model_l1.coefficients).max()
coef_nonzero_l1 = np.sum(model_l1.coefficients != 0)
coef_zero_l1 = np.sum(model_l1.coefficients == 0)

print(f"  Test Accuracy: {model_l1.test_accuracy:.4f}")
print(f"  Test F1: {model_l1.test_f1:.4f}")
print(f"  Mean |coefficient|: {coef_mean_l1:.4f}")
print(f"  Max |coefficient|: {coef_max_l1:.4f}")
print(f"  Non-zero coefficients: {coef_nonzero_l1}/{len(model_l1.coefficients)}")
print(f"  Zero coefficients: {coef_zero_l1}/{len(model_l1.coefficients)}")

# L1 penalty promotes sparsity - many coefficients become exactly zero
# This effectively performs feature selection
print("\n[TEACHING POINT] L1 vs L2:")
print(f"  L2 shrinks all coefficients but rarely to exactly zero")
print(f"  L1 sets many coefficients to exactly zero (feature selection)")
print(f"  L1 gave {coef_zero_l1} zero coefficients ({coef_zero_l1/len(model_l1.coefficients)*100:.1f}%)")


# Analyze coefficients from best model (we'll use C=1.0, L2 as default)
print("\n" + "-" * 80)
print("COEFFICIENT ANALYSIS (C=1.0, L2):")
print("-" * 80)

best_model = models_l2[1.0]  # C=1.0 is usually a good default

# Create DataFrame of coefficients
coef_df = pd.DataFrame({
    'feature': best_model.vocab,
    'coefficient': best_model.coefficients
})

# Sort by coefficient value
coef_df = coef_df.sort_values('coefficient', ascending=False)

# Top 10 positive coefficients (push toward spam)
print("\nTop 10 features pushing toward SPAM (highest positive coefficients):")
top_spam = coef_df.head(10)
for idx, row in top_spam.iterrows():
    print(f"  {row['feature']:30s} → {row['coefficient']:+.4f}")

# Top 10 negative coefficients (push toward ham)
print("\nTop 10 features pushing toward HAM (most negative coefficients):")
top_ham = coef_df.tail(10)
for idx, row in top_ham.iterrows():
    print(f"  {row['feature']:30s} → {row['coefficient']:+.4f}")

# Translate to plain language rules
print("\n" + "-" * 80)
print("PLAIN LANGUAGE INTERPRETATION:")
print("-" * 80)
print("""
[TEACHING POINT] Each coefficient represents a learned "rule":

SPAM INDICATORS (positive coefficients):
""")

for idx, row in top_spam.head(5).iterrows():
    feature = row['feature']
    coef = row['coefficient']
    print(f"  • If email contains '{feature}', "
          f"increase spam score by {coef:.2f}")

    # Provide context about why this might indicate spam
    if any(word in feature.lower() for word in ['click', 'free', 'win', 'money', 'offer']):
        print(f"    → Common marketing/scam language")
    elif any(word in feature.lower() for word in ['http', 'www', '.com']):
        print(f"    → Spam often contains many links")

print("""
HAM INDICATORS (negative coefficients):
""")

for idx, row in top_ham.tail(5).iterrows():
    feature = row['feature']
    coef = row['coefficient']
    print(f"  • If email contains '{feature}', "
          f"decrease spam score by {abs(coef):.2f}")

    # [TEACHING POINT] Provide context about why this might indicate ham
    if any(word in feature.lower() for word in ['meeting', 'schedule', 'team', 'project']):
        print(f"    → Common legitimate business communication")
    elif any(word in feature.lower() for word in ['thank', 'please', 'regards']):
        print(f"    → Polite professional language")


# Visualize coefficient magnitudes across different C values
print("\n[Creating coefficient magnitude comparison plot]")

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for idx, C in enumerate(c_values):
    model = models_l2[C]
    coef_sorted = np.sort(np.abs(model.coefficients))[::-1]  # Sort by magnitude

    axes[idx].plot(coef_sorted, linewidth=2)
    axes[idx].set_xlabel('Feature rank')
    axes[idx].set_ylabel('|Coefficient|')
    axes[idx].set_title(f'C={C}\n(Test F1: {model.test_f1:.3f})')
    axes[idx].set_yscale('log')
    axes[idx].grid(True, alpha=0.3)

plt.suptitle('Coefficient Magnitudes vs. Regularization Strength\n(smaller C = stronger regularization = smaller coefficients)')
plt.tight_layout()
plt.savefig("coefficient_magnitudes.png", dpi=150, bbox_inches='tight')
print("Coefficient magnitude plot saved as: coefficient_magnitudes.png")
plt.close()

# Should observe:
# - Smaller C → flatter curve (more regularization shrinks all coefficients)
# - Larger C → steeper curve (less regularization allows larger coefficients)
# - Trade-off: too much regularization underfits, too little overfits


# ==============================================================================
# PART E (OPTIONAL): ERROR CLINIC AND MODERATION HUDDLE (10 min)
# ==============================================================================
print("\n" + "=" * 80)
print("PART E (OPTIONAL): ERROR CLINIC")
print("=" * 80)

# Analyzing errors helps improve models and understand limitations

# Get predictions and probabilities on test set
test_predictions = best_model.pipeline.predict(test_text)
test_probabilities = best_model.pipeline.predict_proba(test_text)

# Create DataFrame of misclassifications
misclassified_mask = test_predictions != test_labels
misclassifications = pd.DataFrame({
    'text': test_text.values[misclassified_mask],
    'true_label': test_labels.values[misclassified_mask],
    'predicted': test_predictions[misclassified_mask],
    'probability': test_probabilities[misclassified_mask].max(axis=1)
})

print(f"\nTotal misclassifications: {len(misclassifications)} / {len(test_text)} "
      f"({len(misclassifications)/len(test_text)*100:.1f}%)")

# Analyze misclassification types
false_positives = misclassifications[misclassifications['true_label'] == 'ham']
false_negatives = misclassifications[misclassifications['true_label'] == 'spam']

print(f"\nFalse Positives (Ham → Spam): {len(false_positives)}")
print(f"False Negatives (Spam → Ham): {len(false_negatives)}")

# Show examples of high-confidence errors (most interesting)
print("\n" + "-" * 80)
print("HIGH-CONFIDENCE ERRORS (model was confident but wrong):")
print("-" * 80)

high_confidence_errors = misclassifications[misclassifications['probability'] > 0.8]
high_confidence_errors = high_confidence_errors.sort_values('probability', ascending=False)

print(f"\nFound {len(high_confidence_errors)} high-confidence errors (prob > 0.8)")

if len(high_confidence_errors) > 0:
    print("\nTop 3 high-confidence errors:")
    for i, (idx, row) in enumerate(high_confidence_errors.head(3).iterrows()):
        print(f"\nError #{i+1}:")
        print(f"  True label: {row['true_label']}")
        print(f"  Predicted:  {row['predicted']} (confidence: {row['probability']:.3f})")
        print(f"  Text preview: {row['text'][:200]}...")
        print(f"\n  [TEACHING POINT] Ask students to categorize this error:")
        print(f"    - Ambiguous tone (could reasonably be either class)?")
        print(f"    - Missing vocabulary (uses words not in training)?")
        print(f"    - Label noise (was it mislabeled in the dataset)?")
else:
    print("No high-confidence errors found - model is well-calibrated!")

# Analyze confidence distribution
print("\n" + "-" * 80)
print("CONFIDENCE CALIBRATION:")
print("-" * 80)

# A well-calibrated model should be more confident when correct
correct_mask = test_predictions == test_labels
correct_confidences = test_probabilities[correct_mask].max(axis=1)
incorrect_confidences = test_probabilities[~correct_mask].max(axis=1)

print(f"Average confidence when correct: {correct_confidences.mean():.3f}")
print(f"Average confidence when incorrect: {incorrect_confidences.mean():.3f}")

if correct_confidences.mean() > incorrect_confidences.mean():
    print("✓ Model is reasonably well-calibrated (more confident when correct)")
else:
    print("⚠ Model calibration issue (equally/more confident when wrong)")

# Possible additional visualizations:
# - Confidence histogram comparing correct vs. incorrect predictions
# - Text length analysis (do longer/shorter emails get misclassified more?)
# - Feature presence analysis (which features appear in misclassified emails?)


print("\n" + "=" * 80)
print("SOLUTIONS FILE COMPLETE")
print("=" * 80)
print("\nGenerated files:")
print("  - umap_visualization.png")
print("  - confusion_matrix.png")
print("  - coefficient_magnitudes.png")
