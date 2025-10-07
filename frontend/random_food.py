import flet as ft 
import json, os, random, asyncio

BRAND_ORANGE = "#DC7A00"
PHONE_W, PHONE_H = 412, 917


def load_food_data():
    path = os.path.join(os.path.dirname(__file__), "data", "random_food.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)["foods"]


def build_spin_view(page: ft.Page):
    foods = load_food_data()

    # ---------- HEADER ----------
    header_row = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_color=ft.Colors.WHITE,
                on_click=lambda e: page.go("/home"),
            ),
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
        padding=ft.padding.only(left=16, right=16, top=12, bottom=10),
        content=ft.Column(spacing=12, controls=[header_row, search]),
    )

    # ---------- ปุ่มหมวด ----------
    def pill(icon_src: str, label: str, route=None, active=False):
        return ft.GestureDetector(
            on_tap=lambda e: page.go(route) if route else None,
            content=ft.Container(
                bgcolor=ft.Colors.WHITE,
                border_radius=12,
                padding=12,
                width=(PHONE_W - 64) / 2,
                shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.BLACK12),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Image(src=icon_src, width=40, height=40),
                        ft.Text(
                            label,
                            size=14,
                            weight="bold" if active else "normal",
                            color=BRAND_ORANGE if active else ft.Colors.BLACK87,
                        ),
                    ],
                ),
            ),
        )

    top_buttons = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
        controls=[
            pill("star.png", "ร้านเด็ด", route="/highlight"),
            pill("roll.png", "สุ่มอาหาร", active=True),
        ],
    )

    # ---------- ปุ่มฟีเจอร์ ----------
    def feature(icon_src: str, label: str, on_click=None):
        return ft.GestureDetector(
            on_tap=on_click or (lambda e: None),
            content=ft.Container(
                bgcolor=ft.Colors.WHITE,
                border_radius=12,
                padding=10,
                width=(PHONE_W - 64) / 4,
                shadow=ft.BoxShadow(blur_radius=6, color=ft.Colors.BLACK12),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Image(src=icon_src, width=32, height=32),
                        ft.Text(label, size=12),
                    ],
                ),
            ),
        )

    feature_row = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
        controls=[
            feature("ball.png", "กินตามดวง"),
            feature("pin.png", "ร้านใกล้ฉัน"),
            feature("category.png", "หมวดหมู่", on_click=lambda e: page.go("/categories")),
            feature("palette.png", "กินตามสีวัน"),
        ],
    )

    # ---------- กล่องแสดงรูปสุ่ม ----------
    random_image = ft.Image(
        src="photo/placeholder.png",  # รูปเริ่มต้น (สร้างไว้กัน error)
        width=220,
        height=220,
        border_radius=16,
        fit=ft.ImageFit.COVER,
    )
    random_name = ft.Text("", size=18, weight="bold", color=BRAND_ORANGE)
    random_box = ft.Container(
        width=300,
        height=320,
        border_radius=20,
        bgcolor=ft.Colors.WHITE,
        shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.BLACK26),
        alignment=ft.alignment.center,
        padding=15,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            controls=[
                ft.Text("สุ่มอาหารกันเลย!", size=16, weight="bold", color=BRAND_ORANGE),
                random_image,
                random_name,
            ],
        ),
    )

    # ---------- ฟังก์ชันสุ่ม ----------
    async def random_food(e):
        # สุ่มจากข้อมูล JSON
        food = random.choice(foods)
        food_name = food["name"]
        food_image = food["image"]

        # อัปเดตชื่อและรูป
        random_name.value = food_name
        random_image.src = f"photo/{food_image}"
        page.update()

        # เอฟเฟกต์เด้งเบา ๆ
        for scale in [1.0, 1.15, 0.9, 1.0]:
            random_box.scale = ft.Scale(scale)
            random_box.animate_scale = ft.animation.Animation(200, "easeOutBack")
            page.update()
            await asyncio.sleep(0.1)

    # ---------- ปุ่มสุ่ม ----------
    spin_button = ft.Container(
        width=180,
        height=52,
        border_radius=26,
        gradient=ft.LinearGradient(
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=["#FF6B35", "#DC7A00", "#FF8C42"],
        ),
        shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.4, BRAND_ORANGE)),
        alignment=ft.alignment.center,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
            controls=[
                ft.Icon(ft.Icons.CASINO, color=ft.Colors.WHITE, size=24),
                ft.Text("สุ่มเลย !", size=18, weight="bold", color=ft.Colors.WHITE),
            ],
        ),
        on_click=random_food,
    )

    # ---------- Layout ----------
    main_section = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        controls=[random_box, spin_button],
    )

    # ---------- Bottom nav ----------
    def nav_item(icon: str, label: str, route=None, active=False):
        return ft.GestureDetector(
            on_tap=lambda e: page.go(route) if route else None,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Image(src=icon, width=24),
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
                nav_item("home.png", "Home", route="/home"),
                nav_item("history.png", "History"),
                nav_item("review.png", "Review"),
                nav_item("more.png", "More"),
            ],
        ),
    )

    body = ft.Column(
        spacing=12,
        controls=[header, top_buttons, feature_row, main_section, ft.Container(expand=True), bottom_nav],
    )

    # ---------- BG ----------
    bg = ft.Container(
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
        controls=[bg, ft.Container(padding=ft.padding.symmetric(horizontal=12, vertical=10), content=body)],
    )

    return ft.View(
        route="/random",
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
