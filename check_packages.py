"""Prüft, welche Pakete verfügbar sind"""
import sys

packages = ['pandas', 'numpy', 'scipy', 'matplotlib', 'seaborn', 'sklearn', 'pyreadstat']
available = {}
missing = []

for pkg in packages:
    try:
        if pkg == 'sklearn':
            mod = __import__('sklearn')
        else:
            mod = __import__(pkg)
        available[pkg] = mod.__version__ if hasattr(mod, '__version__') else 'OK'
        print(f"✓ {pkg}: {available[pkg]}")
    except ImportError:
        missing.append(pkg)
        print(f"✗ {pkg}: NICHT VERFÜGBAR")

if missing:
    print(f"\nFehlende Pakete: {', '.join(missing)}")
    print("\nVersuchen Sie:")
    print("  python -m pip install " + " ".join(missing))
else:
    print("\n✓ Alle Pakete verfügbar!")



