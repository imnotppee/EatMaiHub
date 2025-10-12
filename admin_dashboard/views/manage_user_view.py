import flet as ft
from components.sidebar import Sidebar
from components.topbar import Topbar
from utils.colors import BRAND_ORANGE, BORDER_COLOR, BG_LIGHT


def build_manage_user_view(page):
    table = ft.DataTable(
        border=ft.border.all(1, BORDER_COLOR),
        border_radius=8,
        horizontal_lines=ft.BorderSide(1, "#EEEEEE"),
        vertical_lines=ft.BorderSide(1, "#F2F2F2"),
        columns=[
            ft.DataColumn(ft.Text("User ID")),
            ft.DataColumn(ft.Text("Name")),
            ft.DataColumn(ft.Text("Email")),
            ft.DataColumn(ft.Text("Status")),
        ],
        rows=[
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("U001")),
                ft.DataCell(ft.Text("Tanawat")),
                ft.DataCell(ft.Text("tanawat@example.com")),
                ft.DataCell(ft.Container(
                    ft.Text("Active", color="#1B5E20"),
                    bgcolor="#E8F5E9",
                    border_radius=10,
                    padding=5,
                    alignment=ft.alignment.center
                ))
            ]),
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("U002")),
                ft.DataCell(ft.Text("Pimchanok")),
                ft.DataCell(ft.Text("pimchanok@example.com")),
                ft.DataCell(ft.Container(
                    ft.Text("Suspended", color="#C62828"),
                    bgcolor="#FFEBEE",
                    border_radius=10,
                    padding=5,
                    alignment=ft.alignment.center
                ))
            ]),
        ],
    )

    content = ft.Container(
        content=ft.Column(
            [
                Topbar(),
                ft.Text("📋 จัดการผู้ใช้ (Manage Users)", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(height=20, color="#F0F0F0"),
                ft.Container(
                    table,
                    expand=True,
                    border=ft.border.all(1, BORDER_COLOR),
                    border_radius=10,
                    padding=15,
                    bgcolor="#FFFFFF",
                    shadow=ft.BoxShadow(blur_radius=4, color="#E0E0E0"),
                )
            ],
            spacing=15,
        ),
        expand=True,
        padding=25,
        bgcolor="#FAFAFA"
    )

    return ft.View(
        "/manage-user",
        controls=[
            ft.Row([
                Sidebar(page),
                content
            ])
        ]
    )
