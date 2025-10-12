import flet as ft
from utils.colors import AppColors


def create_sidebar(page: ft.Page, active_page="Dashboard", update_view=None):
    """
    Sidebar สำหรับ EatMaiHub Admin Dashboard (โลโก้ใหญ่ขึ้น, ชิดบน, เส้นแบ่งเต็มจอ)
    """

    def nav_item(name, icon, route_name):
        is_active = name.lower() == active_page.lower()
        color = AppColors.PRIMARY if is_active else "#666666"
        bgcolor = "#FFF6EB" if is_active else None

        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icon, size=20, color=color),
                    ft.Text(name, size=15, color=color, weight=ft.FontWeight.W_500),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=ft.padding.symmetric(vertical=10, horizontal=20),
            bgcolor=bgcolor,
            border_radius=8,
            on_click=lambda _: update_view(route_name) if update_view else None,
        )

    # ---------- LOGO SECTION ----------
    header = ft.Column(
        [
            ft.Image(src="logo.png", width=120, height=120),  # ✅ โลโก้ใหญ่ขึ้น
            ft.Text(
                "eat mai hub",
                size=24,
                color=AppColors.PRIMARY,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
    )

    # ---------- MENU ITEMS ----------
    menu_items = ft.Column(
        [
            nav_item("Dashboard", ft.Icons.DASHBOARD, "dashboard"),
            nav_item("Manage User", ft.Icons.PEOPLE, "manage_user"),
            nav_item("Edit Features", ft.Icons.SETTINGS, "features"),
            nav_item("Admin", ft.Icons.ADMIN_PANEL_SETTINGS, "admin"),
        ],
        spacing=12,
    )

    # ---------- COPYRIGHT ----------
    footer = ft.Container(
        content=ft.Text(
            "© EatMaiHub Admin",
            size=11,
            color="#AAAAAA",
            text_align=ft.TextAlign.CENTER,
        ),
        padding=ft.padding.only(top=20),
    )

    # ---------- SIDEBAR MAIN CONTAINER ----------
    return ft.Container(
        width=250,
        bgcolor="#FFFFFF",
        padding=ft.padding.symmetric(vertical=20, horizontal=20),
        border=ft.border.only(right=ft.BorderSide(1, "#D9D9D9")),  # ✅ เส้นเทาเต็มจอ
        content=ft.Column(
            [
                header,
                ft.Container(height=20),  # ✅ ลดระยะห่าง
                menu_items,
                ft.Container(expand=True),  # ✅ ดัน footer ลงล่างสุด
                footer,
            ],
            alignment=ft.MainAxisAlignment.START,  # ✅ ชิดบน
            spacing=15,
            expand=True,
        ),
        alignment=ft.alignment.Alignment(0, -1),  # ✅ โลโก้อยู่กึ่งกลางแนว X และชิดบน
    )
