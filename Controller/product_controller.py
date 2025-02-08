from Model.product_model import ProductModel

class ProductController:    
    def __init__(self, view):
        #กำหนด View และสร้าง instance ของ Model
        self.view = view
        self.model = ProductModel()
    
    def add_product(self, product_id, category, expiration_date, condition):
        #เพิ่มสินค้าใหม่เข้าไปในระบบ
        message = self.model.add_product(product_id, category, expiration_date, condition)
        if message:
            self.view.display_message(message)
        else:
            self.view.display_message("เกิดข้อผิดพลาดที่ไม่คาดคิด")
    
    def load_products(self):
        #โหลดข้อมูลสินค้าทั้งหมด
        products = self.model.get_products()
        self.view.display_products(products)
    
    def load_statistics(self, force_reload=False):
        #โหลดข้อมูลสถิติจาก Model และอัปเดต View
        if force_reload:
            self.model.reload_data()
        return self.model.get_statistics()

    
    def refresh_statistics(self):
        #โหลดข้อมูลสถิติใหม่จาก Model และอัปเดต View
        stats = self.model.get_statistics()
        self.view.display_statistics(stats)
        
    def force_reload_statistics(self):
        #โหลดข้อมูลสถิติใหม่จาก CSV และอัปเดต View, บังคับให้ Model โหลดข้อมูลใหม่จาก CSV ก่อนอัปเดต UI
        self.model.reload_data()
        stats = self.model.get_statistics()
        self.view.display_statistics(stats)