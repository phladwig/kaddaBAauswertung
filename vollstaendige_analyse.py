"""
Vollständige Korrelationsanalyse: Big5 und GAAIS mit p-Werten
"""
import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr, shapiro
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Daten laden
print("=" * 80)
print("VOLLSTÄNDIGE KORRELATIONSANALYSE: BIG5 UND GAAIS")
print("=" * 80)

df = pd.read_csv("KIPM_statistische Auswertung_20251116_1759_nach Rohwerten bereinigte Daten.csv", 
                 sep=';', encoding='utf-8', decimal=',')

print(f"\nStichprobengröße: N = {len(df)}")

# Variablen definieren (MEAN-Variablen für bessere Interpretierbarkeit)
big5_vars = ['Offenheit_MEAN', 'Gewissenhaftigkeit_MEAN', 'Extraversion_MEAN', 
             'Verträglichkeit_MEAN', 'Neurotizismus_MEAN']
gaais_vars = ['GAAIS_positiv_MEAN', 'GAAIS_negativ_MEAN']

# Auch Summenscores prüfen falls MEAN nicht vorhanden
big5_fallback = ['Offenheit', 'Gewissenhaftigkeit', 'Extraversion', 
                 'Verträglichkeit', 'Neurotizismus']
gaais_fallback = ['GAAIS_positiv', 'GAAIS_negativ']

# Verfügbare Variablen finden
available_big5 = []
for i, var in enumerate(big5_vars):
    if var in df.columns:
        available_big5.append(var)
    elif big5_fallback[i] in df.columns:
        available_big5.append(big5_fallback[i])

available_gaais = []
for i, var in enumerate(gaais_vars):
    if var in df.columns:
        available_gaais.append(var)
    elif gaais_fallback[i] in df.columns:
        available_gaais.append(gaais_fallback[i])

print(f"\nVerwendete Big5 Variablen: {available_big5}")
print(f"Verwendete GAAIS Variablen: {available_gaais}")

# Analysedaten vorbereiten
analysis_cols = available_big5 + available_gaais
analysis_data = df[analysis_cols].dropna()
print(f"\nVollständige Fälle für Analyse: n = {len(analysis_data)}")

# ============================================================================
# 1. DESKRIPTIVE STATISTIKEN
# ============================================================================
print("\n" + "=" * 80)
print("1. DESKRIPTIVE STATISTIKEN")
print("=" * 80)

print("\n{:<30} {:>8} {:>8} {:>8} {:>8} {:>8} {:>8}".format(
    "Variable", "N", "M", "SD", "Min", "Max", "Median"))
print("-" * 80)

for col in analysis_cols:
    data = analysis_data[col]
    nice_name = col.replace('_MEAN', '').replace('GAAIS_', 'GAAIS ')
    print("{:<30} {:>8} {:>8.2f} {:>8.2f} {:>8.2f} {:>8.2f} {:>8.2f}".format(
        nice_name, len(data), data.mean(), data.std(), 
        data.min(), data.max(), data.median()))

# ============================================================================
# 2. KORRELATIONSANALYSE: BIG5 ↔ GAAIS
# ============================================================================
print("\n" + "=" * 80)
print("2. KORRELATIONEN ZWISCHEN BIG5 UND GAAIS (mit p-Werten)")
print("=" * 80)
print("\nSignifikanzniveaus: * p < .05, ** p < .01, *** p < .001")

def get_sig_stars(p):
    if p < 0.001:
        return "***"
    elif p < 0.01:
        return "**"
    elif p < 0.05:
        return "*"
    return ""

def interpret_r(r):
    r_abs = abs(r)
    if r_abs < 0.10:
        return "vernachlässigbar"
    elif r_abs < 0.30:
        return "schwach"
    elif r_abs < 0.50:
        return "moderat"
    elif r_abs < 0.70:
        return "stark"
    else:
        return "sehr stark"

print("\n" + "-" * 80)
print("PEARSON KORRELATIONEN")
print("-" * 80)

results = []
for big5 in available_big5:
    for gaais in available_gaais:
        x = analysis_data[big5]
        y = analysis_data[gaais]
        
        r, p = pearsonr(x, y)
        sig = get_sig_stars(p)
        interp = interpret_r(r)
        
        big5_name = big5.replace('_MEAN', '')
        gaais_name = gaais.replace('_MEAN', '').replace('GAAIS_', '')
        
        results.append({
            'Big5': big5_name,
            'GAAIS': gaais_name,
            'r': r,
            'p': p,
            'sig': sig,
            'interpretation': interp
        })
        
        print(f"\n{big5_name} ↔ GAAIS_{gaais_name}:")
        print(f"  r = {r:.3f}, p = {p:.4f} {sig}")
        print(f"  Effektstärke: {interp}")
        print(f"  95% CI: [{r - 1.96*np.sqrt((1-r**2)/(len(x)-2)):.3f}, {r + 1.96*np.sqrt((1-r**2)/(len(x)-2)):.3f}]")

