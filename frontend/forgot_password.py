import flet as ft
from flet import Icons, Colors

BRAND_ORANGE = "#DC7A00"
BRAND_BROWN  = "#4D2E1E"
PHONE_W, PHONE_H = 412, 917

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

def phone_frame(*children: ft.Control):
    return ft.Container(
        width=PHONE_W, height=PHONE_H, bgcolor=Colors.WHITE,
        content=ft.Column(controls=list(children), spacing=0),
    )

def build_forgot_view(page: ft.Page) -> ft.View:   # ✅ แก้ชื่อให้ตรง app.py
    pass1 = ft.TextField(label="Password",         width=340, password=True, can_reveal_password=True, border_color=BRAND_ORANGE)
    pass2 = ft.TextField(label="Confirm Password", width=340, password=True, can_reveal_password=True, border_color=BRAND_ORANGE)

    def on_confirm(e):
        if pass1.value != pass2.value:
            page.snack_bar = ft.SnackBar(ft.Text("รหัสผ่านไม่ตรงกัน"))
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Password updated (mock)"))
            page.go("/")
        page.snack_bar.open = True
        page.update()

    logo = ft.Image(src="logo.png", width=120, height=120, fit=ft.ImageFit.CONTAIN)

    content = phone_frame(
        curved_orange_header(),
        ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                logo,
                ft.Container(
                    width=340,
                    alignment=ft.alignment.center,   # ✅ จาก center_left → center
                    content=ft.Text(
                        "Enter your new password",
                    size=18,
                    weight=ft.FontWeight.W_700,
                    text_align="center",         # ✅ ให้ข้อความจัดกลาง
                        ),
                    ),
                ft.Container(height=12),
                pass1, ft.Container(height=12),
                pass2, ft.Container(height=18),
                ft.ElevatedButton(
                    "Confirm",
                    on_click=on_confirm,
                    bgcolor=BRAND_ORANGE,
                    color=Colors.WHITE,
                    width=200,
                    style=ft.ButtonStyle(shape={"": ft.RoundedRectangleBorder(radius=28)}),
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
        # พื้นหลังนอกกรอบ = ดำ
            ft.Container(
                expand=True,
                bgcolor=ft.Colors.BLACK,
                alignment=ft.alignment.center,
                content=ft.Container(
                    width=412,
                    height=917,
                    bgcolor=ft.Colors.WHITE,   # กรอบมือถือ = ขาว
                    content=content,
            ),
        )
    ],
)