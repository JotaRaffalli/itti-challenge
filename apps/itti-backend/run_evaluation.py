import json
import time

import requests

# Configuration
BASE_URL = "http://localhost:8000"
EVALUATION_ENDPOINT = "/evaluation/run-full-dataset"
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds


def run_evaluation():
    """Connects to the API and runs the full semantic evaluation."""
    print("--- Iniciando Evaluación Semántica Completa ---")
    url = f"{BASE_URL}{EVALUATION_ENDPOINT}"

    for attempt in range(MAX_RETRIES):
        try:
            print(f"\nAttempt {attempt + 1} of {MAX_RETRIES}...")
            print(f"Sending POST request to {url}")

            # The request can take a while, so we set a generous timeout
            response = requests.post(url, timeout=300)  # 5 minutes timeout

            # Check if the request was successful
            response.raise_for_status()

            print("\n--- ✅ Evaluación Completada Exitosamente ---")

            # Parse and print the JSON response
            report = response.json()
            print(json.dumps(report, indent=2, ensure_ascii=False))

            # Print server logs if available in the response
            if "logs" in report:
                print("\n--- Server Logs ---")
                for log in report["logs"]:
                    print(log)

            # Exit the loop on success
            return

        except requests.exceptions.HTTPError as http_err:
            print("\n--- ❌ Error HTTP ---")
            print(f"Status Code: {http_err.response.status_code}")
            print(f"Response: {http_err.response.text}")
            break  # Don't retry on HTTP errors like 404 or 500

        except requests.exceptions.RequestException as req_err:
            print("\n--- ❌ Error de Conexión ---")
            print(f"Could not connect to {BASE_URL}. Is the server running?")
            print(f"Error: {req_err}")
            if attempt < MAX_RETRIES - 1:
                print(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                print("\n--- 🚫 Fallo la conexión después de varios intentos ---")
                print("Por favor, asegúrate de que el servidor FastAPI esté corriendo:")
                print("uvicorn itti_backend.main:app --reload")


if __name__ == "__main__":
    run_evaluation()
