import os 

import httpx
from dotenv import load_dotenv
from utils.format_flight_api_response import format_flight_response_duffle

load_dotenv()

DUFFLE_API_TOKEN=os.getenv("DUFFEL_API_TOKEN")

DUFFLE_BASE_URL="https://api.duffel.com"

def search_flights(
    origin:str,
    destination:str,
    departure_date:str,
    adults:int=1
):
    if not DUFFLE_API_TOKEN:
        raise ValueError("DUFFLE API TOKEN IS MISSING")
    
    url=f"{DUFFLE_BASE_URL}/air/offer_requests"
    
    
    headers={
        "Authorization": f"Bearer {DUFFLE_API_TOKEN}",
        "Duffel-Version": "v2",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    
    payload={
        "data": {
            "slices": [
                {
                    "origin": origin,
                    "destination": destination,
                    "departure_date": departure_date,
                }
            ],
            "passengers": [
                {"type": "adult"} for _ in range(adults)
            ],
        }
    }
    
    # The with statement manages the client's lifecycle and ensures it is closed when the block finishes.
    with httpx.Client(timeout=30.0) as client:
        response=client.post(
            url,
            headers=headers,
            params={"return_offers": "true"}, #https://api.duffel.com/air/offer_requests?return_offers=true
            json=payload
        )
    
    response.raise_for_status() #This basically chks the http status.If Duffel returns an unsuccessful status such as 400, 401, or 500, httpx raises an HTTPStatusError.
    
    return format_flight_response_duffle(response.json())


if __name__ == "__main__":
    flights = search_flights(
        origin="BOM",
        destination="DEL",
        departure_date="2026-11-25",
        adults=1,
    )

    print(flights["flights"])
