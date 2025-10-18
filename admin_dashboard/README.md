# 🧭 EatMaiHub Admin Dashboard

แดชบอร์ดสำหรับผู้ดูแลระบบของโครงการ **EatMaiHub**  
สร้างด้วย **Flet (Python UI Framework)** สำหรับจัดการข้อมูลผู้ใช้ ร้านอาหาร และฟีเจอร์หลักของระบบในรูปแบบ **Single Page Application (SPA)**

---

## 📁 โครงสร้างโปรเจกต์

EATMAIHUB/
├── admin_dashboard/
│ ├── assets/ # รูปภาพและไฟล์สื่อทั้งหมด
│ ├── components/ # ส่วนประกอบ UI เช่น sidebar, topbar
│ │ ├── sidebar.py
│ │ ├── topbar.py
│ │ └── card_stat.py
│ ├── data/ # ข้อมูล JSON ตัวอย่าง
│ │ ├── dashboard_data.json
│ │ └── user_data.json
│ ├── utils/ # Utility ต่างๆ (สี / การเชื่อม API)
│ │ ├── colors.py
│ │ └── api_client.py
│ ├── views/ # หน้าต่างๆ ของ Dashboard
│ │ ├── dashboard_view.py
│ │ ├── manage_user_view.py
│ │ ├── edit_features_view.py
│ │ └── admin_view.py
│ └── app.py # ไฟล์หลักของโปรแกรม

yaml
คัดลอกโค้ด



---

## ⚙️ การติดตั้งและตั้งค่าสภาพแวดล้อม (Environment Setup)

> 🔧 **หมายเหตุสำคัญ**  
> โปรเจกต์นี้ต้องใช้ **Flet เวอร์ชัน 0.70.0.dev6281** เท่านั้น  
> หากเคยติดตั้ง Flet เวอร์ชันอื่นไว้แล้ว (เช่น 0.28.x ที่ใช้ใน frontend)  
> กรุณาลบออกทั้งหมดก่อนเพื่อลดปัญหาเวอร์ชันชนกัน

---

### 🧩 ขั้นตอนการติดตั้งแบบครบถ้วน

#### 1️⃣ เปิด Terminal และเข้าโฟลเดอร์โปรเจกต์
```bash
cd EATMAIHUB/admin_dashboard



2️⃣ ลบ Flet เดิมออกให้หมดก่อน (สำคัญมาก!)
pip uninstall flet -y
pip uninstall flet-desktop -y
pip uninstall flet-web -y
pip uninstall flet-cli -y


⚠️ หากขึ้นข้อความว่า “not installed” ข้ามได้เลย
จุดประสงค์คือให้แน่ใจว่าไม่มี Flet เวอร์ชันอื่นค้างอยู่ในระบบ



3️⃣ สร้าง Virtual Environment แยกเฉพาะแดชบอร์ดนี้
เพื่อไม่ให้ชนกับโปรเจกต์หน้าเว็บ (Frontend) ที่ใช้ Flet 0.28.x
python3 -m venv venv



4️⃣ เปิดใช้งาน Virtual Environment
สำหรับ macOS / Linux
source venv/bin/activate


สำหรับ Windows
venv\Scripts\activate


5️⃣ ติดตั้ง Flet เวอร์ชันที่ถูกต้อง (0.70.0.dev6281)
pip install flet==0.70.0.dev6281

💡 ถ้า pip แจ้งว่า “No matching distribution found”
ให้ใช้คำสั่งนี้แทน:
pip install --pre 'flet[all]>=0.70.0.dev0'


6️⃣ ตรวจสอบเวอร์ชัน Flet ที่ติดตั้ง
pip show flet
ผลลัพธ์ควรเป็น:
Name: flet
Version: 0.70.0.dev6281


7️⃣ รันโปรแกรม
เมื่อทุกอย่างพร้อม ให้รันโปรเจกต์ได้เลย:
python app.py


✨ ฟีเจอร์หลักในระบบ
หน้า	รายละเอียด
Dashboard	แสดงสถิติ, กราฟร้านค้ายอดนิยม และการใช้งานรายเดือน
Manage User	ดู/แก้ไข/ลบ รายชื่อผู้ใช้ทั้งหมด
Edit Features	จัดการร้านอาหาร, หมวดหมู่ และฟีเจอร์
Admin	จัดการบัญชีผู้ดูแลระบบ
🎨 การปรับแต่งเพิ่มเติม
🎨 เปลี่ยนธีมสี

ไปที่ไฟล์
utils/colors.py
แล้วปรับค่าสีตามต้องการ

🧩 เพิ่มหน้าใหม่

สร้างไฟล์ใหม่ในโฟลเดอร์ views/

import หน้าใหม่ใน app.py

เพิ่มใน routing เพื่อให้ระบบเรียกใช้งานได้

🌐 เชื่อมต่อ API จริง

ไปที่ utils/api_client.py
แล้วเพิ่ม endpoint เพื่อเชื่อมต่อกับ Backend API จริง

🧰 เทคโนโลยีที่ใช้

Python 3.8+

Flet 0.70.0.dev6281 (Pre-release)

Single Page Application (SPA)

JSON Data Storage / API Ready

⚠️ หมายเหตุสำคัญ

ต้องใช้ Flet เวอร์ชัน 0.70.0.dev6281 เท่านั้น
หากใช้เวอร์ชัน 0.28.x (ของ frontend) จะไม่สามารถรันได้

แนะนำให้แยก environment ของ admin_dashboard ออกจาก frontend

รูปภาพทั้งหมดต้องเก็บไว้ในโฟลเดอร์ assets/

ไฟล์ JSON สำหรับข้อมูลตัวอย่างอยู่ใน data/

สามารถเปลี่ยนการเชื่อมต่อข้อมูลเป็น API จริงได้ในภายหลัง

🔁 การสลับกลับไปใช้ Flet 0.28.x (สำหรับหน้า Frontend)

หากต้องกลับไปพัฒนา หน้าเว็บ EatMaiHub (Frontend)
ให้รันคำสั่งดังนี้:

cd EATMAIHUB/frontend
pip uninstall flet -y
pip install flet==0.28.1


✅ ทำให้ระบบ frontend และ admin แยกเวอร์ชันกันอย่างชัดเจน
และไม่เกิด error จากเวอร์ชันที่ไม่ตรงกัน

👨‍💻 ผู้พัฒนา

EatMaiHub Team
King Mongkut’s Institute of Technology Ladkrabang (KMITL)
Faculty of Industrial Education and Technology

Developer:
Tanawat Putta (67030091)

🧾 License

โค้ดนี้พัฒนาเพื่อการศึกษาในรายวิชา
Software Design & Development – KMITL
ห้ามใช้ในเชิงพาณิชย์โดยไม่ได้รับอนุญาต


---

ต้องการไหมครับให้ผมส่งเป็นไฟล์ **`README.md` ดาวน์โหลดได้ทันที** (แทนที่จะ copy เอง)?  
ผมสามารถแนบไฟล์ให้โหลดโดยตรงได้เลยครับ ✅