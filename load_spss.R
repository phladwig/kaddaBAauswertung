# Skript zum Laden von IBM SPSS .sav Dateien in R
# Benötigt: install.packages("haven")

library(haven)

# Pfad zur SPSS-Datei
sav_file <- "KIPM_statistische Auswertung_20251116_1759_nach Rohwerten bereinigte Daten.sav"

# SPSS-Datei laden
tryCatch({
  # Daten laden
  df <- read_sav(sav_file)
  
  cat("Datei erfolgreich geladen!\n")
  cat(sprintf("Anzahl Zeilen: %d\n", nrow(df)))
  cat(sprintf("Anzahl Spalten: %d\n", ncol(df)))
  cat("\nSpaltennamen:\n")
  print(colnames(df))
  cat("\nErste Zeilen:\n")
  print(head(df))
  cat("\nDatentypen:\n")
  print(str(df))
  cat("\nZusammenfassung:\n")
  print(summary(df))
  
  # Datenrahmen ist jetzt verfügbar für weitere Analysen
  # df enthält die Daten
  
}, error = function(e) {
  cat(sprintf("Fehler beim Laden der Datei: %s\n", e$message))
  cat("\nBitte installieren Sie haven mit:\n")
  cat("install.packages(\"haven\")\n")
})







