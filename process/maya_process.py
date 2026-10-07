import sys, importlib

path_to_rig_folder = "C:/Users/mattis.berquez/OneDrive - PIKTURA/DEV/PY/RIG/"   # dossier qui CONTIENT mb_autoRig
if path_to_rig_folder not in sys.path:
    sys.path.append(path_to_rig_folder)

# Purge tous les sous-modules de mb_autoRig
for name in list(sys.modules):
    if name == "mb_autoRig" or name.startswith("mb_autoRig."):
        del sys.modules[name]

import mb_autoRig
mb_autoRig.show()