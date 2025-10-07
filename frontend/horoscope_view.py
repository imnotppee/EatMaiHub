import flet as ft
import json
import os
import datetime

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
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }

    today_en = weekday_map[datetime.datetime.now().weekday()]
    today_data = data.get(today_en)

    # ---------- ถ้าไม่มีข้อมูลวันนี้ ----------
    if not today_data:
        today_data = {
            "category": "ไม่พบข้อมูลดวงวันนี้",
            "title": "ไม่มีเมนูแนะนำ",
            "subtitle": "กรุณาเพิ่มข้อมูลใน horoscope_foods.json",
            "image": "default.png"
        }

    # ---------- Header ----------
    header = ft.Container(
        padding=ft.padding.only(left=16, right=16, top=30, bottom=10),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[BRAND_ORANGE, "#F6D0A0"]
        ),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color=ft.Colors.WHITE,
                    on_click=lambda e: page.go("/home"),
                ),
                ft.Text("กินตามดวงวันนี้", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Container(width=40),
            ],
        ),
    )

    # ---------- การ์ดเมนู ----------
    card = ft.Container(
        width=PHONE_W - 40,
        height=360,
        bgcolor=ft.Colors.WHITE,
        border_radius=20,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12),
        padding=16,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
            controls=[
                ft.Text(today_data["category"], size=16, weight=ft.FontWeight.BOLD, color=BRAND_ORANGE),
                ft.Container(
                    height=180,
                    width=PHONE_W - 80,
                    border_radius=12,
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    content=ft.Image(src=today_data["image"], fit=ft.ImageFit.COVER),
                ),
                ft.Text(today_data["title"], size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                ft.Text(today_data["subtitle"], size=13, text_align=ft.TextAlign.CENTER, color=ft.Colors.BLACK87),
            ],
        ),
    )

    # ---------- Body ----------
    body = ft.Container(
        width=PHONE_W,
        height=PHONE_H,
        bgcolor=ft.Colors.WHITE,
        padding=ft.padding.symmetric(horizontal=16, vertical=10),
        content=ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            alignment=ft.MainAxisAlignment.START,
            spacing=12,
            controls=[
                header,
                ft.Text(f"วันนี้วัน{today_data['category'].split(' ')[0][4:]}",  # ดึงชื่อวันจาก category
                        size=16, weight=ft.FontWeight.BOLD, color=BRAND_ORANGE),
                card,
                ft.Container(height=40)
            ],
        ),
    )

    # ---------- Frame ----------
    return ft.View(
        route="/horoscope",
        padding=0,
        controls=[
            ft.Container(
                expand=True,
                bgcolor=ft.Colors.BLACK,
                alignment=ft.alignment.center,
                content=ft.Container(
                    width=PHONE_W,
                    height=PHONE_H,
                    bgcolor=ft.Colors.WHITE,
                    content=body,
                ),
            )
        ],
    )
