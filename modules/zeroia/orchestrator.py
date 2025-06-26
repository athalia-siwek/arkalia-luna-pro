import time

from modules.zeroia.reason_loop import reason_loop


def orchestrate_zeroia_loop(max_loops: int | None = None) -> None:
    """Orchestrates the ZeroIA reason loop to run every interval_seconds."""
    count = 0
    while True:
        try:
            print(f"[DEBUG] Loop #{count}")
            decision, score = reason_loop()
            print(f"[DEBUG] Decision: {decision} / Score: {score}")
            if max_loops and count >= max_loops:
                print("[DEBUG] Max loop reached. Exiting.")
                break
            count += 1
        except Exception as e:
            print(f"[ERROR] An error occurred in the reason loop: {e}")
        time.sleep(1)


if __name__ == "__main__":
    orchestrate_zeroia_loop()
