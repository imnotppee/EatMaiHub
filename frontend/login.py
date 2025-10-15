import flet as ft
from flet import Icons, Colors
import requests

# ---------- ค่าคงที่ ----------
BRAND_ORANGE = "#DC7A00"
BRAND_BROWN  = "#4D2E1E"
PHONE_W, PHONE_H = 412, 917
API_BASE = "http://localhost:8000"

# ---------- Header ----------
def curved_orange_header():
    ORANGE_H = 150
    ELLIPSE_W = 413
    ELLIPSE_H = 103
    ELLIPSE_TOP = 110
    ELLIPSE_LEFT = -1

    return ft.Stack(
        width=PHONE_W,
        height=ORANGE_H + 60,
        controls=[
            ft.Container(width=PHONE_W, height=ORANGE_H, bgcolor=BRAND_ORANGE),
            ft.Container(width=ELLIPSE_W, height=ELLIPSE_H, bgcolor=Colors.WHITE,
                         border_radius=ELLIPSE_H // 2, top=ELLIPSE_TOP, left=ELLIPSE_LEFT),
        ],
    )

# ---------- Frame ----------
def phone_frame(*children: ft.Control):
    return ft.Container(
        width=PHONE_W,
        height=PHONE_H,
        bgcolor=Colors.WHITE,
        content=ft.Column(controls=list(children), spacing=0),
    )

# ---------- View ----------
def build_login_view(page: ft.Page) -> ft.View:
    email = ft.TextField(label="Email", width=340, border_color=BRAND_ORANGE)
    password = ft.TextField(label="Password", width=340, password=True, can_reveal_password=True, border_color=BRAND_ORANGE)

    # ✅ ฟังก์ชันล็อกอินจริง
    def on_login(e):
        data = {"email": email.value, "password": password.value}
        try:
            res = requests.post(f"{API_BASE}/auth/login", json=data)
            if res.status_code == 200:
                info = res.json()
                page.snack_bar = ft.SnackBar(ft.Text(f"✅ {info['message']}"))
                page.snack_bar.open = True
                page.go("/home")
            else:
                msg = res.json().get("detail", "Login failed")
                page.snack_bar = ft.SnackBar(ft.Text(f"❌ {msg}"))
                page.snack_bar.open = True
        except Exception as err:
            page.snack_bar = ft.SnackBar(ft.Text(f"⚠️ Connection error: {err}"))
            page.snack_bar.open = True
        page.update()

    def goto_signup(e): page.go("/signup")
    def goto_forgot(e): page.go("/reset")
    def google_login(e):
        page.snack_bar = ft.SnackBar(ft.Text("TODO: Google Sign-In"))
        page.snack_bar.open = True
        page.update()

    logo = ft.Image(src="logo.png", width=140, height=140, fit=ft.ImageFit.CONTAIN)

    content = phone_frame(
        curved_orange_header(),
        ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                logo,
                ft.Container(height=8),
                email,
                ft.Container(height=12),
                password,
                ft.Container(height=8),
                ft.Container(
                    alignment=ft.alignment.center_left,
                    width=340,
                    content=ft.TextButton("Forgot your password?", on_click=goto_forgot),
                ),
                ft.ElevatedButton(
                    text="Login",
                    on_click=on_login,
                    bgcolor=BRAND_ORANGE,
                    color=Colors.WHITE,
                    width=220,
                    style=ft.ButtonStyle(shape={"": ft.RoundedRectangleBorder(radius=28)}),
                ),
                ft.Container(height=6),
                ft.TextButton("Create account", on_click=goto_signup),
                ft.Container(height=12),
                ft.Row(
                    width=340,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Container(ft.Divider(color=Colors.BLACK45, thickness=1), expand=True),
                        ft.Text(" or "),
                        ft.Container(ft.Divider(color=Colors.BLACK45, thickness=1), expand=True),
                    ],
                ),
                ft.Container(height=10),
                ft.GestureDetector(
                    on_tap=google_login,
                    mouse_cursor=ft.MouseCursor.CLICK,
                    content=ft.Image(src="google.png", width=36, height=36, fit=ft.ImageFit.CONTAIN),
                ),
            ],
        ),
    )

    return ft.View(
        route="/",
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
