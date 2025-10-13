import flet as ft
import json, os
from components.card_stat import create_stat_card
from utils.colors import AppColors


def load_user_data():
    """โหลดข้อมูลผู้ใช้จาก JSON"""
    path = os.path.join(os.path.dirname(__file__), "..", "data", "manage_user_data.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def manage_user_view(page: ft.Page):
    data = load_user_data()
    stats = data["stats"]
    users = data["user_list"]

    # ---------- 📊 การ์ดสถิติ ----------
    stat_cards = ft.Row(
        [
            create_stat_card("ผู้ใช้ทั้งหมด", str(stats["total_users"]), ft.Icons.PEOPLE),
            create_stat_card("ผู้ใช้ใหม่เดือนนี้", str(stats["new_users"]), ft.Icons.PERSON_ADD),
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=20,
    )

    # ---------- 🧑 ตารางข้อมูลผู้ใช้ ----------
    user_rows = [
        ft.Row(
            [
                ft.Container(ft.Text(u["id"], size=14), width=120),
                ft.Container(ft.Text(u["name"], size=14), width=200),
                ft.Container(ft.Text(u["gmail"], size=14), width=300),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        )
        for u in users
    ]

    user_table = ft.Container(
        content=ft.Column(
            [
                ft.Text("ภาพรวมบัญชีผู้ใช้", size=18, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY),
                ft.Container(height=10),
                ft.Row(
                    [
                        ft.Container(ft.Text("User ID", weight=ft.FontWeight.BOLD, width=120)),
                        ft.Container(ft.Text("Name", weight=ft.FontWeight.BOLD, width=200)),
                        ft.Container(ft.Text("Gmail", weight=ft.FontWeight.BOLD, width=300)),
                    ],
                    spacing=10,
                ),
                ft.Divider(height=1, color="#CCCCCC"),
                *user_rows,
            ],
            spacing=10,
        ),
        bgcolor=AppColors.BG_LIGHT,
        border_radius=15,
        padding=20,
        margin=ft.margin.only(top=20),
    )

    # ---------- ✅ รวมทั้งหมด ----------
    return ft.Container(
        content=ft.Column(
            [
                stat_cards,
                user_table,
            ],
            spacing=25,
        ),
        padding=ft.Padding.only(left=25, right=25, top=15, bottom=25),
        expand=True,
    )
