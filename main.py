from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Union, Optional
import pickle

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

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
    diabetes_model = pickle.load(open('diabetes_model_RandomForestClassifier.sav', 'rb'))
    diab_prediction = diabetes_model.predict([[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree_function, age]])
    
    result = diab_prediction[0]
    
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
        "prediction": prediction
    }
    return templates.TemplateResponse(request=request, name="test_result.html", context=context)


@app.get("/about", response_class=HTMLResponse)
async def about_diabetes(request: Request):
    return templates.TemplateResponse(request=request, name="about_diabetes.html", context={"status": "Server is running"})

@app.get("/", name="home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="home.html")