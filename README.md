# Google Data Uploader

Requirements:
  - Modern Python3
  - Requirements listed in requirements.txt
  - .env file with needed variables (in password manager)
  - pcsd-google-data service account key (in password manager)
  - venv

Files:
  - Configure .env with needed variables:
```bash
    CLIENT_ID
    CLIENT_SECRET
    SCOPE="https://www.googleapis.com/auth/admin.directory.device.chromeos.readonly"
    ENDPOINT="https://accounts.google.com/o/oauth2/v2/auth"
    CUSTOMER_ID=

    VAULT_HOST_IP
    VAULT_HOST_PORT
    VAULT_USER
    VAULT_PASSWORD
    VAULT_DATABASE
```

# Usage
Create venv
```bash
python3 -m venv google-data
```
activate venv
```bash
source google-data/bin/activate
```
install requirements
```bash
pip install -r requirements.txt
```
run the script
```bash
python3 main.py
```
run with cron
```bash
crontab -e
```
add the following line. this will run at 1am every day
```bash
0 1 * * * /bin/bash /docker/pcsd-google-data/run.sh
```
