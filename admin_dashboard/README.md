"""
# EatMaiHub Admin Dashboard

## โครงสร้างไฟล์

```
EATMAIHUB/
├── admin_dashboard/
│   ├── assets/              # รูปภาพและไฟล์ media
│   ├── components/          # Component ต่างๆ
│   │   ├── sidebar.py       # Sidebar navigation
│   │   ├── topbar.py        # Top bar with search
│   │   └── card_stat.py     # Statistics cards
│   ├── data/               # ข้อมูล JSON
│   │   ├── dashboard_data.json
│   │   └── user_data.json
│   ├── utils/              # Utilities
│   │   ├── colors.py       # Color theme
│   │   └── api_client.py   # API client
│   ├── views/              # หน้าต่างๆ
│   │   ├── dashboard_view.py
│   │   ├── manage_user_view.py
│   │   ├── edit_features_view.py
│   │   └── admin_view.py
│   └── app.py              # ไฟล์หลัก
```

## วิธีติดตั้ง

```bash
pip install flet
```

## วิธีรัน

```bash
cd admin_dashboard
python app.py
```

## ฟีเจอร์

1. **Dashboard** - แสดงสถิติและกราฟ
   - กราฟแท่งร้านค้ายอดนิยม
   - กราฟเส้นการใช้งานรายเดือน
   - สถิติผู้ใช้และร้านอาหาร

2. **Manage User** - จัดการผู้ใช้
   - แสดงรายชื่อผู้ใช้
   - จำนวนผู้ใช้ทั้งหมดและใหม่

3. **Edit Features** - จัดการร้านอาหาร
   - แสดงรายการร้านอาหาร
   - เพิ่ม/แก้ไข/ลบร้านอาหาร
   - จัดการหมวดหมู่

4. **Admin** - จัดการแอดมิน
   - แสดงรายชื่อแอดมิน
   - จัดการบัญชีแอดมิน

## การปรับแต่ง

### เปลี่ยนสีธีม
แก้ไขไฟล์ `utils/colors.py`

### เพิ่มหน้าใหม่
1. สร้างไฟล์ใหม่ใน `views/`
2. Import และเพิ่มใน `app.py`

### เชื่อมต่อ API
แก้ไขไฟล์ `utils/api_client.py`

## เทคโนโลยีที่ใช้

- **Flet** - Framework สำหรับสร้าง UI
- **Python 3.8+**

## หมายเหตุ

- ข้อมูลตัวอย่างอยู่ในโค้ดโดยตรง สามารถแก้ไขให้ดึงจาก JSON หรือ API ได้
- รูปภาพต้องเตรียมไว้ใน folder `assets/`
- การ navigate ระหว่างหน้าทำงานแบบ Single Page Application (SPA)
"""