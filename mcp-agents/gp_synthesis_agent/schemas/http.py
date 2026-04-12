
from datetime import date
from pydantic import BaseModel, Field  

class GetSynthesisRequest(BaseModel):
    user_id: str = Field(description="Identifier of the patient.")
    start_date: date = Field(
        description="ISO 8601 start date for history retrieval (YYYY-MM-DD)."
    )   