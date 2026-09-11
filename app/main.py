from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# load .env
load_dotenv()

from app.db import init_db
from app.routers import scan, history

app = FastAPI(
    title="DeCognito",
    description="OSINT aggregation API",
    version="0.1.0"
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

# initialize the database (creates .db file & tables)
init_db()

# include routers
app.include_router(scan.router)
app.include_router(history.router)

@app.get("/")
def read_root():
    return {"message": "Hello, DeCognito!"}

