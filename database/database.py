import sqlite3
from pathlib import Path
import requests

BASE_DIR = Path(__name__).resolve().parent

class DatabaseConnection:
    def __init__(self, database_path: str) -> None:
        self.database_path = database_path
        self.cursor, self.connection = self.connect()


    def connect(self) -> tuple[sqlite3.Cursor, sqlite3.Connection]:
        connection = sqlite3.connect(BASE_DIR / self.database_path)
        cursor = connection.cursor()
        return cursor, connection

class DatabaseTables(DatabaseConnection):
    def __init__(self, database_path: str) -> None:
        super().__init__(database_path)

    def create(self, query:str) -> None:
        self.cursor.executescript(query)

db_table = DatabaseTables('database.db')
db_table.create('''
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id BIGINT UNIQUE
);
CREATE TABLE IF NOT EXISTS blackjack(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_cards TEXT,
    user_score TEXT,
    comp_cards TEXT,
    comp_score TEXT,
    user_id INTEGER REFERENCES users(id)
);
CREATE TABLE IF NOT EXISTS quiz(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    all_answers TEXT,
    correct_answer TEXT,
    user_id INTEGER REFERENCES users(id)
);
''')

class UsersRepo(DatabaseConnection):
    def get_user(self, chat_id: int) -> tuple | None:
        self.cursor.execute("SELECT id FROM users WHERE chat_id = ?;", (chat_id,))
        result = self.cursor.fetchone()
        return result

    def add_user(self, chat_id:int) -> None:
        query = 'INSERT INTO users(chat_id) VALUES (?);'

        if self.get_user(chat_id) is None:
            self.cursor.execute(query, (chat_id,))
            self.connection.commit()

class BlackJackRepo(DatabaseConnection):
    def delete_cards(self,user_id):
        self.cursor.execute("DELETE FROM blackjack WHERE user_id = ?", (user_id,))
        self.cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'blackjack'")
        self.connection.commit()

    def add_cards(self,
                  user_cards: str,
                  user_score: str,
                  comp_cards: str,
                  comp_score: str,
                  user_id: int,):
        query = ('''INSERT INTO blackjack(user_cards,user_score,comp_cards,comp_score,user_id)
            VALUES(?,?,?,?,?)''')
        self.cursor.execute(query,(user_cards,user_score,comp_cards,comp_score,user_id))
        self.connection.commit()

    def get_cards(self,user_id):
        query = 'SELECT user_cards,user_score,comp_cards,comp_score FROM blackjack WHERE user_id = ?'
        result = self.cursor.execute(query,(user_id,)).fetchone()
        return result

class QuizRepo(DatabaseConnection):
    def delete_quiz(self,user_id):
        self.cursor.execute("DELETE FROM quiz WHERE user_id = ?", (user_id,))
        self.cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'quiz'")
        self.connection.commit()

    def add_question(self,
                     question: str,
                     all_answers: str,
                     correct_answer: str,
                     user_id: int,):
        query = ('''INSERT INTO quiz(question,all_answers,correct_answer,user_id)
            VALUES(?,?,?,?)''')
        self.cursor.execute(query,(question,all_answers,correct_answer,user_id))
        self.connection.commit()

    def get_quiz(self, user_id):
        query = 'SELECT question,all_answers,correct_answer FROM quiz WHERE user_id = ?'
        result = self.cursor.execute(query,(user_id,)).fetchall()
        return result

users_repo = UsersRepo(BASE_DIR/'database.db')
blackjack_repo = BlackJackRepo(BASE_DIR/'database.db')
quiz_repo = QuizRepo(BASE_DIR/'database.db')