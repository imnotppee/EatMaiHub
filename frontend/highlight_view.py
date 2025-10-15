import flet as ft
import requests  # ✅ เพิ่มเพื่อดึงข้อมูลจาก backend
from flet import Colors

BRAND_ORANGE = "#DC7A00"
PHONE_W, PHONE_H = 412, 917
API_URL = "http://127.0.0.1:8000/api/highlights"  # ✅ URL backend

def build_highlight_view(page: ft.Page) -> ft.View:
    # ---------- โหลดข้อมูลร้านจาก Database ผ่าน API ----------
    try:
        res = requests.get(API_URL, timeout=5)
        res.raise_for_status()
        restaurants = res.json()
    except Exception as e:
        print("❌ โหลดข้อมูลร้านเด็ดไม่สำเร็จ:", e)
        restaurants = []  # fallback ถ้าโหลดไม่ได้

    # ---------- Header ----------
    header_row = ft.Row(
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
            ft.Image(src="logo.png", width=150, height=90),
            ft.Container(width=36),
        ],
    )

    # ---------- ช่องค้นหา ----------
    search = ft.TextField(
        hint_text="ค้นหาร้าน / เมนู",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=30,
        border_color=BRAND_ORANGE,
        border_width=2,
        filled=True,
        fill_color=ft.Colors.WHITE,
        height=44,
        cursor_color=BRAND_ORANGE,
        focused_border_color=BRAND_ORANGE,
    )

    header = ft.Container(
        width=PHONE_W,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[BRAND_ORANGE, "#F6D0A0"],
        ),
        padding=ft.padding.symmetric(horizontal=16, vertical=10),
        content=ft.Column(spacing=10, controls=[header_row, search]),
    )

    # ---------- หัวข้อ “ร้านเด็ด” ----------
    highlight_title = ft.Row(
        alignment=ft.MainAxisAlignment.START,
        controls=[
            ft.Text("ร้านเด็ด", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
            ft.Container(width=6),
            ft.Image(src="star.png", width=22, height=22),
        ],
    )

    # ---------- ฟังก์ชันสร้างการ์ดร้าน ----------
    def restaurant_card(img, name, desc, route=None):
        """สร้างการ์ดร้านพร้อมคลิกได้"""
        return ft.GestureDetector(
            on_tap=lambda e: page.go(route) if route else None,
            content=ft.Container(
                bgcolor=ft.Colors.WHITE,
                border_radius=12,
                padding=10,
                margin=ft.margin.only(bottom=16),
                shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12),
                content=ft.Column(
                    spacing=8,
                    controls=[
                        ft.Container(
                            height=200,
                            border_radius=12,
                            clip_behavior=ft.ClipBehavior.HARD_EDGE,
                            content=ft.Image(src=img, fit=ft.ImageFit.COVER, width=PHONE_W - 40),
                        ),
                        ft.Text(name, size=16, weight=ft.FontWeight.BOLD, color=BRAND_ORANGE),
                        ft.Text(desc, size=12, color=ft.Colors.BLACK87),
                    ],
                ),
            ),
        )

    # ---------- สร้างรายการร้านทั้งหมด ----------
    restaurant_list = ft.Column(spacing=12, controls=[])

    for r in restaurants:
        name_lower = r["name"].lower()

        if "sunbae" in name_lower:
            route = "/sunbae"
        elif "urban" in name_lower:
            route = "/urban"
        elif "hotto" in name_lower:
            route = "/hottobun"
        else:
            route = None


        restaurant_list.controls.append(
            restaurant_card(r["image"], r["name"], r["desc"], route)
        )

    # ---------- เนื้อหาหลัก (scroll ได้) ----------
    scrollable_content = ft.Container(
        expand=True,
        content=ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            controls=[
                header,
                ft.Container(
                    padding=ft.padding.all(16),
                    content=ft.Column(
                        spacing=12,
                        controls=[highlight_title, restaurant_list],
                    ),
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
                    ft.Image(src=icon, width=28, height=28, fit=ft.ImageFit.CONTAIN),
                    ft.Text(label, size=10, color=BRAND_ORANGE if active else ft.Colors.BLACK87),
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
            scrollable_content,
            bottom_nav,
        ],
    )

    return ft.View(
        route="/highlight",
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
