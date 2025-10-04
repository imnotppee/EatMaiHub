import flet as ft

BRAND_ORANGE = "#DC7A00"
PHONE_W, PHONE_H = 412, 917

# mock data ร้านอาหาร (ยังไม่เชื่อม DB)
thai_foods = [
    {"name": "ผัดไทย คลาสสิค", "rating": "4.6", "address": "ถนนคลองกรุง", "image": "thai1.png"},
    {"name": "ตำถาดซอย byเจ๊อ๊อด", "rating": "4.2", "address": "ลาดกระบัง 11", "image": "thai2.png"},
    {"name": "หมูกอดบ้านฉัน", "rating": "4.7", "address": "ซอยวิมาน ลาดกระบัง 52", "image": "thai3.png"},
]

def categories_view(page: ft.Page) -> ft.View:
    # ---------- Header ----------
    header_row = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color=ft.Colors.WHITE,
                        on_click=lambda e: page.go("/home"),
                    ),
                    ft.Image(src="logo.png", width=36, height=36),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.IconButton(
                icon=ft.Icons.PERSON,
                icon_color=ft.Colors.WHITE,
                on_click=lambda e: page.go("/"),
            ),
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
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[BRAND_ORANGE, "#F6D0A0"],
        ),
        padding=ft.padding.all(12),
        content=ft.Column(spacing=12, controls=[header_row, search]),
    )

    # ---------- Category buttons ----------
    category_buttons = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
        controls=[
            ft.Column([
                ft.Image(src="thai_icon.png", width=64, height=64),
                ft.Text("อาหารไทย", size=12)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Column([
                ft.Image(src="japan_icon.png", width=64, height=64),
                ft.Text("อาหารญี่ปุ่น", size=12)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Column([
                ft.Image(src="fastfood_icon.png", width=64, height=64),
                ft.Text("อาหารฟาสต์ฟู้ด", size=12)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        ],
    )

    # ---------- List ร้านอาหาร ----------
    food_cards = []
    for f in thai_foods:
        food_cards.append(
            ft.Container(
                bgcolor=ft.Colors.WHITE,
                border_radius=12,
                padding=8,
                shadow=ft.BoxShadow(blur_radius=6, color=ft.Colors.BLACK12),
                content=ft.Row(
                    controls=[
                        ft.Image(src=f["image"], width=100, height=80, fit=ft.ImageFit.COVER),
                        ft.Column(
                            spacing=4,
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Text(f"ชื่อร้าน : {f['name']}", size=14, weight="bold"),
                                ft.Text(f"รีวิว : {f['rating']} ดาว", size=12, color=ft.Colors.BLACK54),
                                ft.Text(f"ที่อยู่ : {f['address']}", size=12, color=ft.Colors.BLACK54),
                            ],
                        )
                    ]
                )
            )
        )

    food_list = ft.Column(spacing=10, controls=food_cards)

    # ---------- Bottom nav ----------
    def nav_item(icon: str, label: str, active=False, on_click=None):
        return ft.GestureDetector(
            on_tap=on_click or (lambda e: None),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
                controls=[
                    ft.Image(src=icon, width=24, height=24),
                    ft.Text(label, size=10, color=BRAND_ORANGE if active else ft.Colors.BLACK87),
                ],
            ),
        )

    bottom_nav = ft.Container(
        bgcolor=ft.Colors.WHITE,
        border=ft.border.only(top=ft.BorderSide(1, ft.Colors.BLACK12)),
        padding=10,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                nav_item("HOME.png", "Home", on_click=lambda e: page.go("/home")),
                nav_item("history.png", "History"),
                nav_item("Review.png", "Review"),
                nav_item("More.png", "More"),
            ],
        ),
    )

    # ---------- Body ----------
    body = ft.Column(
        spacing=16,
        controls=[
            header,
            category_buttons,
            ft.Text("อาหารไทย", size=16, weight="bold", color=BRAND_ORANGE),
            food_list,
            ft.Container(expand=True),
            bottom_nav,
        ],
    )

    # ---------- Phone frame ----------
    phone_frame = ft.Stack(
        width=PHONE_W,
        height=PHONE_H,
        controls=[
            ft.Container(
                padding=ft.padding.symmetric(horizontal=12, vertical=10),
                content=body,
            )
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
