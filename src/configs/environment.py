from os import getenv

from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = str(getenv("DATABASE_URL"))
API_ACCESS_TOKEN = str(getenv("API_ACCESS_TOKEN"))
GROUP_TOTAL_PARTICIPANTS_SAFE_LIMIT = int(
    str(getenv("GROUP_TOTAL_PARTICIPANTS_SAFE_LIMIT"))
)
DEBUG = getenv("DEBUG")
