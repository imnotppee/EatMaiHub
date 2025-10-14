import flet as ft
import json, os, datetime, requests

# ---------- ค่าคงที่ ----------
BRAND_ORANGE = "#DC7A00"
PHONE_W, PHONE_H = 412, 917

# ---------- path ----------
FAV_PATH = os.path.join(os.path.dirname(__file__), "data", "favorite.json")
REVIEW_PATH = os.path.join(os.path.dirname(__file__), "data", "review_data.json")

# ---------- โหลด / บันทึก ----------
def load_json(path, default):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_reviews():
    return load_json(REVIEW_PATH, {"reviews": []})

def save_reviews(data):
    save_json(REVIEW_PATH, data)


# ---------- VIEW หลัก ----------
def build_urban_view(page: ft.Page) -> ft.View:
    # ---------- โหลดข้อมูลร้านจาก Backend ----------
    API_URL = "http://127.0.0.1:5001/api/urban-street"

    try:
        res = requests.get(API_URL)
        res.raise_for_status()
        data = res.json()
        print("✅ ดึงข้อมูลจาก Backend สำเร็จ")
    except Exception as e:
        print("⚠️ ดึงข้อมูลจาก Backend ไม่สำเร็จ:", e)
        # ใช้ fallback จากไฟล์ JSON เดิม
        data_path = os.path.join(os.path.dirname(__file__), "data", "urban_data.json")
        if os.path.exists(data_path):
            with open(data_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {"name": "Urban Street", "review": "-", "menus": [], "banner": []}

    # ---------- ตัวแปรพื้นฐาน ----------
    favorites = load_json(FAV_PATH, [])
    reviews_data = load_reviews()
    restaurant_name = data.get("name", "Urban Street")
    banner_img = data.get("banner", [""])[0] if data.get("banner") else ""

    # ---------- ตรวจ favorite ----------
    def is_favorite():
        return any(f["title"] == restaurant_name for f in favorites)

    def toggle_favorite(e):
        nonlocal favorites
        if is_favorite():
            favorites = [f for f in favorites if f["title"] != restaurant_name]
            heart_icon.icon = ft.Icons.FAVORITE_BORDER
            heart_icon.icon_color = ft.Colors.GREY
            msg = "ลบออกจากรายการโปรดแล้ว"
        else:
            favorites.append({"title": restaurant_name, "image": banner_img})
            heart_icon.icon = ft.Icons.FAVORITE
            heart_icon.icon_color = BRAND_ORANGE
            msg = "เพิ่มในรายการโปรดแล้ว"
        save_json(FAV_PATH, favorites)

        page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=BRAND_ORANGE)
        page.snack_bar.open = True
        page.update()

    # ---------- Header ----------
    header = ft.Container(
        width=PHONE_W,
        padding=ft.padding.only(left=12, right=12, top=28, bottom=10),
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
                ft.Image(src="logo.png", width=90, height=60),
                ft.Container(width=40),
            ],
        ),
    )

    # ---------- การ์ดเมนู ----------
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
        controls=[menu_card(m) for m in data.get("menus", [])],
    )

    # ---------- ปุ่ม “กินแล้ว” ----------
    review_entry = {"is_eaten": False}
    def toggle_eaten(e):
        review_entry["is_eaten"] = not review_entry["is_eaten"]
        update_eat_button()
        msg = "บันทึกว่า 'กินแล้ว'" if review_entry["is_eaten"] else "ยกเลิกสถานะ 'กินแล้ว'"
        page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=BRAND_ORANGE)
        page.snack_bar.open = True
        page.update()

    def update_eat_button():
        if review_entry["is_eaten"]:
            eat_btn.text = "กินแล้ว"
            eat_btn.bgcolor = BRAND_ORANGE
        else:
            eat_btn.text = "ยังไม่ได้กิน"
            eat_btn.bgcolor = ft.Colors.GREY_400
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

    # ---------- ให้คะแนน ----------
    selected_stars = 0
    stars = []

    def update_stars(index):
        nonlocal selected_stars
        selected_stars = index + 1
        for i, s in enumerate(stars):
            s.icon = ft.Icons.STAR if i < selected_stars else ft.Icons.STAR_BORDER
        page.update()

    for i in range(5):
        star = ft.IconButton(
            icon=ft.Icons.STAR_BORDER,
            icon_color=BRAND_ORANGE,
            icon_size=36,
            on_click=lambda e, i=i: update_stars(i),
        )
        stars.append(star)

    review_field = ft.TextField(
        hint_text="เขียนรีวิว...",
        multiline=True,
        min_lines=3,
        max_lines=5,
        width=PHONE_W - 60,
        border_radius=10,
        border_color=ft.Colors.BLACK26,
    )

    # ---------- ปุ่มส่งรีวิว ----------
    def send_review(e):
        nonlocal selected_stars
        if not review_entry["is_eaten"]:
            page.snack_bar = ft.SnackBar(ft.Text("กรุณากด 'กินแล้ว' ก่อนรีวิว"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return
        if selected_stars == 0 or not review_field.value.strip():
            page.snack_bar = ft.SnackBar(ft.Text("กรุณาให้คะแนนและเขียนรีวิวก่อนส่ง"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        new_review = {
            "restaurant": restaurant_name,
            "image": banner_img,
            "is_eaten": True,
            "is_reviewed": True,
            "stars": selected_stars,
            "comment": review_field.value.strip(),
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        reviews_data["reviews"].append(new_review)
        save_reviews(reviews_data)

        review_field.value = ""
        for s in stars:
            s.icon = ft.Icons.STAR_BORDER
        selected_stars = 0

        page.snack_bar = ft.SnackBar(ft.Text("ส่งรีวิวสำเร็จ!"), bgcolor="green")
        page.snack_bar.open = True
        page.update()

    # ---------- ส่วนรีวิว ----------
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

    # ---------- ปุ่มหัวใจ ----------
    heart_icon = ft.IconButton(
        icon=ft.Icons.FAVORITE if is_favorite() else ft.Icons.FAVORITE_BORDER,
        icon_color=BRAND_ORANGE if is_favorite() else ft.Colors.GREY,
        icon_size=24,
        on_click=toggle_favorite,
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
                content=ft.Column(
                    spacing=6,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(restaurant_name, size=18, weight=ft.FontWeight.BOLD),
                                heart_icon,
                            ],
                        ),
                        ft.Text(data.get("review", "-"), size=14, color=ft.Colors.BLACK87),
                    ],
                ),
            ),
            ft.Container(
                padding=ft.padding.only(left=16, bottom=6),
                alignment=ft.alignment.center_left,
                content=ft.Text("เมนูแนะนำ", size=16, weight=ft.FontWeight.BOLD, color=BRAND_ORANGE),
            ),
            ft.Container(padding=ft.padding.symmetric(horizontal=16), alignment=ft.alignment.center, content=menu_grid),
            ft.Divider(thickness=1, color=ft.Colors.BLACK12),
            ft.Container(alignment=ft.alignment.center, padding=ft.padding.symmetric(horizontal=16), content=review_section),
            ft.Container(height=80),
        ],
    )

    return ft.View(
        route="/urban",
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
