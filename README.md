Wird gestartet mit der main.py

# ==========================================
# VIRTUELLE UMGEBUNG
# ==========================================

# Aktivieren (Windows CMD)
.venv\Scripts\activate

# Aktivieren (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Aktivieren (Git Bash)
source .venv/Scripts/activate

# Deaktivieren
deactivate

# ==========================================
# PAKETE INSTALLIEREN
# ==========================================

# Einzelnes Paket installieren
uv add requests

# Mehrere Pakete installieren
uv add requests pandas numpy

# Paket entfernen
uv remove requests

# ==========================================
# ABHÄNGIGKEITEN INSTALLIEREN
# ==========================================

# Alles aus pyproject.toml installieren (am besten eher über requirements.txt, steht auch hier drunter)
uv sync

# Alle Pakete aus requirements.txt installieren
uv pip install -r requirements.txt

# Aktuelle installierte Pakete in requirements.txt speichern, nicht vergessen das nach neuen Bibliotheken zu machen
uv pip freeze > requirements.txt

# ==========================================
# PYTHON AUSFÜHREN
# ==========================================

# Python-Skript starten
uv run main.py

# Alternative
uv run python main.py
