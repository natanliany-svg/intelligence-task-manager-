
from pydantic import BaseModel

class AgnetSchema(BaseModel):
    name: str
    specialty: str
    agent_rank: str

class MisisonSchema(BaseModel):
    title: str
    description: str
    location: str
    difficulty: int
    importance: int

def calc_risk(diff, imp):
    val = (diff * 2) + imp
    if val <= 9:
        return "LOW"
    if val <= 17:
        return "MEDIUM"
    if val <= 24:
        return "HIGH"
    return "CRITICAL"
