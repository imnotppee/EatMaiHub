import flet as ft
from flet import Icons, Colors

BRAND_ORANGE = "#DC7A00"
BRAND_BROWN  = "#4D2E1E"
PHONE_W, PHONE_H = 412, 917

def curved_orange_header():
    """
    หัวส้มโค้งแบบภาพ: ใช้ Stack วางพื้นส้ม + วาง 'วงรีสีขาว' ซ้อนทับด้านล่าง
    ไม่ใช้ Positioned (เวอร์ชันนี้ไม่มี) — ใช้ top/left ของ Container แทน
    """
    return ft.Stack(
        width=PHONE_W,
        height=210,
        controls=[
            ft.Container(width=PHONE_W, height=150, bgcolor=BRAND_ORANGE),
            ft.Container(  # วงรีสีขาวทับเพื่อให้เกิดเส้นโค้ง
                width=PHONE_W + 80,
                height=200,
                bgcolor=Colors.WHITE,
                border_radius=100,
                top=110,          # ยิ่งน้อย โค้งยิ่งสูง
                left=-40,         # ขยายความกว้างให้โค้งกินเต็มขอบ
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

def build_login_view(page: ft.Page) -> ft.View:
    username = ft.TextField(label="Username", width=340, border_color=BRAND_ORANGE)
    password = ft.TextField(label="Password", width=340, password=True, can_reveal_password=True, border_color=BRAND_ORANGE)

    def on_login(e):
        page.snack_bar = ft.SnackBar(ft.Text("Logged in (mock)"))
        page.snack_bar.open = True
        page.update()

    def goto_signup(e): page.go("/signup")
    def goto_forgot(e): page.go("/forgot")

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
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(Icons.STAR_ROUNDED, size=20, color=BRAND_ORANGE),
                        ft.Icon(Icons.STAR_ROUNDED, size=20, color=BRAND_ORANGE),
                        ft.Icon(Icons.STAR_ROUNDED, size=20, color=BRAND_ORANGE),
                    ],
                ),
                ft.Container(height=18),
                username,
                ft.Container(height=12),
                password,
                ft.Container(height=8),
                ft.Container(
                    alignment=ft.alignment.center_left,
                    width=340,
                    content=ft.TextButton("Forgot your password?", on_click=goto_forgot),
                ),
                ft.Container(height=4),
                ft.ElevatedButton(
                    text="Login",
                    on_click=on_login,
                    bgcolor=BRAND_ORANGE,
                    color=Colors.WHITE,
                    width=220,
                    style=ft.ButtonStyle(shape={"": ft.RoundedRectangleBorder(radius=28)}),
                ),
                ft.Container(height=6),
                ft.TextButton(
                    "Create account", on_click=goto_signup,
                    style=ft.ButtonStyle(text_style=ft.TextStyle(size=16, weight=ft.FontWeight.W_700)),
                ),
                ft.Container(height=8),
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
                ft.Container(height=24),
            ],
        ),
    )

    return ft.View(
        route="/",
        padding=0,
        bgcolor=Colors.WHITE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.START,
        controls=[ft.Row(controls=[content], alignment=ft.MainAxisAlignment.CENTER)],
    )
