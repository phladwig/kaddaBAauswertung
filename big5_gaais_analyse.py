"""
Statistische Auswertung: Big5 Persönlichkeitsmerkmale und GAAIS
"""

import sys
import io

# Windows-Konsole Encoding fix
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        # Fallback für ältere Python-Versionen
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try:
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from scipy import stats
    from scipy.stats import pearsonr, spearmanr
    import warnings
    warnings.filterwarnings('ignore')
except ImportError as e:
    print(f"Fehler: Benoetigtes Paket nicht gefunden: {e}")
    print("\nBitte installieren Sie die benoetigten Pakete mit:")
    print("python -m pip install pandas numpy scipy matplotlib seaborn scikit-learn pyreadstat")
    exit(1)

# Stil für Plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

# Daten laden
print("=" * 80)
print("STATISTISCHE AUSWERTUNG: BIG5 PERSOENLICHKEITSMERKMALE UND GAAIS")
print("=" * 80)

# Versuche zuerst CSV zu laden (einfacher, keine zusätzlichen Pakete nötig)
df = None
try:
    df = pd.read_csv("KIPM_statistische Auswertung_20251116_1759_nach Rohwerten bereinigte Daten.csv", 
                    sep=';', encoding='utf-8', decimal=',')
    print("\n[OK] Daten aus CSV Datei geladen")
except Exception as e2:
    # Fallback: Versuche .sav Datei zu laden
    try:
        import pyreadstat
        df, meta = pyreadstat.read_sav("KIPM_statistische Auswertung_20251116_1759_nach Rohwerten bereinigte Daten.sav")
        print("\n[OK] Daten aus .sav Datei geladen")
    except Exception as e:
        print(f"\n[FEHLER] Fehler beim Laden der Daten:")
        print(f"  CSV Fehler: {e2}")
        print(f"  .sav Fehler: {e}")
        exit(1)

print(f"\nDatenstruktur: {df.shape[0]} Zeilen, {df.shape[1]} Spalten")

# Big5 Variablen identifizieren
big5_vars = {
    'Offenheit': ['Offenheit', 'Offenheit_MEAN'],
    'Gewissenhaftigkeit': ['Gewissenhaftigkeit', 'Gewissenhaftigkeit_MEAN'],
    'Extraversion': ['Extraversion', 'Extraversion_MEAN'],
    'Verträglichkeit': ['Verträglichkeit', 'Verträglichkeit_MEAN'],
    'Neurotizismus': ['Neurotizismus', 'Neurotizismus_MEAN']
}

# GAAIS Variablen identifizieren
gaais_vars = {
    'GAAIS_positiv': ['GAAIS_positiv', 'GAAIS_positiv_MEAN'],
    'GAAIS_negativ': ['GAAIS_negativ', 'GAAIS_negativ_MEAN']
}

# Verfügbare Variablen finden
big5_available = {}
for trait, variants in big5_vars.items():
    for var in variants:
        if var in df.columns:
            big5_available[trait] = var
            break

gaais_available = {}
for trait, variants in gaais_vars.items():
    for var in variants:
        if var in df.columns:
            gaais_available[trait] = var
            break

print(f"\nGefundene Big5 Variablen: {list(big5_available.keys())}")
print(f"Gefundene GAAIS Variablen: {list(gaais_available.keys())}")

# Numerische Spalten für Big5 und GAAIS extrahieren
big5_data = df[[col for col in big5_available.values() if col in df.columns]].copy()
gaais_data = df[[col for col in gaais_available.values() if col in df.columns]].copy()

# Spalten umbenennen für bessere Lesbarkeit
big5_data.columns = [f"Big5_{col}" for col in big5_available.keys()]
gaais_data.columns = list(gaais_available.keys())

# Zusammenführen
analysis_data = pd.concat([big5_data, gaais_data], axis=1)

# Fehlende Werte entfernen
analysis_data_clean = analysis_data.dropna()

print(f"\nDaten nach Bereinigung: {len(analysis_data_clean)} vollständige Fälle")

