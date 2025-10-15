import flet as ft

# ===== import views =====
from login import build_login_view
from signup import build_signup_view
from reset_password import build_reset_view
from forgot_password import build_forgot_view
from home import build_home_view
from categories import categories_view
from highlight_view import build_highlight_view
from urban_view import build_urban_view
from sunbae_view import build_sunbae_view
from hottobun_view import build_hottobun_view
from horoscope_view import build_horoscope_view
from random_food import RandomFoodPage    # ✅ ใช้ class ใหม่แทน build_spin_view
from nearby_view import build_nearby_view
from favorite_view import build_favorite_view
from eat_by_color import build_color_view  


# ---------- ฟังก์ชันหลัก ----------
def main(page: ft.Page):
    page.title = "EATMAIHUB"
    page.bgcolor = ft.Colors.BLACK
    page.padding = 0
    page.margin = 0
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.LIGHT

    # ตั้งขนาดจำลองมือถือ
    page.window_width = 412
    page.window_height = 917
    page.window_resizable = False
    page.window_maximized = False
    page.window_full_screen = False
    try:
        page.window_center()
    except Exception:
        pass

    # ---------- Router ----------
    def route_change(e: ft.RouteChangeEvent):
        page.views.clear()
        r = page.route

        if r == "/signup":
            page.views.append(build_signup_view(page))
        elif r == "/reset":
            page.views.append(build_reset_view(page))
        elif r == "/forgot":
            page.views.append(build_forgot_view(page))
        elif r == "/home":
            page.views.append(build_home_view(page))
        elif r == "/categories":
            page.views.append(categories_view(page))
        elif r == "/highlight":
            page.views.append(build_highlight_view(page))
        elif r == "/urban":
            page.views.append(build_urban_view(page))
        elif r == "/sunbae":
            page.views.append(build_sunbae_view(page))
        elif r == "/hottobun":
            page.views.append(build_hottobun_view(page))
        elif r == "/horoscope":
            page.views.append(build_horoscope_view(page))
        elif r == "/random":
            page.views.append(RandomFoodPage(page))   # ✅ OOP Version
        elif r == "/nearby":
            page.views.append(build_nearby_view(page))
        elif r == "/favorite":
            page.views.append(build_favorite_view(page))
        elif r == "/color":
            page.views.append(build_color_view(page))
        else:
            page.views.append(build_login_view(page))

        page.update()

    # ---------- Back Navigation ----------
    def view_pop(e: ft.ViewPopEvent):
        page.views.pop()
        if page.views:
            page.go(page.views[-1].route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route or "/")

# ---------- รันแอป ----------
ft.app(target=main, assets_dir="photo")
