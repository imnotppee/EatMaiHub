import flet as ft
from components.sidebar import Sidebar
from components.topbar import Topbar

def build_admin_view(page):
    content = ft.Container(
        content=ft.Column([
            Topbar(),
            ft.Text("👤 Admin Page", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("จัดการข้อมูลแอดมิน และตั้งค่าระบบ", size=16),
            ft.Divider(height=20, color="#EEEEEE"),
            ft.Container(
                content=ft.Text("ฟังก์ชันตัวอย่าง: เพิ่ม/ลบแอดมิน, เปลี่ยนรหัสผ่าน, ตั้งค่าความปลอดภัย"),
                padding=15,
                border=ft.border.all(1, "#E0E0E0"),
                border_radius=10,
                bgcolor="#FFFFFF",
            )
        ],
        spacing=15,
        expand=True),
        expand=True,
        padding=20,  # ✅ ย้าย padding มาที่ Container
        bgcolor="#FAFAFA"
    )

    return ft.View(
        "/admin",
        controls=[
            ft.Row([
                Sidebar(page),
                content
            ])
        ]
    )
