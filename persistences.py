from kink import di, inject
from sqlite3 import Error

from dtos import LoginDTO, RegisterDTO, UserDTO, LeaderboardDTO

import sqlite3
import os


@inject
class DashSqlDb:
    def __init__(self, db_init: str, db_filename: str, main_dir: str):
        self.db_init = db_init
        self.db_filename = db_filename
        self.db_path = os.path.join(main_dir, db_filename)

        # inisialisasi connection
        self.conn = None
        self.cursor = None

        self.setup_database()

    def setup_database(self):
        if self.db_init == "True":
        # if self.db_init == "True" or os.getenv("PYCHARM_HOSTED") is not None:
            self.recreate_db()

        self.conn = self.create_connection(self.db_path)
        self.cursor = self.conn.cursor()

        if self.db_init == "True":
        # if self.db_init == "True" or os.getenv("PYCHARM_HOSTED") is not None:
            self.setup_db()

    def recreate_db(self):
        if os.path.exists(self.db_path):  # hapus file .db yang sudah ada
            os.remove(self.db_path)

        with open(self.db_filename, "w") as db_file:  # buat file .db baru
            pass

    def create_connection(self, db_path):
        conn = None
        try:
            conn = sqlite3.connect(db_path)
        except Error as e:
            print(e)
        
        return conn
    
    def setup_db(self):
        sql_setup_table = """CREATE TABLE player_data (
                            username text,
                            email text,
                            score int
        )"""

        self.cursor.execute(sql_setup_table)
        self.conn.commit()
    
    def register_acc(self, _register_dto: RegisterDTO) -> None:
        temp_username = _register_dto.username
        temp_email = _register_dto.email

        print("AAH")
        sql_insert_player = f'''
                INSERT INTO player_data VALUES (?, ?, 0)''' 
        
        self.cursor.execute(sql_insert_player, (temp_username, temp_email, ))
        self.conn.commit()

        # results = []
        # for row in all_records:
        #     results.append(UserDTO(row[0], row[1], row[2]))
        
        # return results
    
    def login_acc(self, _username): # erin
        pass
        
    def show_players(self):
        sql_show_players = '''SELECT * FROM player_data'''

        all_records = self.cursor.execute(sql_show_players)
        self.conn.commit()

        results = []
        for row in all_records:
            results.append(UserDTO(row[0], row[1], row[2]))
        
        return results
    
    def set_high_scores(self, _username, _score):
        sql_high_score = '''UPDATE player_data
                            SET score = ?
                            WHERE username = ? AND score<?'''
        
        all_records = self.cursor.execute(sql_high_score, (_score, _username, _score))
        
        results = []
        for row in all_records:
            results.append(UserDTO(row[0], row[1], row[2]))
        
        return results
    
    def get_leaderboards(self):
        sql_top_five = f'''SELECT username, score FROM player_data
                            ORDER BY score DESC'''
        
        all_records = self.cursor.execute(sql_top_five)
        
        results = []
        for row in all_records.fetchall():
            results.append(LeaderboardDTO(row[0], row[1]))
        
        return results
    
    def search_player(self, _username):
        sql_search = f'''SELECT * FROM player_data WHERE username = ?'''
        all_records = self.cursor.execute(sql_search, (_username, ))
        
        results = []
        for row in all_records:
            results.append(UserDTO(row[0], row[1], row[2]))
            
        return results