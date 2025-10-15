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
from random_food import build_spin_view
from nearby_view import build_nearby_view
from favorite_view import build_favorite_view
from eat_by_color import build_color_view
from review_view import build_review_view
from more_view import build_more_view    # ✅ เพิ่มการ import หน้า More


def main(page: ft.Page):
    # ---------- window & page look ----------
    page.title = "EATMAIHUB"

    page.bgcolor = ft.Colors.BLACK         # พื้นหลังรอบเฟรม
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

    # ---------- router ----------
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
        elif r == "/categories":   # ✅ หน้าแสดงหมวดหมู่
            page.views.append(categories_view(page))
        elif r == "/highlight":    # ✅ ร้านเด็ด
            page.views.append(build_highlight_view(page))
        elif r == "/urban":        # ✅ Urban Street
            page.views.append(build_urban_view(page))
        elif r == "/sunbae":       # ✅ Sunbae Korean Restaurant
            page.views.append(build_sunbae_view(page))
        elif r == "/hottobun":     # ✅ Hotto Bun
            page.views.append(build_hottobun_view(page))
        elif r == "/horoscope":    # ✅ กินตามดวง
            page.views.append(build_horoscope_view(page))
        elif r == "/random":       # ✅ สุ่มอาหาร
            page.views.append(build_spin_view(page))
        elif r == "/review":       # ✅ รีวิว
            page.views.append(build_review_view(page))
        elif r == "/nearby":       # ✅ ร้านใกล้ฉัน
            page.views.append(build_nearby_view(page))
        elif r == "/favorite":     # ✅ รายการโปรด
            page.views.append(build_favorite_view(page))
        elif r == "/color":        # ✅ กินตามสีวัน
            page.views.append(build_color_view(page))
        elif r == "/more":         # ✅ หน้า More (ตั้งค่า/เกี่ยวกับ)
            page.views.append(build_more_view(page))
        else:
            page.views.append(build_login_view(page))  # ✅ default = หน้า Login

        page.update()

    # ---------- กลับหน้าก่อนหน้า ----------
    def view_pop(e: ft.ViewPopEvent):
        page.views.pop()
        if page.views:
            page.go(page.views[-1].route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # เริ่มต้นที่หน้า login หรือ route ปัจจุบัน
    page.go(page.route or "/")


# เสิร์ฟไฟล์รูปจากโฟลเดอร์ photo
ft.app(target=main, assets_dir="photo")
