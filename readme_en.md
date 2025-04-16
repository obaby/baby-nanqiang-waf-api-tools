# NanQiang API Tools

A Python-based API tool for interacting with NanQiang (南墙) API, providing functionality for certificate management, site configuration, and user authentication.

## About NanQiang WAF

NanQiang Web Application Firewall (uuWAF) is a comprehensive website protection product developed by YouAn Technology. It is the first to implement a three-layer in-depth defense system at the traffic layer, system layer, and runtime layer. Developed based on YouAn Technology's proprietary WEB intrusion anomaly detection technology and years of accumulated experience in application security attack and defense theory and emergency response practice, it helps government agencies, enterprises, and institutions comprehensively protect WEB application security and achieve all-round protection solutions for WEB servers.

Official Website: [https://waf.uusec.com/#/?id=main](https://waf.uusec.com/#/?id=main)

## Features

- Certificate Management
  - Get certificate list
  - Check certificates
  - Submit certificate configurations
  - Delete certificates
- Site Configuration
  - Get site list
  - Update site configurations
- User Authentication
  - Login with username and password
  - Optional OTP (One-Time Password) support

## Requirements

- Python 3.x
- Required Python packages:
  - requests
  - jwt
  - urllib3

## Installation

1. Clone the repository:
```bash
git clone https://github.com/obaby/baby-nanqiang-waf-api-tools.git
cd baby-nanqiang-waf-api-toos
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from baby_nanqiang_api_tools import NanQiangAPI

# Initialize the API client
api = NanQiangAPI(base_url="https://lang.bi:443")

# Login
result = api.login(username="your_username", password="your_password")
if result:
    print("Login successful")
    
    # Get certificate list
    cert_list = api.get_cert_list()
    if cert_list:
        parsed_certs = api.parse_cert_list(cert_list)
        print("Certificate list:", parsed_certs)
```

### Certificate Management

```python
# Check certificate from files
cert_result = api.check_cert_from_files("cert.pem", "key.pem")
if cert_result:
    # Submit certificate configuration
    submit_result = api.submit_cert_config(cert_result)
    
# Delete certificate
delete_result = api.delete_cert(cert_id=123)
```

### Site Configuration

```python
# Get site list
site_list = api.get_site_list()
if site_list:
    parsed_sites = api.parse_site_list(site_list)
    print("Site list:", parsed_sites)

# Update site configuration
update_result = api.update_site_config(
    ip="192.168.1.1",
    port=443,
    site_id=123,
    uid=456,
    description="My Website"
)
```

## Security Notes

- The API client disables SSL verification by default for development purposes. In production, it's recommended to properly configure SSL certificates.
- Always store credentials securely and never commit them to version control.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

- Author: obaby
- Blog: [https://h4ck.org.cn](https://h4ck.org.cn)
- Blog: [https://oba.by](https://oba.by)

## Version

Current version: 1.0.0 