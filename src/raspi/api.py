from fastapi import FastAPI
import uvicorn
from functions.database import get_top10


app = FastAPI()


@app.get("/")
def get_highscores():
    return get_top10()


if __name__ == "__main__":
    uvicorn.run("api:app",port=50312 ,reload=True)
