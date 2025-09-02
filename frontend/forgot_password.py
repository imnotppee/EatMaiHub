import flet as ft
from flet import Icons, Colors

BRAND_ORANGE = "#DC7A00"
BRAND_BROWN  = "#4D2E1E"
PHONE_W, PHONE_H = 412, 917

def curved_orange_header():
    return ft.Stack(
        width=PHONE_W,
        height=210,
        controls=[
            ft.Container(width=PHONE_W, height=150, bgcolor=BRAND_ORANGE),
            ft.Container(width=PHONE_W + 80, height=200,
                         bgcolor=Colors.WHITE, border_radius=100,
                         top=110, left=-40),
        ],
    )

def phone_frame(*children: ft.Control):
    return ft.Container(
        width=PHONE_W,
        height=PHONE_H,
        bgcolor=Colors.WHITE,
        content=ft.Column(controls=list(children), spacing=0),
    )

def build_forgot_view(page: ft.Page) -> ft.View:
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
                    alignment=ft.alignment.center_left,
                    content=ft.Text("Enter your new password", size=18, weight=ft.FontWeight.W_700),
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
        route="/forgot",
        padding=0,
        bgcolor=Colors.WHITE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.START,
        controls=[ft.Row(controls=[content], alignment=ft.MainAxisAlignment.CENTER)],
    )
