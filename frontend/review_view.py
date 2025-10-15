import flet as ft
import requests

BRAND_ORANGE = "#DC7A00"
PHONE_W, PHONE_H = 412, 917
API_URL = "http://127.0.0.1:5001/api/reviews"


def build_review_view(page: ft.Page) -> ft.View:
    try:
        res = requests.get(API_URL)
        res.raise_for_status()
        reviews = res.json()
    except Exception as e:
        print("⚠️ โหลดข้อมูลไม่สำเร็จ:", e)
        reviews = []

    # ✅ การ์ดแสดงรีวิว
    def review_card(r):
        return ft.Container(
            bgcolor=ft.Colors.WHITE,
            padding=10,
            margin=ft.margin.only(bottom=10),
            border_radius=12,
            shadow=ft.BoxShadow(blur_radius=4, color=ft.Colors.BLACK12),
            content=ft.Column(
                spacing=3,
                controls=[
                    ft.Text(
                        r["restaurant_table"],
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK87,
                    ),
                    ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.STAR if i < r["rating"] else ft.Icons.STAR_BORDER,
                                color=BRAND_ORANGE,
                                size=16,
                            )
                            for i in range(5)
                        ]
                    ),
                    ft.Text(r["review_text"], size=13, color=ft.Colors.BLACK87),
                ],
            ),
        )

    body = (
        ft.Column([review_card(r) for r in reviews])
        if reviews
        else ft.Text("ยังไม่มีรีวิว", color=ft.Colors.BLACK54)
    )

    return ft.View(
        route="/review",
        controls=[
            ft.AppBar(title=ft.Text("รีวิวทั้งหมด"), bgcolor=BRAND_ORANGE),
            ft.Container(padding=10, content=body),
        ],
    )
