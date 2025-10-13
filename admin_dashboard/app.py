import flet as ft
from components.sidebar import create_sidebar
from components.topbar import create_topbar

# ✅ Views หลัก
from views.dashboard_view import dashboard_view
from views.manage_user_view import manage_user_view
from views.edit_features_view import edit_features_view
from views.edit_feature_detail_view import edit_feature_detail_view  # เพิ่มมาใหม่
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

    # ---------- State ----------
    current_view = {"value": "dashboard"}

    # ---------- ฟังก์ชันเปลี่ยนหน้า ----------
    def update_view(view_name: str):
        """เปลี่ยนหน้าและอัปเดต Sidebar"""
        current_view["value"] = view_name

        # ✅ โหลดเนื้อหาตามชื่อ view
        if view_name == "dashboard":
            topbar_title = "Dashboard"
            view_content = dashboard_view(page)
        elif view_name == "manage_user":
            topbar_title = "Manage User"
            view_content = manage_user_view(page)
        elif view_name == "edit_features":
            topbar_title = "Edit Features"
            view_content = edit_features_view(page)
        elif view_name == "edit_feature_detail":  # ✅ หน้าแก้ไขข้อมูลใหม่
            topbar_title = "Edit Feature Detail"
            view_content = edit_feature_detail_view(page)
        elif view_name == "admin":
            topbar_title = "Admin"
            view_content = admin_view(page)
        else:
            topbar_title = "Dashboard"
            view_content = dashboard_view(page)

        # ✅ อัปเดตพื้นที่เนื้อหา
        content_area.content = ft.Column(
            [
                create_topbar(page, topbar_title),
                view_content,
            ],
            spacing=0,
        )

        # ✅ อัปเดต Sidebar ให้ Active ตรงหน้า
        sidebar_container.content = create_sidebar(
            page, active_page=view_name, update_view=update_view
        )

        page.update()

    # ---------- Sidebar ----------
    sidebar_container = ft.Container(
        content=create_sidebar(page, active_page="dashboard", update_view=update_view),
        width=260,
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.only(right=ft.BorderSide(1, ft.Colors.GREY_300)),
        padding=ft.Padding.only(top=15, left=20, right=20, bottom=10),
    )

    # ---------- พื้นที่เนื้อหา ----------
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

    # ---------- รองรับการเปลี่ยน route (จากหน้าแก้ไข) ----------
    def route_change(route):
        """จัดการการเปลี่ยนหน้าแบบ route"""
        if page.route == "/edit_feature_detail":
            update_view("edit_feature_detail")
        else:
            update_view("dashboard")

    page.on_route_change = route_change


# ---------- เริ่มรัน ----------
if __name__ == "__main__":
    ft.run(main, view=ft.AppView.WEB_BROWSER)
