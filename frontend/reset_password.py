import flet as ft
import requests
from flet import Colors

BRAND_ORANGE = "#DC7A00"
BRAND_BROWN = "#4D2E1E"
PHONE_W, PHONE_H = 412, 917
API_BASE = "http://localhost:8000"  # ✅ backend URL

def curved_orange_header():
    ORANGE_H, ELLIPSE_W, ELLIPSE_H = 150, 413, 103
    return ft.Stack(
        width=PHONE_W,
        height=ORANGE_H + 60,
        controls=[
            ft.Container(width=PHONE_W, height=ORANGE_H, bgcolor=BRAND_ORANGE),
            ft.Container(
                width=ELLIPSE_W,
                height=ELLIPSE_H,
                bgcolor=Colors.WHITE,
                border_radius=ELLIPSE_H // 2,
                top=110,
                left=-1,
            ),
        ],
    )

def phone_frame(*children: ft.Control):
    return ft.Container(
        width=PHONE_W,
        height=PHONE_H,
        bgcolor=Colors.WHITE,
        content=ft.Column(controls=list(children), spacing=0),
    )

def build_reset_view(page: ft.Page) -> ft.View:
    email = ft.TextField(label="Email", width=340, border_color=BRAND_ORANGE)
    otp = ft.TextField(label="OTP", width=340, border_color=BRAND_ORANGE, visible=False)

    send_btn = ft.ElevatedButton(
        "Send OTP",
        bgcolor=BRAND_ORANGE,
        color=Colors.WHITE,
        width=200,
        style=ft.ButtonStyle(shape={"": ft.RoundedRectangleBorder(radius=28)}),
    )

    confirm_btn = ft.ElevatedButton(
        "Confirm OTP",
        bgcolor=BRAND_ORANGE,
        color=Colors.WHITE,
        width=200,
        visible=False,
        style=ft.ButtonStyle(shape={"": ft.RoundedRectangleBorder(radius=28)}),
    )

    # ---------- ฟังก์ชันส่ง OTP ----------
    def on_send(e):
        if not email.value:
            page.snack_bar = ft.SnackBar(ft.Text("⚠️ กรุณากรอกอีเมล"))
        else:
            try:
                res = requests.post(f"{API_BASE}/auth/request-otp", json={"email": email.value})
                if res.status_code == 200:
                    page.snack_bar = ft.SnackBar(ft.Text("✅ ส่ง OTP ไปยังอีเมลแล้ว"))
                    otp.visible = True
                    confirm_btn.visible = True
                    send_btn.visible = False
                else:
                    msg = res.json().get("detail", "ส่ง OTP ไม่สำเร็จ")
                    page.snack_bar = ft.SnackBar(ft.Text(f"❌ {msg}"))
            except Exception as err:
                page.snack_bar = ft.SnackBar(ft.Text(f"⚠️ Connection error: {err}"))
        page.snack_bar.open = True
        page.update()

    send_btn.on_click = on_send

    # ---------- ฟังก์ชันตรวจสอบ OTP ----------
    def on_confirm(e):
        if not otp.value:
            page.snack_bar = ft.SnackBar(ft.Text("⚠️ กรุณากรอก OTP"))
        else:
            try:
                res = requests.post(
                    f"{API_BASE}/auth/verify-otp",
                    json={"email": email.value, "otp": otp.value},
                )
                if res.status_code == 200:
                    page.snack_bar = ft.SnackBar(ft.Text("✅ ยืนยัน OTP สำเร็จ"))
                    # ✅ ไปหน้าตั้งรหัสผ่านใหม่
                    page.go("/forgot")
                else:
                    msg = res.json().get("detail", "OTP ไม่ถูกต้อง")
                    page.snack_bar = ft.SnackBar(ft.Text(f"❌ {msg}"))
            except Exception as err:
                page.snack_bar = ft.SnackBar(ft.Text(f"⚠️ Connection error: {err}"))
        page.snack_bar.open = True
        page.update()

    confirm_btn.on_click = on_confirm

    logo = ft.Image(src="logo.png", width=120, height=120, fit=ft.ImageFit.CONTAIN)

    content = phone_frame(
        curved_orange_header(),
        ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                logo,
                ft.Container(height=10),
                ft.Text("Reset password", size=20, weight=ft.FontWeight.W_700, color=BRAND_BROWN),
                ft.Container(height=18),
                email,
                ft.Container(height=12),
                otp,
                ft.Container(height=18),
                send_btn,
                confirm_btn,
            ],
        ),
    )

    return ft.View(
        route="/reset",
        padding=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Container(
                expand=True,
                bgcolor=ft.Colors.BLACK,
                alignment=ft.alignment.center,
                content=ft.Container(
                    width=PHONE_W,
                    height=PHONE_H,
                    bgcolor=ft.Colors.WHITE,
                    content=content,
                ),
            )
        ],
    )
