from pydantic import BaseModel
from datetime import date

class HouseSelection(BaseModel):
    house: int

class DateSelection(BaseModel):
    date: date
