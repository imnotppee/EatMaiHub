import flet as ft
from utils.colors import AppColors


def create_topbar(page: ft.Page, title="Dashboard"):
    # ช่องค้นหา
    search_bar = ft.TextField(
        hint_text="ค้นหา...",
        border_radius=25,
        height=50,
        content_padding=ft.padding.symmetric(horizontal=20, vertical=10),
        bgcolor=AppColors.BG_LIGHT,
        border_color=ft.Colors.TRANSPARENT,
        focused_border_color=AppColors.PRIMARY,
        text_size=14,
        prefix_icon=ft.Icons.SEARCH,
    )
    
    # ไอคอนโปรไฟล์
    profile_icon = ft.Container(
        content=ft.Icon(ft.Icons.PERSON, color=AppColors.TEXT_SECONDARY, size=28),
        width=50,
        height=50,
        border_radius=25,
        bgcolor=AppColors.BG_LIGHT,
        alignment=ft.alignment.Alignment(0, 0),
        on_click=lambda _: print("Profile clicked"),
        ink=True,
    )
    
    # แถบด้านบน
    topbar = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(expand=True),  # Spacer
                ft.Container(
                    content=search_bar,
                    width=600,
                ),
                ft.Container(width=20),
                profile_icon,
            ],
            alignment=ft.MainAxisAlignment.END,
        ),
        padding=ft.padding.symmetric(horizontal=30, vertical=15),
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.only(bottom=ft.BorderSide(1, ft.Colors.GREY_300)),
    )
    
    return topbar
