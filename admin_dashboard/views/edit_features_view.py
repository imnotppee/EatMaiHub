import flet as ft
from utils.colors import AppColors
import json, os


def edit_features_view(page: ft.Page):
    """หน้า Edit Features"""

    # โหลดข้อมูลจาก JSON
    json_path = os.path.join(os.path.dirname(__file__), "../data/features_data.json")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    restaurants = data.get("restaurants", [])
    random_foods = data.get("random_foods", [])
    zodiac_foods = data.get("zodiac_foods", [])

    # ---------- ฟังก์ชันสร้างการ์ดร้าน ----------
    def create_card(item):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Image(
                        src=item["image"],
                        width=200,
                        height=150,
                        fit="cover",
                        border_radius=10,
                    ),
                    ft.Container(width=20),
                    ft.Column(
                        [
                            ft.Text(item["name"], size=16, weight=ft.FontWeight.BOLD, color=AppColors.SECONDARY),
                            ft.Text(item["detail"], size=13, color=AppColors.TEXT_SECONDARY),
                        ],
                        spacing=5,
                    ),
                ],
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            padding=20,
            border=ft.border.all(1, ft.Colors.GREY_300),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
        )

    # ---------- ส่วนของแท็บจำลอง ----------
    current_tab = ft.Ref[ft.Column]()

    def show_tab(tab_name):
        if tab_name == "ร้านเด็ด":
            current_tab.current.controls = [create_card(r) for r in restaurants]
        elif tab_name == "สุ่มอาหาร":
            current_tab.current.controls = [create_card(r) for r in random_foods]
        elif tab_name == "กินตามดวง":
            current_tab.current.controls = [create_card(r) for r in zodiac_foods]
        page.update()

    # ปุ่มจำลองแท็บ
    tab_buttons = ft.Row(
        controls=[
            ft.ElevatedButton("ร้านเด็ด", on_click=lambda e: show_tab("ร้านเด็ด")),
            ft.ElevatedButton("สุ่มอาหาร", on_click=lambda e: show_tab("สุ่มอาหาร")),
            ft.ElevatedButton("กินตามดวง", on_click=lambda e: show_tab("กินตามดวง")),
        ],
        spacing=15,
    )

    # ---------- พื้นที่แสดงข้อมูล ----------
    tab_content = ft.Column(ref=current_tab, spacing=10)
    show_tab("ร้านเด็ด")  # ค่าเริ่มต้น

    # ---------- Layout ----------
    layout = ft.Container(
    content=ft.Column(
        [
            ft.Text("Edit Features", size=22, weight=ft.FontWeight.BOLD),
            ft.Container(tab_buttons, margin=ft.margin.only(bottom=15)),
            tab_content,
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    ),
    padding=20,  # ✅ ย้ายมาที่ Container แทน
    expand=True,
)


    return layout
