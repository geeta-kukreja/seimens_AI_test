import os
from dotenv import load_dotenv

load_dotenv()


DB_USER = os.getenv("DB_USER", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_PORT = os.getenv("DB_PORT", 5432)  # Change default value if locally postgres running on different port
DB_NAME = os.getenv("DB_NAME", "langchain_test")  # Change default value if locally different db is setup for current use
DB_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# print(DB_URI)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

SECRET_KEY = "langchain_task_secret_key"