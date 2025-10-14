import flet as ft
import random, time, requests
from flet import Colors


BRAND_ORANGE = "#DC7A00"
PHONE_W, PHONE_H = 412, 917


# ---------- โหลดข้อมูลจาก Backend ----------
def load_food_data():
    api_url = "http://127.0.0.1:5001/api/foods"  # URL ของ backend Flask
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            print("✅ ดึงข้อมูลจาก backend สำเร็จ")
            return response.json()
        else:
            print("⚠️ ดึงข้อมูลไม่สำเร็จ:", response.status_code)
            return []
    except Exception as e:
        print("❌ เกิดข้อผิดพลาดในการดึงข้อมูล:", e)
        return []


# ---------- หน้าสุ่มอาหาร ----------
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

    header = ft.Container(
        padding=ft.padding.only(left=16, right=16, top=12, bottom=10),
        content=header_row,
    )

    # ---------- กล่องแสดงสุ่ม ----------
    random_image = ft.Image(
        src="qqq.jpg",
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
        width=310,
        height=350,
        border_radius=20,
        bgcolor=ft.Colors.WHITE,
        shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK26),
        alignment=ft.alignment.center,
        padding=20,
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
        if not foods:
            random_name.value = "⚠️ ไม่มีข้อมูลอาหารในระบบ"
            page.update()
            return

        total_rounds = 10

        for i in range(5):
            temp = random.choice(foods)
            random_image.src = f"frontend/photo/menu_bun1.webp/{temp['image']}"
            random_name.value = temp["name"]
            page.update()
            time.sleep(0.25)

        for i in range(5, total_rounds):
            temp = random.choice(foods)
            random_image.src = f"photo/{temp['image']}"
            random_name.value = temp["name"]
            page.update()
            time.sleep(0.25 + (i - 4) * 0.1)

        final_food = random.choice(foods)
        random_image.src = f"photo/{final_food['image']}"
        random_name.value = final_food["name"]
        page.update()

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
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=16)),
                                on_click=lambda e: [remove_popup(), on_spin(e)],
                            ),
                            ft.ElevatedButton(
                                text="ตกลง",
                                bgcolor="#888888",
                                color=ft.Colors.WHITE,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=16)),
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

        def remove_popup():
            if overlay in phone_frame.controls:
                phone_frame.controls.remove(overlay)
                page.update()

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
        shadow=ft.BoxShadow(
            blur_radius=15, color=ft.Colors.with_opacity(0.4, BRAND_ORANGE)
        ),
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
                        content=ft.Image(
                            src=icon, width=28, height=28, fit=ft.ImageFit.CONTAIN
                        ),
                        padding=ft.padding.only(top=2, bottom=2),
                    ),
                    ft.Text(label, size=10, color=BRAND_ORANGE if active else ft.Colors.BLACK87),
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
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[header, main_section, bottom_nav],            
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
