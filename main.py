from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib
import traceback

# 1. Initialize FastAPI app
app = FastAPI()

# 2. Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Load your machine learning model
model = joblib.load("placement_model.pkl")

# 4. Define the prediction route
@app.post("/predict")
def predict(
    gender: str = Form(...),
    ssc_p: float = Form(...),
    hsc_s: str = Form(...),
    hsc_p: float = Form(...),
    degree_t: str = Form(...),
    degree_p: float = Form(...),
    etest_p: float = Form(...)
):
    try:
        # Construct input dictionary from form parameters
        input_dict = {
            "gender": gender,
            "ssc_p": ssc_p,
            "hsc_s": hsc_s,
            "hsc_p": hsc_p,
            "degree_t": degree_t,
            "degree_p": degree_p,
            "etest_p": etest_p
        }

        # Match text fields to what your ML model expects
        input_dict['gender'] = 1 if input_dict['gender'].upper() == 'M' else 0
        
        if input_dict['hsc_s'].lower() == 'science':
            input_dict['hsc_s'] = 0
        elif input_dict['hsc_s'].lower() == 'commerce':
            input_dict['hsc_s'] = 1
        else:
            input_dict['hsc_s'] = 2

        if 'science&Tech' in input_dict['degree_t'].strip():
            input_dict['degree_t'] = 0
        else:
            input_dict['degree_t'] = 1

        # Convert to DataFrame and predict
        data = pd.DataFrame([input_dict])
        prediction = model.predict(data)

        # Return the prediction value
        return {"prediction": str(prediction[0])}

    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}