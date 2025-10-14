import flet as ft
import requests

BRAND_ORANGE = "#DC7A00"
PHONE_W, PHONE_H = 412, 917

API_URL = "http://127.0.0.1:5001/api/favorites"

def build_favorite_view(page: ft.Page) -> ft.View:
    try:
        res = requests.get(API_URL)
        res.raise_for_status()
        favorites = res.json()
    except:
        favorites = []

    # ลบรายการโปรด
    def remove_favorite(item):
        requests.delete(f"{API_URL}/{item['id']}")
        page.snack_bar = ft.SnackBar(ft.Text("ลบออกจากรายการโปรดแล้ว"), bgcolor="red")
        page.snack_bar.open = True
        page.go("/favorite")

    def favorite_card(item):
        heart_icon = ft.IconButton(
            icon=ft.Icons.FAVORITE,
            icon_color=BRAND_ORANGE,
            on_click=lambda e: remove_favorite(item),
        )

        return ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            padding=10,
            margin=ft.margin.only(bottom=10),
            shadow=ft.BoxShadow(blur_radius=6, color=ft.Colors.BLACK12),
            content=ft.Row(
                spacing=10,
                controls=[
                    ft.Image(src=item["image"], width=90, height=90, border_radius=10, fit=ft.ImageFit.COVER),
                    ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Text(item["title"], size=14, weight=ft.FontWeight.BOLD),
                            ft.Text(item["time"], size=11, color=ft.Colors.BLACK54),
                        ],
                    ),
                    heart_icon,
                ],
            ),
        )

    body = (
        ft.Column([favorite_card(f) for f in favorites])
        if favorites
        else ft.Text("ยังไม่มีรายการโปรด", color=ft.Colors.BLACK54)
    )

    return ft.View(
        route="/favorite",
        controls=[
            ft.AppBar(title=ft.Text("รายการโปรด"), bgcolor=BRAND_ORANGE),
            ft.Container(padding=10, content=body),
        ],
    )
