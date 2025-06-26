import time

from modules.zeroia.reason_loop import reason_loop


def orchestrate_zeroia_loop(interval_seconds: int = 60):
    """Orchestrates the ZeroIA reason loop to run every interval_seconds."""
    while True:
        try:
            reason_loop()
        except Exception as e:
            print(f"[ERROR] An error occurred in the reason loop: {e}")
        time.sleep(interval_seconds)


if __name__ == "__main__":
    orchestrate_zeroia_loop()
