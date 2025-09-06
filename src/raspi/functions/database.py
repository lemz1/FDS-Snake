import sqlite3
from datetime import datetime
import time

DB_NAME = "Leaderboard.db"


class DataBase:
    def __init__(self):
        with sqlite3.connect(DB_NAME) as con:
            cur = con.cursor()
            cur.execute(
                "CREATE TABLE IF NOT EXISTS Highscores (Teamname TEXT, Punkte INTEGER, Zeitpunkt TEXT)"
            )
            con.commit()

    def append_team(self,teamname, score):
        with sqlite3.connect(DB_NAME) as con:
            print("append_team")
            cur = con.cursor()
            finished_at = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            cur.execute(
                "INSERT INTO Highscores VALUES(?,?,?)", (teamname, score, finished_at)
            )
            con.commit()
            time.sleep(0.04)

    # for ingame score
    def in_top10(self,score: int) -> bool:
        """
        Check if current score is in the top 10
        """
        with sqlite3.connect(DB_NAME) as con:
            cur = con.cursor()
            cur.execute(
                "SELECT Punkte FROM Highscores ORDER BY Punkte DESC LIMIT 1 OFFSET 9"
            )
            row = cur.fetchone()
            if row is None:
                return True
            return score > row[0]

    # for api
    def get_top10(self):
        with sqlite3.connect(DB_NAME) as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM Highscores ORDER BY Punkte DESC LIMIT 10")
            game_data = cur.fetchall()
            cur.execute("SELECT COUNT(*) FROM Highscores")
            total_games = cur.fetchone()[0]
            return {"Highscores": game_data, "SpieleInsgesamt": total_games}
