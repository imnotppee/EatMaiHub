import flet as ft
from flet import Icons, Colors

BRAND_ORANGE = "#DC7A00"
PHONE_W, PHONE_H = 412, 917


def build_home_view(page: ft.Page) -> ft.View:
    # ---------- Header (แถบส้มด้านบน) ----------
    header_row = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Image(src="logo.png", width=36, height=36),
                    ft.Container(width=8),
                    ft.Text("Hi user", size=16, color=Colors.WHITE),
                ],
            ),
            ft.IconButton(
                icon=Icons.PERSON,
                icon_color=Colors.WHITE,
                on_click=lambda e: page.go("/"),  # ไปหน้า Login ภายหลัง
            ),
        ],
    )

    search = ft.TextField(
        hint_text="ค้นหาร้าน / เมนู",
        prefix_icon=Icons.SEARCH,
        border_radius=20,
        border_color=BRAND_ORANGE,
        filled=True,
        fill_color=Colors.WHITE,
        height=44,
    )

    header = ft.Container(
        padding=ft.padding.only(left=16, right=16, top=12, bottom=16),
        content=ft.Column(spacing=12, controls=[header_row, search]),
    )

    # ---------- ปุ่มบน 2 อัน ----------
    def pill(icon_src: str, label: str):
        return ft.Container(
            bgcolor=Colors.WHITE,              # การ์ดพื้นขาว
            border_radius=12,
            padding=12,
            width=(PHONE_W - 64) / 2,
            shadow=ft.BoxShadow(blur_radius=10, spread_radius=0, color=Colors.BLACK12),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=6,
                controls=[ft.Image(src=icon_src, width=40, height=40), ft.Text(label, size=14)],
            ),
        )

    top_buttons = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
        controls=[pill("star.png", "ร้านเด็ด"), pill("roll.png", "สุ่มอาหาร")],
    )

    # ---------- แถว feature 4 อัน ----------
    def feature(icon_src: str, label: str):
        return ft.Container(
            bgcolor=Colors.WHITE,              # กล่องเล็กพื้นขาว
            border_radius=12,
            padding=10,
            width=(PHONE_W - 64) / 4,
            shadow=ft.BoxShadow(blur_radius=8, color=Colors.BLACK12),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=6,
                controls=[ft.Image(src=icon_src, width=32, height=32), ft.Text(label, size=12)],
            ),
        )

    feature_row = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
        controls=[
            feature("ball.png", "กินตามดวง"),
            feature("pin.png", "ร้านใกล้ฉัน"),
            feature("Category.png", "หมวดหมู่"),
            feature("palette.png", "กินตามสีวัน"),
        ],
    )

    # ---------- หัวข้อร้านเด็ด + ภาพใหญ่ ----------
    highlight_title = ft.Row(
        alignment=ft.MainAxisAlignment.START,
        controls=[
            ft.Image(src="star.png", width=20, height=20),
            ft.Container(width=6),
            ft.Text("ร้านเด็ด", size=16, weight=ft.FontWeight.BOLD, color=BRAND_ORANGE),
        ],
    )

    highlight_image = ft.Container(
        width=PHONE_W - 24,
        height=180,
        border_radius=16,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        shadow=ft.BoxShadow(blur_radius=12, color=Colors.BLACK26),
        content=ft.Image(src="urban.png", fit=ft.ImageFit.COVER),
    )

    # ---------- กินตามดวงวันนี้ (การ์ดอาหารพื้นขาว) ----------
    card_w = 120

    def food_card(img: str, title: str, subtitle: str):
        return ft.Container(
            width=card_w,
            bgcolor=Colors.WHITE,
            border_radius=12,
            padding=8,
            shadow=ft.BoxShadow(blur_radius=8, color=Colors.BLACK12),
            content=ft.Column(
                spacing=6,
                controls=[
                    ft.Container(
                        height=80,
                        border_radius=10,
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                        content=ft.Image(src=img, fit=ft.ImageFit.COVER),
                    ),
                    ft.Text(title, size=12, weight=ft.FontWeight.W_600),
                    ft.Text(subtitle, size=10, color=Colors.BLACK54),
                ],
            ),
        )

    horo_title = ft.Row(
        alignment=ft.MainAxisAlignment.START,
        controls=[
            ft.Image(src="ball.png", width=22, height=22),
            ft.Container(width=6),
            ft.Text("กินตามดวงวันนี้", size=16, weight=ft.FontWeight.BOLD, color=BRAND_ORANGE),
        ],
    )

    horo_scroller = ft.Row(
        scroll=ft.ScrollMode.ALWAYS,
        controls=[
            food_card("food1.png", "เกิดวันจันทร์", "กินข้าวมันไก่"),
            food_card("food2.png", "เกิดวันอังคาร", "กินกะเพราหมูสับ"),
            food_card("food3.png", "เกิดวันพุธ", "กินไก่ทอด"),
        ],
    )

    # ---------- Bottom nav (มี on_tap ให้ครบ ป้องกัน warning) ----------
    def nav_item(icon: str, label: str, active=False, on_click=None):
        return ft.GestureDetector(
            on_tap=on_click or (lambda e: None),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
                controls=[
                    ft.Image(src=icon, width=24, height=24),
                    ft.Text(label, size=10, color=BRAND_ORANGE if active else Colors.BLACK87),
                ],
            ),
        )

    bottom_nav = ft.Container(
        bgcolor=Colors.WHITE,
        border=ft.border.only(top=ft.BorderSide(1, Colors.BLACK12)),
        padding=10,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                nav_item("HOME.png", "Home", active=True),
                nav_item("history.png", "History"),
                nav_item("Review.png", "Review"),
                nav_item("More.png", "More"),
            ],
        ),
    )

    # ---------- เนื้อหาในกรอบแอป ----------
    body = ft.Column(
        spacing=12,
        controls=[
            header,
            top_buttons,
            feature_row,      # <= ถึงตรงนี้คือ “ครึ่งหน้าจอแรก”
            highlight_title,
            highlight_image,
            horo_title,
            horo_scroller,
            ft.Container(expand=True),
            bottom_nav,
        ],
    )

    # ไล่สีส้มลงมาถึง “feature_row”
    orange_gradient_bg = ft.Container(
        width=PHONE_W,
        height=340,  # ปรับให้ครอบคลุมถึงแถว "กินตามดวง"
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[BRAND_ORANGE, "#F6D0A0", "#FFFFFFFF"],  # ส้ม -> อ่อน -> ขาว
            stops=[0.0, 0.6, 1.0],
        ),
    )

    # ซ้อน layer: พื้นไล่สี + เนื้อหา
    phone_frame = ft.Stack(
        width=PHONE_W,
        height=PHONE_H,
        controls=[
            orange_gradient_bg,                    # ชั้นล่าง: ไล่สี
            ft.Container(                          # ชั้นบน: เนื้อหา
                padding=ft.padding.symmetric(horizontal=12, vertical=10),
                content=body,
            ),
        ],
    )

    # กลางจอ / พื้นหลังนอกแอป = ดำสนิท
    return ft.View(
        route="/home",
        padding=0,
        controls=[
            ft.Container(
                expand=True,
                bgcolor=Colors.BLACK,               # พื้นหลังนอกแอปเป็นดำ
                alignment=ft.alignment.center,
                content=ft.Container(
                    width=PHONE_W,
                    height=PHONE_H,
                    bgcolor=Colors.WHITE,           # พื้นในแอปยังขาว
                    content=phone_frame,
                ),
            )
        ],
    )
