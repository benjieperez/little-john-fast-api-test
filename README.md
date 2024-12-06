# Repository Details
This is the Project Repository for Backend Test for Little John

# Setup & Install PostgresSQL
https://www.postgresql.org/download/

# Install Python
https://www.python.org/downloads/ -> Select Python3.11

# To Run the App, run this in terminal accordingly
*  python3.11 -m venv venv
* pip install -r requirements.txt

# To start the server
* python main.py

## Available API Endpoints 

# Google SSO API Endpoint
* http://localhost:8080/auth/login

# For Upload File Endpoint
* http://localhost:8080/user/upload_file

# For Stream File Endpoint
* http://localhost:8080/user/stream_file

# To run test to upload & stream file
* run `pytest`