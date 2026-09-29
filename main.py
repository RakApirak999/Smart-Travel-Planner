"""Entry point: wires the three layers together and starts the CLI."""

import sys

from app import config
from app.data.api_clients import CurrencyClient, PlacesClient, WeatherClient
from app.data.json_store import DEFAULT_FALLBACK_RATES, DEFAULT_REFERENCE_PRICES, load_json
from app.data.repository import TripRepository
from app.exceptions import AppError
from app.logic.budget_estimator import REQUIRED_PRICE_KEYS, BudgetEstimator
from app.logic.expense_service import ExpenseService
from app.logic.trip_service import TripService
from app.presentation.cli import TravelCLI


def build_cli() -> TravelCLI:
    """Create every object the app needs (simple manual dependency injection)."""
    config.load_env_file()
    warnings = []

    prices, warning = load_json(
        config.REFERENCE_PRICES_PATH, DEFAULT_REFERENCE_PRICES, REQUIRED_PRICE_KEYS
    )
    warnings.append(warning)
    fallback, warning = load_json(config.FALLBACK_RATES_PATH, DEFAULT_FALLBACK_RATES, ["rates"])
    warnings.append(warning)

    repository = TripRepository(config.DB_PATH)
    warnings.append(repository.pop_warning())

    api_key = config.get_opentripmap_key()
    if not api_key:
        warnings.append(
            "ยังไม่ได้ตั้งค่า OPENTRIPMAP_API_KEY ในไฟล์ .env: "
            "ค้นหาสถานที่เที่ยวไม่ได้ (ฟีเจอร์อื่นยังใช้ได้)"
        )

    trip_service = TripService(repository, PlacesClient(api_key), WeatherClient())
    expense_service = ExpenseService(
        repository, CurrencyClient(fallback.get("rates", {})), BudgetEstimator(prices)
    )
    return TravelCLI(trip_service, expense_service, warnings)


def main() -> None:
    """Start the program."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # show Thai correctly on Windows
    try:
        cli = build_cli()
    except AppError as error:
        print(f"เริ่มโปรแกรมไม่สำเร็จ: {error}")
        sys.exit(1)
    cli.run()


if __name__ == "__main__":
    main()
