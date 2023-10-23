from dotenv import load_dotenv

load_dotenv('.env.development')

from main import app as app_prod

app = app_prod
