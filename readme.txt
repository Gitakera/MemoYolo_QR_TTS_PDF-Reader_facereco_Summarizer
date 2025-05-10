# 🚀 Projet Python 3.10 – Lancement avec Streamlit

## 📦 Prérequis

Assurez-vous d’avoir **Python 3.10** installé.

Installez les bibliothèques système nécessaires :

```bash
sudo apt update
sudo apt install -y pkg-config libcairo2-dev
sudo apt install -y gobject-introspection libgirepository1.0-dev cmake
```

## 📚 Installation des dépendances Python

Deux fichiers de dépendances sont disponibles :

* `requirements.txt` : contient les versions exactes des packages (recommandé pour la reproduction stricte).
* `requirements_noversion.txt` : contient uniquement les noms des packages, utile pour éviter les conflits de versions.

Installez l’un ou l’autre selon vos besoins :

```bash
# Avec versions précises
pip install -r requirements.txt

# Ou sans versions
pip install -r requirements_noversion.txt
```

## ▶️ Lancement de l'application

Lancez l’application Streamlit avec la commande suivante :

```bash
LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6 streamlit run main.py
```

## ❓ Pourquoi utiliser `LD_PRELOAD` ?

Cela force l’utilisation de la version système de `libstdc++.so.6`.

> ⚠️ Cela est nécessaire si vous utilisez un environnement Conda, qui peut référencer une version incompatible de cette bibliothèque, entraînant des erreurs.

---
