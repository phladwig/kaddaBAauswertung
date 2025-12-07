"""
Skript zum Laden von IBM SPSS .sav Dateien in Python
Benötigt: pip install pyreadstat
"""

import pyreadstat
import pandas as pd

# Pfad zur SPSS-Datei
sav_file = "KIPM_statistische Auswertung_20251116_1759_nach Rohwerten bereinigte Daten.sav"

# SPSS-Datei laden
try:
    # Daten und Metadaten laden
    df, meta = pyreadstat.read_sav(sav_file)
    
    print(f"Datei erfolgreich geladen!")
    print(f"Anzahl Zeilen: {len(df)}")
    print(f"Anzahl Spalten: {len(df.columns)}")
    print(f"\nSpaltennamen:")
    print(df.columns.tolist())
    print(f"\nErste Zeilen:")
    print(df.head())
    print(f"\nDatentypen:")
    print(df.dtypes)
    print(f"\nMetadaten:")
    print(f"Variable Labels: {meta.column_names_to_labels}")
    print(f"Value Labels: {meta.variable_value_labels}")
    
    # DataFrame ist jetzt verfügbar für weitere Analysen
    # df enthält die Daten
    
except Exception as e:
    print(f"Fehler beim Laden der Datei: {e}")
    print("\nBitte installieren Sie pyreadstat mit:")
    print("pip install pyreadstat")







