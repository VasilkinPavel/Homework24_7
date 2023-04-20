import os

from dotenv import load_dotenv

load_dotenv()

my_email = os.getenv('my_email')
my_password = os.getenv('my_password')

my_email_neg = os.getenv('my_email_neg')
my_password_neg = os.getenv('my_password_neg')

my_email_null = os.getenv('my_email_null')
my_password_null = os.getenv('my_password_null')