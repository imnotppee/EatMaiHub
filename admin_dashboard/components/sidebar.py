import flet as ft
from utils.colors import AppColors


def create_sidebar(page: ft.Page, active_page="dashboard", update_view=None):
    def nav_item(name, icon, route_name):
        is_active = route_name == active_page
        color = AppColors.PRIMARY if is_active else "#666666"
        bgcolor = "#FFF6EB" if is_active else None
        border = (
            ft.border.only(left=ft.BorderSide(4, AppColors.PRIMARY))
            if is_active
            else None
        )

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
            border=border,
            border_radius=8,
            on_click=lambda _: update_view(route_name) if update_view else None,
        )

    # ---------- โลโก้ ----------
    header = ft.Column(
        [
            ft.Image(src="logo.png", width=120, height=120),
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

    # ---------- เมนู ----------
    menu_items = ft.Column(
        [
            nav_item("Dashboard", ft.Icons.DASHBOARD, "dashboard"),
            nav_item("Manage User", ft.Icons.PEOPLE, "manage_user"),
            nav_item("Edit Features", ft.Icons.SETTINGS, "edit_features"),
            nav_item("Admin", ft.Icons.ADMIN_PANEL_SETTINGS, "admin"),
        ],
        spacing=10,
    )

    # ---------- Footer ----------
    footer = ft.Container(
        content=ft.Text(
            "© EatMaiHub Admin",
            size=11,
            color="#AAAAAA",
            text_align=ft.TextAlign.CENTER,
        ),
        padding=ft.padding.only(top=10),
    )

    # ---------- Layout ----------
    return ft.Container(
        width=250,
        bgcolor="#FFFFFF",
        padding=ft.padding.symmetric(vertical=20, horizontal=20),
        border=ft.border.only(right=ft.BorderSide(1, "#D9D9D9")),
        content=ft.Column(
            [
                header,
                ft.Container(height=20),
                menu_items,
                ft.Container(expand=True),
                footer,
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=15,
            expand=True,
        ),
        alignment=ft.alignment.Alignment(0, -1),
    )
