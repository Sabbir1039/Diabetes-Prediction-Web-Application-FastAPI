from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Union
import pickle

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.post('/predict')
async def predict_diabetes(request: Request,
    pregnancies: int = Form(...),
    glucose: Union[float, int] = Form(...),
    bloodPressure: Union[float, int] = Form(...),
    skinThickness: Union[float, int] = Form(...),
    insulin: Union[float, int] = Form(...),
    bmi: Union[float, int] = Form(...),
    diabetesPedigreeFunction: Union[float, int] = Form(...),
    age: int = Form(...)
):
    diabetes_model = pickle.load(open('diabetes_model_RandomForestClassifier.sav', 'rb'))
    diab_prediction = diabetes_model.predict([[pregnancies, glucose, bloodPressure, skinThickness, insulin, bmi, diabetesPedigreeFunction, age]])
    
    result = diab_prediction[0]
    context = {
        "result": result,
    }
    return templates.TemplateResponse(request=request, name="home.html", context=context)


@app.get("/about", response_class=HTMLResponse)
async def about_diabetes(request: Request):
    return templates.TemplateResponse(request=request, name="about_diabetes.html", context={"status": "Server is running"})

@app.get("/", name="home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="home.html")