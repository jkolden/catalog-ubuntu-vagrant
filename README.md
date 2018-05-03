# Udacity FSND - Linux Server Configuration Project
This describes the steps taken to deploy the catalog Flask application to an ubuntu linux server

## IP address & URL
- Public IP address: 18.236.198.135
- URL: http://ec2-18-236-198-135.us-west-2.compute.amazonaws.com/

## The following software was installed on my ubuntu server to facilitate app hosting:
- apache2
- libapache2-mod-wsgi
- postgresql
- pip
- python-dev
- Flask
- sqlalchemy
- oauth2client
- requests
- psycopg2

## Configurations
### SSH login as ubuntu from the local machine
Login to Amazon Lightsail's machine only by the browser-based terminal window.

1. Generate ssh key pair for the user `ubuntu` on the client machine
    - `cd ~/.ssh`
    - `ssh-keygen`
        - I named the key pair "udacity"
2. Copy the content of udacity.pub file
    - `cat ~/.ssh/udacity.pub`
3. Paste it in authorized_keys on the Amazon Lightsail machine
    - `sudo nano ~/.ssh/authorized_keys`
4. Test we can login the remote machine by ssh from our local machines
    - `ssh ubuntu@18.236.198.135 -p 22 -i ~/.ssh/udacity.pem`

### Firewall Configuration

#### ufw
Open 80, 123, 2200.

1. Ensure that the firewall is currently disabled
    - `sudo ufw status`
2. Allow http to use the port 80
    - `sudo ufw allow 80`
5. Allow ntp to use the port 123
    - `sudo ufw allow 123`
6. Allow ssh to use the port 2200
    - `sudo ufw allow 2200/tcp`
7. Enable the firewall
    - `sudo ufw enable`
8. Check the firewall is configured properly
    - `sudo ufw status`
        - Confirm that only 22, 80, 123, 2200 are open

#### sshd
Modify sshd configuration so that sshd observes the port 2200.

1. Modify `Port 22` to `Port 2200` in sshd_config file
    - `sudo nano /etc/ssh/sshd_config`
2. Restart sshd
    - `sudo service sshd restart`
3. Confirm we cannot login by the old port 22
    - `ssh ubuntu@18.236.198.135 -p 22 -i ~/.ssh/udacity.pem`
3. Re-login by new port 2200
    - `ssh ubuntu@18.236.198.135 -p 2200 -i ~/.ssh/udacity.pem`

#### Close port 22
1. Let ufw deny port 22
    - `sudo ufw deny ssh`
2. Enable the firewall
    - `sudo ufw enable`
3. Check port 22 is successfully denied
    - `sudo ufw status`

### Install most recent software
     `sudo apt-get update`
     `sudo apt-get upgrade`

### User authentication
#### Disable password-based login
- Change `PasswordAuthentication` to `no` and make sure `PubkeyAuthentication` is `yes`
    - `sudo nano /etc/ssh/sshd_config`
    - `sudo service ssh restart`

#### Disable remote login of the user `root`
- Change `PermitRootLogin` to `no`
    - `sudo nano /etc/ssh/sshd_config`
    - `sudo service ssh restart`

#### Create new user `grader`
1. Create new user "grader"
    - `sudo adduser grader`
2. Give the user "grader" sudo access
    - `sudo nano /etc/sudoers.d/grader`
        - The content: `grader ALL=(ALL:ALL) ALL`
        - **The grader user will have a password of "grader" when performing sudo commands.**   
3. Generate ssh key pair for `grader` on the client
    - `cd ~/.ssh`
    - `ssh-keygen`
    - I named my key pair `grader_key`
4. Load the generated public key to the ubuntu server
    - `sudo su - grader`
    - `mkdir ~/.ssh`
    - `touch ~/.ssh/authorized_keys`
    - Copy the content of pub file from the client
    - `sudo nano ~/.ssh/authorized_keys`
        - Paste the pub's content above
    - `chmod 700 ~/.ssh`
    - `chmod 600 ~/.ssh/authorized_keys`
5. Test you can login as `grader` by ssh on port 2200
    - `ssh grader@18.236.198.135 -p 2200 -i ~/.ssh/grader_key`

### Add Google OAuth origin to the project on the Google Cloud Console
1. Add the URL `http://ec2-18-236-198-135.us-west-2.compute.amazonaws.com/` to authorized Javascript Origins and Authorized redirect URIs 
2. Download new client_secrets.json and replace the old one. In my case I had already clones my git repo so I made this change via sudo nano on the ubuntu server.

### Create environment for Flask app
1. Put Catalog app under `/var/www`
    - `cd /var/www/`
    - Clone this git repo: `sudo git clone https://github.com/jkolden/catalog-ubuntu-vagrant.git`

2. Install Flask in virtual environment by pip
    - `cd catalog/`
    - `sudo apt-get install python-pip`
    - `sudo pip install virtualenv`
    - `sudo virtualenv venv`
    - `source venv/bin/activate`
    - `sudo pip install Flask sqlalchemy oauth2client requests psycopg2`

### Add Posgresql user and database for the Catalog app

1. Change the user to `postgres`
    - `sudo su - postgres`
2. Create the user `catalog`
    - `createuser catalog with password 'catalog'`
3. Create DB `catalog`
    - `psql -c 'create database catalog;'`
4. Create tables and load data to DB
    - `cd /var/www/catalog/catalog`
    - `python database_setup1.py`
    - `python categories.py`

### Apache and wsgi
1. Install Apache
    - `sudo apt-get install apache2`
    
2. Set up Apache config for Item Catalog app
    - `sudo nano /etc/apache2/sites-available/catalog.conf`
```xml
<VirtualHost *:80>
    ServerName 18.236.198.135.xip.io
    ServerAlias ec2-18-236-198-135.us-west-2.compute.amazonaws.com
    ServerAdmin admin@18.236.198.135
    WSGIDaemonProcess catalog python-path=/var/www/catalog:/var/www/catalog/venv/lib/python2.7/site-packages
    WSGIProcessGroup catalog
    WSGIScriptAlias / /var/www/catalog/catalog.wsgi
    <Directory /var/www/catalog/catalog/>
        Order allow,deny
        Allow from all
    </Directory>
    Alias /static /var/www/catalog/catalog/static
    <Directory /var/www/catalog/catalog/static/>
        Order allow,deny
        Allow from all
    </Directory>
    ErrorLog ${APACHE_LOG_DIR}/error.log
    LogLevel warn
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```
3. Enable the virtual host
    - `sudo a2ensite catalog`
4. Install mod_wsgi
    - `sudo apt-get install libapache2-mod-wsgi python-dev`
    - `sudo a2enmod wsgi`
7. Create the wsgi file
    - `cd /var/www/catalog`
    - `sudo nano catalog.wsgi`
```python
#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/catalog/")
from catalog.application import app as application
application.secret_= 'some_secret_key'
```
7. Restart Apache
    - `sudo service apache2 restart`
8. Navigate to http://ec2-18-236-198-135.us-west-2.compute.amazonaws.com/. 
- Test login and adding categories/items.

## Third-party references
- [DNS Lookup](http://www.kloth.net/services/nslookup.php)
- [How to deplay a Flask app - Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)
- [How to install Postgresql on Ubuntu - Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04)
- [Engine Configuration¶](http://docs.sqlalchemy.org/en/latest/core/engines.html)
- [PostgreSQL](http://docs.sqlalchemy.org/en/latest/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg2)
- [Great readme by RR Joson](https://github.com/rrjoson/udacity-linux-server-configuration)
