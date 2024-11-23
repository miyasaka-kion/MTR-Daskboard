from pymongo import MongoClient
from station import Station, DataManager


def test_db_connection():
    try:
        # Initialize DataManager
        data_manager = DataManager()

        # Check connection
        # if not data_manager.is_connected():
        #     print("Failed to connect to the database.")
        #     return

        print("Successfully connected to the database.")

        # Create a test station
        test_station = Station()
        test_station.station_code = "TEST123"
        test_station.station_line = "Test Line"
        test_station.sys_time = "2023-01-01 00:00:00"
        test_station.up_time = "2023-01-01 00:10:00"
        test_station.down_time = "2023-01-01 00:20:00"
        test_station.is_delay = False

        # Store the test station
        data_manager.store_station(test_station)
        print("Stored test station.")

        # Retrieve the test station
        fetched_station = data_manager.fetch_station("TEST123")
        if fetched_station:
            print("Retrieved test station:")
            print(fetched_station)
        else:
            print("Failed to retrieve test station.")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    test_db_connection()