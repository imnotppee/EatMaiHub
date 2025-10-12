"""
ไฟล์หน้า Edit Features สำหรับจัดการร้านอาหาร
"""
import flet as ft
from utils.colors import AppColors


def edit_features_view(page: ft.Page):
    """หน้า Edit Features"""
    
    # ข้อมูลร้านอาหารตัวอย่าง
    restaurants = [
        {
            "name": "Urban street (สเต็กกามปรามเซียน)",
            "detail": "สเต็กและอาหารโปรตุเกสชื่อสถานบาเทอราร์น",
            "image": "assets/urban_street.jpg",
        },
        {
            "name": "Sunbae Korean Restaurant",
            "detail": "อาหารเกาหลี เกาใจ",
            "image": "assets/sunbae.jpg",
        },
    ]
    
    def create_restaurant_card(restaurant):
        """สร้าง Card ร้านอาหาร"""
        return ft.Container(
            content=ft.Row(
                controls=[
                    # รูปภาพ
                    ft.Container(
                        content=ft.Image(
                            src=restaurant["image"],
                            width=200,
                            height=150,
                            fit=ft.ImageFit.COVER,
                            border_radius=10,
                        ),
                        width=200,
                        height=150,
                        border_radius=10,
                        bgcolor=ft.Colors.GREY_300,
                    ),
                    ft.Container(width=20),
                    # ข้อมูล
                    ft.Column(
                        controls=[
                            ft.Text(
                                restaurant["name"],
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=AppColors.SECONDARY,
                            ),
                            ft.Container(height=5),
                            ft.Text(
                                restaurant["detail"],
                                size=13,
                                color=AppColors.TEXT_SECONDARY,
                            ),
                        ],
                        spacing=0,
                        expand=True,
                    ),
                ],
            ),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            border=ft.border.all(1, ft.Colors.GREY_300),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
        )
    
    # Tabs
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="ร้านเด็ด",
                icon=ft.Icons.STAR,
            ),
            ft.Tab(
                text="สุ่มอาหาร",
                icon=ft.Icons.SHUFFLE,
            ),
            ft.Tab(
                text="กินตามดวง",
                icon=ft.Icons.CASINO,
            ),
        ],
        tab_alignment=ft.TabAlignment.START,
    )
    
    # Action buttons
    action_buttons = ft.Column(
        controls=[
            ft.ElevatedButton(
                "Add Features",
                icon=ft.Icons.ADD,
                bgcolor=AppColors.BG_LIGHT,
                color=AppColors.TEXT_PRIMARY,
                height=60,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                ),
            ),
            ft.ElevatedButton(
                "Edit Detail",
                icon=ft.Icons.EDIT,
                bgcolor=AppColors.PRIMARY,
                color=ft.Colors.WHITE,
                height=60,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                ),
            ),
            ft.ElevatedButton(
                "Delete Detail",
                icon=ft.Icons.DELETE,
                bgcolor=AppColors.BG_LIGHT,
                color=AppColors.ERROR,
                height=60,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                ),
            ),
        ],
        spacing=15,
    )
    
    # Layout หลัก
    content = ft.Container(
        content=ft.Row(
            controls=[
                # ส่วนซ้าย: รายการร้าน
                ft.Container(
                    content=ft.Column(
                        controls=[
                            tabs,
                            ft.Container(height=20),
                            ft.Column(
                                controls=[
                                    create_restaurant_card(restaurant)
                                    for restaurant in restaurants
                                ],
                                spacing=15,
                                scroll=ft.ScrollMode.AUTO,
                            ),
                        ],
                    ),
                    expand=True,
                ),
                ft.Container(width=30),
                # ส่วนขวา: ปุ่มจัดการ
                action_buttons,
            ],
        ),
        padding=30,
        expand=True,
    )
    
    return content