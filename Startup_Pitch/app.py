from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Literal
import uvicorn
from openai import OpenAI


app = FastAPI()
API_KEY="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"
class StartupForm(BaseModel):
    StartupDescription: str
    ProductStage: Literal["Idea", "MVP", "Early Revenue"]
    StartupDescriptionLen: int

@app.api_route("/", response_class=HTMLResponse)
def redirect():
    return RedirectResponse("/home")



@app.api_route("/home", response_class=HTMLResponse)
def home(request: Request):
    lines = None
    print("hello")
    with open("templates/index.html", "r") as file:
        lines = file.read()
    return HTMLResponse(lines)

def validate_data(data):
    try:
        
        
        
        startupForm = StartupForm(ProductStage=data.get("ProductStage"), StartupDescription=data.get("StartupDescription"), StartupDescriptionLen=len(data.get("StartupDescription").split(" ")))
        print(startupForm.StartupDescriptionLen)
       

        if int(startupForm.StartupDescriptionLen) < 10:
            return {"error" : "The Prompt is too Short, make sure it is 10 atleast words"}
        client = OpenAI(api_key=API_KEY, base_url="https://openrouter.ai/api/v1")
        response = client.chat.completions.create(model="openai/gpt-oss-120b:free", messages=[{"role": "user", "content" : f"Is this startup description: {startupForm.StartupDescription} too vague for an investor pitch reply in one word Yes or No nothing else"}])
        if "yes" in response.choices[0].message.content.lower():
            return {"error" : "Your Startup Description is too vague"}
        
           
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
            response = client.chat.completions.create(model="openai/gpt-oss-120b:free", messages=[{"role": "user", "content" : f"You need to generate a pitch for a startup in order to attract investors of length of 3-5 normal length sentences, this startup is at the product stage {validation.ProductStage} and is described as a startup {validation.StartupDescription} dont make anything up try to use only whats given in the description, One Sentence must explain the problem you are trying to solve, Another Sentence on the solution and who the solution is for, One sentence tailored depending on the Product Stage if it is idea imply that it is not yet implemented yet but rather a good idea if it is an MVP imagine a sort of prototype is built and tailor your response like in a way to emphasize its commercial potential, if it is early revenue imagine the startup starting to earn revenue and talk about how the money could bulster the growth of the startup, try not directly stating the product stage but rather change thee pitch and what you are asking for based on the product stage, along with this also try to emphasize what makes this startup more distinct compared to real life competitors, do it purely based on the description or product stage dont infer anything and also be very specific about competitors examine the industry name these competitors if you are able to find something distinct that makes the startup look better, try to keep the sentences short and snappy maximum 30 words per sentence and a minimum of 20 words per sentence and simplify the wording and dont infer anything beyond the startup description try to not overstate anything or sound aggressive make sure its quite professional"}])
            return JSONResponse({"pitch" : response.choices[0].message.content})
        except:
            return JSONResponse(validation)
        
        
        
            
        
        

    


        


        
uvicorn.run("app:app", port=8000)

