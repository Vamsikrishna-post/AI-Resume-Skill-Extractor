print("DEBUG: main.py is starting...")
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os
from .nlp_engine import extractor
print("DEBUG: Extractor Initialized. Starting FastAPI...")

app = FastAPI(title="AI Resume Skill Extractor")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    filename = file.filename.lower()
    contents = await file.read()
    text = ""

    if filename.endswith(".pdf"):
        from io import BytesIO
        from pdfminer.high_level import extract_text
        text = extract_text(BytesIO(contents))
    elif filename.endswith(".docx"):
        import docx
        from io import BytesIO
        doc = docx.Document(BytesIO(contents))
        text = "\n".join([para.text for para in doc.paragraphs])
    else:
        # Fallback for .txt or other formats
        try:
            text = contents.decode("utf-8")
        except:
            text = str(contents)

    if not text.strip():
        return {"error": "Could not extract text from file"}

    try:
        categorized_skills = extractor.get_skills(text)
        keywords = extractor.get_keywords(text)
        frequency = extractor.get_skill_frequency(text)

        # Simplified "LLM Hybrid" part: 
        # In a real app, we would send 'text' to Gemini/OpenAI here.
        # We'll simulate the "AI Insight" summary.
        print(f"File: {file.filename}")
        print(f"Extracted Skills: {list(categorized_skills.keys())}")
        
        # AI Summary simulation
        ai_summary = f"Based on the analysis, this candidate shows strong expertise in {', '.join(list(categorized_skills.keys())[:2]) if categorized_skills else 'general professional areas'}."

        return {
            "filename": file.filename,
            "skills": categorized_skills,
            "keywords": keywords,
            "frequency": frequency,
            "ai_summary": ai_summary
        }
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"ERROR DURING ANALYSIS: {error_detail}")
        return {"error": f"Internal Server Error: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
