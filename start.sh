python3 -m venv .venv;
source .venv/bin/activate;
pip3 install -r requirements.txt
python3 main.py -u "$1" -t "$2" -n "$3"