# ============================================================================
# 1. DESKRIPTIVE STATISTIKEN
# ============================================================================
print("\n" + "=" * 80)
print("1. DESKRIPTIVE STATISTIKEN")
print("=" * 80)

desc_stats = analysis_data_clean.describe()
print("\nDeskriptive Statistiken:")
print(desc_stats.round(2))

# Zusätzliche Statistiken
print("\n" + "-" * 80)
print("Zusätzliche Statistiken:")
print("-" * 80)

for col in analysis_data_clean.columns:
    data = analysis_data_clean[col].dropna()
    print(f"\n{col}:")
    print(f"  Mittelwert (M): {data.mean():.2f}")
    print(f"  Standardabweichung (SD): {data.std():.2f}")
    print(f"  Median: {data.median():.2f}")
    print(f"  Minimum: {data.min():.2f}")
    print(f"  Maximum: {data.max():.2f}")
    print(f"  Schiefe: {stats.skew(data):.2f}")
    print(f"  Kurtosis: {stats.kurtosis(data):.2f}")

# ============================================================================
# 2. KORRELATIONSANALYSEN
# ============================================================================
print("\n" + "=" * 80)
print("2. KORRELATIONSANALYSEN")
print("=" * 80)

# Pearson-Korrelationen zwischen Big5 und GAAIS
correlation_matrix = analysis_data_clean.corr(method='pearson')

print("\nKorrelationsmatrix (Pearson):")
print(correlation_matrix.round(3))

# Spezifische Korrelationen zwischen Big5 und GAAIS
print("\n" + "-" * 80)
print("Korrelationen zwischen Big5 Persönlichkeitsmerkmalen und GAAIS:")
print("-" * 80)

big5_cols = [col for col in analysis_data_clean.columns if col.startswith('Big5_')]
gaais_cols = [col for col in analysis_data_clean.columns if col.startswith('GAAIS')]

for big5_col in big5_cols:
    for gaais_col in gaais_cols:
        data_big5 = analysis_data_clean[big5_col].dropna()
        data_gaais = analysis_data_clean[gaais_col].dropna()
        
        # Gemeinsame Fälle finden
        common_idx = analysis_data_clean[[big5_col, gaais_col]].dropna().index
        if len(common_idx) > 3:
            r_pearson, p_pearson = pearsonr(
                analysis_data_clean.loc[common_idx, big5_col],
                analysis_data_clean.loc[common_idx, gaais_col]
            )
            r_spearman, p_spearman = spearmanr(
                analysis_data_clean.loc[common_idx, big5_col],
                analysis_data_clean.loc[common_idx, gaais_col]
            )
            
            sig_pearson = "***" if p_pearson < 0.001 else "**" if p_pearson < 0.01 else "*" if p_pearson < 0.05 else ""
            sig_spearman = "***" if p_spearman < 0.001 else "**" if p_spearman < 0.01 else "*" if p_spearman < 0.05 else ""
            
            print(f"\n{big5_col.replace('Big5_', '')} ↔ {gaais_col}:")
            print(f"  Pearson r = {r_pearson:.3f}, p = {p_pearson:.4f} {sig_pearson}")
            print(f"  Spearman ρ = {r_spearman:.3f}, p = {p_spearman:.4f} {sig_spearman}")

# Korrelationen zwischen Big5 Merkmalen
print("\n" + "-" * 80)
print("Interkorrelationen zwischen Big5 Persönlichkeitsmerkmalen:")
print("-" * 80)

big5_corr = analysis_data_clean[big5_cols].corr()
print(big5_corr.round(3))

# ============================================================================
# 3. VISUALISIERUNGEN
# ============================================================================
print("\n" + "=" * 80)
print("3. ERSTELLE VISUALISIERUNGEN")
print("=" * 80)

# Plot-Verzeichnis erstellen
import os
os.makedirs("plots", exist_ok=True)

