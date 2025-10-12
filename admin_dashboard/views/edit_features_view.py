import flet as ft
from components.sidebar import Sidebar
from components.topbar import Topbar

def build_edit_features_view(page):
    content = ft.Container(
        content=ft.Column([
            Topbar(),
            ft.Text("⚙️ Edit Features Page", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("หน้านี้ใช้แก้ไขฟีเจอร์ภายในระบบ เช่น การเพิ่มหมวดหมู่ใหม่ ฟังก์ชัน หรือข้อมูลแสดงผล"),
        ],
        spacing=15,
        expand=True),
        expand=True,
        padding=20,  # ✅ ใส่ padding ที่ Container แทน
        bgcolor="#FAFAFA"
    )

    return ft.View(
        "/edit-features",
        controls=[
            ft.Row([
                Sidebar(page),
                content
            ])
        ]
    )
