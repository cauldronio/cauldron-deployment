"""
Rename this file as 'settings_secret.py' and fill the parameters
"""

# Generate a new Django key with 'openssl rand -base64 32'
DJANGO_KEY = ''

# Create a GitHub Oauth Application and get the keys
GH_CLIENT_ID = ''
GH_CLIENT_SECRET = ''

# Create a GitLab Oauth Application and get the keys
GL_CLIENT_ID = ''
GL_CLIENT_SECRET = ''

# Create a private Token for Gitlab.
# This will not be necessary in the future.
# Now perceval cannot doesn't allow oauth tokens
GL_PRIVATE_TOKEN = ''

# Database configuration
DB_NAME = 'db_cauldron'
DB_USER = 'grimoirelab'
DB_PASSWORD = ''
DB_HOST = 'grimoirelab_service'
DB_PORT = '3306'