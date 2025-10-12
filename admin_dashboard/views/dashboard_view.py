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
    data = load_dashboard_data()
    shop_stats = data["shop_stats"]
    monthly_usage = data["monthly_usage"]
    stats_cards = data["stats"]
    top_rated = data.get("top_rated_restaurants", [])
    notes = data["notes"]

    # ---------- ⭐ ร้านที่รีวิวดีที่สุด ----------
    top_cards = [
        ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        f"{i+1}. {r['name']}",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=AppColors.TEXT_PRIMARY,
                    ),
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.STAR_ROUNDED, color="#FFD700", size=18),
                            ft.Text(f"{r['rating']} / 5.0", size=14, color="#666666"),
                            ft.Text(f"({r['reviews']} รีวิว)", size=12, color="#999999"),
                        ],
                        spacing=5,
                    ),
                ],
                spacing=4,
                horizontal_alignment=ft.CrossAxisAlignment.START,
            ),
            bgcolor=AppColors.BG_LIGHT,
            border_radius=10,
            padding=15,
            width=270,
            height=75,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=6,
                color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
            ),
        )
        for i, r in enumerate(top_rated)
    ]

    top_rated_section = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.STAR_ROUNDED, color="#FFD700", size=22),
                        ft.Text(
                            "ร้านที่รีวิวดีที่สุด 3 อันดับ",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=AppColors.TEXT_PRIMARY,
                        ),
                    ],
                    spacing=6,
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Container(height=10),
                ft.Row(top_cards, alignment=ft.MainAxisAlignment.START, spacing=20),
            ]
        ),
        padding=ft.padding.only(bottom=20),
    )

    # ---------- 📊 สถิติด้านบน (จัดชิดซ้าย) ----------
    stats_row = ft.Container(
        content=ft.Row(
        [
            ft.Container(
                content=create_stat_card(
                    stat["title"],
                    stat["value"],
                    getattr(ft.Icons, stat["icon"]),
                ),
                alignment=ft.alignment.Alignment(-1, 0),  # ✅ ใช้ Alignment แทน
            )
            for stat in stats_cards
        ],
        alignment=ft.MainAxisAlignment.START,  # ✅ แถวชิดซ้าย
        spacing=15,
    ),
    alignment=ft.alignment.Alignment(-1, 0),  # ✅ Container ชิดซ้ายด้วย
)


    # ---------- 📈 ร้านที่ถูกค้นหามากที่สุด ----------
    max_value = max(s["value"] for s in shop_stats)
    bars = [
        ft.Column(
            [
                ft.Container(
                    width=45,
                    height=(s["value"] / max_value) * 180,
                    bgcolor=AppColors.PRIMARY,
                    border_radius=8,
                ),
                ft.Container(height=6),
                ft.Text(str(s["value"]), size=12, color="#666666"),
                ft.Container(height=4),
                ft.Text(
                    s["name"],
                    size=13,
                    text_align=ft.TextAlign.CENTER,
                    color="#666666",
                    width=100,
                    max_lines=2,
                    no_wrap=False,  # ✅ ให้ขึ้นบรรทัดใหม่ได้
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        for s in shop_stats
    ]

    bar_chart = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    notes["bar_chart_title"],
                    size=19,
                    weight=ft.FontWeight.BOLD,
                    color=AppColors.TEXT_PRIMARY,
                ),
                ft.Container(height=10),
                ft.Row(
                    bars,
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    vertical_alignment=ft.CrossAxisAlignment.END,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=AppColors.BG_LIGHT,
        border_radius=15,
        padding=25,
        expand=True,
        height=360,
    )

    # ---------- 📉 การเข้าใช้งานต่อเดือน ----------
    max_usage = max(m["value"] for m in monthly_usage)
    usage_bars = [
        ft.Column(
            [
                ft.Container(
                    width=40,
                    height=(m["value"] / max_usage) * 180,
                    bgcolor=AppColors.PRIMARY,
                    border_radius=6,
                ),
                ft.Container(height=6),
                ft.Text(str(m["value"]), size=12, color="#666666"),
                ft.Container(height=4),
                ft.Text(
                    m["month"],
                    size=13,
                    color="#666666",
                    text_align=ft.TextAlign.CENTER,
                    width=70,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        for m in monthly_usage
    ]

    line_chart = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    notes["line_chart_title"],
                    size=19,
                    weight=ft.FontWeight.BOLD,
                    color=AppColors.TEXT_PRIMARY,
                ),
                ft.Container(height=10),
                ft.Row(
                    usage_bars,
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    vertical_alignment=ft.CrossAxisAlignment.END,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=AppColors.BG_LIGHT,
        border_radius=15,
        padding=25,
        expand=True,
        height=360,
    )

    # ---------- ✅ รวม Layout ทั้งหมด ----------
    return ft.Container(
        content=ft.Column(
            [
                top_rated_section,  # ⭐ อยู่บนสุด
                stats_row,  # ✅ แถวสถิติชิดซ้าย
                ft.Container(height=15),
                ft.Row(
                    [bar_chart, line_chart],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                ),
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
        ),
        padding=ft.padding.only(left=25, right=25, top=15, bottom=25),
        expand=True,
    )
