import sqlite3


con = sqlite3.connect("Leaderboard.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS Highscores (Teamname TEXT, Punkte INTEGER)")
res = cur.execute("SELECT name FROM sqlite_master")


def append_team(teamname, score):
    cur.execute("INSERT INTO Highscores VALUES(?,?)", (teamname, score))
    con.commit()
