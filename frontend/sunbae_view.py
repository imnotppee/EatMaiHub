import flet as ft
import json
import os

BRAND_ORANGE = "#DC7A00"
PHONE_W, PHONE_H = 412, 917


def build_sunbae_view(page: ft.Page) -> ft.View:
    # ---------- โหลดข้อมูลจากไฟล์ JSON ----------
    data_path = os.path.join(os.path.dirname(__file__), "data", "sunbae_data.json")
    if not os.path.exists(data_path):
        raise FileNotFoundError("❌ ไม่พบไฟล์ data/sunbae_data.json")

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # ---------- Header ----------
    header = ft.Container(
        width=PHONE_W,
        padding=ft.padding.only(left=16, right=16, top=30, bottom=10),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[BRAND_ORANGE, "#F6D0A0"],
        ),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=40,
                    height=40,
                    border_radius=20,
                    bgcolor=ft.Colors.WHITE24,
                    content=ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color=ft.Colors.WHITE,
                        icon_size=22,
                        on_click=lambda e: page.go("/highlight"),
                    ),
                ),
                ft.Image(src="logo.png", width=100, height=80),
                ft.Container(width=36),
            ],
        ),
    )

    # ---------- แบนเนอร์ร้าน ----------
    banner_images = data.get("banner", [])
    banner_section = ft.Container(
        width=PHONE_W,
        height=220,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        content=ft.Image(
            src=banner_images[0] if banner_images else "",
            fit=ft.ImageFit.COVER,
        ),
    )

    # ---------- ข้อมูลร้าน ----------
    info_section = ft.Container(
        padding=ft.padding.symmetric(horizontal=16, vertical=10),
        content=ft.Column(
            spacing=4,
            controls=[
                ft.Text(data.get("name", ""), size=18, weight=ft.FontWeight.BOLD),
                ft.Text(f"รีวิว : {data.get('review', '-')}", size=14, color=ft.Colors.BLACK87),
                ft.Text(f"ที่อยู่ : {data.get('address', '-')}", size=14, color=ft.Colors.BLACK87),
                ft.Divider(color=ft.Colors.BLACK12),
            ],
        ),
    )

    # ---------- หัวข้อเมนู ----------
    menu_title = ft.Container(
        padding=ft.padding.only(left=16, bottom=6),
        content=ft.Text("เมนูแนะนำ", size=16, weight=ft.FontWeight.BOLD, color=BRAND_ORANGE),
    )

    # ---------- การ์ดเมนู ----------
    def menu_card(item):
        return ft.Container(
            width=(PHONE_W - 60) / 2,
            height=200,
            bgcolor=ft.Colors.WHITE,
            border_radius=14,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12),
            padding=ft.padding.all(10),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
                controls=[
                    ft.Container(
                        height=120,
                        width=(PHONE_W - 100) / 2,
                        border_radius=10,
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                        content=ft.Image(
                            src=item.get("image", ""),
                            fit=ft.ImageFit.COVER,
                        ),
                    ),
                    ft.Text(
                        item.get("name", ""),
                        size=13,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK87,
                        weight=ft.FontWeight.W_500,
                    ),
                ],
            ),
        )

    menus = data.get("menus", [])
    menu_grid = ft.Row(
        wrap=True,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=16,
        run_spacing=16,
        controls=[menu_card(m) for m in menus],
    )

    # ---------- Body ----------
    body = ft.Container(
        width=PHONE_W,
        height=PHONE_H,
        bgcolor=ft.Colors.WHITE,
        content=ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            controls=[
                header,
                banner_section,
                info_section,
                menu_title,
                ft.Container(
                    alignment=ft.alignment.center,
                    padding=ft.padding.symmetric(horizontal=12),
                    content=menu_grid,
                ),
                ft.Container(height=40),
            ],
        ),
    )

    # ---------- Frame ----------
    return ft.View(
        route="/sunbae",
        padding=0,
        controls=[
            ft.Container(
                expand=True,
                bgcolor=ft.Colors.BLACK,
                alignment=ft.alignment.center,
                content=ft.Container(
                    width=PHONE_W,
                    height=PHONE_H,
                    bgcolor=ft.Colors.WHITE,
                    content=body,
                ),
            )
        ],
    )
