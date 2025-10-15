import flet as ft
import requests
from flet import Colors

# ---------- Constants ----------
BRAND_ORANGE = "#DC7A00"
BRAND_BROWN = "#4D2E1E"
PHONE_W, PHONE_H = 412, 917
API_BASE = "http://localhost:8000"  # ✅ backend URL


# ---------- Layout ----------
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


# ---------- Forgot Password View ----------
def build_forgot_view(page: ft.Page) -> ft.View:
    pass1 = ft.TextField(
        label="New Password",
        width=340,
        password=True,
        can_reveal_password=True,
        border_color=BRAND_ORANGE,
    )
    pass2 = ft.TextField(
        label="Confirm Password",
        width=340,
        password=True,
        can_reveal_password=True,
        border_color=BRAND_ORANGE,
    )

    # ---------- ฟังก์ชันเปลี่ยนรหัสผ่าน ----------
    def on_confirm(e):
        if not pass1.value or not pass2.value:
            show_dialog("⚠️ กรุณากรอกข้อมูลให้ครบ")
            return

        if pass1.value != pass2.value:
            show_dialog("❌ รหัสผ่านไม่ตรงกัน")
            return

        try:
            # ✅ backend จะเชื่อมต่อกับ OTP ที่ verify แล้ว
            data = {"new_password": pass1.value}
            res = requests.post(f"{API_BASE}/auth/forgot-password", json=data)

            if res.status_code == 200:
                show_dialog("✅ เปลี่ยนรหัสผ่านสำเร็จ!")
                # ✅ กลับไปหน้า login ทันที
                page.go("/login")
            else:
                msg = res.json().get("detail", "Reset failed")
                show_dialog(f"❌ {msg}")

        except Exception as err:
            show_dialog(f"⚠️ Connection error: {err}")

    # ---------- ฟังก์ชันแสดง Popup ----------
    def show_dialog(message: str):
        page.dialog = ft.AlertDialog(
            title=ft.Text(message),
            bgcolor=Colors.WHITE,
        )
        page.dialog.open = True
        page.update()

    # ---------- UI ----------
    logo = ft.Image(src="logo.png", width=120, height=120, fit=ft.ImageFit.CONTAIN)

    content = phone_frame(
        curved_orange_header(),
        ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                logo,
                ft.Text(
                    "Enter your new password",
                    size=18,
                    weight=ft.FontWeight.W_700,
                    text_align="center",
                    color=BRAND_BROWN,
                ),
                ft.Container(height=12),
                pass1,
                ft.Container(height=12),
                pass2,
                ft.Container(height=24),
                ft.ElevatedButton(
                    "Confirm",
                    on_click=on_confirm,
                    bgcolor=BRAND_ORANGE,
                    color=Colors.WHITE,
                    width=200,
                    style=ft.ButtonStyle(
                        shape={"": ft.RoundedRectangleBorder(radius=28)}
                    ),
                ),
            ],
        ),
    )

    return ft.View(
        route="/forgot",
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
            ),
        ],
    )
