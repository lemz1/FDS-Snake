import sqlite3
import time

DB_NAME = "Leaderboard.db"


def init_db():
    with sqlite3.connect(DB_NAME) as con:
        cur = con.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS Highscores (Teamname TEXT, Punkte INTEGER)"
        )
        con.commit()


def append_team(teamname, score):
    with sqlite3.connect(DB_NAME) as con:
        cur = con.cursor()
        cur.execute("INSERT INTO Highscores VALUES(?,?)", (teamname, score))
        con.commit()
        time.sleep(1000)


def in_top10(score: int) -> bool:
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


def get_top10():
    with sqlite3.connect(DB_NAME) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(
            "SELECT Punkte,Teamname FROM Highscores ORDER BY Punkte DESC LIMIT 10"
        )
        return cur.fetchall()


init_db()
