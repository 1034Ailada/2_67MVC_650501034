import csv
import os
import re
from datetime import datetime

PRODUCTS_CSV = "Database/products.csv"
STATS_CSV = "Database/stats.csv"
HEADERS = ["product_id", "category", "expiration_date", "condition"]
STATS_HEADERS = ["category", "accepted", "rejected"]

def create_csv():
    #สร้างไฟล์ CSV ถ้ายังไม่มี
    if not os.path.exists(PRODUCTS_CSV):
        with open(PRODUCTS_CSV, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(HEADERS)

    if not os.path.exists(STATS_CSV):
        with open(STATS_CSV, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(STATS_HEADERS)
            writer.writerows([["อาหาร", 0, 0], ["อิเล็กทรอนิกส์", 0, 0], ["เสื้อผ้า", 0, 0]])

def insert_product(product_id, category, expiration_date, condition):
    #เพิ่มสินค้าใหม่ลง CSV ถ้าผ่านเงื่อนไข
    # ตรวจสอบว่า product_id เป็นตัวเลข 6 หลัก และตัวแรกไม่ใช่ 0
    if not re.match(r"^[1-9]\d{5}$", product_id):
        return "รหัสสินค้าต้องเป็นตัวเลข 6 หลัก และตัวแรกต้องไม่ใช่ 0"

    # ตรวจสอบว่ารหัสสินค้าไม่ซ้ำ
    with open(PRODUCTS_CSV, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["product_id"] == product_id:
                return "รหัสสินค้านี้มีอยู่แล้ว"

    # ตรวจสอบประเภทสินค้า
    today = datetime.today().strftime("%Y-%m-%d")
    if category == "อาหาร":
        if not expiration_date:
            return "สินค้าประเภทอาหารต้องระบุวันที่หมดอายุ"
        if expiration_date < today:
            update_stats(category, rejected=True)
            return "วันหมดอายุไม่ถูกต้อง"

    if category == "อิเล็กทรอนิกส์" and condition in ["เสียหาย", "ต้องตรวจสอบเพิ่มเติม"]:
        update_stats(category, rejected=True)
        return "สินค้าอิเล็กทรอนิกส์ต้องอยู่ในสภาพปกติ"

    if category == "เสื้อผ้า" and condition == "เสียหาย":
        update_stats(category, rejected=True)
        return "สินค้าเสื้อผ้าต้องไม่เสียหาย"

    # บันทึกข้อมูลลง CSV
    with open(PRODUCTS_CSV, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([product_id, category, expiration_date if expiration_date else "", condition])

    update_stats(category, accepted=True)
    return "เพิ่มสินค้าสำเร็จ"

def get_all_products():
    #ดึงข้อมูลสินค้าทั้งหมด
    products = []
    with open(PRODUCTS_CSV, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            products.append(row)
    return products

def update_stats(category, accepted=False, rejected=False):
    #อัปเดตสถิติสินค้า
    stats = []
    with open(STATS_CSV, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["category"] == category:
                if accepted:
                    row["accepted"] = str(int(row["accepted"]) + 1)
                if rejected:
                    row["rejected"] = str(int(row["rejected"]) + 1)
            stats.append(row)

    with open(STATS_CSV, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=STATS_HEADERS)
        writer.writeheader()
        writer.writerows(stats)

def get_stats():
    #ดึงข้อมูลสถิติสินค้า
    stats = []
    with open(STATS_CSV, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            stats.append(row)
    return stats