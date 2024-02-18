import configparser
import pathlib

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

file_config = pathlib.Path(__file__).parent.parent.joinpath('config.ini')
config = configparser.ConfigParser()
config.read(file_config)

# Для PostgreSQL формат: postgresql://<username>:<password>@<host>:<port>/<database_name>
username = config.get('DEV_DB', 'USER')
password = config.get('DEV_DB', 'PASSWORD')
host = config.get('DEV_DB', 'HOST')
port = config.get('DEV_DB', 'PORT')
database_name = config.get('DEV_DB', 'DB_NAME')

# Формуємо рядок підключення
URI = f'postgresql://{username}:{password}@{host}:{port}/{database_name}'
print(URI)

# Створюємо об'єкт рушія (engine)
engine = create_engine(URI, echo=False, pool_size=5, max_overflow=0)

# Для роботи з ORM SQLAlchemy створюють об'єкт сесії для роботи з базою даних
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Перевірка з'єднання
if __name__ == '__main__':
    try:
        # Відкриваємо з'єднання з базою даних
        with engine.connect() as connection:
            # Виконуємо SQL-запит для отримання назви поточної бази даних
            result = connection.execute(text("SELECT current_database()"))
            # Отримуємо результат запиту
            db_name = result.scalar()

            # Виводимо назву бази даних
            print("Connection successful!\nDatabase name:", db_name)

    except OperationalError as e:
        # Виникає виключення, якщо підключення не вдалося
        print("Connection failed:", e)
