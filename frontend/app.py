import flet as ft

# ===== import views =====
from login import build_login_view
from signup import build_signup_view
from reset_password import build_reset_view
from forgot_password import build_forgot_view
from home import build_home_view


def main(page: ft.Page):
    # ---------- window & page look ----------
    page.title = "EATMAIHUB"

    # พื้นหลัง “นอกแอป” ให้ดำ และตัดขอบ/พื้นที่ว่างรอบ ๆ ออก
    page.bgcolor = ft.Colors.BLACK         # พื้นหลังรอบเฟรม
    page.padding = 0                       # ตัด padding รอบ page
    page.margin = 0                        # ตัด margin รอบ page
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    # โหมดสีของคอมโพเนนต์ภายใน ให้เป็นสว่าง (ตัวหนังสือดำ บนพื้นขาว)
    page.theme_mode = ft.ThemeMode.LIGHT

    # ขนาดจำลองมือถือ 412x917
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
        else:
            # default = login
            page.views.append(build_login_view(page))

        page.update()

    def view_pop(e: ft.ViewPopEvent):
        page.views.pop()
        if page.views:
            page.go(page.views[-1].route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # เริ่มที่ route ปัจจุบัน หรือหน้า login
    page.go(page.route or "/")


# เสิร์ฟไฟล์รูปจากโฟลเดอร์ photo (เช่น logo.png, google.png, …)
ft.app(target=main, assets_dir="photo")
