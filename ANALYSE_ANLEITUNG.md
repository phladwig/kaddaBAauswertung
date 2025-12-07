# Anleitung: Statistische Auswertung Big5 und GAAIS

## Übersicht

Dieses Projekt enthält Skripte zur statistischen Auswertung der Beziehung zwischen Big5 Persönlichkeitsmerkmalen und GAAIS (General Attitudes toward Artificial Intelligence Scale).

## Voraussetzungen

### Python-Version
```bash
pip install pyreadstat pandas numpy scipy matplotlib seaborn scikit-learn
```

### R-Version
```r
install.packages(c("haven", "dplyr", "ggplot2", "corrplot", "psych", "car"))
```

## Durchführung der Analyse

### Python

Führen Sie das Skript aus:
```bash
python big5_gaais_analyse.py
```

Das Skript führt automatisch folgende Analysen durch:

1. **Deskriptive Statistiken**
   - Mittelwerte, Standardabweichungen, Median
   - Schiefe und Kurtosis
   - Minimum und Maximum

2. **Korrelationsanalysen**
   - Pearson-Korrelationen zwischen allen Variablen
   - Spearman-Korrelationen zwischen Big5 und GAAIS
   - Interkorrelationen zwischen Big5 Merkmalen

3. **Visualisierungen**
   - Korrelationsmatrix (Heatmap)
   - Verteilungen der Big5 Merkmale
   - Verteilungen der GAAIS Skalen
   - Scatterplots: Big5 vs GAAIS
   - Boxplots der Big5 Merkmale

4. **Regressionsanalysen**
   - Multiple Regression: GAAIS ~ Big5 Merkmale
   - Standardisierte Regressionskoeffizienten
   - R² und angepasstes R²

### R

Führen Sie das Skript aus:
```r
source("big5_gaais_analyse.R")
```

Das R-Skript führt die gleichen Analysen durch wie das Python-Skript.

## Ausgabe

Alle Visualisierungen werden im Ordner `plots/` gespeichert:

- `korrelationsmatrix.png` - Korrelationsmatrix aller Variablen
- `big5_verteilungen.png` - Histogramme der Big5 Verteilungen
- `gaais_verteilungen.png` - Histogramme der GAAIS Verteilungen
- `big5_gaais_scatterplots.png` - Scatterplots mit Regressionslinien
- `big5_boxplots.png` - Boxplots der Big5 Merkmale

## Big5 Persönlichkeitsmerkmale

Die Big5 (auch Fünf-Faktoren-Modell) umfassen:

1. **Offenheit** (Openness to Experience)
2. **Gewissenhaftigkeit** (Conscientiousness)
3. **Extraversion** (Extraversion)
4. **Verträglichkeit** (Agreeableness)
5. **Neurotizismus** (Neuroticism)

## GAAIS Skalen

- **GAAIS_positiv** - Positive Einstellungen gegenüber KI
- **GAAIS_negativ** - Negative Einstellungen gegenüber KI

## Interpretation der Ergebnisse

### Korrelationen
- **r > 0.3**: Mittlere bis starke positive Korrelation
- **r < -0.3**: Mittlere bis starke negative Korrelation
- **|r| < 0.3**: Schwache Korrelation

### Signifikanzniveaus
- `***`: p < 0.001 (sehr signifikant)
- `**`: p < 0.01 (signifikant)
- `*`: p < 0.05 (marginal signifikant)

### Regressionsanalysen
- **R²**: Anteil der erklärten Varianz
- **β-Koeffizienten**: Standardisierte Regressionskoeffizienten (Vergleichbarkeit zwischen Variablen)

## Weitere Analysen

Für erweiterte Analysen können Sie die Skripte anpassen:

- Moderationsanalysen
- Mediationsanalysen
- Strukturgleichungsmodelle
- Clusteranalysen
- Faktorenanalysen

## Unterstützung

Bei Fragen oder Problemen:
1. Prüfen Sie, ob alle benötigten Pakete installiert sind
2. Stellen Sie sicher, dass die Daten-Datei im richtigen Format vorliegt
3. Überprüfen Sie die Variablennamen in den Daten





