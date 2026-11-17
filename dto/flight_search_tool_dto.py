from pydantic import BaseModel,Field

class FlightSearchToolInput(BaseModel):
    
    origin:str=Field(
        description="Three-letter IATA code of the departure airport, e.g., BOM for Mumbai."
    )
    
    destination:str=Field(
        description="Three-letter IATA code of the destination airport, e.g., DEL for Delhi."
    )
    
    departure_date: str = Field(
        description="Departure date in YYYY-MM-DD format."
    )

    adults: int = Field(
        default=1,
        ge=1, #Greater than or equal to 1 this should be else pydantic will throw error 
        description="Number of adult passengers. Must be at least 1."
    )