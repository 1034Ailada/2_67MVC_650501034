from Model.database import insert_product, get_all_products, get_stats
import csv
import os

PRODUCTS_CSV = "Database/products.csv"
STATS_CSV = "Database/stats.csv"

class ProductModel:    
    def add_product(self, product_id, category, expiration_date, condition):
        #เพิ่มสินค้าโดยตรวจสอบค่าที่ส่งมาให้ไม่เป็น None
        if not product_id or not category or not condition:
            return "ข้อมูลสินค้าไม่ครบถ้วน"
        
        if category == "อาหาร" and not expiration_date:
            return "สินค้าประเภทอาหารต้องระบุวันที่หมดอายุ"

        return insert_product(product_id, category, expiration_date, condition)
    
    def get_products(self):
        #ดึงข้อมูลสินค้าทั้งหมด
        products = get_all_products()
        return products if products else []

    def get_statistics(self):
        #ดึงข้อมูลสถิติสินค้า
        stats = get_stats()
        return stats if stats else []
    
    def reload_data(self):
        self.stats = get_stats()  # โหลดข้อมูลจากไฟล์ CSV ใหม่