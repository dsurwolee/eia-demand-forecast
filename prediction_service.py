from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
import numpy as np
import tensorflow as tf

# Load Model 
lstm = tf.keras.models.load_model('lstm_model')

# To jump start the prediction service, run this command:
# uvicorn prediction_service:app --reload
# Make request via UI on: //localhost:8000/docs?/predict

# Initialize the FastAPI server instance
app = FastAPI()

# Pydantic models
class ModelInput(BaseModel):
	inputs: List[float]

# API Calls
@app.get("/")
async def home():
    return {"Hello": "World"}

@app.post("/predict/")
async def model_predict(payload: ModelInput):
	inputs = np.array(payload.inputs)[None, :]
	tf_input = tf.reshape(inputs, [1, 24, 1])
	tf_output = lstm.predict(tf_input)
	tf_output =	tf.reshape(tf_output, [-1]).numpy().tolist()
	print(tf_output)
	return {'prediction': tf_output}