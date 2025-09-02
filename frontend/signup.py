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

def build_signup_view(page: ft.Page) -> ft.View:
    username = ft.TextField(label="Username", width=340, border_color=BRAND_ORANGE)
    password = ft.TextField(label="Password", width=340, password=True, can_reveal_password=True, border_color=BRAND_ORANGE)
    email    = ft.TextField(label="Email",    width=340, border_color=BRAND_ORANGE)

    def on_create(e):
        page.snack_bar = ft.SnackBar(ft.Text("Account created (mock)"))
        page.snack_bar.open = True
        page.go("/")
        page.update()

    logo = ft.Image(src="logo.png", width=120, height=120, fit=ft.ImageFit.CONTAIN)

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
                    "Create account",
                    on_click=on_create,
                    bgcolor=BRAND_ORANGE,
                    color=Colors.WHITE,
                    width=240,
                    style=ft.ButtonStyle(shape={"": ft.RoundedRectangleBorder(radius=28)}),
                ),
            ],
        ),
    )

    return ft.View(
        route="/signup",
        padding=0,
        bgcolor=Colors.WHITE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.START,
        controls=[ft.Row(controls=[content], alignment=ft.MainAxisAlignment.CENTER)],
    )
