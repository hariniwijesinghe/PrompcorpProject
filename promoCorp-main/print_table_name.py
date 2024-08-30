import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'promoCorpApp.settings')

# Setup Django environment
django.setup()

# Import User model
from django.contrib.auth.models import User

# Get the table name of the default user model
table_name = User._meta.db_table

# Print the table name
print(f"User model table name: {table_name}")