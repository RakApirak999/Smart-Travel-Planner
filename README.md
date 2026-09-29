# Smart Travel Planner

แอปพลิเคชัน Python แบบ Command Line สำหรับวางแผนการท่องเที่ยว ค้นหาสถานที่เที่ยว ดูพยากรณ์อากาศ ประมาณค่าใช้จ่าย และจดค่าใช้จ่ายจริงเทียบกับงบ

โครงการภาคปลาย รายวิชา CP352301 Script Programming ภาคการศึกษาที่ 1/2569
ดูรายละเอียดข้อเสนอโครงการได้ที่ [PITCH.md](PITCH.md)

> ค่าใช้จ่ายในแอปเป็นการประมาณการจากราคาอ้างอิงเท่านั้น ไม่มีการจองหรือชำระเงิน

## ฟีเจอร์

- สร้าง ดู แก้ไข ลบทริป พร้อมค้นหาและเรียงลำดับทริป
- ค้นหาสถานที่เที่ยวรอบปลายทางจาก OpenTripMap แล้วค้นหา กรอง เรียงลำดับ และบันทึกลงทริป
- จัดสถานที่ลงแผนเที่ยวรายวัน
- พยากรณ์อากาศช่วงวันเดินทางจาก Open-Meteo
- ประมาณค่าใช้จ่ายของทริปจากระยะทางและราคาอ้างอิง
- จดค่าใช้จ่ายจริงหลายสกุลเงิน แปลงเป็นบาทด้วย Frankfurter และสรุปเทียบกับงบ
- ทำงานต่อได้เมื่อไม่มีอินเทอร์เน็ต ไฟล์หาย หรือไฟล์เสีย

## โครงสร้างโปรเจกต์

```
smart-travel-planner/
├── main.py                      # จุดเริ่มโปรแกรม เชื่อมทุกเลเยอร์
├── app/
│   ├── config.py                # path ของไฟล์และการอ่าน .env
│   ├── exceptions.py            # Exception ของแอป
│   ├── presentation/            # Presentation Layer
│   │   ├── cli.py               # เมนูและหน้าจอทั้งหมด
│   │   ├── input_helpers.py     # รับข้อมูลพร้อมตรวจสอบ
│   │   └── formatting.py        # จัดตารางภาษาไทย
│   ├── logic/                   # Business Logic Layer
│   │   ├── models.py            # Trip, Place, Expense, DayPlan
│   │   ├── trip_service.py      # ทริปและสถานที่ ค้นหา/กรอง/เรียง
│   │   ├── expense_service.py   # ค่าใช้จ่ายและสรุปงบ
│   │   ├── budget_estimator.py  # ประมาณค่าใช้จ่าย
│   │   └── geo.py               # คำนวณระยะทาง
│   └── data/                    # Data Access Layer
│       ├── repository.py        # SQLite
│       ├── api_clients.py       # OpenTripMap, Open-Meteo, Frankfurter
│       └── json_store.py        # อ่านไฟล์ JSON
├── data/
│   ├── reference_prices.json    # ราคาอ้างอิงสำหรับประมาณค่าใช้จ่าย
│   └── fallback_rates.json      # อัตราแลกเปลี่ยนสำรอง
├── scripts/seed_demo.py         # เพิ่มทริปตัวอย่าง (ไม่ต้องใช้อินเทอร์เน็ต)
└── docs/                        # PLAN.md และ REPORT.md ของแต่ละ Sprint
```

## การติดตั้ง (Windows)

ต้องมี Python 3.10 ขึ้นไป เปิด Terminal ใน VS Code (Ctrl+`) ที่โฟลเดอร์โปรเจกต์ แล้วรัน

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

ถ้า PowerShell ไม่ยอมให้รัน `activate` ให้รัน `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` หนึ่งครั้งแล้วลองใหม่

## ตั้งค่า API key

1. สมัครบัญชีและรับ API key ฟรีที่ https://dev.opentripmap.com
2. คัดลอกไฟล์ `.env.example` แล้วเปลี่ยนชื่อเป็น `.env`
3. แก้บรรทัด `OPENTRIPMAP_API_KEY=` ให้เป็น key ของตัวเอง

ไฟล์ `.env` อยู่ใน `.gitignore` แล้ว ห้าม commit key ขึ้น GitHub
Open-Meteo และ Frankfurter ไม่ต้องใช้ key

## การใช้งาน

```
python main.py
```

เพิ่มข้อมูลตัวอย่าง (ทริปเชียงใหม่ 3 วัน พร้อมสถานที่และค่าใช้จ่าย) สำหรับ demo หรือทดสอบตอนไม่มีอินเทอร์เน็ต

```
python -m scripts.seed_demo
```

คำสั่งที่ใช้ได้ทุกที่: พิมพ์ `0` หรือ `back` เพื่อกลับ, `quit` หรือ `ออก` ที่เมนูหลักเพื่อออก, และ `cancel` หรือ `ยกเลิก` ระหว่างกรอกข้อมูลเพื่อยกเลิกรายการนั้น
วันที่กรอกได้ทั้ง `2026-10-15` และ `15/10/2569`

## ปรับราคาอ้างอิง

แก้ตัวเลขใน `data/reference_prices.json` ได้โดยไม่ต้องแก้โค้ด เช่น ค่าที่พักต่อห้องต่อคืน หรือค่าอาหารต่อคนต่อวัน แยก 3 ระดับ (budget / mid / luxury)

## เอกสาร Sprint

| Sprint | แผนงาน | รายงาน |
| --- | --- | --- |
| Sprint 1: Front-End | [PLAN.md](docs/sprint1/PLAN.md) | [REPORT.md](docs/sprint1/REPORT.md) |
| Sprint 2: Back-End | [PLAN.md](docs/sprint2/PLAN.md) | [REPORT.md](docs/sprint2/REPORT.md) |
| Sprint 3: Full-Stack | [PLAN.md](docs/sprint3/PLAN.md) | [REPORT.md](docs/sprint3/REPORT.md) |

## ทีมพัฒนา

| บทบาทหลัก | สมาชิก |
| --- | --- |
| Project Manager / CI-CD Integrator | ปวริศ สายโยค (โอ๊ค) |
| Automated Tester & QA | เอกปฐวี มีไชยา (ลีออง) |
| Core Developer | อภิรักษ์ สุริยะศรี (รักษ์) |
