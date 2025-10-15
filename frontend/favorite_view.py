import flet as ft
import requests
import time
import threading

# ---------- ค่าคงที่ ----------
BRAND_ORANGE = "#DC7A00"
PHONE_W, PHONE_H = 412, 917
API_BASE_URL = "http://127.0.0.1:8000/api/favorites"  # ✅ URL backend ของคุณ

# ---------- โหลดข้อมูลจาก Backend ----------
def load_favorites():
    try:
        res = requests.get(API_BASE_URL)
        if res.status_code == 200:
            return res.json()
        else:
            print(f"⚠️ Error {res.status_code}: {res.text}")
            return []
    except Exception as e:
        print("❌ ไม่สามารถเชื่อมต่อ backend ได้:", e)
        return []

# ---------- ลบข้อมูลรายการโปรดใน backend ----------
def delete_favorite_api(fav_id: int):
    try:
        res = requests.delete(f"{API_BASE_URL}/{fav_id}")
        if res.status_code == 200:
            print("🗑️ ลบสำเร็จ:", fav_id)
        else:
            print("⚠️ ลบไม่สำเร็จ:", res.text)
    except Exception as e:
        print("❌ error ในการลบ:", e)

# ---------- UI หลัก ----------
def build_favorite_view(page: ft.Page) -> ft.View:
    favorites = load_favorites()

    # ---------- Header ----------
    header = ft.Container(
        width=PHONE_W,
        height=180,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[BRAND_ORANGE, "#F6D0A0"],
        ),
        border_radius=ft.border_radius.only(bottom_left=40, bottom_right=40),
        padding=ft.padding.only(left=16, right=16, top=36, bottom=16),
        content=ft.Column(
            spacing=16,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            icon_color=ft.Colors.WHITE,
                            icon_size=24,
                            on_click=lambda e: page.go("/home"),
                        ),
                        ft.Image(src="logo.png", width=90, height=70),
                        ft.IconButton(
                            icon=ft.Icons.PERSON,
                            icon_color=ft.Colors.WHITE,
                            icon_size=24,
                        ),
                    ],
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(
                            "รายการโปรด",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE,
                        ),
                        ft.Container(
                            border=ft.border.all(1, ft.Colors.WHITE),
                            border_radius=25,
                            padding=ft.padding.symmetric(horizontal=16, vertical=4),
                            content=ft.Text("ทั้งหมด", size=12, color=ft.Colors.WHITE),
                        ),
                    ],
                ),
            ],
        ),
    )

    # ---------- การ์ดโปรด ----------
    def favorite_card(item):
        heart_icon = ft.Icon(
            name=ft.Icons.FAVORITE,  # หัวใจเต็ม
            color=BRAND_ORANGE,
            size=26,
        )

        card = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=16,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12),
            padding=12,
            margin=ft.margin.only(bottom=14),
            opacity=1,
        )

        # เมื่อกดหัวใจ → จางหาย + ลบออกจาก backend
        def remove_favorite(e):
            def fade():
                for i in range(10, -1, -1):
                    card.opacity = i / 10
                    page.update()
                    time.sleep(0.02)

                delete_favorite_api(item.get("fav_id"))
                page.go("/favorite")  # โหลดหน้าใหม่หลังลบเสร็จ

            threading.Thread(target=fade, daemon=True).start()

        card.content = ft.Row(
            spacing=14,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=100,
                    height=100,
                    border_radius=12,
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    content=ft.Image(
                        src=item.get("image", "default.png"),
                        fit=ft.ImageFit.COVER,
                    ),
                ),
                ft.Column(
                    alignment=ft.MainAxisAlignment.START,
                    spacing=6,
                    expand=True,
                    controls=[
                        ft.Text(
                            item.get("name", "ไม่ระบุ"),
                            size=15,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLACK,
                        ),
                        ft.Text(item.get("location", ""), size=13, color=ft.Colors.BLACK54),
                        ft.Text(f"User ID: {item.get('user_id', '')}", size=12, color=ft.Colors.BLACK54),
                    ],
                ),
                ft.GestureDetector(on_tap=remove_favorite, content=heart_icon),
            ],
        )
        return card

    # ---------- ถ้าไม่มีรายการ ----------
    if not favorites:
        fav_list = ft.Container(
            alignment=ft.alignment.center,
            height=500,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
                controls=[
                    ft.Icon(name=ft.Icons.FAVORITE_BORDER, size=60, color=ft.Colors.BLACK45),
                    ft.Text("ยังไม่มีรายการโปรด", size=14, color=ft.Colors.BLACK54),
                ],
            ),
        )
    else:
        fav_list = ft.Column(spacing=10, controls=[favorite_card(f) for f in favorites])

    scroll_area = ft.Container(
        padding=ft.padding.symmetric(horizontal=16, vertical=10),
        content=fav_list,
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
                nav_item("heart.png", "Favorite", route="/favorite", active=True),
                nav_item("review.png", "Review", route="/review"),
                nav_item("more.png", "More", route="/more"),
            ],
        ),
    )

    # ---------- Layout ----------
    layout = ft.Stack(
        controls=[
            ft.Column(
                expand=True,
                scroll=ft.ScrollMode.ALWAYS,
                controls=[header, scroll_area, ft.Container(height=80)],
            ),
            ft.Container(bottom=0, left=0, right=0, content=bottom_nav),
        ],
    )

    return ft.View(
        route="/favorite",
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
