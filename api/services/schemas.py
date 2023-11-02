from pydantic import BaseModel
from enum import Enum

class ValueTypeEnum(str, Enum):
    fact = "fact"
    plan = "plan"


class FileIDResponse(BaseModel):
    file_id: int


class RequestForDiagram(BaseModel):
    file_id: int
    year: int
    value_type: ValueTypeEnum
