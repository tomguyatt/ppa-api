import os
import sys
import urllib3

from typing import Optional
from getpass import getpass

from ppa_api import client


# Uncomment below if not using a trusted certificate.
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def _get_env_key(key: str, prompt: str, hidden: Optional[bool] = False) -> str:
    try:
        return os.environ[key]
    except KeyError:
        return getpass(prompt) if hidden else input(prompt)


def _get_task_name() -> str:
    try:
        return sys.argv[1]
    except IndexError:
        return input("Task Name: ")


def main() -> None:
    ppa = client.PPAClient(
        _get_env_key("PPA_ADDRESS", "Address: "),
        api_key=_get_env_key("PPA_API_KEY", "API Key: ", hidden=True),
        verify_cert=True,  # Change to False if not using a trusted certificate.
    )

    task_name = _get_task_name()

    # Ensure the task exists before printing the "starting task" message.
    ppa.image_by_name(task_name)

    print("Waiting up to 3 minutes for the started task to complete...")
    task = ppa.start_task(task_name, timeout=180)

    print(f"Task state: {task.state}")
    print(f"Exit code: {task.exit_code}")
    print(f"Duration: {task.duration}")


if __name__ == "__main__":
    main()
