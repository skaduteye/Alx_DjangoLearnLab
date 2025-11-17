# Deployment Instructions for HTTPS

To deploy this Django project securely with HTTPS:

1. **Obtain an SSL/TLS certificate**
   - Use Let's Encrypt (free) or purchase a certificate from a trusted provider.

2. **Configure your web server**
   - For Nginx:
     - Add `listen 443 ssl;` to your server block
     - Set `ssl_certificate` and `ssl_certificate_key` to your certificate files
     - Redirect HTTP to HTTPS:
       ```
       server {
           listen 80;
           server_name yourdomain.com;
           return 301 https://$host$request_uri;
       }
       ```
   - For Apache:
     - Enable `mod_ssl`
     - Set `SSLEngine on`, `SSLCertificateFile`, and `SSLCertificateKeyFile`
     - Use `Redirect permanent / https://yourdomain.com/`

3. **Update Django settings**
   - Ensure `SECURE_SSL_REDIRECT = True` and other security settings are enabled (see `settings.py`).
   - Set `ALLOWED_HOSTS` to your domain.

4. **Test your deployment**
   - Access your site via HTTPS and verify all cookies are marked as secure.
   - Use browser developer tools and online scanners (e.g., [securityheaders.com](https://securityheaders.com/)) to check headers.

---
For more details, see comments in `settings.py`.
