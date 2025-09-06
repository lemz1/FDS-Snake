from fastapi import FastAPI
import uvicorn
from functions.database import DataBase
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db = DataBase()
    yield

app = FastAPI(lifespan=lifespan)



@app.get("/")
def get_highscores():
    return app.state.db.get_top10()


if __name__ == "__main__":
    uvicorn.run("api:app",port=50312 ,reload=True)
