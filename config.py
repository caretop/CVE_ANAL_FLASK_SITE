import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config:
    # "csv" (default) or "mongo". CSV is primary; if it's missing or empty,
    # analysis/kev_analysis.py automatically falls back to MongoDB.
    DATA_SOURCE = os.environ.get("DATA_SOURCE", "csv").strip().lower()

    CSV_PATH = os.environ.get(
        "KEV_CSV_PATH",
        os.path.join(BASE_DIR, "data", "known_exploited_vulnerabilities.csv"),
    )

    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB = os.environ.get("MONGO_DB", "kev_db")
    MONGO_COLLECTION = os.environ.get("MONGO_COLLECTION", "vulnerabilities")
