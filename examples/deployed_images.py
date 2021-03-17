import os
import csv
import urllib3

from typing import Optional
from getpass import getpass

from ppa_api import client


# Uncomment below if not using a trusted certificate.
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


FILE_PATH = "ppa_deployed_images.csv"


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
        csv_writer.writerow(["Name", "Description", "Author", "Updated At"])
        list(
            map(
                lambda i: csv_writer.writerow([i.name, i.description, i.author, i.updated_at]),
                list(filter(lambda i: i.deployed, ppa.images())),
            )
        )
    print(f"Deployed images spreadsheet was written to {FILE_PATH}.")


if __name__ == "__main__":
    main()
