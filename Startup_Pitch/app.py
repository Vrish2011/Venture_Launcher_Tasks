from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Literal
import uvicorn
from openai import OpenAI

API_KEY = "Your_API_KEY"
app = FastAPI()

class StartupForm(BaseModel):
    StartupDescription: str
    ProductStage: Literal["Idea", "MVP", "Early Revenue"]

@app.api_route("/", response_class=HTMLResponse)
def redirect():
    return RedirectResponse("/home")



@app.api_route("/home", response_class=HTMLResponse)
def home(request: Request):
    lines = None
    with open("templates/index.html", "r") as file:
        lines = file.read()
    return HTMLResponse(lines)

def validate_data(data):
    try:
        startupForm = StartupForm(ProductStage=data.get("ProductStage"), StartupDescription=data.get("StartupDescription"))
        return startupForm
    except:
        
        return {"error": "You need to add a product stage"}
        


       

        
        
           
                
        
        

        

@app.api_route("/generate_pitch", methods=["GET", "POST"], response_class=JSONResponse)
async def generate_startup_pitch(request: Request):
    if request.method == "POST":
        data = await request.json()
        validation = validate_data(data)
        print(validation)
        try:
            client = OpenAI(api_key=API_KEY, base_url="https://openrouter.ai/api/v1")
            response = client.chat.completions.create(model="openai/gpt-oss-120b:free", messages=[{"role": "user", "content" : f"You need to generate a pitch for a startup in order to attract investors of length of 3-4 normal length sentences, this startup is at the product stage {validation.ProductStage} and is described as a startup {validation.StartupDescription} dont make anything up try to use only whats given in the description first try to hook the investor then explain the startup then explain why they should invest, while highlighting its importance"}])
            return JSONResponse({"pitch" : response.choices[0].message.content})
        except:
            return JSONResponse(validation)
        
        
        
            
        
        

    


        


        
uvicorn.run("app:app", port=8000)

