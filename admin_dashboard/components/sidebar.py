import flet as ft
from utils.colors import AppColors


def create_sidebar(page: ft.Page, active_page="Dashboard", update_view=None):
    """
    สร้าง Sidebar พร้อมเมนูนำทาง
    Args:
        page: ft.Page
        active_page: หน้าที่กำลังอยู่
        update_view: callback function (ใช้เปลี่ยนหน้า)
    """

    def nav_item(name, icon, route_name):
        """สร้างแต่ละปุ่มใน Sidebar"""
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

    # Logo + Title
    header = ft.Column(
        [
            ft.Image(src="logo.png", width=70, height=70),
            ft.Text("eat mai hub", size=20, color=AppColors.PRIMARY, weight=ft.FontWeight.BOLD),
            ft.Container(height=30),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Navigation menu
    menu_items = ft.Column(
        [
            nav_item("Dashboard", ft.Icons.DASHBOARD, "dashboard"),
            nav_item("Manage User", ft.Icons.PEOPLE, "manage_user"),
            nav_item("Edit Features", ft.Icons.SETTINGS, "features"),
            nav_item("Admin", ft.Icons.ADMIN_PANEL_SETTINGS, "admin"),
        ],
        spacing=10,
    )

    return ft.Container(
        width=250,
        bgcolor="#FFFFFF",
        padding=20,
        content=ft.Column(
            [
                header,
                menu_items,
                ft.Container(expand=True),  # Spacer ด้านล่าง
                ft.Text("© EatMaiHub Admin", size=11, color="#AAAAAA", text_align=ft.TextAlign.CENTER),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
    )
