import random 
import time
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import asyncio
from ai4 import OTCGraphGenerator

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


class CandleData(BaseModel):
    x: int
    y: List[float]


@app.get("/get-candles/", response_model=List[CandleData])
async def generate_otc_candles(
    initial_price: float = Query(100, description="Initial price"),
    volatility_percent: float = Query(1, description="Volatility percentage"),
    trend_strength: float = Query(0.0005, description="Trend strength"),
    num_points: int = Query(1000, description="Number of data points to generate"),
    candle_size: int = Query(10, description="Number of price points per candle")
):
    generator = OTCGraphGenerator(initial_price, volatility_percent, trend_strength)

    for _ in range(num_points):
        generator.update()

    
    return generator.generate_candles_for_apexcharts(candle_size)



@app.get('/')
async def hello_world():
    return {"message": "Hello World"}


