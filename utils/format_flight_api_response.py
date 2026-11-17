def format_flight_response_duffle(api_response: dict) -> dict:

    offers = api_response.get("data", {}).get("offers", [])

    formatted_flights = []

    for offer in offers:

        # Basic flight information
        airline = offer["owner"]["name"]
        price = offer["total_amount"]
        currency = offer["total_currency"]

        # Journey information
        slices = offer["slices"]
        first_slice = slices[0]   #--> At this stage traveligo doesnt support round flights hence we are only taking the the first slice 

        segments = first_slice["segments"]

        first_segment = segments[0]
        last_segment = segments[-1]

        flight = {
            "offer_id": offer["id"],
            "airline": airline,
            "flight_number": (
                first_segment["marketing_carrier"]["iata_code"]
                + first_segment["marketing_carrier_flight_number"]
            ),
            "origin": first_slice["origin"]["iata_code"],
            "destination": first_slice["destination"]["iata_code"],
            "departure": first_segment["departing_at"],
            "arrival": last_segment["arriving_at"],
            "duration": first_slice["duration"],
            "stops": len(segments) - 1,
            "cabin_class": api_response["data"]["cabin_class"],
            "price": price,
            "currency": currency,
        }

        formatted_flights.append(flight)

    return {
        "total_results": len(formatted_flights),
        "flights": formatted_flights,
    }