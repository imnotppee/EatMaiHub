# EatMaiHub

**EatMaiHub** เป็นแอปพลิเคชันแนะนำร้านอาหารอัจฉริยะ ช่วยให้ผู้ใช้เลือกร้านอาหารหรือเมนูได้ง่ายขึ้นตามความชอบ สไตล์ หรือปัจจัยอื่น ๆ เช่น สีประจำวัน ราศี หรือร้านยอดนิยม โดยพัฒนาด้วย **FastAPI**, **Flet** และ **PostgreSQL**

---

## 🍜 ภาพรวมของโครงงาน

EatMaiHub ถูกออกแบบมาเพื่อช่วยให้นักศึกษาและบุคลากร KMITL สามารถค้นหาร้านอาหารที่เหมาะกับตนเองได้อย่างสะดวกและรวดเร็ว ผ่านระบบแนะนำเมนู รีวิวจากผู้ใช้จริง และฟีเจอร์แปลกใหม่ เช่น “สีประจำวัน” และ “อาหารตามราศี” ที่ช่วยให้การเลือกอาหารไม่น่าเบื่ออีกต่อไป

---

## 🌟 ฟีเจอร์หลัก

* 🔐 ระบบล็อกอิน / สมัครสมาชิก (รองรับ Google OAuth2)
* 🍱 ระบบแนะนำร้านอาหารแบบสุ่ม
* 🎨 หน้าสีประจำวันและราศี
* 🏠 หน้า Home แสดงร้านอาหารทั้งหมดพร้อมภาพประกอบ
* ❤️ ระบบ Favorite สำหรับเก็บร้านโปรด
* 💬 ระบบ Review พร้อมคะแนนและคอมเมนต์จากผู้ใช้จริง
* 🧾 หน้าสำหรับผู้ดูแลระบบ (Admin Dashboard)

---

## 🧩 เทคโนโลยีที่ใช้

| ส่วนระบบ           | เทคโนโลยี                  |
| ------------------ | -------------------------- |
| **Frontend**       | Flet (Python-based UI)     |
| **Backend**        | FastAPI                    |
| **Database**       | PostgreSQL                 |
| **Authentication** | OAuth2 (Google Login), JWT |
| **ORM**            | SQLAlchemy                 |
| **Environment**    | Python 3.11+               |

---

## ⚙️ ขั้นตอนติดตั้งและรันบนเครื่อง (Run Locally)

### 1. โคลนโปรเจกต์

```bash
git clone https://github.com/imnotppee/EatMaiHub.git
cd EatMaiHub
```

### 2. สร้าง Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### 3. ติดตั้ง Dependencies

```bash
pip install -r requirements.txt
```

### 4. ตั้งค่า Environment Variables

สร้างไฟล์ `.env` ภายในโฟลเดอร์ `backend/` และเพิ่มข้อมูลตัวอย่างดังนี้

```env
DATABASE_URL=postgresql://postgres:1234@localhost/EatMaiHub
SECRET_KEY=your_secret_key
GOOGLE_CLIENT_ID=your_google_client_id
REDIRECT_URI=http://127.0.0.1:8000/auth/google/callback
```

### 5. รัน Backend Server

```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 6. รัน Frontend (Flet)

```bash
cd frontend
python app.py
```

> 🔗 Backend จะรันบน `http://127.0.0.1:8000` และ Frontend จะเปิดเป็นหน้าต่างแอปโดยอัตโนมัติ

---

## 📁 โครงสร้างของโปรเจกต์

```
EatMaiHub/
├── backend/
│   ├── main.py              # จุดเริ่มต้นของ FastAPI
│   ├── models.py            # ORM (SQLAlchemy)
│   ├── database.py          # การเชื่อมต่อฐานข้อมูล
│   ├── component/           # โค้ดย่อย เช่น login, signup, review
│   └── static/images/       # รูปภาพร้านอาหาร
│
├── frontend/
│   ├── app.py               # จุดเริ่มต้นของ UI
│   ├── login.py, signup.py  # หน้า Login / Signup
│   ├── review_view.py       # หน้ารีวิว
│   └── data/                # ข้อมูลร้านและรีวิว (JSON)
│
├── admin_dashboard/         # หน้าสำหรับผู้ดูแลระบบ
└── Database/                # ไฟล์ SQL สำหรับสร้างตารางฐานข้อมูล
```

---

## 👥 สมาชิกทีมผู้พัฒนา

| ชื่อผู้ใช้ GitHub   | หน้าที่                            |
| ------------------- | ---------------------------------- |
| **Tanawatkub**      | Backend & API Integration          |
| **imnotppee**       | Frontend (Flet UI) & Documentation |
| **snowfake99**      | UI/UX Design & Review Module       |
| **023Kittikarn**    | Database Design                    |
| **Chutiporn120846** | Data Management & QA               |
| **natthapong073**   | Admin Dashboard                    |
| **Kotchanat**       | Database & Branch Integration      |

---

## 🏫 หมายเหตุ

โครงงานนี้จัดทำขึ้นเพื่อการศึกษาในรายวิชาของคณะครุศาสตร์อุตสาหกรรมและเทคโนโลยี มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าลาดกระบัง (KMITL)
โปรดใช้เพื่อการศึกษาเท่านั้น ห้ามนำไปใช้ในเชิงพาณิชย์โดยไม่ได้รับอนุญาต

copyright © 2024 EatMaiHub Team. All rights reserved.
