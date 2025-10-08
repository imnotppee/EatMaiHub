import flet as ft
import json
import os
import datetime
from flet import Colors

BRAND_ORANGE = "#DC7A00"
PHONE_W, PHONE_H = 412, 917


def build_horoscope_view(page: ft.Page) -> ft.View:
    # ---------- โหลดข้อมูลจาก JSON ----------
    data_path = os.path.join(os.path.dirname(__file__), "data", "horoscope_foods.json")
    if not os.path.exists(data_path):
        raise FileNotFoundError("❌ ไม่พบไฟล์ data/horoscope_foods.json")

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # ---------- ตรวจวันปัจจุบัน ----------
    weekday_map = {
        0: ("Monday", "วันจันทร์"),
        1: ("Tuesday", "วันอังคาร"),
        2: ("Wednesday", "วันพุธ"),
        3: ("Thursday", "วันพฤหัสบดี"),
        4: ("Friday", "วันศุกร์"),
        5: ("Saturday", "วันเสาร์"),
        6: ("Sunday", "วันอาทิตย์")
    }

    weekday_index = datetime.datetime.now().weekday()
    today_en, today_th = weekday_map[weekday_index]
    today_foods = data.get(today_en, [])

    # ---------- Header ----------
    header = ft.Container(
        width=PHONE_W,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[BRAND_ORANGE, "#F6D0A0"]
        ),
        padding=ft.padding.only(left=16, right=16, top=30, bottom=16),
        content=ft.Column(
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
                        ft.Image(src="logo.png", width=120, height=60),
                        ft.Container(width=36),
                    ],
                ),
                ft.TextField(
                    hint_text="ค้นหาร้าน / เมนู",
                    prefix_icon=ft.Icons.SEARCH,
                    border_radius=30,
                    height=42,
                    filled=True,
                    fill_color=ft.Colors.WHITE,
                    border_color=ft.Colors.WHITE,
                    content_padding=ft.padding.symmetric(horizontal=14),
                ),
            ],
        ),
    )

    # ---------- หัวข้อ “กินตามดวงวันนี้ (วัน...)” ----------
    title_row = ft.Row(
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=8,
        controls=[
            ft.Image(src="ball.png", width=26, height=26),
            ft.Text(
                f"กินตามดวงวันนี้ ({today_th})",
                size=16,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLACK,
            ),
        ],
    )

    # ---------- การ์ดแสดงเมนู ----------
    def food_card(food):
        return ft.Container(
            width=PHONE_W - 40,
            bgcolor=ft.Colors.WHITE,
            border_radius=16,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12),
            padding=16,
            margin=ft.margin.only(bottom=20),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
                controls=[
                    ft.Text(food["category"], size=15, weight=ft.FontWeight.BOLD, color=BRAND_ORANGE),
                    ft.Container(
                        height=180,
                        width=PHONE_W - 80,
                        border_radius=12,
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                        content=ft.Image(src=food["image"], fit=ft.ImageFit.COVER),
                    ),
                    ft.Text(food["title"], size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(food["subtitle"], size=12, text_align=ft.TextAlign.CENTER, color=ft.Colors.BLACK87),
                ],
            ),
        )

    food_list = [food_card(f) for f in today_foods]

    # ---------- Scrollable Content ----------
    scrollable_area = ft.Container(
        expand=True,
        content=ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            controls=[
                header,
                ft.Container(padding=ft.padding.all(16), content=title_row),
                ft.Container(
                    padding=ft.padding.symmetric(horizontal=16),
                    content=ft.Column(spacing=12, controls=food_list),
                ),
            ],
        ),
    )

    # ---------- Bottom Navigation ----------
    def nav_item(icon: str, label: str, route=None, active=False):
        return ft.GestureDetector(
            on_tap=lambda e: page.go(route) if label == "Home" else None,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
                controls=[
                    ft.Container(
                        content=ft.Image(src=icon, width=28, height=28, fit=ft.ImageFit.CONTAIN),
                        padding=ft.padding.only(top=2, bottom=2),
                    ),
                    ft.Text(
                        label,
                        size=10,
                        color=BRAND_ORANGE if active else Colors.BLACK87,
                    ),
                ],
            ),
        )

    bottom_nav = ft.Container(
        bgcolor=Colors.WHITE,
        border=ft.border.only(top=ft.BorderSide(1, Colors.BLACK12)),
        padding=10,
        height=65,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                nav_item("home.png", "Home", route="/home"),
                nav_item("heart.png", "Favorite"),
                nav_item("review.png", "Review"),
                nav_item("more.png", "More"),
            ],
        ),
    )

    # ---------- Layout รวม ----------
    layout = ft.Column(
        expand=True,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.Container(expand=True, content=scrollable_area),
            bottom_nav,
        ],
    )

    return ft.View(
        route="/horoscope",
        padding=0,
        controls=[
            ft.Container(
                expand=True,
                bgcolor=Colors.BLACK,
                alignment=ft.alignment.center,
                content=ft.Container(
                    width=PHONE_W,
                    height=PHONE_H,
                    bgcolor=Colors.WHITE,
                    content=layout,
                ),
            )
        ],
    )
