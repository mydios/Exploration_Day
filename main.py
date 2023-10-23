from collections import defaultdict
import datetime
from fastapi import FastAPI
import uvicorn
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

import os
from dotenv import load_dotenv
try:
    load_dotenv('.env.development')
except:
    print("PRODUCTION DETECTED")

app = FastAPI()
client = AsyncIOMotorClient(os.getenv("CONNECTION_STRING"))
db = client["dylanvanparysDotCom"]

@app.get("/hello")
async def hello():
    return {"hello": "world"}

@app.get("/")
async def root():
    projection = {"_id": 0}
    weight_entries = await db["weight"].find({}, projection).to_list(length=None)
    return {"message": "Hello World", "weight_entries": weight_entries}

@app.get("/rolling-average")
async def calculate_rolling_average():
    # Use async/await to retrieve all documents
    projection = {"_id": 0}
    cursor = db["weight"].find({}, projection)
    
    data = await cursor.to_list(None)
    
    # Parse and organize the data by day
    day_data = defaultdict(list)
    
    for doc in data:
        #format: 2023-02-14 21:46:47.387000
        timestamp = doc["entryTime"]
        #float
        weight = doc["weight"]
        ## TODO fill in day_data

        # Convert the timestamp to a date
        date = timestamp.date()

        #print("date, weight: ", date, ", ", weight)
        
        # Store the weight for the corresponding date
        day_data[date].append(weight)

    day_data_single_value = {}
    for day, weights in day_data.items():
        day_data_single_value[day] = sum(weights)/len(weights)

    
    #populate missing values
    current_day = min(day_data_single_value.keys())
    last_day = max(day_data_single_value.keys())

    last_value = day_data_single_value[current_day]

    while(current_day < last_day):
        if current_day in day_data_single_value:
            last_value = day_data_single_value[current_day]
            current_day += datetime.timedelta(days=1)
            continue
        day_data_single_value[current_day] = last_value
        current_day += datetime.timedelta(days=1)


    # Calculate the rolling average for each day
    rolling_averages = {}
    rolling_window = 7  # Adjust the window size as needed

    for day, weight in day_data_single_value.items():
        previous_days = [day]
        for i in range(1, rolling_window):
            previous_days.append(day - datetime.timedelta(days=i))
        available_days = list(filter(lambda x: (x in day_data_single_value), previous_days))
        weights = []
        for av_day in available_days:
            weights.append(day_data_single_value[av_day])
        rolling_averages[day] = sum(weights)/len(weights)

    
    rolling_averages = dict(sorted(rolling_averages.items()))


    return {"message": "Rolling Averages by Day", "rolling_averages": rolling_averages}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)