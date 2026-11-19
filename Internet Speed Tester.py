
import speedtest
import socket
import csv
import os
from datetime import datetime


def check_connection():
    """Check whether the internet is available."""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except OSError:
        return False


def format_speed(speed):
    """Convert bits per second to Mbps."""
    return round(speed / 1_000_000, 2)


def connection_rating(download):
    """Rate internet performance."""
    if download >= 100:
        return "Excellent - Ultra Fast"
    elif download >= 50:
        return "Very Good - Fast"
    elif download >= 25:
        return "Good - Stable"
    elif download >= 10:
        return "Average - Moderate"
    else:
        return "Slow - Poor Connection"


def save_result(download, upload, ping, ip):
    """Save results to a CSV file."""
    filename = "speed_test_history.csv"

    file_exists = os.path.exists(filename)

    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Date",
                "Download (Mbps)",
                "Upload (Mbps)",
                "Ping (ms)",
                "Public IP"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            download,
            upload,
            ping,
            ip
        ])

    print("\nResult saved successfully!")


def run_speed_test():
    print("\nChecking internet connection...")

    if not check_connection():
        print("No internet connection detected!")
        return

    print("Internet connection is active!")
    print("\nInitializing speed test...")

    try:
        tester = speedtest.Speedtest()

        print("Finding the best server...")
        tester.get_best_server()

        print("Testing download speed...")
        download = format_speed(tester.download())

        print("Testing upload speed...")
        upload = format_speed(tester.upload())

        ping = round(tester.results.ping, 2)

        result = tester.results.dict()
        ip = result.get("client", {}).get("ip", "Unknown")

        print("\n" + "=" * 45)
        print("          INTERNET SPEED REPORT")
        print("=" * 45)

        print(f"Download Speed : {download} Mbps")
        print(f"Upload Speed   : {upload} Mbps")
        print(f"Ping           : {ping} ms")
        print(f"Public IP      : {ip}")

        print(f"\nConnection Rating: {connection_rating(download)}")

        print("=" * 45)

        choice = input("\nSave result? (y/n): ").lower()

        if choice == "y":
            save_result(download, upload, ping, ip)

    except Exception as error:
        print(f"\nSpeed test failed: {error}")


def main():
    while True:
        print("\n" + "=" * 45)
        print("          INTERNET SPEED TESTER")
        print("=" * 45)

        print("1. Run Internet Speed Test")
        print("2. Check Internet Connection")
        print("3. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            run_speed_test()

        elif choice == "2":
            if check_connection():
                print("\nInternet is connected!")
            else:
                print("\nInternet is disconnected!")

        elif choice == "3":
            print("\nThank you for using Internet Speed Tester!")
            break

        else:
            print("\nInvalid choice! Try again.")


if __name__ == "__main__":
    main()
