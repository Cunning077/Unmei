from dotenv import load_dotenv
import os

load_dotenv()

db_name = os.getenv("DBNAME")
global_host = os.getenv('GLOBAL_HOST')
reader_user = os.getenv('READER_USER')
reader_password = os.getenv('READER_PASSWORD')
writer_user = os.getenv('WRITER_USER')
writer_password = os.getenv('WRITER_PASSWORD')
