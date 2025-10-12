import flet as ft
from utils.colors import BG_LIGHT

def Topbar():
    return ft.Container(
        height=60,
        bgcolor=BG_LIGHT,
        padding=ft.padding.only(left=20, right=20),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(),
                ft.Icon(name=ft.Icons.PERSON, size=28),
            ]
        ),
        border=ft.border.only(bottom=ft.BorderSide(1, "#E0E0E0"))
    )
