import flet as ft
import json
import os
import requests

# ---------- ค่าคงที่ ----------
BRAND_ORANGE = "#DC7A00"
PHONE_W, PHONE_H = 412, 917
FAV_PATH = os.path.join(os.path.dirname(__file__), "data", "favorite.json")
API_URL = "http://127.0.0.1:8000/api/restaurants"  # ✅ Backend API

# ---------- โหลด / บันทึก Favorites ----------
def load_favorites():
    if os.path.exists(FAV_PATH):
        with open(FAV_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_favorites(favorites):
    os.makedirs(os.path.dirname(FAV_PATH), exist_ok=True)
    with open(FAV_PATH, "w", encoding="utf-8") as f:
        json.dump(favorites, f, ensure_ascii=False, indent=2)


# ---------- View หลัก ----------
def categories_view(page: ft.Page) -> ft.View:
    current_category = "อาหารไทย"
    favorites = load_favorites()

    # ---------- Header ----------
    header_row = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_color=ft.Colors.WHITE,
                on_click=lambda e: page.go("/home"),
            ),
            ft.Image(src="logo.png", width=80, height=36),
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

    # ---------- สร้างการ์ดร้านอาหาร + ปุ่ม Favorite ----------
    def build_food_list(food_items):
        cards = []
        for f in food_items:
            is_fav = any(fav.get("name") == f.get("name") for fav in favorites)
            heart_icon = ft.IconButton(
                icon=ft.Icons.FAVORITE if is_fav else ft.Icons.FAVORITE_BORDER,
                icon_color=BRAND_ORANGE,
                icon_size=24,
            )

            def toggle_favorite(e, food=f, heart=heart_icon):
                current_favorites = load_favorites()
                if any(fav.get("name") == food["name"] for fav in current_favorites):
                    current_favorites = [fav for fav in current_favorites if fav.get("name") != food["name"]]
                    heart.icon = ft.Icons.FAVORITE_BORDER
                else:
                    current_favorites.append({
                        "name": food["name"],
                        "image": food.get("image", ""),
                        "location": food.get("location", ""),
                        "rating": food.get("rating", ""),
                    })
                    heart.icon = ft.Icons.FAVORITE
                save_favorites(current_favorites)
                heart.update()

            heart_icon.on_click = toggle_favorite

            card = ft.Container(
                bgcolor=ft.Colors.WHITE,
                border_radius=22,
                padding=12,
                margin=ft.margin.symmetric(vertical=8, horizontal=8),
                shadow=ft.BoxShadow(
                    blur_radius=10,
                    spread_radius=1,
                    color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                ),
                content=ft.Row(
                    spacing=14,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            width=110,
                            height=100,
                            border_radius=12,
                            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                            content=ft.Image(
                                src=f.get("image", "default.png"),
                                fit=ft.ImageFit.COVER,
                            ),
                        ),
                        ft.Column(
                            alignment=ft.MainAxisAlignment.START,
                            spacing=4,
                            expand=True,
                            controls=[
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        ft.Text(
                                            f.get("name", "-"),
                                            size=14,
                                            weight="bold",
                                            color=ft.Colors.BLACK87,
                                            width=180,
                                            max_lines=1,
                                            overflow="ellipsis",
                                        ),
                                        heart_icon,
                                    ],
                                ),
                                ft.Text(
                                    f"รีวิว : {f.get('rating', '4.5')} ดาว",
                                    size=12,
                                    color=ft.Colors.BLACK87,
                                ),
                                ft.Text(
                                    f.get("location", "-"),
                                    size=12,
                                    color=ft.Colors.BLACK54,
                                ),
                            ],
                        ),
                    ],
                ),
            )
            cards.append(card)
        return cards

    food_list_column = ft.Column(spacing=12, scroll=ft.ScrollMode.AUTO, expand=True)

    # ---------- โหลดข้อมูลจาก Backend ----------
    def load_restaurants(category):
        nonlocal current_category
        current_category = category
        try:
            res = requests.get(API_URL)
            res.raise_for_status()
            data = res.json()
        except Exception as ex:
            print("❌ Error fetching data:", ex)
            data = []

        food_list_column.controls.clear()
        food_list_column.controls.extend(build_food_list(data))
        title.value = f"ร้านอาหาร - {category}"

        for btn in category_buttons.controls:
            btn.content.controls[1].color = BRAND_ORANGE if btn.data == category else ft.Colors.BLACK87
            btn.content.controls[1].weight = "bold" if btn.data == category else "normal"
        page.update()

    # ---------- ปุ่มหมวด ----------
    def category_card(img: str, label: str, active=False):
        return ft.GestureDetector(
            data=label,
            on_tap=lambda e: load_restaurants(label),
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

    # ---------- Layout ----------
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

    # ---------- โหลดข้อมูลเริ่มต้น ----------
    load_restaurants(current_category)

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