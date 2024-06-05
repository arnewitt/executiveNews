
import os

from utils.utils import check_time_and_run, run_summarization

DEBUG = True

if __name__ == "__main__":
    if DEBUG == True:
        run_summarization(
            base_url=os.environ.get("BASE_URL", ""),
            api_key=os.environ.get("API_KEY", "")
        )

    else:
        # Define the specific time to run (24-hour format)
        target_hour = os.environ.get("TARGET_HOUR", "7")
        target_minute = os.environ.get("TARGET_MINUTE", "30")

        check_time_and_run(target_hour, target_minute)