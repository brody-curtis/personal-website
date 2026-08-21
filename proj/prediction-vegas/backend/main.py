from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from logic import logic
from preferability import preferability

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_methods=["*"],
  allow_headers=["*"],
)

class PredictInput(BaseModel):
  years: list
  player: str
  pTeamA: str
  cTeamA: str
  currentW: int
  currentY: int
  PREDICT2: float
  csv: str
  o: float
  u: float

@app.get("/")
def home():
  return {"message": "API is running"}

@app.post("/predict")
def predict_endpoint(data: PredictInput):
  prediction = logic(
    years=data.years,
    player=data.player,
    pTeamA=data.pTeamA,
    cTeamA=data.cTeamA,
    currentW=data.currentW,
    currentY=data.currentY,
    PREDICT2=data.PREDICT2,
    csv=data.csv
  )
  pref, safety, bet_side, bet_odds = preferability(
    line=data.PREDICT2,
    predict=float(prediction),
    o=data.o,
    u=data.u
  )
  return {
    "prediction": float(prediction),
    "preferability": float(pref),
    "safety": float(safety),
    "bet_side": bet_side,
    "bet_odds": bet_odds
  }