import json
import requests
import boto3
import time
import threading

KINESIS_STREAM_NAME = "stock-market-stream"
REGION_NAME = "us-east-1"

kinesis_client = boto3.client("kinesis", region_name=REGION_NAME)

symbols = ["USD", "AAPL", "GOOGL"]

def send_to_kinesis(data: dict, partition_key: str):
    try:
        data_json = json.dumps(data)

        response = kinesis_client.put_record(
            StreamName=KINESIS_STREAM_NAME,
            Data=data_json,
            PartitionKey=partition_key
        )
        print(f"Sent to Kinesis: {data_json}")
        return response
    except Exception as e:
        print(f"Error sending to Kinesis: {e}")

def consume_stock_data(symbol: str):
    url = f"http://localhost/stocks/{symbol}"
    try:
        response = requests.get(url, stream=True)

        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode('utf-8'))
                send_to_kinesis(data, symbol)
                time.sleep(1) 
    except requests.exceptions.RequestException as e:
        print(f"Error consuming endpoint {symbol}: {e}")

def main():
    threads = []
    for symbol in symbols:
        thread = threading.Thread(target=consume_stock_data, args=(symbol,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
