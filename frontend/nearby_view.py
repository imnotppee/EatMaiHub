import flet as ft
import json
import os

BRAND_ORANGE = "#DC7A00"
PHONE_W, PHONE_H = 412, 917

def build_nearby_view(page: ft.Page) -> ft.View:
    # ---------- โหลดข้อมูลจาก JSON ----------
    data_path = os.path.join(os.path.dirname(__file__), "data", "nearby_data.json")
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
        padding=ft.padding.only(left=16, right=16, top=30, bottom=12),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.WHITE24,
                    icon_size=22,
                    on_click=lambda e: page.go("/home"),
                ),
                ft.Image(src="logo.png", width=100, height=60),
                ft.Container(width=36),
            ],
        ),
    )

    # ---------- แผนที่ (Google Maps Embed) ----------
    map_section = ft.Container(
        width=PHONE_W - 20,
        height=200,
        border_radius=12,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.BLACK26),
        content=ft.IFrame(
            src="https://www.google.com/maps/embed/v1/view?key=YOUR_GOOGLE_MAPS_API_KEY&center=13.729,100.775&zoom=14",
            width=PHONE_W - 20,
            height=200,
        ),
    )

    # ---------- การ์ดร้าน ----------
    def restaurant_card(item):
        return ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            padding=10,
            margin=ft.margin.only(bottom=12),
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12),
            content=ft.Row(
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        width=80,
                        height=80,
                        border_radius=10,
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                        content=ft.Image(src=item.get("image", ""), fit=ft.ImageFit.COVER),
                    ),
                    ft.Column(
                        spacing=4,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Row(
                                spacing=4,
                                controls=[
                                    ft.Icon(ft.Icons.STAR, color=BRAND_ORANGE, size=16),
                                    ft.Text(f"{item['rating']} / {item['distance']} km", size=12),
                                ],
                            ),
                            ft.Text(item["name"], size=14, weight=ft.FontWeight.BOLD, color=BRAND_ORANGE),
                            ft.Text(item["category"], size=12, color=ft.Colors.BLACK87),
                            ft.ElevatedButton(
                                text="ดูร้านนี้",
                                bgcolor=BRAND_ORANGE,
                                color="white",
                                height=28,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                                on_click=lambda e: page.go(f"/{item['name'].lower().replace(' ', '')}"),
                            ),
                        ],
                    ),
                ],
            ),
        )

    restaurant_list = ft.Column(
        spacing=12,
        controls=[restaurant_card(r) for r in restaurants],
    )

    # ---------- รวมทุกส่วน ----------
    body = ft.Container(
        width=PHONE_W,
        height=PHONE_H,
        bgcolor=ft.Colors.WHITE,
        content=ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            controls=[
                header,
                ft.Container(padding=ft.padding.all(12), content=map_section),
                ft.Container(padding=ft.padding.symmetric(horizontal=16), content=restaurant_list),
                ft.Container(height=20),
            ],
        ),
    )

    return ft.View(
        route="/nearby",
        padding=0,
        controls=[
            ft.Container(
                expand=True,
                bgcolor="black",
                alignment=ft.alignment.center,
                content=body,
            )
        ],
    )
