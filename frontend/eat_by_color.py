import flet as ft
import json, os

BRAND_ORANGE = "#DC7A00"
PHONE_W, PHONE_H = 412, 917


def load_color_data():
    path = os.path.join(os.path.dirname(__file__), "data", "color_menus.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_color_view(page: ft.Page) -> ft.View:
    color_data = load_color_data()

    # สีและชื่อวัน
    day_colors = [
        ("Sunday", "อาทิตย์", "#FF4D4D"),
        ("Monday", "จันทร์", "#FFD93D"),
        ("Tuesday", "อังคาร", "#FF99CC"),
        ("Wednesday", "พุธ", "#00C851"),
        ("Thursday", "พฤหัส", "#FF8C00"),
        ("Friday", "ศุกร์", "#00BFFF"),
        ("Saturday", "เสาร์", "#9B59B6")
    ]

    selected_day = ft.Ref[str]()
    menu_container = ft.Ref[ft.Row]()

    # ---------------- Header ----------------
    def header_section():
        top_row = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color=ft.Colors.WHITE,
                    on_click=lambda e: page.go("/home")
                ),
                ft.Image(src="logo.png", width=40, height=40),
                ft.IconButton(
                    icon=ft.Icons.PERSON,
                    icon_color=ft.Colors.WHITE,
                    on_click=lambda e: page.go("/")
                )
            ]
        )

        search_box = ft.TextField(
            hint_text="ค้นหาร้าน / เมนู",
            prefix_icon=ft.Icons.SEARCH,
            border_radius=20,
            border_color=BRAND_ORANGE,
            filled=True,
            fill_color=ft.Colors.WHITE,
            height=42
        )

        return ft.Container(
            width=PHONE_W,
            padding=ft.padding.only(left=16, right=16, top=12, bottom=12),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[BRAND_ORANGE, "#F6D0A0"]
            ),
            content=ft.Column(spacing=10, controls=[top_row, search_box])
        )

    # ---------------- แถบสีของวัน ----------------
    def color_bar_section():
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=0,
            controls=[
                ft.Container(
                    expand=True,
                    height=100,
                    bgcolor=color,
                    content=ft.Text(
                        eng_day,
                        color=ft.Colors.WHITE,
                        rotate=ft.Rotate(angle=-1.5708),
                        size=11,  # ✅ ลดขนาดฟอนต์ลง
                        text_align=ft.TextAlign.CENTER,
                        weight=ft.FontWeight.BOLD
                    ),
                    alignment=ft.alignment.center,
                    ink=True,
                    on_click=lambda e, d=thai_day: show_menu(d)
                )
                for eng_day, thai_day, color in day_colors
            ]
        )

    # ---------------- แสดงเมนู ----------------
    def show_menu(day_thai):
        selected_day.current = day_thai
        menus = color_data.get(day_thai_color_key(day_thai), [])
        menu_container.current.controls.clear()

        if not menus:
            page.update()
            return

        for item in menus:
            menu_container.current.controls.append(
                ft.Container(
                    width=160,
                    height=180,
                    bgcolor=ft.Colors.WHITE,
                    padding=10,
                    border_radius=16,
                    shadow=ft.BoxShadow(blur_radius=8, spread_radius=1, color="#dddddd"),
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Image(src=item["image"], width=100, height=100, fit=ft.ImageFit.COVER),
                            ft.Text(item["name"], size=14, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
                        ],
                    ),
                )
            )
        page.update()

    def day_thai_color_key(day_thai):
        mapping = {
            "อาทิตย์": "red",
            "จันทร์": "yellow",
            "อังคาร": "pink",
            "พุธ": "green",
            "พฤหัส": "orange",
            "ศุกร์": "blue",
            "เสาร์": "purple"
        }
        return mapping.get(day_thai, "")

    menu_container.current = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
        wrap=True,
        controls=[]
    )

    # ---------------- Bottom Nav ----------------
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
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                nav_item("home.png", "Home", route="/home"),
                nav_item("heart.png", "favorite", route="/favorite"),
                nav_item("review.png", "Review"),
                nav_item("more.png", "More"),
            ],
        ),
    )

    # ---------------- Layout ----------------
    body = ft.Column(
        expand=True,
        controls=[
            ft.Text(
                "กินตามสีวัน",  # ✅ ข้อความสั้นตามภาพ
                size=16,
                weight=ft.FontWeight.BOLD,
                color=BRAND_ORANGE,
                text_align=ft.TextAlign.CENTER
            ),
            color_bar_section(),
            ft.Divider(),
            menu_container.current,
            ft.Container(expand=True)  # ✅ ดัน bottom nav ไปล่างสุด
        ],
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    phone_frame = ft.Container(
        width=PHONE_W,
        height=PHONE_H,
        bgcolor=ft.Colors.WHITE,
        content=ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                header_section(),
                ft.Container(
                    expand=True,
                    alignment=ft.alignment.top_center,
                    padding=ft.padding.symmetric(horizontal=12, vertical=10),
                    content=body
                ),
                bottom_nav,  # ✅ อยู่ล่างสุดแน่นอน
            ]
        ),
    )

    # ---------------- Return View ----------------
    return ft.View(
        route="/color",
        padding=0,
        controls=[
            ft.Container(
                expand=True,
                bgcolor=ft.Colors.BLACK,
                alignment=ft.alignment.center,
                content=phone_frame
            )
        ]
    )
