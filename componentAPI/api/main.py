from fastapi import FastAPI
import pandas as pd

app = FastAPI()

componentFIle = pd.read_csv("comps.csv")

@app.get("/allCopms")
async def allCopms():
    return componentFIle["cNumber"]