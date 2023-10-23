from dotenv import load_dotenv

load_dotenv('.env.development')

from main import app as app_prod
import uvicorn

app = app_prod


if __name__ == "__main__":
    uvicorn.run("dev:app", host="0.0.0.0", port=8000, reload=True)