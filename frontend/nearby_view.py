import flet as ft
import json
import os
import random
from flet import Colors

# ---------- ค่าคงที่ ----------
BRAND_ORANGE = "#DC7A00"
PHONE_W, PHONE_H = 412, 917


def build_nearby_view(page: ft.Page) -> ft.View:
    # ---------- โหลดข้อมูลร้านจาก nearby_restaurants.json ----------
    data_path = os.path.join(os.path.dirname(__file__), "data", "nearby_restaurants.json")
    if not os.path.exists(data_path):
        raise FileNotFoundError("❌ ไม่พบไฟล์ data/nearby_restaurants.json")

    with open(data_path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    # ---------- Header ----------
    header = ft.Container(
        width=PHONE_W,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[BRAND_ORANGE, "#F6D0A0"],
        ),
        padding=ft.padding.symmetric(horizontal=16, vertical=10),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.WHITE24,
                    icon_size=22,
                    on_click=lambda e: page.go("/home"),
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                ),
                ft.Text("ร้านใกล้ฉัน", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Container(width=36),
            ],
        ),
    )

    # ---------- ปุ่มระบุตำแหน่ง ----------
    async def get_location(e):
        try:
            fake_lat = 13.7276 + random.uniform(-0.002, 0.002)
            fake_lng = 100.7772 + random.uniform(-0.002, 0.002)
            msg = f"📍 ตำแหน่งจำลอง: KMITL\nLat: {fake_lat:.4f}, Lng: {fake_lng:.4f}"
            page.snack_bar = ft.SnackBar(content=ft.Text(msg), bgcolor=BRAND_ORANGE, duration=3000)
            page.snack_bar.open = True
            await page.update_async()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"เกิดข้อผิดพลาด: {ex}"), bgcolor="red")
            page.snack_bar.open = True
            await page.update_async()

    locate_button = ft.ElevatedButton(
        text="📍 ระบุตำแหน่งของฉัน",
        color=ft.Colors.WHITE,
        bgcolor=BRAND_ORANGE,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
        on_click=get_location,
    )

    # ---------- หัวข้อ ----------
    title = ft.Container(
        padding=ft.padding.symmetric(horizontal=16, vertical=10),
        content=ft.Text("แนะนำร้านใกล้คุณ 🍜", size=18, weight=ft.FontWeight.BOLD, color=BRAND_ORANGE),
    )

    # ---------- การ์ดร้าน ----------
    def restaurant_card(r):
        return ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.BLACK12),
            padding=10,
            margin=ft.margin.only(bottom=16),
            content=ft.Row(
                controls=[
                    ft.Container(
                        width=100,
                        height=100,
                        border_radius=10,
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                        content=ft.Image(src=r["image"], fit=ft.ImageFit.COVER),
                    ),
                    ft.Container(width=12),
                    ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=6,
                        controls=[
                            ft.Text(r["name"], size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                            ft.Text(f"ประเภท: {r['type']}", size=12, color=ft.Colors.BLACK87),
                            ft.Text(f"ระยะทาง: {r['distance']} กม.", size=12, color=ft.Colors.BLACK54),
                        ],
                    ),
                ],
            ),
        )

    # ---------- รายการร้าน ----------
    restaurant_list = ft.Column(
        controls=[restaurant_card(r) for r in sorted(restaurants, key=lambda x: x["distance"])],
    )

    # ---------- โซน scroll ----------
    scrollable_content = ft.Container(
        expand=True,
        bgcolor=ft.Colors.WHITE,
        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            controls=[
                header,
                title,
                ft.Container(
                    padding=ft.padding.symmetric(horizontal=16),
                    content=locate_button,
                ),
                ft.Container(
                    padding=ft.padding.symmetric(horizontal=16, vertical=10),
                    content=restaurant_list,
                ),
            ],
        ),
    )

    # ---------- Bottom Navigation ----------
    def nav_item(icon: str, label: str, route=None, active=False):
        return ft.GestureDetector(
            on_tap=lambda e: page.go(route) if route else None,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
                controls=[
                    ft.Container(
                        content=ft.Image(src=icon, width=28, height=28, fit=ft.ImageFit.CONTAIN),
                        padding=ft.padding.only(top=2, bottom=2),
                    ),
                    ft.Text(label, size=10, color=BRAND_ORANGE if active else ft.Colors.BLACK87),
                ],
            ),
        )

    bottom_nav = ft.Container(
        bgcolor=ft.Colors.WHITE,
        border=ft.border.only(top=ft.BorderSide(1, ft.Colors.BLACK12)),
        padding=10,
        height=65,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                nav_item("home.png", "Home", route="/home"),
                nav_item("heart.png", "Favorite", route="/favorite"),
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
            ft.Container(expand=True, content=scrollable_content),
            bottom_nav,
        ],
    )

    return ft.View(
        route="/nearby",
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
                    content=layout,
                ),
            )
        ],
    )
