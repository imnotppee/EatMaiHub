# 🍜 EatMaiHub Frontend

ส่วนหน้าแอปพลิเคชันหลักของโครงการ **EatMaiHub**  
พัฒนาโดยใช้ **Flet (Python UI Framework)** เวอร์ชัน **0.28.3**  
ออกแบบให้ใช้งานง่าย รองรับทั้ง Desktop และ Mobile UI

---

## 📁 โครงสร้างโปรเจกต์

EATMAIHUB/
├── frontend/
│ ├── assets/ # รูปภาพและไฟล์ media
│ ├── components/ # ส่วนประกอบ UI เช่น ปุ่ม, การ์ด, Navigation bar
│ ├── data/ # ข้อมูล JSON เช่น เมนูอาหาร, สีวัน, ดวง
│ ├── pages/ # หน้าหลักของแอป เช่น Home, Random Food, Horoscope
│ ├── utils/ # Utility / Color / Helper function
│ ├── app.py # ไฟล์หลักในการรันแอป
│ └── requirements.txt # รายการ dependencies (ถ้ามี)

yaml
คัดลอกโค้ด

---

## ⚙️ การตั้งค่าสภาพแวดล้อม (Environment Setup)

> 🧩 โปรเจกต์นี้ใช้ **Flet เวอร์ชัน 0.28.3** เท่านั้น  
> เพื่อป้องกันปัญหา error หรือเวอร์ชันชนกับ `admin_dashboard`  
> ให้ลบ Flet เดิมทั้งหมดออกก่อนติดตั้งใหม่ทุกครั้ง

---

### 1️⃣ เปิด Terminal และเข้าโฟลเดอร์โปรเจกต์

```bash
cd EATMAIHUB/frontend
2️⃣ ลบ Flet เดิมออกทั้งหมด
bash
คัดลอกโค้ด
pip uninstall flet -y
pip uninstall flet-desktop -y
pip uninstall flet-web -y
pip uninstall flet-cli -y
⚠️ หากขึ้นข้อความ “not installed” ข้ามได้เลย
จุดประสงค์คือให้แน่ใจว่าไม่มี Flet เวอร์ชันอื่นเหลืออยู่

3️⃣ สร้าง Virtual Environment แยกเฉพาะหน้า Frontend
เพื่อแยกจาก admin_dashboard ที่ใช้ Flet 0.70.0.dev6281

bash
คัดลอกโค้ด
python3 -m venv venv
4️⃣ เปิดใช้งาน Virtual Environment
macOS / Linux

bash
คัดลอกโค้ด
source venv/bin/activate
Windows

bash
คัดลอกโค้ด
venv\Scripts\activate
5️⃣ ติดตั้ง Flet เวอร์ชันที่ถูกต้อง (0.28.3)
bash
คัดลอกโค้ด
pip install flet==0.28.3
6️⃣ ตรวจสอบเวอร์ชัน Flet ที่ติดตั้ง
bash
คัดลอกโค้ด
pip show flet
ควรได้ผลลัพธ์ดังนี้:

makefile
คัดลอกโค้ด
Name: flet
Version: 0.28.3
7️⃣ รันโปรแกรม
เมื่ออยู่ในโฟลเดอร์ frontend และเปิด venv แล้ว ให้รันคำสั่งนี้:


ถ้ายังไม่ได้ติดตั้ง library requests
ซึ่งใช้สำหรับ “เรียก API หรือดึงข้อมูลจากเว็บ”
วิธีแก้ (ง่ายมาก)
ใน Terminal (ที่อยู่ในโฟลเดอร์ frontend และอยู่ใน venv แล้ว)
รันคำสั่งนี้ได้เลย:

pip install requests

bash
คัดลอกโค้ด
python app.py
🌐 ระบบจะเปิดแอป EatMaiHub ในเบราว์เซอร์อัตโนมัติ

✨ ฟีเจอร์หลักในหน้า Frontend
ฟีเจอร์	รายละเอียด
Home	หน้าหลัก รวมเมนูแนะนำและเมนูยอดนิยม
Random Food	สุ่มอาหารอัตโนมัติ
Eat by Color of the Day	แนะนำอาหารตามสีประจำวัน
Eat by Horoscope	แนะนำอาหารตามราศี
Review & Rating	ให้คะแนนและรีวิวร้านอาหาร
Nearby Shops	แสดงร้านอาหารใกล้ตัว

🎨 การปรับแต่ง
เปลี่ยนธีมสี
ไปที่ไฟล์
utils/colors.py
และแก้ไขค่าธีมที่ต้องการ

เพิ่มหน้าใหม่
สร้างไฟล์ใหม่ใน pages/

import หน้าใหม่ใน app.py

เพิ่ม routing ให้รองรับหน้าใหม่

🧰 เทคโนโลยีที่ใช้
Python 3.8+

Flet 0.28.3 (Stable)

JSON Data / SPA Concept

⚠️ หมายเหตุสำคัญ
โปรเจกต์ Frontend ต้องใช้ Flet เวอร์ชัน 0.28.3 เท่านั้น
หากใช้ Flet เวอร์ชัน 0.70.x (ของ admin dashboard) จะเกิด error

ควรแยก virtual environment ระหว่าง frontend และ admin_dashboard อย่างเด็ดขาด

รูปภาพทั้งหมดต้องเก็บไว้ในโฟลเดอร์ assets/

หากมีข้อมูล JSON เช่น เมนูหรือสีวัน ให้วางไว้ในโฟลเดอร์ data/

🔁 การสลับกลับไปใช้ Flet 0.70 (สำหรับ Admin Dashboard)
หากต้องกลับไปพัฒนา หน้าแดชบอร์ดแอดมิน
ให้รันคำสั่งดังนี้:

bash
คัดลอกโค้ด
cd EATMAIHUB/admin_dashboard
pip uninstall flet -y
pip install flet==0.70.0.dev6281
✅ เพื่อให้เวอร์ชันตรงกับแดชบอร์ดแอดมิน และป้องกันความขัดแย้งของ Flet

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

yaml
คัดลอกโค้ด

---

✅ ใช้งานได้ทันที — เพียงนำทั้งหมดนี้ไปวางใน  
`EATMAIHUB/frontend/README.md`

ต้องการให้ผมส่งเป็นไฟล์ `.md` พร้อมดาวน์โหลดได้เลยไหมครับ (จะสร้างไฟล์ให้คุณใช้ตรง ๆ ได้ทันที)?