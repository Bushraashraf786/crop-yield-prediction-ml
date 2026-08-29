from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import pickle
import numpy as np
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model = pickle.load(open("dtr.pkl", "rb"))
preprocessor = pickle.load(open("processor.pkl", "rb"))

# Yeh route frontend (crop.html) ko serve karta hai jab koi
# root URL ("/") kholega - isi tarah local aur deployed dono jagah
# frontend + backend EK HI URL se milte hain, alag se koi
# 127.0.0.1 ya extra setup ki zaroorat nahi rehti.
@app.get("/")
def read_index():
    return FileResponse("crop.html")

@app.post("/predict")
def predict(
    year: int = Form(...),
    rainfall: float = Form(...),
    pesticides: float = Form(...),
    temp: float = Form(...),
    area: str = Form(...),
    item: str = Form(...)
):
    try:
        # Colab exact features columns structural list alignment
        columns_layout = ['Year', 'average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp', 'Area', 'Item']
        
        # Wrapping array raw inputs inside a structured Dataframe layout metadata
        raw_inputs = [[year, rainfall, pesticides, temp, area, item]]
        df_inputs = pd.DataFrame(raw_inputs, columns=columns_layout)
        
        # Transform structural variables safely
        clean_inputs = preprocessor.transform(df_inputs)
        result = model.predict(clean_inputs)
        
        
return {"predicted_yield": round(float(result[0]), 2)}
    except Exception as e:
        return {"error": str(e)}

