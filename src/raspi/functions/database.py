import sqlite3
from datetime import datetime

DB_NAME = "Leaderboard.db"


class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS Highscores (Teamname TEXT, Punkte INTEGER, Zeitpunkt TEXT)"
        )
        self.conn.commit()

    #to do if not in top 10 ente team with name _ also add total time the game took in seconds
    def append_team(self, teamname, score):
        finished_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cur.execute(
            "INSERT INTO Highscores VALUES(?,?,?)", (teamname, score, finished_at)
        )
        self.conn.commit()

    # for ingame score
    def in_top10(self, score: int) -> bool:
        """
        Check if current score is in the top 10
        """
        self.cur.execute(
            "SELECT Punkte FROM Highscores ORDER BY Punkte DESC LIMIT 1 OFFSET 9"
        )
        row = self.cur.fetchone()
        if row is None:
            return True
        return score > row[0]

    # for api
    def get_best_alltime(self):
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Highscores ORDER BY Punkte DESC LIMIT 10")
        game_data = cur.fetchall()
        conn.close()
        return {"Highscores": game_data}

    # To-Do return time in format DD.MM.YYYY HH:MM:SS
    def get_best_date(self, days_ago: int, offset: int):
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            f"SELECT * FROM Highscores WHERE date(Zeitpunkt)>= date('now', '-{days_ago} days') ORDER BY Punkte DESC LIMIT 10 OFFSET ?",
            (offset,),
        )
        best_date = cur.fetchall()
        conn.close()
        return {"Highscores": best_date}

    def get_stats(self):
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # Select total games for daily, weekly, monthly and all time
        cur.execute(
            """
        SELECT
            COUNT(*),
            SUM(CASE WHEN date(Zeitpunkt) = date('now') THEN 1 ELSE 0 END),
            SUM(CASE WHEN date(Zeitpunkt) >= date('now', '-6 days') THEN 1 ELSE 0 END),
            SUM(CASE WHEN date(Zeitpunkt) >= date('now', '-29 days') THEN 1 ELSE 0 END) 
        FROM Highscores
            """
        )

        games_date = cur.fetchone()
        results = {
            "Daily": games_date[1],
            "Weekly": games_date[2],
            "Monthly": games_date[3],
            "AllTime": games_date[0],
        }
        conn.close()
        return results
