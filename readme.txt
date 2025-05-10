>>>PYTHON 3.10 <<<


sudo apt update
sudo apt install pkg-config libcairo2-dev
sudo apt install pkg-config gobject-introspection libgirepository1.0-dev cmake

THEN 

pip install -r requirements_noversion.txt

lancer avec 
LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6 streamlit run main.py

Pourquoi ? => probleme avec libstdc que conda et l'os on mais celui de conda est par defaut mais bad
