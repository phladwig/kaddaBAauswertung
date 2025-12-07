# Statistische Auswertung: Big5 Persönlichkeitsmerkmale und GAAIS
# Benötigt: install.packages(c("haven", "dplyr", "ggplot2", "corrplot", "psych", "car"))

library(haven)
library(dplyr)
library(ggplot2)
library(corrplot)
library(psych)
library(car)

# Daten laden
cat(paste(rep("=", 80), collapse = ""), "\n")
cat("STATISTISCHE AUSWERTUNG: BIG5 PERSÖNLICHKEITSMERKMALE UND GAAIS\n")
cat(paste(rep("=", 80), collapse = ""), "\n")

# Versuche zuerst .sav Datei zu laden, sonst CSV
df <- NULL
tryCatch({
  df <- read_sav("KIPM_statistische Auswertung_20251116_1759_nach Rohwerten bereinigte Daten.sav")
  cat("\n✓ Daten aus .sav Datei geladen\n")
}, error = function(e) {
  tryCatch({
    df <<- read.csv2("KIPM_statistische Auswertung_20251116_1759_nach Rohwerten bereinigte Daten.csv", 
                     encoding = "UTF-8", dec = ",")
    cat("\n✓ Daten aus CSV Datei geladen\n")
  }, error = function(e2) {
    cat("\n✗ Fehler beim Laden der Daten:", e2$message, "\n")
    stop()
  })
})

cat(sprintf("\nDatenstruktur: %d Zeilen, %d Spalten\n", nrow(df), ncol(df)))

# Big5 Variablen identifizieren
big5_vars <- c("Offenheit", "Offenheit_MEAN", 
                "Gewissenhaftigkeit", "Gewissenhaftigkeit_MEAN",
                "Extraversion", "Extraversion_MEAN",
                "Verträglichkeit", "Verträglichkeit_MEAN",
                "Neurotizismus", "Neurotizismus_MEAN")

# GAAIS Variablen identifizieren
gaais_vars <- c("GAAIS_positiv", "GAAIS_positiv_MEAN",
                "GAAIS_negativ", "GAAIS_negativ_MEAN")

# Verfügbare Variablen finden
big5_available <- c()
for (var in big5_vars) {
  if (var %in% colnames(df)) {
    trait_name <- gsub("_MEAN", "", var)
    if (!trait_name %in% names(big5_available)) {
      big5_available[trait_name] <- var
    }
  }
}

gaais_available <- c()
for (var in gaais_vars) {
  if (var %in% colnames(df)) {
    trait_name <- gsub("_MEAN", "", var)
    if (!trait_name %in% names(gaais_available)) {
      gaais_available[trait_name] <- var
    }
  }
}

cat(sprintf("\nGefundene Big5 Variablen: %s\n", paste(names(big5_available), collapse = ", ")))
cat(sprintf("Gefundene GAAIS Variablen: %s\n", paste(names(gaais_available), collapse = ", ")))

# Numerische Spalten für Big5 und GAAIS extrahieren
big5_cols <- unname(big5_available)
gaais_cols <- unname(gaais_available)

analysis_data <- df %>%
  select(all_of(c(big5_cols, gaais_cols))) %>%
  mutate_all(as.numeric)

# Spalten umbenennen
colnames(analysis_data) <- c(
  paste0("Big5_", names(big5_available)),
  names(gaais_available)
)

# Fehlende Werte entfernen
analysis_data_clean <- analysis_data %>%
  na.omit()

cat(sprintf("\nDaten nach Bereinigung: %d vollständige Fälle\n", nrow(analysis_data_clean)))

# ============================================================================
# 1. DESKRIPTIVE STATISTIKEN
# ============================================================================
cat("\n", strrep("=", 80), "\n", sep = "")
cat("1. DESKRIPTIVE STATISTIKEN\n")
cat(strrep("=", 80), "\n")

desc_stats <- describe(analysis_data_clean)
print(desc_stats)

# ============================================================================
# 2. KORRELATIONSANALYSEN
# ============================================================================
cat("\n", strrep("=", 80), "\n", sep = "")
cat("2. KORRELATIONSANALYSEN\n")
cat(strrep("=", 80), "\n")

# Korrelationsmatrix
cor_matrix <- cor(analysis_data_clean, use = "complete.obs", method = "pearson")
cat("\nKorrelationsmatrix (Pearson):\n")
print(round(cor_matrix, 3))

# Spezifische Korrelationen zwischen Big5 und GAAIS
cat("\n", strrep("-", 80), "\n", sep = "")
cat("Korrelationen zwischen Big5 Persönlichkeitsmerkmalen und GAAIS:\n")
cat(strrep("-", 80), "\n")

big5_col_names <- paste0("Big5_", names(big5_available))
gaais_col_names <- names(gaais_available)

for (big5_col in big5_col_names) {
  for (gaais_col in gaais_col_names) {
    if (big5_col %in% colnames(analysis_data_clean) && 
        gaais_col %in% colnames(analysis_data_clean)) {
      test_result <- cor.test(analysis_data_clean[[big5_col]], 
                              analysis_data_clean[[gaais_col]], 
                              method = "pearson")
      
      sig <- ifelse(test_result$p.value < 0.001, "***",
                   ifelse(test_result$p.value < 0.01, "**",
                         ifelse(test_result$p.value < 0.05, "*", "")))
      
      cat(sprintf("\n%s ↔ %s:\n", gsub("Big5_", "", big5_col), gaais_col))
      cat(sprintf("  r = %.3f, p = %.4f %s\n", 
                  test_result$estimate, test_result$p.value, sig))
    }
  }
}

