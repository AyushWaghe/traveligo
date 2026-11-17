from langchain_core.tools import tool
from typing import Annotated
from pydantic import Field
from dto.flight_search_tool_dto import FlightSearchToolInput
from services.flight_service import search_flights


@tool(args_schema=FlightSearchToolInput) #args schema tells langhain "Use the fields, descriptions, and validation rules defined in FlightSearchInput as the input schema for this tool."
def search_flight_tool(
    origin: str,
    destination: str,
    departure_date: str,
    adults: int = 1,
)->dict:
    """
    Search for available one-way flights using the Duffel Flight API.

    Use this tool when the user wants to search for flights
    between two airports on a specific departure date.

    Args:
        origin: Three-letter IATA airport code, e.g., BOM, DEL, PNQ.
        destination: Three-letter IATA airport code.
        departure_date: Departure date in YYYY-MM-DD format.
        adults: Number of adult passengers. Defaults to 1.

    Returns:
        A dictionary containing available flights, prices,
        airlines, timings, and other flight details.
    """
    
    return search_flights(
            origin=origin,
            destination=destination,
            departure_date=departure_date,
            adults=adults,
        )
    
        