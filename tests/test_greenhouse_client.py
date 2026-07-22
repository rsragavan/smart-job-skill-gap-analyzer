from app.clients.greenhouse_client import GreenhouseClient

client = GreenhouseClient()

try:
    data = client.fetch_jobs("YOUR_BOARD_TOKEN")

    print("Connected successfully!")

    print(f"Total Jobs: {len(data['jobs'])}")

except Exception as e:
    print(e)