import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

TOKEN = os.getenv("TOKEN")
DB_ENGINE = os.getenv("DB_ENGINE")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

URL_CHECK = os.getenv("URL_CHECK")
URL_TESTS = os.getenv("URL_TESTS")
URL_TEST = os.getenv("URL_TEST")
URL_COUNT = os.getenv("URL_COUNT")
URL_QUESTION = os.getenv("URL_QUESTION")
URL_ANSWER = os.getenv("URL_ANSWER")
URL_RESULT = os.getenv("URL_RESULT")

START_MESSAGE = os.getenv("START_MESSAGE")
LIST_TEST = os.getenv("LIST_TEST")
GO_MESSAGE = os.getenv("GO_MESSAGE")
NEXT_QUESTION = os.getenv("NEXT_QUESTION")
SELECTED = os.getenv("SELECTED")
ERROR = os.getenv("ERROR")
END = os.getenv("END")
