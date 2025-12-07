# SPSS .sav Dateien in Python und R laden

## Python

### Installation
```bash
pip install pyreadstat
```

### Verwendung
```python
import pyreadstat
import pandas as pd

df, meta = pyreadstat.read_sav("datei.sav")
```

**Alternative Bibliotheken:**
- `savReaderWriter` (älter, weniger aktiv entwickelt)
- `pandas` mit `pyreadstat` (empfohlen)

## R

### Installation
```r
install.packages("haven")
```

### Verwendung
```r
library(haven)
df <- read_sav("datei.sav")
```

**Alternative Bibliotheken:**
- `foreign::read.spss()` (älter, weniger Features)
- `haven` (empfohlen, Teil des tidyverse)

## Datei
Die Datei `KIPM_statistische Auswertung_20251116_1759_nach Rohwerten bereinigte Daten.sav` kann mit beiden Skripten geladen werden.





