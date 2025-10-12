import flet as ft
import json, os
from utils.colors import AppColors
from components.card_stat import create_stat_card


def load_dashboard_data():
    """โหลดข้อมูล Dashboard จาก JSON"""
    path = os.path.join(os.path.dirname(__file__), "..", "data", "dashboard_data.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def dashboard_view(page: ft.Page):
    """หน้า Dashboard หลัก"""
    data = load_dashboard_data()
    shop_stats = data["shop_stats"]
    monthly_usage = data["monthly_usage"]

    # ---------- สร้างกราฟแท่ง (Top 5 ร้าน) ----------
    max_value = max(s["value"] for s in shop_stats)
    bars = [
        ft.Column(
            [
                ft.Container(
                    width=50,
                    height=(s["value"] / max_value) * 180,
                    bgcolor=AppColors.PRIMARY,
                    border_radius=8,
                ),
                ft.Text(
                    s["name"],
                    size=12,
                    text_align=ft.TextAlign.CENTER,
                    color=AppColors.TEXT_SECONDARY,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        for s in shop_stats
    ]

    bar_chart = ft.Container(
        content=ft.Column(
            [
                ft.Text(data["notes"]["bar_chart_title"], size=20, weight=ft.FontWeight.BOLD),
                ft.Container(height=10),
                ft.Row(bars, alignment=ft.MainAxisAlignment.SPACE_AROUND),
            ]
        ),
        padding=30,
        bgcolor=AppColors.BG_LIGHT,
        border_radius=15,
        expand=True,
    )

    # ---------- สร้างกราฟเส้นจำลอง (จำนวนการเข้าใช้งานต่อเดือน) ----------
    line_chart = ft.Container(
        content=ft.Column(
            [
                ft.Text(data["notes"]["line_chart_title"], size=20, weight=ft.FontWeight.BOLD),
                ft.Container(height=10),
                ft.Row(
                    [ft.Text(m["month"], size=13, color="#666") for m in monthly_usage],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                ),
                ft.ProgressBar(value=None, width=400, height=10, color=AppColors.PRIMARY),
                ft.Container(height=10),
                ft.Text(data["notes"]["line_chart_note"], size=12, color="#999"),
            ]
        ),
        padding=30,
        bgcolor=AppColors.BG_LIGHT,
        border_radius=15,
        expand=True,
    )

    # ---------- สถิติด้านบน (Stat Cards) ----------
    stats_row = ft.Row(
        [
            create_stat_card(s["title"], s["value"], getattr(ft.Icons, s["icon"]))
            for s in data["stats"]
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        spacing=20,
    )

    # ---------- รวม Layout ทั้งหมด ----------
    return ft.Container(
        content=ft.Column(
            [
                stats_row,
                ft.Container(height=25),
                ft.Row(
                    [bar_chart, line_chart],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            spacing=30,
            scroll=ft.ScrollMode.AUTO,
        ),
        padding=40,
        expand=True,
    )
