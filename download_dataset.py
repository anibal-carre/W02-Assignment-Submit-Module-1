"""Download the public historical sales data to the local project folder.

The project bundles a verified 50-record example so core analysis can be
reproduced offline. Downloading the complete file requires internet access.
"""

from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen


DATASET_URL = (
    "https://huggingface.co/datasets/haoxianc/"
    "thedevastator_global-video-game-sales/resolve/main/vgsales.csv"
)
DESTINATION = Path(__file__).resolve().parent / "data" / "vgsales.csv"


def download_sales_data(destination: Path = DESTINATION) -> Path:
    """Fetch the dataset and validate its header before replacing local data."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = Request(DATASET_URL, headers={"User-Agent": "CSE310-DataAnalysis/1.0"})
    try:
        with urlopen(request, timeout=45) as response:
            file_bytes = response.read()
    except (OSError, URLError) as error:
        raise RuntimeError(
            "Unable to download the dataset. Download vgsales.csv manually "
            "from the URL in README.md and place it inside data/."
        ) from error

    header = file_bytes.splitlines()[0].decode("utf-8-sig", errors="replace")
    needed = ("Name", "Platform", "Genre", "NA_Sales", "EU_Sales", "Global_Sales")
    if not all(part in header.split(",") for part in needed):
        raise RuntimeError("The download does not contain the expected CSV columns.")

    destination.write_bytes(file_bytes)
    return destination


def main() -> None:
    """Download a full CSV and show the user its saved location."""
    try:
        saved = download_sales_data()
    except RuntimeError as error:
        print(f"Download failed: {error}")
        raise SystemExit(1) from error
    print(f"Downloaded {saved.name} ({saved.stat().st_size:,} bytes) to {saved}")


if __name__ == "__main__":
    main()
