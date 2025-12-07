"""
Vollständige Korrelationsanalyse: Big5 und GAAIS mit SUMMEN-Variablen (SPEARMAN)
"""
import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr
import warnings
warnings.filterwarnings('ignore')

# Ausgabe-Liste für Datei
output_lines = []

def log(text=""):
    print(text)
    output_lines.append(text)

# Daten laden
log("=" * 80)
log("VOLLSTÄNDIGE KORRELATIONSANALYSE: BIG5 UND GAAIS (SUMMEN-VARIABLEN) - SPEARMAN")
log("=" * 80)

df = pd.read_csv("KIPM_statistische Auswertung_20251116_1759_nach Rohwerten bereinigte Daten.csv", 
                 sep=';', encoding='utf-8', decimal=',')

log(f"\nStichprobengröße: N = {len(df)}")

# SUMMEN-Variablen definieren (statt MEAN)
big5_vars = ['Offenheit', 'Gewissenhaftigkeit', 'Extraversion', 
             'Verträglichkeit', 'Neurotizismus']
gaais_vars = ['GAAIS_positiv', 'GAAIS_negativ']

log(f"\nVerwendete Big5 Variablen (SUMMEN): {big5_vars}")
log(f"Verwendete GAAIS Variablen (SUMMEN): {gaais_vars}")

# Analysedaten vorbereiten
analysis_cols = big5_vars + gaais_vars
analysis_data = df[analysis_cols].dropna()
log(f"\nVollständige Fälle für Analyse: n = {len(analysis_data)}")

# ============================================================================
# 1. DESKRIPTIVE STATISTIKEN
# ============================================================================
log("\n" + "=" * 80)
log("1. DESKRIPTIVE STATISTIKEN (SUMMENWERTE)")
log("=" * 80)

log("\n{:<30} {:>8} {:>8} {:>8} {:>8} {:>8} {:>8}".format(
    "Variable", "N", "M", "SD", "Min", "Max", "Median"))
log("-" * 80)

for col in analysis_cols:
    data = analysis_data[col]
    nice_name = col.replace('GAAIS_', 'GAAIS ')
    log("{:<30} {:>8} {:>8.2f} {:>8.2f} {:>8.2f} {:>8.2f} {:>8.2f}".format(
        nice_name, len(data), data.mean(), data.std(), 
        data.min(), data.max(), data.median()))

# ============================================================================
# 2. KORRELATIONSANALYSE: BIG5 ↔ GAAIS
# ============================================================================
log("\n" + "=" * 80)
log("2. KORRELATIONEN ZWISCHEN BIG5 UND GAAIS (mit p-Werten)")
log("=" * 80)
log("\nSignifikanzniveaus: * p < .05, ** p < .01, *** p < .001")

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

log("\n" + "-" * 80)
log("SPEARMAN RANGKORRELATIONEN")
log("-" * 80)

results = []
for big5 in big5_vars:
    for gaais in gaais_vars:
        x = analysis_data[big5]
        y = analysis_data[gaais]
        
        r, p = spearmanr(x, y)
        sig = get_sig_stars(p)
        interp = interpret_r(r)
        
        gaais_name = gaais.replace('GAAIS_', '')
        
        results.append({
            'Big5': big5,
            'GAAIS': gaais_name,
            'r': r,
            'p': p,
            'sig': sig,
            'interpretation': interp
        })
        
        log(f"\n{big5} ↔ GAAIS_{gaais_name}:")
        log(f"  r = {r:.3f}, p = {p:.4f} {sig}")
        log(f"  Effektstärke: {interp}")
        log(f"  95% CI: [{r - 1.96*np.sqrt((1-r**2)/(len(x)-2)):.3f}, {r + 1.96*np.sqrt((1-r**2)/(len(x)-2)):.3f}]")

# ============================================================================
# 3. VOLLSTÄNDIGE KORRELATIONSMATRIX
# ============================================================================
log("\n" + "=" * 80)
log("3. VOLLSTÄNDIGE KORRELATIONSMATRIX (Spearman ρ)")
log("=" * 80)

# Korrelationsmatrix berechnen
corr_matrix = analysis_data.corr(method='spearman')

# Schöne Namen
nice_names = {col: col.replace('GAAIS_', 'GAAIS_') for col in analysis_cols}

header = " " * 20
for col in analysis_cols:
    header += f"{nice_names[col][:10]:>12}"
log("\n" + header)
log("-" * (20 + 12 * len(analysis_cols)))

for row_col in analysis_cols:
    row = f"{nice_names[row_col]:<20}"
    for col_col in analysis_cols:
        r = corr_matrix.loc[row_col, col_col]
        x = analysis_data[row_col]
        y = analysis_data[col_col]
        _, p = spearmanr(x, y)
        sig = get_sig_stars(p)
        row += f"{r:>8.2f}{sig:<4}"
    log(row)

# ============================================================================
# 4. ÜBERSICHTSTABELLE FÜR PUBLIKATION
# ============================================================================
log("\n" + "=" * 80)
log("4. ÜBERSICHTSTABELLE (für wissenschaftliche Arbeit)")
log("=" * 80)

log("\nTabelle: Korrelationen zwischen Big5-Persönlichkeitsmerkmalen und GAAIS-Subskalen (Summenwerte)")
log()
log("{:<25} {:>20} {:>20}".format("", "GAAIS positiv", "GAAIS negativ"))
log("-" * 65)

for big5 in big5_vars:
    row = f"{big5:<25}"
    
    for gaais in gaais_vars:
        x = analysis_data[big5]
        y = analysis_data[gaais]
        r, p = spearmanr(x, y)
        sig = get_sig_stars(p)
        row += f"{r:>8.2f}{sig:<12}"
    
    log(row)

log("-" * 65)
log(f"Anmerkung. N = {len(analysis_data)}. * p < .05, ** p < .01, *** p < .001")

# ============================================================================
# 5. KORRELATION ZWISCHEN GAAIS-SUBSKALEN
# ============================================================================
log("\n" + "=" * 80)
log("5. KORRELATION ZWISCHEN GAAIS-SUBSKALEN")
log("=" * 80)

x = analysis_data['GAAIS_positiv']
y = analysis_data['GAAIS_negativ']

r, p = spearmanr(x, y)
sig = get_sig_stars(p)

log(f"\nGAAIS_positiv ↔ GAAIS_negativ:")
log(f"  ρ = {r:.3f}, p = {p:.4f} {sig}")

# ============================================================================
# 6. ZUSAMMENFASSUNG DER SIGNIFIKANTEN BEFUNDE
# ============================================================================
log("\n" + "=" * 80)
log("6. ZUSAMMENFASSUNG DER SIGNIFIKANTEN BEFUNDE")
log("=" * 80)

sig_results = [r for r in results if r['p'] < 0.05]
log(f"\nAnzahl signifikanter Korrelationen: {len(sig_results)} von {len(results)}")

if sig_results:
    log("\nSignifikante Zusammenhänge:")
    for r in sorted(sig_results, key=lambda x: abs(x['r']), reverse=True):
        direction = "positiv" if r['r'] > 0 else "negativ"
        log(f"\n  • {r['Big5']} ↔ GAAIS_{r['GAAIS']}:")
        log(f"    r = {r['r']:.3f}{r['sig']}, {r['interpretation']}er {direction}er Zusammenhang")

log("\n" + "=" * 80)
log("ANALYSE ABGESCHLOSSEN")
log("=" * 80)

# In Datei speichern
with open('analyse_summen_spearman_output.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))
