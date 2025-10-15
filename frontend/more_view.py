import flet as ft

# ---------- ค่าคงที่ ----------
BRAND_ORANGE = "#DC7A00"
PHONE_W, PHONE_H = 412, 917


def build_more_view(page: ft.Page) -> ft.View:
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
                # ✅ บรรทัดบนสุด (ลูกศรกลับ + โลโก้ + ไอคอน user)
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,         # 🔙 ปุ่มลูกศร
                            icon_color=ft.Colors.WHITE,
                            icon_size=24,
                            on_click=lambda e: page.go("/home"),  # ✅ กลับหน้า home เหมือน favorite
                        ),
                        ft.Image(src="logo.png", width=90, height=70),
                        ft.IconButton(
                            icon=ft.Icons.PERSON,
                            icon_color=ft.Colors.WHITE,
                            icon_size=24,
                        ),
                    ],
                ),
                # ✅ ชื่อหัวข้อ
                ft.Text(
                    "เพิ่มเติม (More)",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
            ],
        ),
    )

    # ---------- ปุ่มเมนูย่อย ----------
    def menu_item(title: str):
        return ft.GestureDetector(
            on_tap=lambda e: page.open(ft.SnackBar(ft.Text(f"คุณกดที่ '{title}'"))),
            content=ft.Container(
                width=PHONE_W - 40,
                padding=ft.padding.symmetric(vertical=12, horizontal=12),
                border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.BLACK12)),
                content=ft.Text(title, size=14, color=ft.Colors.BLACK87),
            ),
        )

    # ---------- ส่วนตั้งค่า ----------
    settings_section = ft.Column(
        spacing=0,
        controls=[
            ft.Text("การตั้งค่า", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
            menu_item("เปลี่ยนรหัสผ่าน"),
            menu_item("เปลี่ยนภาษา"),
            menu_item("เปลี่ยนธีม"),
        ],
    )

    # ---------- ส่วนเกี่ยวกับ ----------
    about_section = ft.Column(
        spacing=0,
        controls=[
            ft.Text("เกี่ยวกับ Eat mai hub", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
            menu_item("ช่วยเหลือ ติดต่อ"),
        ],
    )

    # ---------- ปุ่มออกจากระบบ ----------
    logout_button = ft.GestureDetector(
        on_tap=lambda e: page.go("/"),
        content=ft.Container(
            alignment=ft.alignment.center_left,
            padding=ft.padding.symmetric(horizontal=12, vertical=14),
            content=ft.Text("ออกจากระบบ", size=14, color=ft.Colors.RED_700, weight=ft.FontWeight.W_500),
        ),
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
                nav_item("more.png", "More", route="/more", active=True),
            ],
        ),
    )

    # ---------- Layout ----------
    content = ft.Column(
        controls=[
            header,
            ft.Container(padding=ft.padding.symmetric(horizontal=20, vertical=10), content=settings_section),
            ft.Container(padding=ft.padding.symmetric(horizontal=20, vertical=10), content=about_section),
            ft.Container(padding=ft.padding.symmetric(horizontal=20, vertical=20), content=logout_button),
            ft.Container(height=80),
        ],
        scroll=ft.ScrollMode.AUTO,
    )

    layout = ft.Stack(
        controls=[
            content,
            ft.Container(bottom=0, left=0, right=0, content=bottom_nav),
        ],
    )

    return ft.View(
        route="/more",
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
