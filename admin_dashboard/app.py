import flet as ft
from components.sidebar import create_sidebar
from components.topbar import create_topbar
from views.dashboard_view import dashboard_view
from views.manage_user_view import manage_user_view
from views.edit_features_view import edit_features_view
from views.admin_view import admin_view


def main(page: ft.Page):
    # ---------- ตั้งค่าหน้า ----------
    page.title = "EatMaiHub - Admin Dashboard"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.bgcolor = ft.Colors.WHITE
    page.window_width = 1400
    page.window_height = 900
    page.scroll = ft.ScrollMode.AUTO

    # ---------- State สำหรับหน้า ----------
    current_view = {"value": "dashboard"}

    # ---------- ฟังก์ชันเปลี่ยนหน้า ----------
    def update_view(view_name: str):
        """เปลี่ยนคอนเทนต์เมื่อกดเมนู Sidebar"""
        current_view["value"] = view_name

        # อัปเดตเนื้อหาตามหน้า
        if view_name == "dashboard":
            content_area.content = ft.Column(
                [
                    create_topbar(page, "Dashboard"),
                    dashboard_view(page),
                ],
                spacing=0,
            )
        elif view_name == "manage_user":
            content_area.content = ft.Column(
                [
                    create_topbar(page, "Manage User"),
                    manage_user_view(page),
                ],
                spacing=0,
            )
        elif view_name == "edit_features":
            content_area.content = ft.Column(
                [
                    create_topbar(page, "Edit Features"),
                    edit_features_view(page),
                ],
                spacing=0,
            )
        elif view_name == "admin":
            content_area.content = ft.Column(
                [
                    create_topbar(page, "Admin"),
                    admin_view(page),
                ],
                spacing=0,
            )

        # อัปเดต Sidebar ให้ Active หน้าปัจจุบัน
        sidebar_container.content = create_sidebar(page, view_name, update_view)
        page.update()

    # ---------- สร้าง Sidebar ----------
    sidebar_container = ft.Container(
        content=create_sidebar(page, "dashboard", update_view),
        width=280,
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.only(right=ft.BorderSide(1, ft.Colors.GREY_300)),
        padding=20,
    )

    # ---------- พื้นที่เนื้อหาหลัก ----------
    content_area = ft.Container(
        content=ft.Column(
            [
                create_topbar(page, "Dashboard"),
                dashboard_view(page),
            ],
            spacing=0,
        ),
        expand=True,
        bgcolor=ft.Colors.WHITE,
    )

    # ---------- Layout หลัก ----------
    layout = ft.Row(
        [
            sidebar_container,
            content_area,
        ],
        spacing=0,
        expand=True,
    )

    page.add(layout)


# ---------- เริ่มรัน ----------
if __name__ == "__main__":
    ft.run(main, view=ft.AppView.WEB_BROWSER)
