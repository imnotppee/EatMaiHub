import flet as ft
import json
import os
from flet import Colors

BRAND_ORANGE = "#DC7A00"
PHONE_W, PHONE_H = 412, 917


# ---------- โหลด JSON ----------
def load_data(filename: str):
    path = os.path.join(os.path.dirname(__file__), "data", filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def categories_view(page: ft.Page) -> ft.View:
    current_category = "อาหารไทย"
    data_map = {
        "อาหารไทย": ("thai_food.json", "thai_foods"),
        "อาหารญี่ปุ่น": ("japan_food.json", "japan_foods"),
        "อาหารฟาสต์ฟู้ด": ("fast_food.json", "fast_foods"),
    }

    data = load_data(data_map[current_category][0])
    foods = data.get(data_map[current_category][1], [])

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

    # ---------- การ์ดร้านอาหาร ----------
    def build_food_list(food_items):
        cards = []
        for f in food_items:
            cards.append(
                ft.Container(
                    bgcolor=ft.Colors.WHITE,
                    border_radius=22,
                    padding=18,
                    margin=ft.margin.symmetric(vertical=10, horizontal=8),
                    shadow=ft.BoxShadow(
                        blur_radius=15,
                        spread_radius=1,
                        color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                    ),
                    height=150,
                    content=ft.Row(
                        spacing=14,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                width=110,
                                height=110,
                                border_radius=12,
                                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                                content=ft.Image(
                                    src=f"assets/{f['image']}",
                                    fit=ft.ImageFit.COVER,
                                ),
                            ),
                            ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.START,
                                spacing=6,
                                controls=[
                                    ft.Text(f"ชื่อร้าน : {f['name']}", size=16, weight="bold", color=ft.Colors.BLACK87),
                                    ft.Row(
                                        spacing=5,
                                        controls=[
                                            ft.Icon(name=ft.Icons.STAR_ROUNDED, color=BRAND_ORANGE, size=18),
                                            ft.Text(f"รีวิว : {f['rating']} ดาว", size=14, color=BRAND_ORANGE),
                                        ],
                                    ),
                                    ft.Row(
                                        spacing=5,
                                        controls=[
                                            ft.Icon(name=ft.Icons.LOCATION_ON_ROUNDED, color="#FF6F61", size=18),
                                            ft.Text(f"ที่อยู่ : {f['address']}", size=13, color=ft.Colors.BLACK54),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                )
            )
        return cards

    food_list_column = ft.Column(spacing=12, scroll=ft.ScrollMode.AUTO, expand=True, controls=build_food_list(foods))

    # ---------- เปลี่ยนหมวด ----------
    def change_category(e):
        nonlocal current_category
        current_category = e.control.data
        json_file, key = data_map[current_category]
        new_data = load_data(json_file)
        new_foods = new_data.get(key, [])
        food_list_column.controls.clear()
        for c in build_food_list(new_foods):
            food_list_column.controls.append(c)
        title.value = f"ร้านอาหาร - {current_category}"
        for btn in category_buttons.controls:
            label = btn.content.controls[1]
            label.color = BRAND_ORANGE if btn.data == current_category else ft.Colors.BLACK87
            label.weight = "bold" if btn.data == current_category else "normal"
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
                nav_item("heart.png", "Favorite"),
                nav_item("review.png", "Review"),
                nav_item("more.png", "More"),
            ],
        ),
    )

    title = ft.Text("ร้านอาหาร - อาหารไทย", size=18, weight="bold", color=BRAND_ORANGE)

    # ---------- Body ----------
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

    # ---------- พื้นหลังไล่สี ----------
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
