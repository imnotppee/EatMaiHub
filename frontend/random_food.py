import flet as ft
import random, time, requests

BRAND_ORANGE = "#DC7A00"
PHONE_W, PHONE_H = 412, 917


class FoodService:
    """โหลดข้อมูลอาหารจาก Backend"""
    API_URL = "http://127.0.0.1:8000/api/random"
    BASE_IMAGE_URL = "http://127.0.0.1:8000"

    @staticmethod
    def load_food_data():
        try:
            response = requests.get(FoodService.API_URL)
            if response.status_code == 200:
                print("✅ ดึงข้อมูลจาก backend สำเร็จ")
                data = response.json()
                if isinstance(data, dict) and "data" in data:
                    return data["data"]
                return data
            else:
                print(f"⚠️ ดึงข้อมูลไม่สำเร็จ: {response.status_code}")
                return []
        except Exception as e:
            print("❌ เกิดข้อผิดพลาด:", e)
            return []


# ---------- หน้าสุ่มอาหาร ----------
class RandomFoodPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/random")
        self.page = page
        self.foods = FoodService.load_food_data()

        # --- State เริ่มต้น ---
        self.random_image = ft.Image(
            src=f"{FoodService.BASE_IMAGE_URL}/static/images/random1.png",
            border_radius=20,
            fit=ft.ImageFit.COVER
        )
        self.random_name = ft.Text(
            "ยังไม่ได้สุ่มนะ ลองกดปุ่มด้านล่างเลย!",
            size=16, weight="bold", color=BRAND_ORANGE, text_align=ft.TextAlign.CENTER,
        )

        self.phone_frame = None
        self.controls = [self.build_view()]

    # ---------- Layout ----------
    def build_view(self):
        header = self.build_header()
        main_section = self.build_main_section()
        bottom_nav = self.build_bottom_nav()

        body = ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[header, main_section, bottom_nav],
        )

        bg = ft.Container(
            width=PHONE_W,
            height=340,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[BRAND_ORANGE, "#F6D0A0", "#FFFFFFFF"],
                stops=[0.0, 0.6, 1.0],
            ),
        )

        self.phone_frame = ft.Stack(
            width=PHONE_W,
            height=PHONE_H,
            controls=[
                bg,
                ft.Container(padding=ft.padding.symmetric(horizontal=12, vertical=10), content=body),
            ],
        )

        return ft.Container(
            expand=True,
            bgcolor=ft.Colors.BLACK,
            alignment=ft.alignment.center,
            content=ft.Container(
                width=PHONE_W,
                height=PHONE_H,
                bgcolor=ft.Colors.WHITE,
                content=self.phone_frame,
            ),
        )

    # ---------- Header ----------
    def build_header(self):
        return ft.Container(
            padding=ft.padding.only(left=16, right=16, top=12, bottom=10),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color=ft.Colors.WHITE,
                        on_click=lambda e: self.page.go("/home"),
                    ),
                    ft.Image(src="logo.png", width=36, height=36),
                    ft.IconButton(icon=ft.Icons.PERSON, icon_color=ft.Colors.WHITE),
                ],
            ),
        )

    # ---------- กล่องสุ่ม ----------
    def build_main_section(self):
        random_box = ft.Container(
            width=310,
            height=350,
            border_radius=20,
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK26),
            alignment=ft.alignment.center,
            padding=20,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
                controls=[
                    ft.Text("สุ่มอาหารกันเลย!", size=16, weight="bold", color=BRAND_ORANGE),
                    self.random_image,
                    self.random_name,
                ],
            ),
        )

        spin_button = ft.Container(
            width=180,
            height=52,
            border_radius=26,
            gradient=ft.LinearGradient(
                begin=ft.alignment.center_left,
                end=ft.alignment.center_right,
                colors=["#FF6B35", "#DC7A00", "#FF8C42"],
            ),
            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.4, BRAND_ORANGE)),
            alignment=ft.alignment.center,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
                controls=[
                    ft.Icon(ft.Icons.CASINO, color=ft.Colors.WHITE, size=24),
                    ft.Text("สุ่มเลย !", size=18, weight="bold", color=ft.Colors.WHITE),
                ],
            ),
            on_click=self.on_spin,
        )

        return ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=25,
                controls=[random_box, spin_button],
            ),
        )

    # ---------- Bottom Nav ----------
    def build_bottom_nav(self):
        def nav_item(icon: str, label: str, route=None, active=False):
            return ft.GestureDetector(
                on_tap=lambda e: self.page.go(route) if route else None,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=2,
                    controls=[
                        ft.Image(src=icon, width=28, height=28, fit=ft.ImageFit.CONTAIN),
                        ft.Text(label, size=10, color=BRAND_ORANGE if active else ft.Colors.BLACK87),
                    ],
                ),
            )

        return ft.Container(
            bgcolor=ft.Colors.WHITE,
            border=ft.border.only(top=ft.BorderSide(1, ft.Colors.BLACK12)),
            padding=10,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                controls=[
                    nav_item("home.png", "Home", route="/home"),
                    nav_item("heart.png", "Favorite", route="/favorite"),
                    nav_item("review.png", "Review", route="/review"),
                    nav_item("more.png", "More", route="/more"),
                ],
            ),
        )

    # ---------- ฟังก์ชันสุ่ม ----------
    def on_spin(self, e):
        if not self.foods:
            self.random_name.value = "⚠️ ไม่มีข้อมูลอาหารในระบบ"
            self.page.update()
            return

        total_rounds = 10
        for i in range(total_rounds):
            temp = random.choice(self.foods)
            self.random_image.src = f"{FoodService.BASE_IMAGE_URL}{temp['image']}"
            self.random_name.value = temp.get("name", "ไม่พบชื่ออาหาร")
            self.page.update()
            time.sleep(0.25 + (i * 0.05))

        final_food = random.choice(self.foods)
        self.random_image.src = f"{FoodService.BASE_IMAGE_URL}{final_food['image']}"
        self.random_name.value = final_food.get("name", "ไม่พบชื่ออาหาร")
        self.page.update()
        self.show_popup(final_food)

    # ---------- Popup ----------
    def show_popup(self, food):
        popup = ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=20,
            width=280,
            height=360,
            padding=20,
            shadow=ft.BoxShadow(blur_radius=25, color=ft.Colors.BLACK26),
            alignment=ft.alignment.center,
            margin=ft.margin.only(top=100),  # ✅ ปรับจาก 80 → 100 ให้พอดีจอ
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # จัดให้อยู่กลางแนวนอน
                spacing=15,
                controls=[
                    ft.Text("ผลการสุ่มอาหาร", size=18, weight="bold", color=BRAND_ORANGE),
                    ft.Image(
                        src=f"{FoodService.BASE_IMAGE_URL}{food['image']}",
                        width=180,
                        height=180,
                        border_radius=12,
                        fit=ft.ImageFit.COVER,
                    ),
                    ft.Text(
                        food.get("name", "ไม่พบชื่ออาหาร"),
                        size=14,
                        weight="bold",
                        color=ft.Colors.BLACK,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        controls=[
                            ft.ElevatedButton(
                                text="สุ่มอีกครั้ง",
                                bgcolor=BRAND_ORANGE,
                                color=ft.Colors.WHITE,
                                on_click=lambda e: [self.remove_popup(), self.on_spin(e)],
                            ),
                            ft.ElevatedButton(
                                text="ตกลง",
                                bgcolor="#888888",
                                color=ft.Colors.WHITE,
                                on_click=lambda e: self.remove_popup(),
                            ),
                        ],
                    ),
                ],
            ),
        )

        overlay = ft.Container(
            width=PHONE_W,
            height=PHONE_H,
            alignment=ft.alignment.center,
            content=popup,
        )

        self.overlay = overlay
        self.phone_frame.controls.append(overlay)
        self.page.update()

    def remove_popup(self):
        if hasattr(self, "overlay") and self.overlay in self.phone_frame.controls:
            self.phone_frame.controls.remove(self.overlay)
            self.page.update()
