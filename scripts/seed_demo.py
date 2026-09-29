"""Add a sample trip with places and expenses, without calling any API.

Useful for demos and for testing when there is no internet.
Run from the project folder:  python -m scripts.seed_demo
"""

from datetime import date, timedelta

from app import config
from app.data.repository import TripRepository
from app.logic.models import Expense, Place, Trip


def seed() -> None:
    """Insert one demo trip into the database."""
    repository = TripRepository(config.DB_PATH)
    start = date.today() + timedelta(days=7)
    trip = repository.add_trip(Trip(
        name="เชียงใหม่ 3 วัน 2 คืน (ตัวอย่าง)",
        destination="Chiang Mai",
        country="TH",
        lat=18.7883,
        lon=98.9853,
        origin="Khon Kaen",
        distance_km=440.0,
        travel_mode="bus",
        stay_level="mid",
        start_date=start,
        end_date=start + timedelta(days=2),
        travelers=3,
        budget_thb=15000,
    ))

    places = [
        Place("Wat Phra Singh", "religion", 18.7886, 98.9819, 3, 0.4, day_number=1),
        Place("Wat Chedi Luang", "religion", 18.7870, 98.9866, 3, 0.2, day_number=1),
        Place("Three Kings Monument", "historic", 18.7902, 98.9875, 2, 0.3, day_number=1),
        Place("Chiang Mai City Arts and Cultural Centre", "museum", 18.7904, 98.9873, 2, 0.3),
        Place("Doi Suthep", "nature", 18.8048, 98.9216, 3, 7.0, day_number=2),
        Place("Warorot Market", "shopping", 18.7907, 99.0010, 2, 1.6, day_number=3),
    ]
    for place in places:
        repository.add_place(trip.id, place)

    expenses = [
        Expense("transport", 1650, "THB", start, 1650, "ตั๋วรถทัวร์ขาไป 3 คน"),
        Expense("accommodation", 2400, "THB", start, 2400, "โรงแรมคืนแรก"),
        Expense("food", 780, "THB", start, 780, "ข้าวซอยมื้อเย็น"),
        Expense("attraction", 90, "THB", start + timedelta(days=1), 90, "ค่าเข้าดอยสุเทพ"),
    ]
    for expense in expenses:
        repository.add_expense(trip.id, expense)

    print(f"เพิ่มทริปตัวอย่างแล้ว (รหัส {trip.id}) ที่ {config.DB_PATH}")


if __name__ == "__main__":
    seed()
