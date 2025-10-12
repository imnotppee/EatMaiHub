import flet as ft

BRAND_ORANGE = "#DC7A00"

def create_stat_card(title, value, icon, color=BRAND_ORANGE):
    """สร้างการ์ดสถิติแบบยืดหยุ่น"""
    return ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    content=ft.Icon(icon, size=40, color=color),
                    width=50,
                    height=50,
                    bgcolor="#FFF6EB",
                    border_radius=12,
                    alignment=ft.alignment.Alignment(0, 0),
                ),
                ft.Column(
                    [
                        ft.Text(title, size=14, color="#666666"),
                        ft.Text(value, size=22, weight=ft.FontWeight.BOLD, color=color),
                    ],
                    spacing=2,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        ),
        bgcolor="#FFFFFF",
        padding=ft.padding.all(16),
        border_radius=12,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=6,
            color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
        ),
        width=250,
        height=100,
    )
