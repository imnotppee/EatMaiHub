import flet as ft
from utils.colors import AppColors


def create_stat_card(title: str, value: str, icon, width: int = 250):
    """สร้างการ์ดสถิติ (Stat Card)"""
    return ft.Container(
        width=width,
        padding=20,
        bgcolor=AppColors.BG_LIGHT,
        border_radius=12,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=8,
            color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
        ),
        content=ft.Row(
            [
                ft.Icon(icon, color=AppColors.PRIMARY, size=28),
                ft.Column(
                    [
                        ft.Text(title, size=14, color="#666666"),
                        ft.Text(value, size=22, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY),
                    ],
                    spacing=4,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            spacing=15,
            alignment=ft.MainAxisAlignment.START,
        ),
    )
