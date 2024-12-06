# Repository Details
This is the Project Repository for Backend Test for Little John

# Setup & Install PostgresSQL
* https://www.postgresql.org/download/

* Create db according to your preference, then migrate `users.sql`.

# Install Python
https://www.python.org/downloads/ -> Select Python3.11

# To Run the App, run this in terminal accordingly
* python3.11 -m venv venv
* pip install -r requirements.txt

# To generate credentials.json using google sign in endpoint.
* https://console.cloud.google.com/apis/credentials then create credentials

# Please see image google-sso-setup.png & google-setup-1.png for instructions

# To start the server
* python main.py

## Available API Endpoints 

# Google SSO API Endpoint
* http://localhost:8080/auth/register

# For Upload File Endpoint
* http://localhost:8080/user/upload_file

# For Stream File Endpoint
* http://localhost:8080/user/stream_file

# To run test to upload & stream file
* run `pytest`