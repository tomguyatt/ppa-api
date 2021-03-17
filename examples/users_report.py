import os
import csv
import urllib3

from typing import Optional
from getpass import getpass

from ppa_api import client


# Uncomment below if not using a trusted certificate.
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


FILE_PATH = "ppa_users.csv"


def _get_env_key(key: str, prompt: str, hidden: Optional[bool] = False) -> str:
    try:
        return os.environ[key]
    except KeyError:
        return getpass(prompt) if hidden else input(prompt)


def main() -> None:
    ppa = client.PPAClient(
        _get_env_key("PPA_ADDRESS", "Address: "),
        api_key=_get_env_key("PPA_API_KEY", "API Key: ", hidden=True),
        verify_cert=True,  # Change to False if not using a trusted certificate.
    )
    with open(FILE_PATH, "w") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Name", "Email Address", "Last Logon"])
        list(map(lambda u: csv_writer.writerow([u.name, u.email, u.authenticated_at]), ppa.users()))
    print(f"Users spreadsheet was written to {FILE_PATH}.")


if __name__ == "__main__":
    main()
