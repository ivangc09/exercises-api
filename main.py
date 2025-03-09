from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RoutineRequest(BaseModel):
    objective: str
    level: str
    days_per_week: int
    equipment: List[str]

class Excercise(BaseModel):
    name:str
    muscle_group:List[str]
    level:str
    equipment:Optional[List[str]] = None

excercises_db = [
    # Piernas
    Excercise(name="Squat", muscle_group=["Quadricep", "Gluteus"], level="Beginner", equipment=None),
    Excercise(name="Deadlift", muscle_group=["Hamstring", "Gluteus"], level="Intermediate", equipment=["barbell"]),
    Excercise(name="Lunges", muscle_group=["Quadricep", "Gluteus"], level="Beginner", equipment=["dumbbells"]),
    Excercise(name="Leg Press", muscle_group=["Quadricep", "Hamstring"], level="Intermediate", equipment=["machine"]),
    Excercise(name="Bulgarian Split Squat", muscle_group=["Quadricep", "Gluteus"], level="Advanced", equipment=["dumbbells"]),
    
    # Pecho
    Excercise(name="Bench Press", muscle_group=["Pectoral", "Tricep"], level="Beginner", equipment=["dumbells", "barbell"]),
    Excercise(name="Incline Bench Press", muscle_group=["Pectoral", "Tricep"], level="Intermediate", equipment=["barbell"]),
    Excercise(name="Push-ups", muscle_group=["Pectoral", "Tricep"], level="Beginner", equipment=None),
    Excercise(name="Dips", muscle_group=["Pectoral", "Tricep"], level="Advanced", equipment=["parallel bars"]),
    
    # Espalda
    Excercise(name="Pull-ups", muscle_group=["Lats", "Biceps"], level="Advanced", equipment=None),
    Excercise(name="Lat Pulldown", muscle_group=["Lats", "Biceps"], level="Beginner", equipment=["machine"]),
    Excercise(name="Seated Row", muscle_group=["Lats", "Trapezius"], level="Intermediate", equipment=["machine"]),
    Excercise(name="Bent-over Row", muscle_group=["Lats", "Biceps"], level="Intermediate", equipment=["barbell"]),
    
    # Hombros
    Excercise(name="Overhead Press", muscle_group=["Deltoid", "Tricep"], level="Intermediate", equipment=["barbell"]),
    Excercise(name="Lateral Raises", muscle_group=["Deltoid"], level="Beginner", equipment=["dumbbells"]),
    Excercise(name="Face Pulls", muscle_group=["Rear Deltoid"], level="Intermediate", equipment=["cable machine"]),

    # Brazos
    Excercise(name="Bicep Curl", muscle_group=["Biceps"], level="Beginner", equipment=["dumbbells", "barbell"]),
    Excercise(name="Tricep Dips", muscle_group=["Triceps"], level="Advanced", equipment=["parallel bars"]),
    Excercise(name="Hammer Curl", muscle_group=["Biceps"], level="Beginner", equipment=["dumbbells"]),
    Excercise(name="Skull Crushers", muscle_group=["Triceps"], level="Intermediate", equipment=["barbell"]),

    # Core
    Excercise(name="Plank", muscle_group=["Core"], level="Beginner", equipment=None),
    Excercise(name="Crunches", muscle_group=["Core"], level="Beginner", equipment=None),
    Excercise(name="Russian Twists", muscle_group=["Obliques"], level="Intermediate", equipment=["medicine ball"]),
    Excercise(name="Hanging Leg Raises", muscle_group=["Core"], level="Advanced", equipment=["pull-up bar"]),
]


@app.post("/generate-routine")
def generate_routine(routine_request: RoutineRequest):
    routine = {}
    for day in range(1, routine_request.days_per_week + 1):
        filtered_exercises = [
            e for e in excercises_db if e.level == routine_request.level or e.level == "Begginer"
        ]
        routine[f"Day {day}"] = random.sample(filtered_exercises, min(3, len(filtered_exercises)))
    return {"routine": routine}

@app.get("/excercises")
def get_excercises():
    return excercises_db

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)