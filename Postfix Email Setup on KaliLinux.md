## Setting up Email Sending with Postfix on Kali Linux

This guide explains how to configure Postfix on Kali Linux to send emails via Gmail SMTP. It includes steps to open firewall ports, install required packages, create SSL certificates, and configure Postfix.

### 1. Change Email Settings for Second Password

- Update email settings to allow a second password.

### 2. Firewall Configuration

Check firewall rules using `iptables`:
```bash
iptables -L
```

Open port 587 (SMTP) for both inbound and outbound traffic:
```bash
sudo iptables -A INPUT -p tcp --dport 587 -j ACCEPT
sudo iptables -A OUTPUT -p tcp --dport 587 -j ACCEPT
```

### 3. Package Installation and Postfix Setup

Update packages and install necessary tools:
```bash
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install postfix mailutils libsasl2-2 ca-certificates libsasl2-modules
```

Enable the Postfix service:
```bash
sudo systemctl enable postfix
```

### 4. SSL Certificate Creation

Create a directory for SSL certificates and generate a self-signed certificate:
```bash
sudo mkdir /etc/postfix/ssl/
cd /etc/postfix/ssl/
sudo openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout cacert-smtp-gmail.key -out cacert-smtp-gmail.pem
```

### 5. Postfix Configuration

Edit the Postfix configuration file:
```bash
sudo nano /etc/postfix/main.cf
```
Add the following lines:
```plaintext
relayhost = [smtp.gmail.com]:587
smtp_sasl_auth_enable = yes
smtp_sasl_password_maps = hash:/etc/postfix/smtp_sasl_password_map
smtp_sasl_security_options = noanonymous
smtp_tls_CAfile = /etc/postfix/ssl/cacert-smtp-gmail.pem
smtp_use_tls = yes
```

### 6. Create SMTP Credentials File

Create and edit the SMTP credentials map file:
```bash
sudo nano /etc/postfix/smtp_sasl_password_map
```
Add your Gmail SMTP credentials:
```plaintext
[smtp.gmail.com]:587 USERNAME@gmail.com:YOUR_APPLICATION_PASSWORD
```

Set appropriate permissions and update the hash database:
```bash
sudo chmod 400 /etc/postfix/smtp_sasl_password_map
sudo postmap /etc/postfix/smtp_sasl_password_map
```

### 7. Manage Postfix Service

Restart Postfix for changes to take effect:
```bash
sudo systemctl restart postfix 
```

Check the status of Postfix:
```bash
sudo systemctl status postfix 
```

### 8. Send Test Email

Send a test email using Postfix:
```bash
echo 'test mail from postfix" | mail -s "Test postfix" recipient@example.com
```

---
### Conclusion!!!

- This guide outlines the step-by-step process to configure and use Postfix on Kali Linux to send emails via Gmail's SMTP server.
- Adjust the placeholders (`USERNAME@gmail.com`, `YOUR_APPLICATION_PASSWORD`, `recipient@example.com`) with your actual credentials and recipient email address.