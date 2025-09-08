from fastapi import FastAPI
import uvicorn
from functions.database import DataBase
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db = DataBase()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/best")
def return_highscores():
    return app.state.db.get_best_alltime()


@app.get("/best-today")
def return_best_today():
    return app.state.db.get_best_date(days_ago=0,offset=0)


@app.get("/best-weekly")
def return_best_weekly():
    return app.state.db.get_best_date(days_ago=7,offset=0)


@app.get("/best-monthly")
def return_best_monthly():
    return app.state.db.get_best_date(days_ago=31,offset=10)

@app.get("/stats")
def return_stats():
    return app.state.db.get_stats()

if __name__ == "__main__":
    uvicorn.run("api:app", port=50312, reload=True)
