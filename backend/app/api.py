from fastapi import APIRouter
from pydantic import BaseModel,Field, field_validator
from typing import Literal
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader

from app.supabase import supabase

router=APIRouter()

templates=Environment(loader=FileSystemLoader("app/templates"))

class CourseSubmission(BaseModel):
    faculty_email: str=Field(min_length=3, max_length=254)
    course_title: str=Field(min_length=3, max_length=150)
    offering_department: Literal["MA", "CS", "UZ"]
    target_department: Literal["CSE", "ECE", "ME", "BT", "EEE", "AIML"]
    semester: Literal["1", "2", "3", "4", "5", "6", "7", "8"]
    credit_category: Literal["0", "2", "4", "5"]
    raw_course_content: str=Field(min_length=50)
    text_books: str=Field(min_length=5)
    reference_books: str=""
    preferred_tools: str=""

    @field_validator(
        "faculty_email", "course_title", "raw_course_content", "text_books", "reference_books", "preferred_tools", mode="before",)
    @classmethod
    def strip(cls, v):
        return v.strip() if isinstance(v, str) else v
    
@router.post("/submissions")
def receive(data: CourseSubmission):
    """
    print("=== NEW SUBMISSION ===")
    for field, values in data.model_dump().items():
        print(f"{field}: {values}")
    print("======================")
    return {"message": "Submission received successfully!", "submission": data.model_dump()}
    """
    
    data_dict=data.model_dump()
    data_dict["status"]="pending"
    result=supabase.table("submissions").insert(data_dict).execute()
    print("New Submission Received! Course Title: ", data.course_title)
    return {"message":"Submission Received!", "submission":result.data[0]}

@router.get("/preview/semester/{sem}/courses")
def list_courses(sem:str):
    result=supabase.table("refined_submissions").select("id").execute()
    return {"course_ids": [r["id"] for r in result.data]}

@router.get("/preview/course/{refined_id}")
def preview_course(refined_id:int):
    row=supabase.table("refined_submissions").select("*").eq("id", refined_id).single().execute()
    from app.preview import build_course_preview
    course=build_course_preview(row.data)
    html=templates.get_template("jinja_sample.html").render(course=course, curriculum_year="", page_number="")
    return HTMLResponse(content=html)
