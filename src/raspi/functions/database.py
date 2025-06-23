import sqlite3


con = sqlite3.connect("Leaderboard.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS Highscores (Teamname TEXT, Punkte INTEGER)")
res = cur.execute("SELECT name FROM sqlite_master")


def append_team(teamname, score):
    cur.execute("INSERT INTO Highscores VALUES(?,?)", (teamname, score))
    con.commit()


def in_top10(score: int) -> bool:

    """
    Check if current score is in the top 10
    """
    cur.execute("SELECT Punkte FROM Highscores ORDER BY Punkte DESC LIMIT 1 OFFSET 9")
    row = cur.fetchone()
    if row is None:
        return True
    return score > row[0]
