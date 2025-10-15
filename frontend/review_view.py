import flet as ft
import json, os
from functools import partial

BRAND_ORANGE = "#DC7A00"
PHONE_W, PHONE_H = 412, 917
REVIEW_PATH = os.path.join(os.path.dirname(__file__), "data", "review_data.json")


def load_reviews():
    if os.path.exists(REVIEW_PATH):
        with open(REVIEW_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"reviews": []}


def build_review_view(page: ft.Page) -> ft.View:
    data = load_reviews()
    reviews = data.get("reviews", [])

    reviewed = [r for r in reviews if r.get("is_reviewed")]
    pending = [r for r in reviews if r.get("is_eaten") and not r.get("is_reviewed")]

    # ---------- ฟังก์ชันเปลี่ยนหน้า ----------
    def go_to_restaurant(name, e):
        """ไปยังหน้าร้านเพื่อเพิ่มหรือแก้ไขรีวิว"""
        if name == "Urban Street":
            page.go("/urban")
        elif name == "Hotto Bun":
            page.go("/hottobun")
        elif "Sunbae" in name:
            page.go("/sunbae")
        else:
            page.snack_bar = ft.SnackBar(ft.Text("ยังไม่มีหน้ารีวิวสำหรับร้านนี้"), bgcolor="red")
            page.snack_bar.open = True
            page.update()

    # ---------- แสดงดาว ----------
    def star_row(star_count):
        return ft.Row(
            spacing=1,
            controls=[
                ft.Icon(
                    ft.Icons.STAR if i < star_count else ft.Icons.STAR_BORDER,
                    color=BRAND_ORANGE,
                    size=16,
                )
                for i in range(5)
            ],
        )

    # ---------- การ์ดรีวิวแล้ว ----------
    def reviewed_card(r):
        return ft.GestureDetector(
            on_tap=partial(go_to_restaurant, r["restaurant"]),  # ✅ คลิกทั้งการ์ดเพื่อไปหน้ารีวิว
            content=ft.Container(
                padding=8,
                margin=ft.margin.symmetric(vertical=5, horizontal=10),
                border_radius=12,
                bgcolor=ft.Colors.WHITE,
                shadow=ft.BoxShadow(blur_radius=4, color=ft.Colors.BLACK12),
                content=ft.Row(
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Image(
                            src=r.get("image", ""),
                            width=70,
                            height=70,
                            border_radius=8,
                            fit=ft.ImageFit.COVER,
                        ),
                        ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=3,
                            controls=[
                                ft.Text(
                                    r["restaurant"],
                                    size=13,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLACK87,
                                ),
                                star_row(r["stars"]),
                                ft.Text(
                                    r["comment"],
                                    size=11,
                                    color=ft.Colors.BLACK87,
                                    no_wrap=False,
                                ),
                            ],
                        ),
                    ],
                ),
            ),
        )

    # ---------- การ์ดที่รอรีวิว ----------
    def pending_card(r):
        return ft.Container(
            padding=8,
            margin=ft.margin.symmetric(vertical=5, horizontal=10),
            border_radius=12,
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(blur_radius=4, color=ft.Colors.BLACK12),
            content=ft.Row(
                spacing=8,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Image(
                        src=r.get("image", ""),
                        width=70,
                        height=70,
                        border_radius=8,
                        fit=ft.ImageFit.COVER,
                    ),
                    ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=6,
                        controls=[
                            ft.Text(r["restaurant"], size=13, weight=ft.FontWeight.BOLD),
                            ft.ElevatedButton(
                                text="รีวิวร้าน",
                                bgcolor=BRAND_ORANGE,
                                color=ft.Colors.WHITE,
                                width=85,
                                height=28,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=20)
                                ),
                                on_click=partial(go_to_restaurant, r["restaurant"]),
                            ),
                        ],
                    ),
                ],
            ),
        )

    # ---------- Header (เพิ่ม Gradient ไล่สี) ----------
    header = ft.Container(
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#B85C00", "#DC7A00", "#F7C16E"],
            stops=[0.0, 0.5, 1.0],
        ),
        padding=ft.padding.only(top=24, left=12, right=12, bottom=10),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            icon_color=ft.Colors.WHITE,
                            icon_size=22,
                            on_click=lambda e: page.go("/home"),
                        ),
                        ft.Image(src="logo.png", width=55),
                        ft.IconButton(
                            icon=ft.Icons.PERSON,
                            icon_color=ft.Colors.WHITE,
                            icon_size=22,
                        ),
                    ],
                ),
                ft.Text("รีวิว", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ],
        ),
    )

    # ---------- Layout หลัก ----------
    layout = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.ALWAYS,
        spacing=8,
        controls=[
            header,
            ft.Container(
                padding=ft.padding.only(left=16, bottom=4),
                content=ft.Text("รีวิวแล้ว", size=14, weight=ft.FontWeight.BOLD, color=BRAND_ORANGE),
            ),
            *(
                [reviewed_card(r) for r in reviewed]
                if reviewed
                else [
                    ft.Container(
                        padding=ft.padding.only(left=16),
                        content=ft.Text("ยังไม่มีรีวิว", color=ft.Colors.BLACK54, size=12),
                    )
                ]
            ),
            ft.Container(
                padding=ft.padding.only(left=16, top=6, bottom=4),
                content=ft.Text("รอรีวิว", size=14, weight=ft.FontWeight.BOLD, color=BRAND_ORANGE),
            ),
            *(
                [pending_card(r) for r in pending]
                if pending
                else [
                    ft.Container(
                        padding=ft.padding.only(left=16),
                        content=ft.Text("ไม่มีร้านที่รอรีวิว", color=ft.Colors.BLACK54, size=12),
                    )
                ]
            ),
            ft.Container(height=15),
        ],
    )

    # ---------- เฟรมมือถือ ----------
    phone_frame = ft.Container(
        width=PHONE_W,
        height=PHONE_H,
        bgcolor=ft.Colors.WHITE,
        border_radius=ft.border_radius.all(20),
        shadow=ft.BoxShadow(blur_radius=18, color=ft.Colors.BLACK26),
        content=layout,
    )

    return ft.View(
        route="/review",
        padding=0,
        controls=[
            ft.Container(
                expand=True,
                bgcolor=ft.Colors.BLACK,
                alignment=ft.alignment.center,
                content=phone_frame,
            )
        ],
    )
