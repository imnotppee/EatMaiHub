import flet as ft
import requests

BRAND_ORANGE = "#DC7A00"
PHONE_W, PHONE_H = 412, 917
API_URL = "http://127.0.0.1:5001/api"

def build_favorite_view(page: ft.Page, user_id=1) -> ft.View:
    response = requests.get(f"{API_URL}/favorites/{user_id}")
    favorites = response.json()

    # ---------- Header ----------
    header = ft.Container(
        width=PHONE_W,
        height=180,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[BRAND_ORANGE, "#F6D0A0"],
        ),
        border_radius=ft.border_radius.only(bottom_left=40, bottom_right=40),
        padding=ft.padding.only(left=16, right=16, top=36, bottom=16),
        content=ft.Column(
            spacing=16,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            icon_color=ft.Colors.WHITE,
                            on_click=lambda e: page.go("/home"),
                        ),
                        ft.Image(src="logo.png", width=90, height=70),
                        ft.IconButton(icon=ft.Icons.PERSON, icon_color=ft.Colors.WHITE),
                    ],
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("รายการโปรด", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ft.Container(
                            border=ft.border.all(1, ft.Colors.WHITE),
                            border_radius=25,
                            padding=ft.padding.symmetric(horizontal=16, vertical=4),
                            content=ft.Text("ทั้งหมด", size=12, color=ft.Colors.WHITE),
                        ),
                    ],
                ),
            ],
        ),
    )

    # ---------- การ์ดโปรด ----------
    def favorite_card(item):
        heart_icon = ft.Icon(name=ft.Icons.FAVORITE, color=BRAND_ORANGE, size=26)

        def remove_favorite(e):
            requests.post(f"{API_URL}/favorites/toggle", json={
                "user_id": user_id,
                "restaurant_id": item["id"]
            })
            page.go("/favorite")  # reload

        return ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=16,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12),
            padding=12,
            margin=ft.margin.only(bottom=14),
            content=ft.Row(
                spacing=14,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Image(src=item.get("image", "default.png"), width=100, height=100, border_radius=12),
                    ft.Column(
                        alignment=ft.MainAxisAlignment.START,
                        spacing=6,
                        expand=True,
                        controls=[
                            ft.Text(item.get("title", "ไม่ระบุ"), size=15, weight=ft.FontWeight.BOLD),
                            ft.Text(item.get("location", ""), size=13, color=ft.Colors.BLACK54),
                            ft.Text(f"เวลาเปิด: {item.get('open_hours', '-')}", size=12, color=ft.Colors.BLACK45),
                        ],
                    ),
                    ft.GestureDetector(on_tap=remove_favorite, content=heart_icon),
                ],
            ),
        )

    if not favorites:
        fav_list = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[ft.Text("ยังไม่มีรายการโปรด", color=ft.Colors.BLACK54)],
        )
    else:
        fav_list = ft.Column(spacing=10, controls=[favorite_card(f) for f in favorites])

    layout = ft.Column(controls=[header, fav_list])
    return ft.View("/favorite", controls=[layout])
