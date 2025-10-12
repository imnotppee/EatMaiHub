import flet as ft
from utils.colors import BRAND_ORANGE


class Sidebar(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.active_route = "/"  # ✅ route เริ่มต้น (หน้า Dashboard)

    def navigate(self, e, route):
        self.active_route = route
        self.page.go(route)
        self.update()

    def build_button(self, text, route, icon=None):
        is_active = self.active_route == route
        return ft.Container(
            content=ft.Text(text, size=16, weight=ft.FontWeight.BOLD, color="#000000" if not is_active else "white"),
            alignment=ft.alignment.center,
            border=ft.border.all(1, "#E0E0E0"),
            border_radius=10,
            bgcolor=BRAND_ORANGE if is_active else "#F5F5F5",
            height=50,
            ink=True,
            on_click=lambda e: self.navigate(e, route),
            animate=ft.animation.Animation(250, ft.AnimationCurve.EASE_IN_OUT),
        )

    def build(self):
        return ft.Container(
            width=200,
            bgcolor="#FAFAFA",
            padding=15,
            content=ft.Column(
                [
                    ft.Image(src="/logo.png", width=80, height=80),
                    ft.Divider(height=20, color="#EEEEEE"),
                    self.build_button("Dashboard", "/"),
                    self.build_button("Manage User", "/manage-user"),
                    self.build_button("Edit Features", "/edit-features"),
                    self.build_button("Admin", "/admin"),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.START,
            ),
        )
