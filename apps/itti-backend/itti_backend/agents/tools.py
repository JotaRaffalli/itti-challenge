"""Simulated tools for the VuelaConNosotros chatbot."""

from langchain.tools import tool


@tool
def get_flight_status(flight_number: str) -> dict:
    """Simulates getting the status of a flight.

    Args:
        flight_number: The flight number to check.

    Returns:
        A dictionary with the flight status.
    """
    print(f"--- Tool: Getting status for flight {flight_number} ---")
    if "VW123" in flight_number:
        return {"status": "a tiempo", "departure": "10:00", "arrival": "12:00"}
    return {"status": "desconocido", "message": "No se encontró el vuelo."}


@tool
def get_flight_details(flight_number: str, passenger_name: str) -> dict:
    """Simulates getting the details of a flight reservation.

    Args:
        flight_number: The flight number.
        passenger_name: The name of the passenger.

    Returns:
        A dictionary with the flight details.
    """
    print(
        f"--- Tool: Getting details for flight {flight_number} for {passenger_name} ---"
    )
    if "VW123" in flight_number and "Juan Pérez" in passenger_name:
        return {
            "flight_number": "VW123",
            "origin": "BUE",
            "destination": "MAD",
            "date": "2025-08-15",
            "passenger": "Juan Pérez",
        }
    return {
        "status": "no_encontrado",
        "message": "No se encontraron detalles para este vuelo y pasajero.",
    }


@tool
def check_flight_availability(origin: str, destination: str, date: str) -> dict:
    """Simulates checking for available flights.

    Args:
        origin: The origin airport code.
        destination: The destination airport code.
        date: The desired date for the flight.

    Returns:
        A dictionary with flight availability.
    """
    print(
        f"--- Tool: Checking availability for {origin} to {destination} on {date} ---"
    )
    if origin == "BUE" and destination == "MIA" and date == "2025-09-20":
        return {
            "available": True,
            "flights": [
                {"flight_number": "VW789", "time": "22:00"},
                {"flight_number": "VW987", "time": "23:30"},
            ],
        }
    return {
        "available": False,
        "message": "No hay vuelos disponibles para la ruta y fecha seleccionadas.",
    }