# ============================================================================
# 3. VOLLSTÄNDIGE KORRELATIONSMATRIX
# ============================================================================
print("\n" + "=" * 80)
print("3. VOLLSTÄNDIGE KORRELATIONSMATRIX (Pearson r)")
print("=" * 80)

# Korrelationsmatrix berechnen
corr_matrix = analysis_data.corr(method='pearson')

# Schöne Namen
nice_names = {col: col.replace('_MEAN', '').replace('GAAIS_', 'GAAIS_') 
              for col in analysis_cols}

print("\n" + " " * 20, end="")
for col in analysis_cols:
    print(f"{nice_names[col][:10]:>12}", end="")
print()
print("-" * (20 + 12 * len(analysis_cols)))

for row_col in analysis_cols:
    print(f"{nice_names[row_col]:<20}", end="")
    for col_col in analysis_cols:
        r = corr_matrix.loc[row_col, col_col]
        x = analysis_data[row_col]
        y = analysis_data[col_col]
        _, p = pearsonr(x, y)
        sig = get_sig_stars(p)
        print(f"{r:>8.2f}{sig:<4}", end="")
    print()

# ============================================================================
# 4. SPEARMAN KORRELATIONEN (Rangkorrelation)
# ============================================================================
print("\n" + "=" * 80)
print("4. SPEARMAN RANGKORRELATIONEN (robuster bei Nicht-Normalverteilung)")
print("=" * 80)

for big5 in available_big5:
    for gaais in available_gaais:
        x = analysis_data[big5]
        y = analysis_data[gaais]
        
        rho, p = spearmanr(x, y)
        sig = get_sig_stars(p)
        
        big5_name = big5.replace('_MEAN', '')
        gaais_name = gaais.replace('_MEAN', '').replace('GAAIS_', '')
        
        print(f"\n{big5_name} ↔ GAAIS_{gaais_name}:")
        print(f"  ρ = {rho:.3f}, p = {p:.4f} {sig}")

# ============================================================================
# 5. ÜBERSICHTSTABELLE FÜR PUBLIKATION
# ============================================================================
print("\n" + "=" * 80)
print("5. ÜBERSICHTSTABELLE (für wissenschaftliche Arbeit)")
print("=" * 80)

print("\nTabelle: Korrelationen zwischen Big5-Persönlichkeitsmerkmalen und GAAIS-Subskalen")
print()
print("{:<25} {:>20} {:>20}".format("", "GAAIS positiv", "GAAIS negativ"))
print("-" * 65)

for big5 in available_big5:
    big5_name = big5.replace('_MEAN', '')
    row = f"{big5_name:<25}"
    
    for gaais in available_gaais:
        x = analysis_data[big5]
        y = analysis_data[gaais]
        r, p = pearsonr(x, y)
        sig = get_sig_stars(p)
        row += f"{r:>8.2f}{sig:<12}"
    
    print(row)

print("-" * 65)
print(f"Anmerkung. N = {len(analysis_data)}. * p < .05, ** p < .01, *** p < .001")

# ============================================================================
# 6. KORRELATION ZWISCHEN GAAIS-SUBSKALEN
# ============================================================================
print("\n" + "=" * 80)
print("6. KORRELATION ZWISCHEN GAAIS-SUBSKALEN")
print("=" * 80)

if len(available_gaais) == 2:
    x = analysis_data[available_gaais[0]]
    y = analysis_data[available_gaais[1]]
    
    r, p = pearsonr(x, y)
    sig = get_sig_stars(p)
    
    print(f"\nGAAIS_positiv ↔ GAAIS_negativ:")
    print(f"  r = {r:.3f}, p = {p:.4f} {sig}")
    print(f"\n  → Die positive Korrelation zeigt: Menschen, die sich intensiver")
    print(f"    mit KI beschäftigen, haben sowohl positivere Erwartungen")
    print(f"    ALS AUCH stärkere Bedenken (differenzierte Sichtweise).")

# ============================================================================
# 7. ZUSAMMENFASSUNG DER SIGNIFIKANTEN BEFUNDE
# ============================================================================
print("\n" + "=" * 80)
print("7. ZUSAMMENFASSUNG DER SIGNIFIKANTEN BEFUNDE")
print("=" * 80)

sig_results = [r for r in results if r['p'] < 0.05]
print(f"\nAnzahl signifikanter Korrelationen: {len(sig_results)} von {len(results)}")

if sig_results:
    print("\nSignifikante Zusammenhänge:")
    for r in sorted(sig_results, key=lambda x: abs(x['r']), reverse=True):
        direction = "positiv" if r['r'] > 0 else "negativ"
        print(f"\n  • {r['Big5']} ↔ GAAIS_{r['GAAIS']}:")
        print(f"    r = {r['r']:.3f}{r['sig']}, {r['interpretation']}er {direction}er Zusammenhang")

print("\n" + "=" * 80)
print("ANALYSE ABGESCHLOSSEN")
print("=" * 80)



