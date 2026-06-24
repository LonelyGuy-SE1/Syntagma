from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI(
    title="PESU Curriculum Automation",
    version="0.1.0",
)


templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
def show_input_form(request: Request):
    return templates.TemplateResponse(
        "input_form.html",
        {"request": request},
    )