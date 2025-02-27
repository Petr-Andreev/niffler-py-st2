from typing import Optional
from sqlalchemy import create_engine, Engine, text


class UsersDB:
    engine: Engine

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)

    def delete_user_from_database(self):
        """
        Очищаем таблицы в базе данных:
        1) authority
        2) user
        """

        with self.engine.connect() as connection:
            try:
                # Удаляем все записи из таблицы authority
                connection.execute(text('DELETE FROM public."authority";'))

                # Удаляем все записи из таблицы user
                connection.execute(text('DELETE FROM public."user";'))

                # Применяем изменения
                connection.commit()
                print("Database cleaned successfully.")
            except Exception as e:
                # В случае ошибки откатываем транзакцию
                connection.rollback()
                print(f"Error while cleaning database: {e}")
