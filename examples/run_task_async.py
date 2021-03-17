import os
import sys
import time
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

    task = ppa.start_task_async(_get_task_name())
    print(
        f"The task has been started with UUID {task.uuid}, waiting up to 3 minutes for it to complete..."
    )
    for i in range(0, 60):
        if ppa.task_running(task.uuid):
            time.sleep(3)
            continue
        break
    else:
        raise Exception(f"Task {task.uuid} is still running after 3 minutes.")

    updated_task = ppa.task_by_uuid(task.uuid)

    print(f"Task state: {updated_task.state}")
    print(f"Exit code: {updated_task.exit_code}")
    print(f"Duration: {updated_task.duration}")


if __name__ == "__main__":
    main()
