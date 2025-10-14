import flet as ft
import requests
from flet import Colors

BRAND_ORANGE = "#DC7A00"
PHONE_W, PHONE_H = 412, 917
API_URL = "http://127.0.0.1:8000/api/restaurants"  # เปลี่ยนพอร์ต backend เป็น 8000

def categories_view(page: ft.Page) -> ft.View:
    current_category = "อาหารไทย"

    # ---------- Header ----------
    header_row = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color=ft.Colors.WHITE, on_click=lambda e: page.go("/home")),
            ft.Image(src="logo.png", width=36, height=36),
            ft.IconButton(icon=ft.Icons.PERSON, icon_color=ft.Colors.WHITE),
        ],
    )

    search = ft.TextField(
        hint_text="ค้นหาร้าน / เมนู",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=20,
        border_color=BRAND_ORANGE,
        filled=True,
        fill_color=ft.Colors.WHITE,
        height=44,
    )

    header = ft.Container(
        padding=ft.padding.only(left=16, right=16, top=12, bottom=12),
        content=ft.Column(spacing=12, controls=[header_row, search]),
    )

    # ---------- ดึงข้อมูลร้านอาหารจาก backend ----------
    def fetch_restaurants():
        try:
            res = requests.get(API_URL)
            res.raise_for_status()
            return res.json()
        except Exception as e:
            print("Error fetching restaurants:", e)
            return []

    all_restaurants = fetch_restaurants()

    # ฟิลเตอร์ตามหมวดหมู่ (เนื่องจาก backend ไม่มี field category, filter ตามชื่อ)
    def get_category_restaurants(category_name):
        keyword_map = {
            "อาหารไทย": "ไทย",
            "อาหารญี่ปุ่น": "ญี่ปุ่น",
            "อาหารฟาสต์ฟู้ด": "ฟาสต์ฟู้ด"
        }
        keyword = keyword_map.get(category_name, "")
        return [r for r in all_restaurants if keyword in r.get("name", "")]

    food_list_column = ft.Column(spacing=12, scroll=ft.ScrollMode.AUTO, expand=True)
    food_list_column.controls = []

    # ---------- สร้างการ์ดร้านอาหาร ----------
    def build_food_list(food_items):
        cards = []
        for f in food_items:
            card = ft.Container(
                bgcolor=ft.Colors.WHITE,
                border_radius=22,
                padding=18,
                margin=ft.margin.symmetric(vertical=10, horizontal=8),
                shadow=ft.BoxShadow(
                    blur_radius=15,
                    spread_radius=1,
                    color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                ),
                height=140,
                content=ft.Row(
                    spacing=14,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            width=100,
                            height=100,
                            border_radius=12,
                            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                            content=ft.Image(
                                src=f.get("banner", "default.png"),
                                fit=ft.ImageFit.COVER,
                            ),
                        ),
                        ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                            spacing=6,
                            expand=True,
                            controls=[
                                ft.Text(
                                    f"ชื่อร้าน : {f.get('name', '-')}",
                                    size=14,
                                    weight="bold",
                                    color=ft.Colors.BLACK87,
                                    max_lines=1,
                                    overflow="ellipsis",
                                    width=180,
                                ),
                                ft.Row(
                                    spacing=5,
                                    controls=[
                                        ft.Icon(name=ft.Icons.STAR_ROUNDED, color=BRAND_ORANGE, size=18),
                                        ft.Text(f"รีวิว : {f.get('review', '-')}", size=13, color=BRAND_ORANGE),
                                    ],
                                ),
                                ft.Row(
                                    spacing=5,
                                    controls=[
                                        ft.Icon(name=ft.Icons.LOCATION_ON_ROUNDED, color="#FF6F61", size=18),
                                        ft.Text(f"ที่อยู่ : {f.get('address', '-')}", size=12, color=ft.Colors.BLACK54),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            )
            cards.append(card)
        return cards

    # โหลด category แรกตอนเริ่ม
    food_list_column.controls = build_food_list(get_category_restaurants(current_category))

    # ---------- เปลี่ยนหมวด ----------
    def change_category(e):
        nonlocal current_category
        current_category = e.control.data
        food_list_column.controls.clear()
        food_list_column.controls.extend(build_food_list(get_category_restaurants(current_category)))
        title.value = f"ร้านอาหาร - {current_category}"
        page.update()

    # ---------- ปุ่มหมวด ----------
    def category_card(img: str, label: str, active=False):
        return ft.GestureDetector(
            data=label,
            on_tap=change_category,
            content=ft.Column(
                [
                    ft.Container(
                        width=72,
                        height=72,
                        bgcolor=ft.Colors.WHITE,
                        border_radius=12,
                        shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.BLACK12),
                        alignment=ft.alignment.center,
                        content=ft.Image(src=img, width=48, height=48, fit=ft.ImageFit.CONTAIN),
                    ),
                    ft.Text(
                        label,
                        size=14,
                        weight="bold" if active else "normal",
                        color=BRAND_ORANGE if active else ft.Colors.BLACK87,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=6,
            ),
        )

    category_buttons = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
        controls=[
            category_card("catthai.png", "อาหารไทย", active=True),
            category_card("catjapan.png", "อาหารญี่ปุ่น"),
            category_card("catfastfood.png", "อาหารฟาสต์ฟู้ด"),
        ],
    )

    # ---------- Bottom nav ----------
    bottom_nav = ft.Container(
        bgcolor=Colors.WHITE,
        border=ft.border.only(top=ft.BorderSide(1, Colors.BLACK12)),
        padding=10,
        height=65,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                ft.GestureDetector(
                    on_tap=lambda e: page.go("/home"),
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=2,
                        controls=[ft.Image(src="home.png", width=28, height=28, fit=ft.ImageFit.CONTAIN), ft.Text("Home", size=10)],
                    ),
                ),
                ft.GestureDetector(
                    on_tap=lambda e: page.go("/favorite"),
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=2,
                        controls=[ft.Image(src="heart.png", width=28, height=28, fit=ft.ImageFit.CONTAIN), ft.Text("Favorite", size=10)],
                    ),
                ),
            ],
        ),
    )

    title = ft.Text(f"ร้านอาหาร - {current_category}", size=18, weight="bold", color=BRAND_ORANGE)

    scrollable_area = ft.Column(
        spacing=16,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            header,
            category_buttons,
            ft.Row(alignment=ft.MainAxisAlignment.START, controls=[title]),
            food_list_column,
        ],
    )

    orange_gradient_bg = ft.Container(
        width=PHONE_W,
        height=340,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[BRAND_ORANGE, "#F6D0A0", "#FFFFFFFF"],
            stops=[0.0, 0.6, 1.0],
        ),
    )

    phone_frame = ft.Stack(
        width=PHONE_W,
        height=PHONE_H,
        controls=[
            orange_gradient_bg,
            ft.Container(
                padding=ft.padding.symmetric(horizontal=12),
                content=ft.Column(
                    expand=True,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Container(expand=True, content=scrollable_area),
                        bottom_nav,
                    ],
                ),
            ),
        ],
    )

    return ft.View(
        route="/categories",
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
                    content=phone_frame,
                ),
            )
        ],
    )