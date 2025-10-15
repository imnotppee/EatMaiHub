import flet as ft
import requests

BRAND_ORANGE = "#DC7A00"
PHONE_W, PHONE_H = 412, 917

API_URL = "http://127.0.0.1:8000/api/favorites"

def build_favorite_view(page: ft.Page) -> ft.View:
    page.window_width = PHONE_W
    page.window_height = PHONE_H
    page.window_resizable = False
    page.bgcolor = ft.Colors.WHITE

    # ---------- โหลดข้อมูลรายการโปรด ----------
    try:
        res = requests.get(API_URL, timeout=10)
        res.raise_for_status()
        favorites = res.json()
    except Exception as e:
        print("⚠️ โหลดรายการโปรดไม่สำเร็จ:", e)
        favorites = []

    # แปลงเป็นเซตของ restaurant_id เพื่อเช็กสถานะง่าย
    favorite_ids = {f["restaurant_id"] for f in favorites}

    # ---------- ฟังก์ชัน toggle favorite ----------
    def toggle_favorite(item):
        rest_id = item["restaurant_id"]
        if rest_id in favorite_ids:
            # ลบออก
            try:
                res = requests.delete(f"{API_URL}/{rest_id}", timeout=5)
                if res.status_code == 200:
                    favorite_ids.remove(rest_id)
                    page.snack_bar = ft.SnackBar(
                        ft.Text("ลบออกจากรายการโปรดแล้ว", color="white"),
                        bgcolor="red"
                    )
            except Exception as e:
                print("❌ ลบไม่สำเร็จ:", e)
        else:
            # เพิ่มเข้า
            try:
                res = requests.post(API_URL, json={"restaurant_id": rest_id}, timeout=5)
                if res.status_code in (200, 201):
                    favorite_ids.add(rest_id)
                    page.snack_bar = ft.SnackBar(
                        ft.Text("เพิ่มเข้ารายการโปรดแล้ว", color="white"),
                        bgcolor=BRAND_ORANGE
                    )
            except Exception as e:
                print("❌ เพิ่มไม่สำเร็จ:", e)

        page.snack_bar.open = True
        page.update()

    # ---------- การ์ดแต่ละรายการ ----------
    def favorite_card(item):
        is_fav = item["restaurant_id"] in favorite_ids
        heart_icon = ft.IconButton(
            icon=ft.Icons.FAVORITE if is_fav else ft.Icons.FAVORITE_BORDER,
            icon_color=BRAND_ORANGE if is_fav else ft.Colors.BLACK45,
            on_click=lambda e: toggle_favorite(item),
        )

        return ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            padding=10,
            margin=ft.margin.only(bottom=10),
            shadow=ft.BoxShadow(blur_radius=6, color=ft.Colors.BLACK12),
            content=ft.Row(
                spacing=10,
                controls=[
                    ft.Image(
                        src=item["image"],
                        width=90,
                        height=90,
                        border_radius=10,
                        fit=ft.ImageFit.COVER,
                    ),
                    ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        expand=True,
                        controls=[
                            ft.Text(item["title"], size=14, weight=ft.FontWeight.BOLD),
                            ft.Text(item["time"], size=11, color=ft.Colors.BLACK54),
                        ],
                    ),
                    heart_icon,
                ],
            ),
        )

    # ---------- ส่วนแสดงผล ----------
    body = (
        ft.Column([favorite_card(f) for f in favorites])
        if favorites
        else ft.Text("ยังไม่มีรายการโปรด", color=ft.Colors.BLACK54)
    )

    return ft.View(
        route="/favorite",
        controls=[
            ft.AppBar(
                title=ft.Text("รายการโปรด", size=18, weight=ft.FontWeight.BOLD),
                bgcolor=BRAND_ORANGE,
                color=ft.Colors.WHITE,
                center_title=True,
                elevation=2,
            ),
            ft.Container(padding=10, content=body, expand=True),
        ],
    )
