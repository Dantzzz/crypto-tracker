from apscheduler.schedulers.blocking import BlockingScheduler
from src.extract import load_config
from main import run_etl

def start_scheduler() -> None:
    config = load_config()
    interval_min = config["scheduler"]["interval_min"]

    scheduler = BlockingScheduler()
    scheduler.add_job(
        func=run_etl,        # what func
        args=[config],       # what arg(s)
        trigger='interval',  # what trigger
        minutes=interval_min
    )

    print(f"Scheduler started. Retrieving every {interval_min} minutes. \nPress Crtl+C to stop.")

    try:
        scheduler.start()
    except KeyboardInterrupt:
        print("Scheduler interrupted.")
        scheduler.shutdown()

if __name__ == "__main__":
    start_scheduler()