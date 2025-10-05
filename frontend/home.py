import flet as ft
from flet import Icons, Colors
import json
import os

BRAND_ORANGE = "#DC7A00"
PHONE_W, PHONE_H = 412, 917


def build_home_view(page: ft.Page) -> ft.View:
    # ---------- โหลดข้อมูลจาก foods.json ----------
    foods_path = os.path.join(os.path.dirname(__file__), "data", "foods.json")
    with open(foods_path, "r", encoding="utf-8") as f:
        foods = json.load(f)

    # ---------- Header ----------
    header_row = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Image(src="logo.png", width=36, height=36),
                    ft.Container(width=8),
                    ft.Text("Hi user", size=16, color=Colors.WHITE),
                ],
            ),
            ft.IconButton(
                icon=Icons.PERSON,
                icon_color=Colors.WHITE,
                on_click=lambda e: page.go("/"),  # กลับหน้า Login
            ),
        ],
    )

    search = ft.TextField(
        hint_text="ค้นหาร้าน / เมนู",
        prefix_icon=Icons.SEARCH,
        border_radius=20,
        border_color=BRAND_ORANGE,
        filled=True,
        fill_color=Colors.WHITE,
        height=44,
    )

    header = ft.Container(
        padding=ft.padding.only(left=16, right=16, top=12, bottom=16),
        content=ft.Column(spacing=12, controls=[header_row, search]),
    )

    # ---------- ปุ่มบน ----------
    def pill(icon_src: str, label: str, route=None):
        return ft.GestureDetector(
            on_tap=lambda e: page.go(route) if route else None,
            content=ft.Container(
                bgcolor=Colors.WHITE,
                border_radius=12,
                padding=12,
                width=(PHONE_W - 64) / 2,
                shadow=ft.BoxShadow(blur_radius=10, spread_radius=0, color=Colors.BLACK12),
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=6,
                    controls=[
                        ft.Image(src=icon_src, width=40, height=40),
                        ft.Text(label, size=14),
                ],
            ),
        ),
    )


    top_buttons = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
        controls=[
            pill("star.png", "ร้านเด็ด", route="/highlight"),
            pill("roll.png", "สุ่มอาหาร")
        ],
    )

   


    # ---------- Feature 4 อัน ----------
    def feature(icon_src: str, label: str):
        return ft.Container(
            bgcolor=Colors.WHITE,
            border_radius=12,
            padding=10,
            width=(PHONE_W - 64) / 4,
            shadow=ft.BoxShadow(blur_radius=8, color=Colors.BLACK12),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=6,
                controls=[ft.Image(src=icon_src, width=32, height=32), ft.Text(label, size=12)],
            ),
        )

    feature_row = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
        controls=[
            feature("ball.png", "กินตามดวง"),
            feature("pin.png", "ร้านใกล้ฉัน"),
            feature("Category.png", "หมวดหมู่"),
            feature("palette.png", "กินตามสีวัน"),
        ],
    )

         # ---------- ร้านเด็ด (Banner slide ทีละรูป + จุด indicator) ----------
    highlight_title = ft.Row(
        alignment=ft.MainAxisAlignment.START,
        controls=[
            ft.Image(src="star.png", width=20, height=20),
            ft.Container(width=6),
            ft.Text("ร้านเด็ด", size=16, weight=ft.FontWeight.BOLD, color=BRAND_ORANGE),
        ],
    )

    banners = ["banner.png", "banner2.png", "banner3.png"]
    current_index = 0
    drag_start_x = {"value": None}
    drag_last_x = {"value": None}

    banner_image = ft.Image(
        src=banners[current_index],
        fit=ft.ImageFit.COVER,
        width=PHONE_W - 24,
        height=180,
    )

    # จุด indicator ด้านล่าง
    dots = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=6,
        controls=[
            ft.Container(
                width=8, height=8, border_radius=20,
                bgcolor=BRAND_ORANGE if i == current_index else ft.Colors.BLACK26
            )
            for i in range(len(banners))
        ],
    )

    def update_banner(new_index: int):
        nonlocal current_index
        current_index = new_index % len(banners)
        banner_image.src = banners[current_index]
        banner_image.update()
        for i, d in enumerate(dots.controls):
            d.bgcolor = BRAND_ORANGE if i == current_index else ft.Colors.BLACK26
        dots.update()

    def on_pan_start(e: ft.DragStartEvent):
        drag_start_x["value"] = e.local_x
        drag_last_x["value"] = e.local_x

    def on_pan_update(e: ft.DragUpdateEvent):
        drag_last_x["value"] = e.local_x

    def on_pan_end(e: ft.DragEndEvent):
        start = drag_start_x["value"]
        end = drag_last_x["value"]
        if start is None or end is None:
            return
        delta = end - start
        if delta < -50:   # ปัดซ้าย
            update_banner(current_index + 1)
        elif delta > 50:  # ปัดขวา
            update_banner(current_index - 1)
        drag_start_x["value"] = None
        drag_last_x["value"] = None

    # ✅ เพิ่มให้กด banner แล้วไปหน้า urban
    def on_banner_tap(e):
        if current_index == 0:
            page.go("/urban")  # banner แรก → Urban Street
        elif current_index == 1:
            page.go("/sunbae")  # banner ที่สอง → Sunbae Korean Restaurant
        else:
            page.go("/highlight")  # banner ที่สาม → highlight รวม


    highlight_banner = ft.Column(
        spacing=6,
        controls=[
            ft.GestureDetector(
                on_tap=on_banner_tap,
                on_pan_start=on_pan_start,
                on_pan_update=on_pan_update,
                on_pan_end=on_pan_end,
                content=ft.Container(
                    width=PHONE_W - 24,
                    height=180,
                    border_radius=16,
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    shadow=ft.BoxShadow(blur_radius=12, color=ft.Colors.BLACK26),
                    content=banner_image,
                ),
            ),
            dots
        ],
    )

    # ---------- การ์ดอาหาร (จาก foods.json) ----------
    card_w, card_h = 120, 160

    def food_card(img: str, title: str, subtitle: str):
        return ft.Container(
            width=card_w,
            height=card_h,
            bgcolor=Colors.WHITE,
            border_radius=12,
            padding=8,
            shadow=ft.BoxShadow(blur_radius=8, color=Colors.BLACK12),
            content=ft.Column(
                spacing=6,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        height=80,
                        border_radius=10,
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                        content=ft.Image(src=img, fit=ft.ImageFit.COVER),
                    ),
                    ft.Text(title, size=12, weight=ft.FontWeight.W_600, text_align=ft.TextAlign.CENTER),
                    ft.Text(
                        subtitle,
                        size=10,
                        color=Colors.BLACK54,
                        max_lines=1,
                        overflow="ellipsis",
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
            ),
        )

    horo_title = ft.Row(
        alignment=ft.MainAxisAlignment.START,
        controls=[
            ft.Image(src="ball.png", width=22, height=22),
            ft.Container(width=6),
            ft.Text("กินตามดวงวันนี้", size=16, weight=ft.FontWeight.BOLD, color=BRAND_ORANGE),
        ],
    )

    horo_scroller = ft.Row(
        scroll=ft.ScrollMode.ALWAYS,
        spacing=12,
        controls=[food_card(f["image"], f["title"], f["subtitle"]) for f in foods],
    )

    # ---------- Bottom nav ----------
    def nav_item(icon: str, label: str, active=False, on_click=None):
        return ft.GestureDetector(
            on_tap=on_click or (lambda e: None),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
                controls=[
                    ft.Image(src=icon, width=24, height=24),
                    ft.Text(label, size=10, color=BRAND_ORANGE if active else Colors.BLACK87),
                ],
            ),
        )

    bottom_nav = ft.Container(
        bgcolor=Colors.WHITE,
        border=ft.border.only(top=ft.BorderSide(1, Colors.BLACK12)),
        padding=10,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                nav_item("HOME.png", "Home", active=True),
                nav_item("history.png", "History"),
                nav_item("Review.png", "Review"),
                nav_item("More.png", "More"),
            ],
        ),
    )

    # ---------- เนื้อหา ----------
    body = ft.Column(
        spacing=12,
        controls=[
            header,
            top_buttons,
            feature_row,
            highlight_title,
            highlight_banner,
            horo_title,
            horo_scroller,
            ft.Container(expand=True),
            bottom_nav,
        ],
    )

    # ---------- BG ----------
    orange_gradient_bg = ft.Container(
        width=PHONE_W,
        height=340,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[BRAND_ORANGE, "#F6D0A0", "#FFFFFFFF"],
            stops=[0.0, 0.6, 1.0],
        ),
    )

    phone_frame = ft.Stack(
        width=PHONE_W,
        height=PHONE_H,
        controls=[
            orange_gradient_bg,
            ft.Container(padding=ft.padding.symmetric(horizontal=12, vertical=10), content=body),
        ],
    )

    return ft.View(
        route="/home",
        padding=0,
        controls=[
            ft.Container(
                expand=True,
                bgcolor=Colors.BLACK,
                alignment=ft.alignment.center,
                content=ft.Container(
                    width=PHONE_W,
                    height=PHONE_H,
                    bgcolor=Colors.WHITE,
                    content=phone_frame,
                ),
            )
        ],
    )
