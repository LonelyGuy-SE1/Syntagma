# Deterministic Service

def compute_hours(cat:str)->dict:
    return{
        "5":{"lecture_hours":4,"tutorial_hours":0,"practical_hours":2, "self_study":5, "credits":5},
        "4":{"lecture_hours":4,"tutorial_hours":0,"practical_hours":0, "self_study":4, "credits":4},
        "2":{"lecture_hours":2,"tutorial_hours":0,"practical_hours":0, "self_study":2, "credits":2},
        "0":{"lecture_hours":0,"tutorial_hours":0,"practical_hours":0, "self_study":0, "credits":0}
    }[cat]

def compute_program(dept: str) -> str:
    return {
        "CSE": "B. TECH IN COMPUTER SCIENCE AND ENGINEERING",
        "AIML": "B. TECH IN ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING",
        "ECE": "B. TECH IN ELECTRONICS AND COMMUNICATION ENGINEERING",
        "ME": "B. TECH IN MECHANICAL ENGINEERING",
        "EEE": "B. TECH IN ELECTRICAL AND ELECTRONICS ENGINEERING",
        "BT": "B. TECH IN BIOTECHNOLOGY",
    }[dept]

def compute_course_type(cat: str) -> str:
    return {
        "5": "Core Course-Lab Integrated",
        "4": "Core Course",
        "2": "Core Theory",
    }[cat]