# 3.1 Korrelationsmatrix Heatmap
plt.figure(figsize=(12, 10))
mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
sns.heatmap(correlation_matrix, mask=mask, annot=True, fmt='.2f', cmap='coolwarm', 
            center=0, square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
plt.title('Korrelationsmatrix: Big5 Persönlichkeitsmerkmale und GAAIS', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('plots/korrelationsmatrix.png', dpi=300, bbox_inches='tight')
print("[OK] Korrelationsmatrix gespeichert: plots/korrelationsmatrix.png")
plt.close()

# 3.2 Verteilungen der Big5 Merkmale
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

for idx, col in enumerate(big5_cols):
    if idx < len(axes):
        data = analysis_data_clean[col].dropna()
        axes[idx].hist(data, bins=20, edgecolor='black', alpha=0.7)
        axes[idx].axvline(data.mean(), color='red', linestyle='--', linewidth=2, label=f'M = {data.mean():.2f}')
        axes[idx].axvline(data.median(), color='blue', linestyle='--', linewidth=2, label=f'Median = {data.median():.2f}')
        axes[idx].set_title(col.replace('Big5_', ''), fontweight='bold')
        axes[idx].set_xlabel('Wert')
        axes[idx].set_ylabel('Häufigkeit')
        axes[idx].legend()
        axes[idx].grid(True, alpha=0.3)

# Letztes Subplot entfernen wenn ungerade Anzahl
if len(big5_cols) < len(axes):
    fig.delaxes(axes[-1])

plt.suptitle('Verteilungen der Big5 Persönlichkeitsmerkmale', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('plots/big5_verteilungen.png', dpi=300, bbox_inches='tight')
print("[OK] Big5 Verteilungen gespeichert: plots/big5_verteilungen.png")
plt.close()

# 3.3 Verteilungen der GAAIS Skalen
fig, axes = plt.subplots(1, len(gaais_cols), figsize=(6*len(gaais_cols), 5))
if len(gaais_cols) == 1:
    axes = [axes]

for idx, col in enumerate(gaais_cols):
    data = analysis_data_clean[col].dropna()
    axes[idx].hist(data, bins=20, edgecolor='black', alpha=0.7, color='green' if 'positiv' in col else 'orange')
    axes[idx].axvline(data.mean(), color='red', linestyle='--', linewidth=2, label=f'M = {data.mean():.2f}')
    axes[idx].axvline(data.median(), color='blue', linestyle='--', linewidth=2, label=f'Median = {data.median():.2f}')
    axes[idx].set_title(col, fontweight='bold')
    axes[idx].set_xlabel('Wert')
    axes[idx].set_ylabel('Häufigkeit')
    axes[idx].legend()
    axes[idx].grid(True, alpha=0.3)

plt.suptitle('Verteilungen der GAAIS Skalen', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('plots/gaais_verteilungen.png', dpi=300, bbox_inches='tight')
print("[OK] GAAIS Verteilungen gespeichert: plots/gaais_verteilungen.png")
plt.close()

# 3.4 Scatterplots: Big5 vs GAAIS
n_big5 = len(big5_cols)
n_gaais = len(gaais_cols)
fig, axes = plt.subplots(n_big5, n_gaais, figsize=(6*n_gaais, 5*n_big5))

if n_big5 == 1:
    axes = axes.reshape(1, -1)
if n_gaais == 1:
    axes = axes.reshape(-1, 1)

for i, big5_col in enumerate(big5_cols):
    for j, gaais_col in enumerate(gaais_cols):
        common_idx = analysis_data_clean[[big5_col, gaais_col]].dropna().index
        if len(common_idx) > 0:
            x = analysis_data_clean.loc[common_idx, big5_col]
            y = analysis_data_clean.loc[common_idx, gaais_col]
            
            axes[i, j].scatter(x, y, alpha=0.5, s=50)
            
            # Regressionslinie
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            axes[i, j].plot(x, p(x), "r--", alpha=0.8, linewidth=2)
            
            # Korrelation
            r, p_val = pearsonr(x, y)
            sig = "***" if p_val < 0.001 else "**" if p_val < 0.01 else "*" if p_val < 0.05 else ""
            axes[i, j].set_title(f'r = {r:.3f}{sig}', fontsize=10)
            axes[i, j].set_xlabel(big5_col.replace('Big5_', ''))
            axes[i, j].set_ylabel(gaais_col)
            axes[i, j].grid(True, alpha=0.3)

plt.suptitle('Scatterplots: Big5 Persönlichkeitsmerkmale vs GAAIS', fontsize=14, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig('plots/big5_gaais_scatterplots.png', dpi=300, bbox_inches='tight')
print("[OK] Scatterplots gespeichert: plots/big5_gaais_scatterplots.png")
plt.close()

# 3.5 Boxplots für Big5
plt.figure(figsize=(12, 6))
data_for_box = [analysis_data_clean[col].dropna() for col in big5_cols]
labels = [col.replace('Big5_', '') for col in big5_cols]
bp = plt.boxplot(data_for_box, labels=labels, patch_artist=True)
for patch in bp['boxes']:
    patch.set_facecolor('lightblue')
plt.title('Boxplots der Big5 Persönlichkeitsmerkmale', fontsize=14, fontweight='bold')
plt.ylabel('Wert')
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('plots/big5_boxplots.png', dpi=300, bbox_inches='tight')
print("[OK] Big5 Boxplots gespeichert: plots/big5_boxplots.png")
plt.close()

# ============================================================================
# 4. REGRESSIONSANALYSEN
# ============================================================================
print("\n" + "=" * 80)
print("4. REGRESSIONSANALYSEN")
print("=" * 80)

try:
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import r2_score
    from sklearn.preprocessing import StandardScaler
    
    # Für jede GAAIS Variable eine multiple Regression mit allen Big5 Merkmalen
    for gaais_col in gaais_cols:
        print(f"\n{'='*80}")
        print(f"Multiple Regression: {gaais_col} ~ Big5 Merkmale")
        print(f"{'='*80}")
        
        # Daten vorbereiten
        X = analysis_data_clean[big5_cols].values
        y = analysis_data_clean[gaais_col].values
        
        # Fehlende Werte entfernen
        mask = ~(np.isnan(X).any(axis=1) | np.isnan(y))
        X_clean = X[mask]
        y_clean = y[mask]
        
        if len(X_clean) > len(big5_cols):
            # Standardisierung
            scaler_X = StandardScaler()
            scaler_y = StandardScaler()
            X_scaled = scaler_X.fit_transform(X_clean)
            y_scaled = scaler_y.fit_transform(y_clean.reshape(-1, 1)).ravel()
            
            # Regression
            reg = LinearRegression()
            reg.fit(X_scaled, y_scaled)
            
            # Vorhersagen
            y_pred = reg.predict(X_scaled)
            
            # Ergebnisse
            r2 = r2_score(y_scaled, y_pred)
            
            print(f"\nR² = {r2:.4f}")
            print(f"Angepasstes R² = {1 - (1 - r2) * (len(X_clean) - 1) / (len(X_clean) - len(big5_cols) - 1):.4f}")
            print(f"\nRegressionskoeffizienten (standardisiert):")
            
            for i, big5_col in enumerate(big5_cols):
                print(f"  {big5_col.replace('Big5_', '')}: β = {reg.coef_[i]:.4f}")
            
            print(f"\nKonstante: {reg.intercept_:.4f}")
            
            # Signifikanztests (vereinfacht)
            print(f"\nHinweis: Für Signifikanztests der einzelnen Koeffizienten verwenden Sie bitte")
            print(f"         statsmodel oder scipy.stats für detaillierte p-Werte.")
            
except ImportError:
    print("\nHinweis: scikit-learn nicht verfügbar. Regressionsanalysen übersprungen.")
    print("Installieren Sie scikit-learn mit: pip install scikit-learn")

# ============================================================================
# 5. ZUSAMMENFASSUNG
# ============================================================================
print("\n" + "=" * 80)
print("5. ZUSAMMENFASSUNG")
print("=" * 80)

print("\n[OK] Analyse abgeschlossen!")
print(f"\nErgebnisse gespeichert in:")
print("  - plots/korrelationsmatrix.png")
print("  - plots/big5_verteilungen.png")
print("  - plots/gaais_verteilungen.png")
print("  - plots/big5_gaais_scatterplots.png")
print("  - plots/big5_boxplots.png")

print("\n" + "=" * 80)

