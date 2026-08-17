Wird gestartet mit der main.py
vorher wichtig uv installieren(und natürlich auch python)
-> unten tutorial zu uv


# ==========================================
# UV - WICHTIGSTE BEFEHLE (CHEATSHEET)
# ==========================================

# UV installieren
pip install uv

# Version prüfen
uv --version

# ==========================================
# NEUES PROJEKT
# ==========================================

# Neues Projekt erstellen (unnötig, haben wir schon)
uv init mein_projekt

# In Projekt wechseln
cd mein_projekt

# ==========================================
# VIRTUELLE UMGEBUNG
# ==========================================

# Virtuelle Umgebung erstellen (muss jeder selber machen meine ich)
uv venv

# Aktivieren (Windows CMD)
.venv\Scripts\activate

# Aktivieren (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Aktivieren (Git Bash)
source .venv/Scripts/activate

# Aktivieren (Linux/macOS)
source .venv/bin/activate

# Deaktivieren
deactivate

# ==========================================
# PAKETE INSTALLIEREN
# ==========================================

# Einzelnes Paket installieren
uv add requests

# Mehrere Pakete installieren
uv add requests pandas numpy

# Entwicklungsabhängigkeit installieren
uv add --dev pytest

# Paket entfernen
uv remove requests

# ==========================================
# ABHÄNGIGKEITEN INSTALLIEREN
# ==========================================

# Alles aus pyproject.toml installieren (am besten eher über requirements.txt, steht auch hier drunter)
uv sync

# ==========================================
# REQUIREMENTS.TXT
# ==========================================

# requirements.txt aus Projekt erzeugen
uv export --format requirements-txt -o requirements.txt

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

# Python-Kommando ausführen
uv run python -c "print('Hallo Welt')"

# ==========================================
# PYTHON VERSIONEN
# ==========================================

# Verfügbare Python-Versionen anzeigen
uv python list

# Python-Version installieren
uv python install 3.12

# Bestimmte Python-Version für venv nutzen
uv venv --python 3.12
