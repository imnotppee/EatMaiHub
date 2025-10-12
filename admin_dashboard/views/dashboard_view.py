import flet as ft
import json
import os
from utils.colors import BRAND_ORANGE, BORDER_COLOR, BG_LIGHT
from components.sidebar import Sidebar
from components.topbar import Topbar


def build_dashboard_view(page: ft.Page):
    # โหลดข้อมูล mock จากไฟล์ JSON
    data_path = os.path.join(os.path.dirname(__file__), "../data/dashboard_data.json")
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # ========== กราฟร้านยอดนิยม ==========
    bars = [
        ft.BarChartGroup(
            x=i,
            bar_rods=[
                ft.BarChartRod(
                    from_y=0,
                    to_y=restaurant["count"],
                    color=BRAND_ORANGE,
                    tooltip=restaurant["name"],
                    width=25,
                    border_radius=5,
                )
            ],
        )
        for i, restaurant in enumerate(data["popular_restaurants"])
    ]

    chart_popular = ft.BarChart(
        bar_groups=bars,
        border=ft.border.all(1, BORDER_COLOR),
        left_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(value=v, label=ft.Text(str(v)))
                for v in range(0, 301, 50)
            ]
        ),
        bottom_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=i,
                    label=ft.Text(r["name"], size=11, rotate=30),
                )
                for i, r in enumerate(data["popular_restaurants"])
            ]
        ),
        horizontal_grid_lines=ft.ChartGridLines(color="#EEEEEE", width=1),
        vertical_grid_lines=ft.ChartGridLines(color="#F8F8F8", width=1),
        interactive=True,
        animate=1000,
        expand=True,
        height=260,
    )

    # ========== กราฟจำนวนการใช้งานต่อเดือน ==========
    months = ["Jan", "Feb", "Mar", "Apr", "May", "June", "July"]

    usage_points = [
        ft.LineChartDataPoint(
            x=i,
            y=v,
            tooltip=f"{months[i]}: {v} ครั้ง"   # ✅ tooltip ต่อจุด
        )
        for i, v in enumerate(data["monthly_usage"])
    ]

    line_chart = ft.LineChart(
        data_series=[
            ft.LineChartData(
                data_points=usage_points,
                color=BRAND_ORANGE,
                stroke_width=3,
                curved=True,
                stroke_cap_round=True
            )
        ],
        bottom_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(value=i, label=ft.Text(month))
                for i, month in enumerate(months)
            ]
        ),
        left_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(value=v, label=ft.Text(str(v)))
                for v in range(0, 401, 100)
            ]
        ),
        border=ft.border.all(1, BORDER_COLOR),
        horizontal_grid_lines=ft.ChartGridLines(color="#EEEEEE", width=1),
        interactive=True,
        animate=1000,
        height=260,
    )


    # ========== การ์ดสรุปข้อมูล ==========
    summary_row = ft.Row(
        [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("จำนวนผู้ใช้ทั้งหมด (Users)", size=16),
                        ft.Text(
                            f"{data['users']} User",
                            size=22,
                            weight=ft.FontWeight.BOLD,
                            color=BRAND_ORANGE,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                border=ft.border.all(1, BORDER_COLOR),
                border_radius=10,
                bgcolor=BG_LIGHT,
                expand=True,
                padding=20,
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("จำนวนร้านอาหารทั้งหมดในระบบ", size=16),
                        ft.Text(
                            f"{data['restaurants']} ร้านอาหารในระบบ",
                            size=22,
                            weight=ft.FontWeight.BOLD,
                            color=BRAND_ORANGE,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                border=ft.border.all(1, BORDER_COLOR),
                border_radius=10,
                bgcolor=BG_LIGHT,
                expand=True,
                padding=20,
            ),
        ],
        spacing=15,
    )

     # ========== Layout หลัก ==========
    return ft.View(
        "/",
        controls=[
            ft.Row(
                [
                    Sidebar(page),
                    ft.Container(  # ✅ ใช้ Container ครอบ Column แล้วใส่ padding ที่นี่แทน
                        content=ft.Column(
                            [
                                Topbar(),
                                ft.Row(
                                    [
                                        ft.Container(
                                            ft.Column(
                                                [
                                                    ft.Text(
                                                        "ร้านที่ถูกค้นหามากที่สุด",
                                                        size=18,
                                                        weight=ft.FontWeight.BOLD,
                                                    ),
                                                    chart_popular,
                                                ]
                                            ),
                                            expand=2,
                                        ),
                                        ft.Container(
                                            ft.Column(
                                                [
                                                    ft.Text(
                                                        "จำนวนการเข้าใช้งานต่อเดือน",
                                                        size=18,
                                                        weight=ft.FontWeight.BOLD,
                                                    ),
                                                    line_chart,
                                                ]
                                            ),
                                            expand=1,
                                        ),
                                    ],
                                    spacing=15,
                                ),
                                summary_row,
                            ],
                            expand=True,
                            spacing=15,
                        ),
                        expand=True,
                        padding=20,  # ✅ padding ถูกต้องแล้ว
                    )
                ],
                expand=True,
            )
        ],
    )
