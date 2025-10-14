"""
ไฟล์หน้า Admin สำหรับจัดการแอดมิน
"""
import flet as ft
from utils.colors import AppColors


def admin_view(page: ft.Page):
    """หน้า Admin System"""
    
    # ข้อมูลแอดมินตัวอย่าง
    admins = [
        {"id": "A-001", "name": "woonsen", "password": "****"},
        {"id": "A-002", "name": "kittikarn", "password": "****"},
        {"id": "A-003", "name": "tonoak", "password": "****"},
    ]
    
    def create_admin_table():
        """สร้างตารางแอดมิน"""
        
        # Header
        header = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text(
                        "Admin ID",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=AppColors.TEXT_PRIMARY,
                    ),
                    width=200,
                ),
                ft.Container(
                    content=ft.Text(
                        "Name",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=AppColors.TEXT_PRIMARY,
                    ),
                    width=200,
                ),
                ft.Container(
                    content=ft.Text(
                        "Password",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=AppColors.TEXT_PRIMARY,
                    ),
                    expand=True,
                ),
            ],
            spacing=20,
        )
        
        # Rows
        admin_rows = []
        for admin in admins:
            row = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text(
                                admin["id"],
                                size=13,
                                color=AppColors.TEXT_SECONDARY,
                            ),
                            width=200,
                        ),
                        ft.Container(
                            content=ft.Text(
                                admin["name"],
                                size=13,
                                color=AppColors.TEXT_SECONDARY,
                            ),
                            width=200,
                        ),
                        ft.Container(
                            content=ft.Text(
                                admin["password"],
                                size=13,
                                color=AppColors.TEXT_SECONDARY,
                            ),
                            expand=True,
                        ),
                    ],
                    spacing=20,
                ),
                padding=15,
                bgcolor=ft.Colors.WHITE,
                border_radius=8,
                border=ft.border.all(1, ft.Colors.GREY_300),
            )
            admin_rows.append(row)
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Admin system",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=AppColors.TEXT_PRIMARY,
                    ),
                    ft.Container(height=20),
                    header,
                    ft.Divider(height=1, color=ft.Colors.GREY_400),
                    ft.Container(height=10),
                    ft.Column(
                        controls=admin_rows,
                        spacing=10,
                    ),
                ],
            ),
            padding=25,
            bgcolor=AppColors.BG_LIGHT,
            border_radius=15,
            width=700,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
        )
    
    # Layout หลัก
    content = ft.Container(
        content=ft.Column(
            controls=[
                create_admin_table(),
            ],
            scroll=ft.ScrollMode.AUTO,
        ),
        padding=30,
        expand=True,
    )
    
    return content