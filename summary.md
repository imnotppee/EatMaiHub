# EatMaiHub — Problem(04/09/2025)

---

## 1) โครงสร้างการทำงาน (Overall Flow)

**Main branches**

* `main` — โค้ดเสถียร พร้อมเดโม/รีลีส
* `develop` — โค้ดรวมงานระหว่างสปรินต์

**Feature branches** (แตกจาก `develop`)

* ชื่อ: `feature/<feature-name>-<ชื่อ>` เช่น `feature/login-Piyawit`, `feature/random-Chutiporn`

**Fix branches** (แก้บั๊กด่วน)

* ชื่อ: `fix/<สั้นๆ-อธิบายปัญหา>` เช่น `fix/login-null-check`

**Flow (สรุป)**

```
Issue/Task -> feature/* -> Pull Request -> Code Review -> Merge to develop -> (พ้นสปรินต์) PR -> main
```

---

### ย้ายมาใช้ “รีโปเดียว”

1. ให้เจ้าของรีโป `imnotppee/EatMaiHub` เพิ่มทุกคนเป็น **Collaborator**
2. ทุกคน `git clone` รีโปเดียวกันนี้ ไม่ต้อง fork
3. แต่ละคนสร้าง branch ของตัวเองตามกติกา แล้วเปิด PR ในรีโปเดียวกันทันทีที่พร้อม review

```bash
# ตั้ง remote ของต้นน้ำ (upstream = repo หลัก)
git remote add upstream https://github.com/imnotppee/EatMaiHub.git

# ดึงอัปเดตจาก upstream ทุก branch
git fetch upstream

# สร้าง local branch ติดตาม branch ของคนอื่น (ตัวอย่าง: develop)
git checkout -b develop upstream/develop

# สลับไป branch ของเพื่อนที่อยากดูหรือต่อยอด (ตัวอย่าง)
git checkout -b feature/random-Chutiporn upstream/feature/random-Chutiporn
```

อัปเดตเรื่อยๆ:

```bash
git fetch upstream
# รีเบสงานเราให้ตาม upstream/develop ล่าสุด
git checkout develop && git rebase upstream/develop
```

ส่งงานขึ้น **fork** ของตัวเอง และเปิด PR **กลับไปที่ repo หลัก**:

```bash
# ทำงานใน branch ของเราแล้ว commit
git push origin feature/login-Piyawit
# เปิด PR จาก fork:feature/login-Piyawit -> upstream:develop
```

---

## 3) กติกาการตั้งชื่อ Branch / Commit / PR

**Branch**

* `feature/<feature-name>-<ชื่อ>` เช่น `feature/signup-Piyawit`
* `fix/<short-bug>` เช่น `fix/api-timeout`

**Commit message** (ใช้ Conventional Commits เพื่อให้ log อ่านง่าย)

* `feat: add login form and validation`
* `fix: handle empty password on login`
* `docs: update README with setup steps`
* `refactor: extract auth service`

**Pull Request (PR) title**

* `[feat] Login: UI + basic validation (Piyawit)`

**PR Checklist (แนบในคำอธิบาย PR)**

* [ ] Build ผ่านในเครื่อง
* [ ] เพิ่ม/อัปเดต Unit tests (ถ้ามี)
* [ ] ผ่าน lint/format (black, ruff/flake8)
* [ ] ไม่มี credential/hardcode secret
* [ ] อธิบายผลกระทบ/ไฟล์หลักที่แก้

> แนะนำเพิ่มไฟล์ `.github/pull_request_template.md` เพื่อบังคับใช้เช็กลิสต์

ตัวอย่าง `pull_request_template.md`:

```md
## What changed?
-

## How to test
-

## Checklist
- [ ] Build ผ่าน
- [ ] Test ผ่าน/อัปเดตแล้ว
- [ ] Lint/Format ผ่าน
- [ ] ไม่มี secret
```

---

## 4) กติกา Review & Merge คุณภาพ

**วิธีรีวิว**

* อย่างน้อย 1 reviewer (ถ้ามีเวลา 2 คนยิ่งดี)
* ตรวจ: logic, tests, error handling, naming, UX, และผลกระทบข้ามโมดูล

**กฎ Merge (Repository Settings → Branch protection)**

* Protect `main`, `develop`
* Require PR review ≥ 1
* Require status checks (CI) to pass (ถ้ายังไม่มี CI ให้เพิ่มภายหลัง)
* Disallow direct push to `main`, `develop`

**แนวทางแก้คอนฟลิกต์**

* ให้คนเปิด PR รีเบสก่อนไปต่อ: `git fetch origin && git rebase origin/develop`
* แก้คอนฟลิกต์ในเครื่อง → รันทดสอบ → `git push --force-with-lease`

---

## 5) เวิร์กโฟลว์รายวัน (ตัวอย่างที่ทำตามได้เลย)

1. เลือกงานจาก Issues/Project Board → สร้าง branch จาก `develop`

```bash
git checkout develop
git pull origin develop

# ตัวอย่าง
git checkout -b feature/login-Piyawit
```

2. ทำงาน/commit เป็นช่วงสั้นๆ พร้อมคอมเมนต์ที่มีความหมาย

```bash
git add .
git commit -m "feat: login page with validation and API hook"
```

3. ดันขึ้นรีโมตและเปิด PR

```bash
git push -u origin feature/login-Piyawit
```

4. ขอรีวิว → แก้ไขตามคอมเมนต์ → รีวิวยืนยัน → Merge → ลบ branch

5. **ทุกครั้งที่ทำงาน** ซิงค์ `develop` ของเราให้ทันก่อนเริ่มงานใหม่

```bash
git checkout develop
git pull origin develop
```

---

## 6) ตัวอย่าง Project Board (GitHub Projects)

* Columns: **Backlog → In Progress → In Review → Done**
* ทุกงานเปิดเป็น **Issue**: ใส่ acceptance criteria, assignee, labels (`frontend`, `backend`, `database`, `bug`, `enhancement`)
* PR ที่ลิงก์กับ Issue จะปิดอัตโนมัติเมื่อ merge (ใช้คำ `Closes #<issue-number>` ในคำอธิบาย PR)

---

---

**.gitignore (สั้นๆ สำหรับ Python/Flet/venv)**

```
# Python
__pycache__/
*.py[cod]
*.pyc

# Venv
.venv/
venv/
ENV/

# OS / IDE
.DS_Store
.idea/
.vscode/

# Build/Cache
build/
dist/
*.log
```

## 7) สปีดรันคำสั่งที่ใช้บ่อย (Cheatsheet)

```bash
# อัปเดต develop ในเครื่องให้ทัน
git checkout develop && git pull origin develop

# สร้างฟีเจอร์ใหม่
git checkout -b feature/<name>-<yourname>

# ทำงาน/คอมมิต
git add . && git commit -m "feat: ..."

# ดันขึ้นรีโมต
git push -u origin feature/<name>-<yourname>

# หลังรีวิวเสร็จและ merge แล้ว
git checkout develop && git pull && git branch -d feature/<name>-<yourname>
```

---

### สรุปสั้น

* ใช้ **รีโปเดียว** + Collaborator → ทุกคนเห็น branch ง่ายสุด
* ตั้งชื่อ branch/commit/PR ให้สื่อความหมาย (Conventional Commits)
* PR ต้องมีรีวิว + เปิด Branch Protection
* ช่วงนี้ “ล็อก UI” Flet ด้วย artboard 430×932 ก่อน เพื่อความเร็วและควบคุมคุณภาพ
