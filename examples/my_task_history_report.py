import os
import csv

from typing import Optional
from getpass import getpass

from ppa_api import client

# Uncomment below if not using a trusted certificate.
# import urllib3
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


FILE_PATH = "ppa_my_task_history.csv"


def _get_env_key(key: str, prompt: str, hidden: Optional[bool] = False) -> str:
    try:
        return os.environ[key]
    except KeyError:
        return getpass(prompt) if hidden else input(prompt)


def main() -> None:
    ppa = client.PPAClient(
        _get_env_key("PPA_ADDRESS", "Address: "),
        api_key=_get_env_key("PPA_API_KEY", "API Key: ", hidden=True),
        verify=True,  # Change to False if not using a trusted certificate.
    )
    with open(FILE_PATH, "w") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Name", "Started At", "Duration", "State"])
        list(
            map(
                lambda t: csv_writer.writerow([t.image, t.started_at, t.duration, t.state]),
                ppa.tasks_started_by_me(),
            )
        )
    print(f"Your task history spreadsheet was written to {FILE_PATH}.")


if __name__ == "__main__":
    main()
