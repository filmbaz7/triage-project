from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import openai
import os

app = FastAPI()

# --------------------
#  OpenAI API KEY
# --------------------
openai.api_key = os.getenv("OPENAI_API_KEY")

class TriageRequest(BaseModel):
    symptoms: str

# --------------------
#  Serve index.html
# --------------------
@app.get("/")
def home():
    return FileResponse("index.html")

# --------------------
#  API for triage
# --------------------
@app.post("/api/triage")
async def analyze(req: TriageRequest):

    prompt = f"""
    تو یک پزشک تریاژ اورژانس هستی.
    علائم بیمار: {req.symptoms}
    تشخیص احتمالی، سطح خطر، و توصیه‌های فوری ارائه بده.
    """

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    result = response.choices[0].message["content"]

    return {"result": result}