# ============================================================================
# 3. VISUALISIERUNGEN
# ============================================================================
cat("\n", strrep("=", 80), "\n", sep = "")
cat("3. ERSTELLE VISUALISIERUNGEN\n")
cat(strrep("=", 80), "\n")

# Plot-Verzeichnis erstellen
if (!dir.exists("plots")) {
  dir.create("plots")
}

# 3.1 Korrelationsmatrix Heatmap
png("plots/korrelationsmatrix_R.png", width = 1200, height = 1000, res = 300)
corrplot(cor_matrix, method = "color", type = "upper", 
         order = "hclust", tl.cex = 0.8, tl.col = "black",
         addCoef.col = "black", number.cex = 0.7)
title("Korrelationsmatrix: Big5 Persönlichkeitsmerkmale und GAAIS", 
      cex.main = 1.2, font.main = 2)
dev.off()
cat("✓ Korrelationsmatrix gespeichert: plots/korrelationsmatrix_R.png\n")

# 3.2 Verteilungen der Big5 Merkmale
png("plots/big5_verteilungen_R.png", width = 1500, height = 1000, res = 300)
par(mfrow = c(2, 3))
for (col in big5_col_names) {
  if (col %in% colnames(analysis_data_clean)) {
    hist(analysis_data_clean[[col]], main = gsub("Big5_", "", col),
         xlab = "Wert", ylab = "Häufigkeit", col = "lightblue", border = "black")
    abline(v = mean(analysis_data_clean[[col]], na.rm = TRUE), 
           col = "red", lty = 2, lwd = 2)
    abline(v = median(analysis_data_clean[[col]], na.rm = TRUE), 
           col = "blue", lty = 2, lwd = 2)
  }
}
mtext("Verteilungen der Big5 Persönlichkeitsmerkmale", 
      side = 3, line = -2, outer = TRUE, font = 2, cex = 1.2)
dev.off()
cat("✓ Big5 Verteilungen gespeichert: plots/big5_verteilungen_R.png\n")

# 3.3 Scatterplots: Big5 vs GAAIS
png("plots/big5_gaais_scatterplots_R.png", 
    width = 600 * length(gaais_col_names), 
    height = 500 * length(big5_col_names), res = 300)
par(mfrow = c(length(big5_col_names), length(gaais_col_names)))
for (big5_col in big5_col_names) {
  for (gaais_col in gaais_col_names) {
    if (big5_col %in% colnames(analysis_data_clean) && 
        gaais_col %in% colnames(analysis_data_clean)) {
      plot(analysis_data_clean[[big5_col]], analysis_data_clean[[gaais_col]],
           xlab = gsub("Big5_", "", big5_col), ylab = gaais_col,
           main = "", pch = 19, alpha = 0.5)
      abline(lm(analysis_data_clean[[gaais_col]] ~ analysis_data_clean[[big5_col]]), 
             col = "red", lwd = 2)
      r <- cor(analysis_data_clean[[big5_col]], analysis_data_clean[[gaais_col]], 
               use = "complete.obs")
      mtext(sprintf("r = %.3f", r), side = 3, line = -1, cex = 0.8)
    }
  }
}
mtext("Scatterplots: Big5 Persönlichkeitsmerkmale vs GAAIS", 
      side = 3, line = -2, outer = TRUE, font = 2, cex = 1.2)
dev.off()
cat("✓ Scatterplots gespeichert: plots/big5_gaais_scatterplots_R.png\n")

# 3.4 Boxplots für Big5
png("plots/big5_boxplots_R.png", width = 1200, height = 600, res = 300)
boxplot(analysis_data_clean[, big5_col_names], 
        names = gsub("Big5_", "", big5_col_names),
        main = "Boxplots der Big5 Persönlichkeitsmerkmale",
        ylab = "Wert", col = "lightblue")
dev.off()
cat("✓ Big5 Boxplots gespeichert: plots/big5_boxplots_R.png\n")

# ============================================================================
# 4. REGRESSIONSANALYSEN
# ============================================================================
cat("\n", strrep("=", 80), "\n", sep = "")
cat("4. REGRESSIONSANALYSEN\n")
cat(strrep("=", 80), "\n")

# Für jede GAAIS Variable eine multiple Regression mit allen Big5 Merkmalen
for (gaais_col in gaais_col_names) {
  if (gaais_col %in% colnames(analysis_data_clean)) {
    cat("\n", strrep("=", 80), "\n", sep = "")
    cat(sprintf("Multiple Regression: %s ~ Big5 Merkmale\n", gaais_col))
    cat(strrep("=", 80), "\n")
    
    # Formel erstellen
    formula_str <- paste(gaais_col, "~", paste(big5_col_names, collapse = " + "))
    formula_obj <- as.formula(formula_str)
    
    # Regression
    model <- lm(formula_obj, data = analysis_data_clean)
    
    # Zusammenfassung
    summary_model <- summary(model)
    print(summary_model)
    
    # VIF für Multikollinearität
    if (length(big5_col_names) > 1) {
      cat("\nVariance Inflation Factors (VIF):\n")
      vif_values <- vif(model)
      print(vif_values)
    }
  }
}

# ============================================================================
# 5. ZUSAMMENFASSUNG
# ============================================================================
cat("\n", strrep("=", 80), "\n", sep = "")
cat("5. ZUSAMMENFASSUNG\n")
cat(strrep("=", 80), "\n")

cat("\n✓ Analyse abgeschlossen!\n")
cat("\nErgebnisse gespeichert in:\n")
cat("  - plots/korrelationsmatrix_R.png\n")
cat("  - plots/big5_verteilungen_R.png\n")
cat("  - plots/big5_gaais_scatterplots_R.png\n")
cat("  - plots/big5_boxplots_R.png\n")

cat("\n", strrep("=", 80), "\n", sep = "")

