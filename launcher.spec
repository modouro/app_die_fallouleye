# -*- mode: python ; coding: utf-8 -*-


import os
import sys

from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT


# ============================================================
# DOSSIER DU PROJET
# ============================================================

project_dir = os.getcwd()


# ============================================================
# DJANGO
# ============================================================

if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "facturation.settings"
)

import django

django.setup()


# ============================================================
# MIGRATIONS AUTOMATIQUES AVANT COMPILATION
# ============================================================

from django.core.management import call_command

print("\n" + "=" * 60)
print("MIGRATION DE LA BASE DE DONNEES")
print("=" * 60)

try:

    call_command(
        "migrate",
        interactive=False,
        verbosity=1
    )

    print("=" * 60)
    print("MIGRATIONS TERMINEES AVEC SUCCES")
    print("=" * 60 + "\n")

except Exception as e:

    print("=" * 60)
    print("ERREUR DE MIGRATION")
    print("=" * 60)
    print(e)

    raise


def collect_folder(src_folder, dest_folder):
    datas = []
    if os.path.exists(src_folder):
        for root, _, files in os.walk(src_folder):
            for f in files:
                full_path = os.path.join(root, f)
                dest_path = os.path.join(dest_folder, os.path.relpath(root, src_folder))
                datas.append((full_path, dest_path))
    return datas

datas = []
datas += collect_folder(os.path.join(project_dir, "templates"), "templates")
datas += collect_folder(os.path.join(project_dir, "static"), "static")
datas += collect_folder(os.path.join(project_dir, "media"), "media")

# ============================================================
# DOSSIER DATA
# ============================================================

data_dir = os.path.join(
    project_dir,
    "DATA"
)

os.makedirs(
    data_dir,
    exist_ok=True
)


# ============================================================
# BASE DE DONNÉES
# ============================================================

db_path = os.path.join(
    data_dir,
    "db.sqlite3"
)

if not os.path.exists(db_path):

    raise FileNotFoundError(
        f"Base de données introuvable : {db_path}"
    )

print(
    f"Base SQLite utilisée : {db_path}"
)

datas.append(
    (
        db_path,
        "DATA"
    )
)

a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'waitress',
        'django',
        'weasyprint',
        'weasyprint.text',
        'weasyprint.images',
        'weasyprint.fonts',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='launcher',
    debug=False,
    strip=False,
    upx=True,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='launcher',
)