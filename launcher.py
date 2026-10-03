from waitress import serve  # type: ignore

import os
import sys
import threading
import webbrowser
import time


# ============================================================
# GESTION PYINSTALLER
# ============================================================

if getattr(sys, 'frozen', False):

    BASE_DIR = sys._MEIPASS

    APP_DIR = os.path.dirname(
        os.path.abspath(sys.executable)
    )

else:

    BASE_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )

    APP_DIR = BASE_DIR


# ============================================================
# DOSSIER DATA
# ============================================================

DATA_DIR = os.path.join(
    APP_DIR,
    "DATA"
)

os.makedirs(
    DATA_DIR,
    exist_ok=True
)


# ============================================================
# PYTHON PATH
# ============================================================

if BASE_DIR not in sys.path:

    sys.path.insert(
        0,
        BASE_DIR
    )


# ============================================================
# DJANGO
# ============================================================

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "facturation.settings"
)

import django

django.setup()


# ============================================================
# MIGRATIONS AU DEMARRAGE
# ============================================================

from django.core.management import call_command

try:

    print("Vérification de la base de données...")

    call_command(
        "migrate",
        interactive=False,
        verbosity=0
    )

    print(
        "Base de données prête."
    )

except Exception as e:

    print(
        f"Erreur migration : {e}"
    )


# ============================================================
# WSGI
# ============================================================

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()


# ============================================================
# SERVEUR
# ============================================================

def start_server():

    try:

        serve(
            application,
            host="127.0.0.1",
            port=8000,
            threads=6
        )

    except Exception as e:

        print(
            f"Erreur serveur : {e}"
        )


# ============================================================
# NAVIGATEUR
# ============================================================

def open_browser():

    time.sleep(2)

    webbrowser.open(
        "http://127.0.0.1:8000"
    )


# ============================================================
# THREAD SERVEUR
# ============================================================

threading.Thread(
    target=start_server,
    daemon=True
).start()


# ============================================================
# THREAD NAVIGATEUR
# ============================================================

threading.Thread(
    target=open_browser,
    daemon=True
).start()


# ============================================================
# MAINTENIR L'APPLICATION
# ============================================================

while True:

    time.sleep(1)