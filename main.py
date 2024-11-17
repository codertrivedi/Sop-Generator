# -*- coding: utf-8 -*-

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from refine_sop import sop_generator_refiner
from question_extract import extract_questions
 

#Initialize app
app = FastAPI()


app = FastAPI()

# Extract questions from the questionnaire file
questions = extract_questions("S:/datasets/Sop_dataset/Questionnaire/questionnaire_1.docx")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def display_form():
    form_html = """
    <html>
        <head>
            <title>SOP Generator</title>
            <link rel="stylesheet" href="/static/styles.css">
        </head>
        <body>
            <div class="container">
                <h1>SOP Generator</h1>
                <form action="/generate_sop" method="post">
    """
    # Dynamically add each question as a field
    for i, question in enumerate(questions):
        form_html += f"""
        <label for="answer{i}">{question}</label><br>
        <textarea name="answer{i}" rows="4" cols="50" required></textarea><br><br>
        """
    form_html += """
                    <input type="submit" value="Generate SOP">
                </form>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=form_html)

# Route to handle SOP generation
@app.post("/generate_sop")
async def generate_sop(request: Request):  # Ensure `request` is passed as an argument
    form_data = await request.form()  # Collect all form data
    # Gather answers based on the question count, ensuring they align with the names assigned in display_form
    answers = [form_data.get(f"answer{i}", "") for i in range(len(questions))]
    
    # Debugging: Print the answers to verify they are correctly collected
    print("Collected Answers:", answers)

    try:
        sop_content = sop_generator_refiner(answers)  # Generate SOP based on answers
        return HTMLResponse(content=f"<h2>Your Generated SOP:</h2><p>{sop_content}</p>")
    except Exception as e:
        # Print error message for debugging
        print("Error during SOP generation:", str(e))
        return HTMLResponse(content=f"<h2>Error generating SOP:</h2><p>{str(e)}</p>", status_code=500)