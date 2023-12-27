git pull;
python3 -m venv .venv;
. .venv/bin/activate;
pip3 install -r requirements.txt;
nohup python3 main.py -u http://43.139.195.214:10810 -t dt1112728325 -n prod-test &;