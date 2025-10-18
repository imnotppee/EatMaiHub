import flet as ft
from flet import Icons, Colors
import requests

# ---------- ค่าคงที่ ----------
BRAND_ORANGE = "#DC7A00"
BRAND_BROWN  = "#4D2E1E"
PHONE_W, PHONE_H = 412, 917
API_BASE = "http://localhost:8000"

# ---------- UI ส่วนหัว ----------
def curved_orange_header():
    ORANGE_H    = 150
    ELLIPSE_W   = 413
    ELLIPSE_H   = 103
    ELLIPSE_TOP = 110
    ELLIPSE_LEFT = -1
    return ft.Stack(
        width=PHONE_W,
        height=ORANGE_H + 60,
        controls=[
            ft.Container(width=PHONE_W, height=ORANGE_H, bgcolor=BRAND_ORANGE),
            ft.Container(width=ELLIPSE_W, height=ELLIPSE_H,
                         bgcolor=Colors.WHITE, border_radius=ELLIPSE_H // 2,
                         top=ELLIPSE_TOP, left=ELLIPSE_LEFT),
        ],
    )

# ---------- เฟรมมือถือ ----------
def phone_frame(*children: ft.Control):
    return ft.Container(
        width=PHONE_W, height=PHONE_H, bgcolor=Colors.WHITE,
        content=ft.Column(controls=list(children), spacing=0),
    )

# ---------- หน้า Signup ----------
def build_signup_view(page: ft.Page) -> ft.View:
    username = ft.TextField(label="Username", width=340, border_color=BRAND_ORANGE)
    password = ft.TextField(label="Password", width=340, password=True, can_reveal_password=True, border_color=BRAND_ORANGE)
    email    = ft.TextField(label="Email",    width=340, border_color=BRAND_ORANGE)

    # ✅ ฟังก์ชันสมัคร (เชื่อม backend)
    def on_create(e):
        data = {
            "username": username.value,
            "email": email.value,
            "password": password.value
        }
        try:
            res = requests.post(f"{API_BASE}/auth/signup", json=data)
            if res.status_code == 200:
                page.snack_bar = ft.SnackBar(ft.Text("✅ Account created successfully!"))
                page.snack_bar.open = True
                page.go("/login")  # ไปหน้าล็อกอิน
            else:
                msg = res.json().get("detail", "Signup failed.")
                page.snack_bar = ft.SnackBar(ft.Text(f"❌ {msg}"))
                page.snack_bar.open = True
        except Exception as err:
            page.snack_bar = ft.SnackBar(ft.Text(f"⚠️ Connection error: {err}"))
            page.snack_bar.open = True
        page.update()

    # ---------- โลโก้ ----------
    logo = ft.Image(src="logo.png", width=120, height=120, fit=ft.ImageFit.CONTAIN)

    # ---------- ส่วนเนื้อหา ----------
    content = phone_frame(
        curved_orange_header(),
        ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                logo,
                ft.Container(height=16),
                username, ft.Container(height=12),
                password, ft.Container(height=12),
                email,    ft.Container(height=18),
                ft.ElevatedButton(
                    "Create account", on_click=on_create,
                    bgcolor=BRAND_ORANGE, color=Colors.WHITE, width=240,
                    style=ft.ButtonStyle(shape={"": ft.RoundedRectangleBorder(radius=28)}),
                ),
                ft.TextButton(
                    "Already have an account? Log in",
                    on_click=lambda e: page.go("/login"),
                ),
            ],
        ),
    )

    # ---------- กรอบมือถือ ----------
    return ft.View(
        route="/signup",
        padding=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Container(
                expand=True,
                bgcolor=ft.Colors.BLACK,  # พื้นหลังนอกกรอบ = ดำ
                alignment=ft.alignment.center,
                content=ft.Container(
                    width=PHONE_W,
                    height=PHONE_H,
                    bgcolor=ft.Colors.WHITE,  # กรอบมือถือ = ขาว
                    content=content,
                ),
            ),
        ],
    )
