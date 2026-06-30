import json
from app.supabase import supabase
from app.services.deterministic import compute_hours, compute_program, compute_course_type
from app.services.openrouter import call as llm

SYS = "You are a PES University curriculum assistant. Given raw course input, fill missing fields, fix errors, remove redundancy, and return valid JSON in the schema shown in the example. No markdown, no commentary."

EX = """Input:
Course Title: Python for Computational Problem Solving | Offering: CS | Target: CSE | Sem: 1 | Credits: 5
Content: Python basics, data types, control flow, functions, lists, tuples, dictionaries, file I/O, OOP intro
Textbooks: 1. John Zelle - Python Programming 2. Mark Lutz - Learning Python
References:
Tools: Python 3, Jupyter

Output:
{"prelude": "This course introduces computational problem solving using Python, covering fundamental programming constructs, data structures, and object-oriented programming.", "objectives": ["Write and execute Python programs using correct syntax and semantics", "Apply control flow constructs and functions to solve problems", "Use built-in data structures — lists, tuples, dicts — effectively", "Implement file I/O and basic OOP concepts"], "units": [{"title": "Introduction to Python", "content": "Interpreter, variables, data types, input/output", "hours": 8}, {"title": "Control Flow and Functions", "content": "Conditionals, loops, function definition, scope", "hours": 10}, {"title": "Data Structures", "content": "Lists, tuples, dictionaries, sets, comprehensions", "hours": 10}, {"title": "File Handling and OOP", "content": "File I/O, exception handling, classes, objects, inheritance", "hours": 8}], "lab_experiments": ["Implement a grade calculator with statistics", "Build a text analyzer using dictionaries", "Develop a student management system using OOP"], "tools_languages": "Python 3.8+, Jupyter Notebook; AI tool - Copilot aided teaching", "desirable_knowledge": "Basic mathematical reasoning, no prior programming required"}

---

Now process this one.
Input:"""

def refine(submission_id: int):
    sub = supabase.table("submissions").select("*").eq("id", submission_id).single().execute().data
    det = compute_hours(sub["credit_category"])
    program = compute_program(sub["target_department"])
    ctype = compute_course_type(sub["credit_category"])

    prompt = f"Course Title: {sub['course_title']} | Offering: {sub['offering_department']} | Target: {sub['target_department']} | Sem: {sub['semester']} | Credits: {sub['credit_category']}\nContent: {sub['raw_course_content']}\nTextbooks: {sub['text_books']}\nReferences: {sub.get('reference_books') or '(none)'}\nTools: {sub.get('preferred_tools') or '(none)'}"

    out = llm(SYS, EX + prompt)

    merged = {
        "course_title": sub["course_title"],
        "program": program,
        "semester": sub["semester"],
        "course_type": ctype,
        **det,
        **out,
    }

    supabase.table("refined_submissions").insert({
        "submission_id": submission_id,
        "semester": int(sub["semester"]),
        "course_title": sub["course_title"],
        "refined_content": json.dumps(merged),
        "prelude": out.get("prelude", ""),
        "objectives": out.get("objectives", []),
    }).execute()

    supabase.table("submissions").update({"status": "refined"}).eq("id", submission_id).execute()

    return merged