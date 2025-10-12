import flet as ft
from views.dashboard_view import build_dashboard_view
from views.manage_user_view import build_manage_user_view
from views.edit_features_view import build_edit_features_view
from views.admin_view import build_admin_view

def main(page: ft.Page):
    page.title = "EatMaiHub Admin Dashboard"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 1280
    page.window_height = 800

    def route_change(e):
        page.views.clear()
        if page.route == "/":
            page.views.append(build_dashboard_view(page))
        elif page.route == "/manage-user":
            page.views.append(build_manage_user_view(page))
        elif page.route == "/edit-features":
            page.views.append(build_edit_features_view(page))
        elif page.route == "/admin":
            page.views.append(build_admin_view(page))
        page.update()

    page.on_route_change = route_change
    page.go("/")

ft.app(target=main, view=ft.AppView.WEB_BROWSER)
