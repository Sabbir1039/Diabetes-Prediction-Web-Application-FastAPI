from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Union, Optional
import pickle

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

#Loading pre-trained machine learning model
try:
    diabetes_model = pickle.load(open('diabetes_model_RandomForestClassifier.sav', 'rb'))
except Exception as e:
    print("**Error occured while loading model**", e)
    diabetes_model = None

@app.post('/predict', response_class=HTMLResponse)
async def predict_diabetes(request: Request,
    patient_name: Optional[str] = Form(None),
    patient_gender: Optional[str] = Form(None),
    pregnancies: int = Form(...),
    glucose: Union[float, int] = Form(...),
    blood_pressure: Union[float, int] = Form(...),
    skin_thickness: Union[float, int] = Form(...),
    insulin: Union[float, int] = Form(...),
    bmi: Union[float, int] = Form(...),
    diabetes_pedigree_function: Union[float, int] = Form(...),
    age: int = Form(...)
):
    
    if diabetes_model is None:
        raise HTTPException(status_code=500, detail="Model not loaded. Please try again later.")
    
    try:
        input_data = [[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree_function, age]]
        
        diab_prediction = diabetes_model.predict(input_data)
        result = diab_prediction[0]
        
        probabilities = diabetes_model.predict_proba(input_data)
        # Extract probabilities
        probability_diabetic = probabilities[0][1] * 100  # Probability of being diabetic
        probability_not_diabetic = probabilities[0][0] * 100  # Probability of not being diabetic

        # Round to 2 decimal places
        probability_diabetic = round(probability_diabetic, 2)
        probability_not_diabetic = round(probability_not_diabetic, 2)
        
        if result == 1:
            prediction = "Diabetes Positve"
        else:
            prediction = "Diabetes Negative"
            
        context = {
            "patient_name": patient_name,
            "patient_gender": patient_gender,
            "pregnancies": pregnancies,
            "glucose_level": glucose,
            "blood_pressure": blood_pressure,
            "skin_thickness": skin_thickness,
            "insulin": insulin,
            "bmi": bmi,
            "diabetes_pedigree_function": diabetes_pedigree_function,
            "patient_age": age,
            "prediction": prediction,
            "probability_diabetic": probability_diabetic,
            "probability_not_diabetic": probability_not_diabetic
        }
        return templates.TemplateResponse(request=request, name="test_result.html", context=context)
    
    except Exception as e:
        print("**Error occured making prediction**", e)
        raise HTTPException(status_code=500, detail="An error occurred while making the prediction.")

@app.get("/about", response_class=HTMLResponse)
async def about_diabetes(request: Request):
    return templates.TemplateResponse(request=request, name="about_diabetes.html", context={"status": "Server is running"})

@app.get("/", name="home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="home.html")