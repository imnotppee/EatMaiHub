import flet as ft
import requests
import datetime

# ---------- CONFIG ----------
BRAND_ORANGE = "#DC7A00"
PHONE_W, PHONE_H = 412, 917

# ---------- API URL ----------
API_FAVORITE = "http://127.0.0.1:8000/api/favorites"
API_REVIEW = "http://127.0.0.1:8000/api/reviews"
API_SUNBAE = "http://127.0.0.1:8000/api/sunbae"
 

# ---------- VIEW ----------
def build_sunbae_view(page: ft.Page) -> ft.View:
    # ---------- โหลดข้อมูลร้านจาก Backend ----------
    try:
        res = requests.get(API_SUNBAE, timeout=5)
        res.raise_for_status()
        data = res.json()
    except Exception as e:
        print("❌ โหลดข้อมูลร้าน Sunbae ไม่สำเร็จ:", e)
        data = {
            "name": "Sunbae Korean Restaurant",
            "banner": ["default.png"],
            "menus": []
        }

    restaurant_name = data.get("name", "Sunbae")
    banner_img = data.get("banner", [""])[0]
    menus = data.get("menus", [])

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
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color=ft.Colors.WHITE,
                    on_click=lambda e: page.go("/highlight"),
                ),
                ft.Image(src="logo.png", width=90, height=60),
                ft.Container(width=36),
            ],
        ),
    )

    # ---------- ปุ่มหัวใจ (Favorite) ----------
    is_favorite = [False]  # ใช้ list เพื่อแก้ไขค่าภายในได้

    def toggle_favorite(e):
        try:
            if not is_favorite[0]:
                payload = {"user_id": 1, "restaurant_id": 2}  # 🧩 restaurant_id = id ของ Sunbae
                requests.post(API_FAVORITE, json=payload, timeout=3)
                is_favorite[0] = True
                heart_icon.icon = ft.Icons.FAVORITE
                heart_icon.icon_color = BRAND_ORANGE
                msg = "เพิ่มในรายการโปรดแล้ว"
            else:
                requests.delete(f"{API_FAVORITE}/2")  # 🧩 restaurant_id = 2
                is_favorite[0] = False
                heart_icon.icon = ft.Icons.FAVORITE_BORDER
                heart_icon.icon_color = ft.Colors.GREY
                msg = "ลบออกจากรายการโปรดแล้ว"
            page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=BRAND_ORANGE)
            page.snack_bar.open = True
            page.update()
        except Exception as err:
            print("❌ Favorite error:", err)

    heart_icon = ft.IconButton(
        icon=ft.Icons.FAVORITE_BORDER,
        icon_color=ft.Colors.GREY,
        icon_size=24,
        on_click=toggle_favorite,
    )

    # ---------- เมนู ----------
    def menu_card(item):
        return ft.Container(
            width=(PHONE_W - 64) / 2,
            height=190,
            bgcolor=ft.Colors.WHITE,
            border_radius=14,
            shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.BLACK12),
            padding=ft.padding.all(8),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Image(src=item.get("image", ""), height=110, fit=ft.ImageFit.COVER),
                    ft.Text(item.get("name", ""), size=13, text_align=ft.TextAlign.CENTER),
                ],
            ),
        )

    menu_grid = ft.Row(
        wrap=True,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=16,
        run_spacing=16,
        controls=[menu_card(m) for m in menus],
    )

    # ---------- ปุ่ม “กินแล้ว” ----------
    is_eaten = [False]

    def toggle_eaten(e):
        is_eaten[0] = not is_eaten[0]
        update_eat_button()
        if is_eaten[0]:
            show_review_dialog()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("ยกเลิกสถานะ 'กินแล้ว'"), bgcolor=BRAND_ORANGE)
            page.snack_bar.open = True
            page.update()

    def update_eat_button():
        if is_eaten[0]:
            eat_btn.text = "กินแล้ว"
            eat_btn.bgcolor = BRAND_ORANGE
        else:
            eat_btn.text = "ยังไม่ได้กิน"
            eat_btn.bgcolor = ft.Colors.GREY_400
        page.update()

    def show_review_dialog():
        page.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("รีวิวไหม?", weight=ft.FontWeight.BOLD),
            content=ft.Text("คุณต้องการรีวิวร้านนี้ตอนนี้เลยไหม?"),
            actions=[
                ft.TextButton("รีวิวเลย", on_click=lambda e: page.dialog.close(), data="review"),
                ft.TextButton("ยังไม่รีวิว", on_click=lambda e: page.dialog.close(), data="skip"),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog.open = True
        page.update()

    eat_btn = ft.ElevatedButton(
        text="ยังไม่ได้กิน",
        bgcolor=ft.Colors.GREY_400,
        color=ft.Colors.WHITE,
        width=180,
        height=50,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=30)),
        on_click=toggle_eaten,
    )

    # ---------- ระบบรีวิว ----------
    selected_stars = [0]

    def update_stars(index):
        selected_stars[0] = index + 1
        for i, s in enumerate(stars):
            s.icon = ft.Icons.STAR if i < selected_stars[0] else ft.Icons.STAR_BORDER
        page.update()

    stars = [
        ft.IconButton(
            icon=ft.Icons.STAR_BORDER,
            icon_color=BRAND_ORANGE,
            icon_size=36,
            on_click=lambda e, i=i: update_stars(i),
        )
        for i in range(5)
    ]

    review_field = ft.TextField(
        hint_text="เขียนรีวิว...",
        multiline=True,
        min_lines=3,
        max_lines=5,
        width=PHONE_W - 60,
        border_radius=10,
        border_color=ft.Colors.BLACK26,
    )

    def send_review(e):
        if not is_eaten[0]:
            page.snack_bar = ft.SnackBar(ft.Text("กรุณากด 'กินแล้ว' ก่อนรีวิว"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return
        if selected_stars[0] == 0 or not review_field.value.strip():
            page.snack_bar = ft.SnackBar(ft.Text("กรุณาให้คะแนนและเขียนรีวิวก่อนส่ง"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        payload = {
            "restaurant_name": restaurant_name,
            "menu_name": "",
            "stars": selected_stars[0],
            "comment": review_field.value.strip(),
            "user_id": 1,
            "restaurant_table": "sunbae"
        }

        try:
            res = requests.post(API_REVIEW, json=payload, timeout=5)
            res.raise_for_status()
            page.snack_bar = ft.SnackBar(ft.Text("ส่งรีวิวสำเร็จ!"), bgcolor="green")
        except Exception as err:
            print("❌ ส่งรีวิวไม่สำเร็จ:", err)
            page.snack_bar = ft.SnackBar(ft.Text("เกิดข้อผิดพลาดในการส่งรีวิว"), bgcolor="red")
        page.snack_bar.open = True
        page.update()

        review_field.value = ""
        for s in stars:
            s.icon = ft.Icons.STAR_BORDER
        selected_stars[0] = 0
        page.update()

    review_section = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            eat_btn,
            ft.Container(height=20),
            ft.Text("ให้คะแนนร้าน", size=16, weight=ft.FontWeight.BOLD, color=BRAND_ORANGE),
            ft.Row(controls=stars, alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=10),
            review_field,
            ft.Container(height=10),
            ft.ElevatedButton(
                text="ส่งรีวิว",
                bgcolor=BRAND_ORANGE,
                color=ft.Colors.WHITE,
                width=150,
                height=40,
                on_click=send_review,
            ),
        ],
    )

    # ---------- Layout ----------
    layout = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.ALWAYS,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            header,
            ft.Container(width=PHONE_W, height=210, clip_behavior=ft.ClipBehavior.HARD_EDGE,
                         content=ft.Image(src=banner_img, fit=ft.ImageFit.COVER)),
            ft.Container(
                padding=ft.padding.symmetric(horizontal=16, vertical=12),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(restaurant_name, size=18, weight=ft.FontWeight.BOLD),
                        heart_icon,
                    ],
                ),
            ),
            ft.Divider(thickness=1, color=ft.Colors.BLACK12),
            ft.Container(
                alignment=ft.alignment.center,
                padding=ft.padding.symmetric(horizontal=16),
                content=menu_grid,
            ),
            ft.Divider(thickness=1, color=ft.Colors.BLACK12),
            ft.Container(alignment=ft.alignment.center, padding=ft.padding.symmetric(horizontal=16), content=review_section),
            ft.Container(height=80),
        ],
    )

    return ft.View(
        route="/sunbae",
        padding=0,
        controls=[
            ft.Container(
                expand=True,
                bgcolor=ft.Colors.BLACK,
                alignment=ft.alignment.center,
                content=ft.Container(width=PHONE_W, height=PHONE_H, bgcolor=ft.Colors.WHITE, content=layout),
            )
        ],
    )
