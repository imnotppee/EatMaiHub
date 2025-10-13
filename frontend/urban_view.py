import flet as ft
import json
import os

# ---------- ค่าคงที่ ----------
BRAND_ORANGE = "#DC7A00"
PHONE_W, PHONE_H = 412, 917

# ---------- path ของ favorite ----------
FAV_PATH = os.path.join(os.path.dirname(__file__), "data", "favorite.json")


def load_favorites():
    if os.path.exists(FAV_PATH):
        with open(FAV_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_favorites(favorites):
    os.makedirs(os.path.dirname(FAV_PATH), exist_ok=True)
    with open(FAV_PATH, "w", encoding="utf-8") as f:
        json.dump(favorites, f, ensure_ascii=False, indent=2)


def build_urban_view(page: ft.Page) -> ft.View:
    # ---------- โหลดข้อมูลร้าน ----------
    data_path = os.path.join(os.path.dirname(__file__), "data", "urban_data.json")
    if not os.path.exists(data_path):
        raise FileNotFoundError("❌ ไม่พบไฟล์ data/urban_data.json")

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    favorites = load_favorites()

    restaurant_info = {
        "title": data.get("name", "ไม่ระบุชื่อร้าน"),
        "category": data.get("review", ""),
        "time": "3 ตุลาคม 2568 13:40 น.",
        "image": data.get("banner", [""])[0] if data.get("banner") else "",
    }

    # ---------- ตรวจว่าชอบแล้วหรือยัง ----------
    def is_favorite():
        return any(f["title"] == restaurant_info["title"] for f in favorites)

    # ---------- ปุ่มหัวใจ ----------
    heart_icon = ft.IconButton(
        icon=ft.Icons.FAVORITE if is_favorite() else ft.Icons.FAVORITE_BORDER,
        icon_color=BRAND_ORANGE,
        icon_size=28,
    )

    def toggle_favorite(e):
        nonlocal favorites
        if is_favorite():
            favorites = [f for f in favorites if f["title"] != restaurant_info["title"]]
            heart_icon.icon = ft.Icons.FAVORITE_BORDER
        else:
            favorites.append(restaurant_info)
            heart_icon.icon = ft.Icons.FAVORITE
        save_favorites(favorites)
        heart_icon.update()

    heart_icon.on_click = toggle_favorite

    # ---------- Header ----------
    header = ft.Container(
        width=PHONE_W,
        padding=ft.padding.only(left=16, right=16, top=30, bottom=10),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[BRAND_ORANGE, "#F6D0A0"],
        ),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=40,
                    height=40,
                    border_radius=20,
                    bgcolor=ft.Colors.WHITE24,
                    content=ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color=ft.Colors.WHITE,
                        icon_size=22,
                        on_click=lambda e: page.go("/highlight"),
                    ),
                ),
                ft.Image(src="logo.png", width=100, height=80),
                ft.Container(width=36),
            ],
        ),
    )

    # ---------- แบนเนอร์ ----------
    banner_images = data.get("banner", [])
    banner_section = ft.Container(
        width=PHONE_W,
        height=210,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        content=ft.Image(src=banner_images[0] if banner_images else "", fit=ft.ImageFit.COVER),
    )

    # ---------- ข้อมูลร้าน ----------
    info_section = ft.Container(
        padding=ft.padding.symmetric(horizontal=16, vertical=10),
        content=ft.Column(
            spacing=4,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(
                            data.get("name", ""),
                            size=18,
                            weight=ft.FontWeight.BOLD,
                        ),
                        heart_icon,
                    ],
                ),
                ft.Text(f"รีวิว : {data.get('review', '-')}", size=14, color=ft.Colors.BLACK87),
                ft.Text(f"ที่อยู่ : {data.get('address', '-')}", size=14, color=ft.Colors.BLACK87),
                ft.Divider(color=ft.Colors.BLACK12),
            ],
        ),
    )

    # ---------- หัวข้อเมนู ----------
    menu_title = ft.Container(
        padding=ft.padding.only(left=16, bottom=6),
        content=ft.Text(
            "เมนูแนะนำ",
            size=16,
            weight=ft.FontWeight.BOLD,
            color=BRAND_ORANGE,
        ),
    )

    # ---------- การ์ดเมนู ----------
    def menu_card(item):
        return ft.Container(
            width=(PHONE_W - 64) / 2,
            height=190,
            bgcolor=ft.Colors.WHITE,
            border_radius=14,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12),
            padding=ft.padding.all(8),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                controls=[
                    ft.Container(
                        height=110,
                        width=(PHONE_W - 84) / 2,
                        border_radius=10,
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                        content=ft.Image(src=item.get("image", ""), fit=ft.ImageFit.COVER),
                    ),
                    ft.Text(
                        item.get("name", ""),
                        size=13,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK87,
                        weight=ft.FontWeight.W_500,
                    ),
                ],
            ),
        )

    menus = data.get("menus", [])
    menu_grid = ft.Row(
        wrap=True,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=16,
        run_spacing=16,
        controls=[menu_card(m) for m in menus],
    )

    # ---------- Bottom Navigation ----------
    def nav_item(icon: str, label: str, route=None, active=False):
        return ft.GestureDetector(
            on_tap=lambda e: page.go(route) if route else None,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
                controls=[
                    ft.Image(src=icon, width=26, height=26, fit=ft.ImageFit.CONTAIN),
                    ft.Text(
                        label,
                        size=10,
                        color=BRAND_ORANGE if active else ft.Colors.BLACK87,
                    ),
                ],
            ),
        )

    bottom_nav = ft.Container(
        bgcolor=ft.Colors.WHITE,
        border=ft.border.only(top=ft.BorderSide(1, ft.Colors.BLACK12)),
        height=65,
        padding=10,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                nav_item("home.png", "Home", route="/home"),
                nav_item("heart.png", "Favorite", route="/favorite"),
                nav_item("review.png", "Review", route="/review"),
                nav_item("more.png", "More", route="/more"),
            ],
        ),
    )

    # ---------- Layout หลัก ----------
    layout = ft.Stack(
        controls=[
            ft.Column(
                expand=True,
                scroll=ft.ScrollMode.ALWAYS,
                controls=[
                    header,
                    banner_section,
                    info_section,
                    menu_title,
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=16),
                        alignment=ft.alignment.center,
                        content=menu_grid,
                    ),
                    ft.Container(height=80),  # เผื่อพื้นที่ให้ bottom nav
                ],
            ),
            ft.Container(bottom=0, left=0, right=0, content=bottom_nav),
        ],
    )

    # ---------- Frame ----------
    return ft.View(
        route="/urban",
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
