"""
ไฟล์หน้า Manage User สำหรับจัดการผู้ใช้
"""
import flet as ft
from utils.colors import AppColors
from components.card_stat import create_stat_card


def manage_user_view(page: ft.Page):
    """หน้า Manage User"""
    
    # ข้อมูลผู้ใช้ตัวอย่าง
    users = [
        {"id": "U-001", "name": "woonsen", "email": "woonsen123@gmail.com"},
        {"id": "U-002", "name": "kittikarn", "email": "kittikarn456@gmail.com"},
        {"id": "U-003", "name": "tonoak", "email": "tonoak789@gmail.com"},
    ]
    
    def create_user_table():
        """สร้างตารางผู้ใช้"""
        
        # Header
        header = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text(
                        "User ID",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=AppColors.TEXT_PRIMARY,
                    ),
                    width=150,
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
                        "Gmail",
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
        user_rows = []
        for user in users:
            row = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text(
                                user["id"],
                                size=13,
                                color=AppColors.TEXT_SECONDARY,
                            ),
                            width=150,
                        ),
                        ft.Container(
                            content=ft.Text(
                                user["name"],
                                size=13,
                                color=AppColors.TEXT_SECONDARY,
                            ),
                            width=200,
                        ),
                        ft.Container(
                            content=ft.Text(
                                user["email"],
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
            user_rows.append(row)
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "ภาพรวมบัญชีผู้ใช้",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=AppColors.TEXT_PRIMARY,
                    ),
                    ft.Container(height=20),
                    header,
                    ft.Divider(height=1, color=ft.Colors.GREY_400),
                    ft.Container(height=10),
                    ft.Column(
                        controls=user_rows,
                        spacing=10,
                    ),
                ],
            ),
            padding=25,
            bgcolor=AppColors.BG_LIGHT,
            border_radius=15,
            width=800,
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
                # สถิติ
                ft.Row(
                    controls=[
                        create_stat_card("ผู้ใช้ทั้งหมด", "15", ft.Icons.PEOPLE, width=350),
                        create_stat_card("จำนวนผู้ใช้ใหม่", "4", ft.Icons.PERSON_ADD, width=350),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=25,
                ),
                ft.Container(height=30),
                # ตารางผู้ใช้
                create_user_table(),
            ],
            scroll=ft.ScrollMode.AUTO,
        ),
        padding=30,
        expand=True,
    )
    
    return content