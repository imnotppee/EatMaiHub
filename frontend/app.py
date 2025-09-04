import flet as ft
from login import build_login_view
from signup import build_signup_view
from forgot_password import build_forgot_view
from reset_password import build_reset_view

def main(page: ft.Page):
    page.title = "EATMAIHUB"
    page.bgcolor = "white"                  
    page.theme_mode = ft.ThemeMode.LIGHT    
    page.theme = ft.Theme(color_scheme=ft.ColorScheme(
        surface=ft.Colors.BLACK,            
        background=ft.Colors.BLACK,
    ))

    page.window_width = 412
    page.window_height = 917
    page.window_resizable = False
    page.window_maximized = False
    page.window_full_screen = False
    try:
        page.window_center()
    except:
        pass

    # Alignment
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 0
    page.scroll = ft.ScrollMode.AUTO

    # Router
    def route_change(e: ft.RouteChangeEvent):
        page.views.clear()
        if page.route == "/signup":
            page.views.append(build_signup_view(page))
        elif page.route == "/reset":
            page.views.append(build_reset_view(page))
        elif page.route == "/forgot":
            page.views.append(build_forgot_view(page))
        else:
            page.views.append(build_login_view(page))
        page.update()

    def view_pop(e: ft.ViewPopEvent):
        page.views.pop()
        if page.views:
            page.go(page.views[-1].route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route or "/")

# ให้ Flet เสิร์ฟรูปจากโฟลเดอร์ photo/
ft.app(main, assets_dir="photo")
