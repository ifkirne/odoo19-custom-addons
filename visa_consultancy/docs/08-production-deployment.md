# Phase 5 — Day 8: Production Deployment & Hosting Odoo 19

## Objective
Move from a development machine to a real, internet-facing production server delivering the ERP to actual users.

## Deployment Architecture
```
User Browser
     |
   HTTPS
     |
 Nginx Server
     |
Odoo Application
     |
PostgreSQL Database
     |
 File Storage
```

## Step 1 — Choose Server (VPS)
Recommended minimum for a small consultancy:
```
CPU     : 2 cores
RAM     : 4 GB
Storage : 40-80 GB SSD
OS      : Ubuntu 24.04 LTS
```
Providers: DigitalOcean, Hetzner, Contabo, Linode, AWS Lightsail.

## Step 2 — Connect to Server
```bash
ssh root@SERVER_IP
```

## Step 3 — Update Ubuntu
```bash
apt update && apt upgrade -y
apt install git wget curl nano unzip -y
```

## Step 4 — Create Odoo User
Never run Odoo as root.
```bash
adduser odoo
usermod -aG sudo odoo
su - odoo
```

## Step 5 — Install PostgreSQL
```bash
sudo apt install postgresql postgresql-contrib -y
sudo systemctl status postgresql
sudo su - postgres
createuser -s odoo
exit
```

## Step 6 — Install Python Environment
```bash
sudo apt install python3 python3-pip python3-venv \
python3-dev gcc g++ make \
libxml2-dev libxslt1-dev \
libldap2-dev libsasl2-dev \
libjpeg-dev \
libpq-dev \
-y

python3 --version   # Odoo 19 requires Python 3.10+
```

## Step 7 — Download Odoo 19
```bash
cd /opt
sudo git clone https://github.com/odoo/odoo.git --branch 19.0 --depth 1
sudo mv odoo odoo19
sudo chown -R odoo:odoo /opt/odoo19
```

## Step 8 — Create Virtual Environment
```bash
su - odoo
cd /opt/odoo19
python3 -m venv venv
source venv/bin/activate
pip install wheel
pip install -r requirements.txt
```

## Step 9 — Deploy Custom Module
```bash
mkdir /opt/custom_addons
```
Upload `visa_consultancy` into `/opt/custom_addons/`:
```
/opt
├── odoo19
└── custom_addons
       └── visa_consultancy
```

## Step 10 — Odoo Configuration
```bash
sudo nano /etc/odoo19.conf
```
```ini
[options]
admin_passwd = strong_master_password
db_host = False
db_port = False
db_user = odoo
db_password = False
addons_path = /opt/odoo19/addons,/opt/custom_addons
http_port = 8069
logfile = /var/log/odoo19/odoo.log
```
```bash
sudo mkdir /var/log/odoo19
sudo chown odoo:odoo /var/log/odoo19
```

## Step 11 — System Service (systemd)
```bash
sudo nano /etc/systemd/system/odoo19.service
```
```ini
[Unit]
Description=Odoo 19 ERP
After=network.target postgresql.service

[Service]
Type=simple
User=odoo
ExecStart=/opt/odoo19/venv/bin/python3 /opt/odoo19/odoo-bin -c /etc/odoo19.conf
Restart=always

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl daemon-reload
sudo systemctl start odoo19
sudo systemctl enable odoo19
sudo systemctl status odoo19
```

## Step 12 — Test Odoo
Open `http://SERVER_IP:8069` → should show the Database Manager / Create Database screen.

## Step 13 — Configure Domain
Example: `myvisaerp.com`
```
Type: A   Name: @    Value: SERVER_IP
Type: A   Name: www  Value: SERVER_IP
```
After DNS propagation, the domain points to the VPS.

## Step 14 — Install Nginx (Reverse Proxy)
Why: users should access `https://myvisaerp.com`, not `http://IP:8069`.
```bash
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/odoo19
```
```nginx
server {
    listen 80;
    server_name myvisaerp.com www.myvisaerp.com;

    location / {
        proxy_pass http://127.0.0.1:8069;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```
```bash
sudo ln -s /etc/nginx/sites-available/odoo19 /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

## Step 15 — Enable HTTPS (SSL)
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d myvisaerp.com -d www.myvisaerp.com
```
Result: `http://myvisaerp.com` becomes `https://myvisaerp.com`.

## Step 16 — Backup Strategy
```bash
# Backup
pg_dump database_name > backup.sql

# Restore
psql database_name < backup.sql
```
Recommended: a nightly cron job (e.g. 2 AM) dumping the database and uploading it to cloud storage.

## Final Production Checklist

**Development**
| Item | Status |
|---|---|
| Custom module | ✅ |
| Models | ✅ |
| Views | ✅ |
| Security | ✅ |
| Workflow | ✅ |
| Documents | ✅ |
| Payments | ✅ |
| Appointments | ✅ |
| Reports | ✅ |

**Deployment**
| Item | Status |
|---|---|
| Ubuntu Server | ✅ |
| PostgreSQL | ✅ |
| Odoo Service | ✅ |
| Custom Addons | ✅ |
| Domain | ✅ |
| Nginx | ✅ |
| SSL | ✅ |
| Backup | ✅ |

## Full Waterfall Recap
```
Phase 1  Requirement Analysis
Phase 2  System Design
Phase 3  Database & Architecture
Phase 4  Development
Phase 5  Testing
Phase 6  Deployment
```

---
**Previous:** [07-professionalization.md](07-professionalization.md) · **Next:** [09-website-portal.md](09-website-portal.md)
