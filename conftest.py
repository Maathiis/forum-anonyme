import os
import sys

# Permet `from api.app import app` / `from front.app import app` quand on lance `pytest`
# depuis n'importe quel sous-dossier.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

