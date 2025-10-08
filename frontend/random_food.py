import flet as ft
import json, os, random, time
from flet import Colors


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

    # ---------- กล่องแสดงสุ่ม ----------
    random_image = ft.Image(
        src="photo/qqq.jpg",
        width=220,
        height=220,
        border_radius=20,
        fit=ft.ImageFit.COVER,
    )

    random_name = ft.Text(
        "ยังไม่ได้สุ่มนะ ลองกดปุ่มด้านล่างเลย!",
        size=16,
        weight="bold",
        color=BRAND_ORANGE,
        text_align=ft.TextAlign.CENTER,
    )

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
    def on_spin(e):
        total_rounds = 10

        # หมุนเร็ว 5 ครั้งแรก
        for i in range(5):
            temp = random.choice(foods)
            random_image.src = f"photo/{temp['image']}"
            random_name.value = temp["name"]
            page.update()
            time.sleep(0.3)

        # หมุนช้าลง 5 ครั้งหลัง
        for i in range(5, total_rounds):
            temp = random.choice(foods)
            random_image.src = f"photo/{temp['image']}"
            random_name.value = temp["name"]
            page.update()
            time.sleep(0.3 + (i - 4) * 0.1)

        # เมนูสุดท้ายจริง
        final_food = random.choice(foods)
        random_image.src = f"photo/{final_food['image']}"
        random_name.value = final_food["name"]
        page.update()

        # ---------- popup ----------
        popup = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=20,
            width=280,
            height=360,
            padding=20,
            shadow=ft.BoxShadow(blur_radius=25, color=ft.Colors.BLACK26),
            alignment=ft.alignment.center,
            margin=ft.margin.only(top=80),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
                controls=[
                    ft.Text("ผลการสุ่มอาหาร", size=18, weight="bold", color=BRAND_ORANGE),
                    ft.Image(
                        src=f"photo/{final_food['image']}",
                        width=180,
                        height=180,
                        border_radius=12,
                        fit=ft.ImageFit.COVER,
                    ),
                    ft.Text(final_food["name"], size=14, weight="bold", color=ft.Colors.BLACK),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        controls=[
                            ft.ElevatedButton(
                                text="สุ่มอีกครั้ง",
                                bgcolor=BRAND_ORANGE,
                                color=ft.Colors.WHITE,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=16)
                                ),
                                on_click=lambda e: [remove_popup(), on_spin(e)],
                            ),
                            ft.ElevatedButton(
                                text="ตกลง",
                                bgcolor="#888888",
                                color=ft.Colors.WHITE,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=16)
                                ),
                                on_click=lambda e: remove_popup(),
                            ),
                        ],
                    ),
                ],
            ),
        )

        overlay = ft.Container(
            width=PHONE_W,
            height=PHONE_H,
            alignment=ft.alignment.center,
            content=popup,
        )

        # ---------- ฟังก์ชันลบ popup ----------
        def remove_popup():
            if overlay in phone_frame.controls:
                phone_frame.controls.remove(overlay)
                page.update()

        # เพิ่ม popup ลงไป (เช็กไม่ให้ซ้ำ)
        if overlay not in phone_frame.controls:
            phone_frame.controls.append(overlay)
        page.update()






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
        on_click=on_spin,
    )

    # ---------- ส่วนกลาง ----------
    main_section = ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=25,
            controls=[random_box, spin_button],
        ),
    )

        # ---------- Bottom nav ----------
    def nav_item(icon: str, label: str, route=None, active=False):
        return ft.GestureDetector(
            on_tap=lambda e: page.go(route) if route else None,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
                controls=[
                    ft.Container(
                        content=ft.Image(src=icon, width=28, height=28, fit=ft.ImageFit.CONTAIN),
                        padding=ft.padding.only(top=2, bottom=2),
                    ),
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
        border=ft.border.only(top=ft.BorderSide(1, Colors.BLACK12)),
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


    # ---------- Layout รวม ----------
    body = ft.Column(
        expand=True,
        controls=[
            header,
            top_buttons,
            feature_row,
            main_section,
            bottom_nav,
        ],
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
        controls=[
            bg,
            ft.Container(
                padding=ft.padding.symmetric(horizontal=12, vertical=10),
                content=body,
            ),
        ],
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
