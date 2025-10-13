import flet as ft
from utils.colors import AppColors
import json, os
from utils.global_state import get_edit_data, clear_edit_data


def edit_feature_detail_view(page: ft.Page):
    """หน้าแก้ไขข้อมูลร้าน + เมนูแนะนำ"""

    item, feature_name = get_edit_data()

    if not item or not feature_name:
        return ft.Text("❌ ไม่พบข้อมูลที่ต้องการแก้ไข", color="red")

    json_path = os.path.join(os.path.dirname(__file__), "../data/features_data.json")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # ----------------------------- [ SECTION 1 : ข้อมูลร้าน ] -----------------------------
    store_name_field = ft.TextField(label="ชื่อร้าน", value=item.get("store_name", ""), width=400)
    store_detail_field = ft.TextField(
        label="รายละเอียดร้าน / รีวิว / ที่อยู่", 
        value=item.get("store_detail", ""), 
        width=400, multiline=True
    )
    store_image_field = ft.TextField(label="ลิงก์รูปภาพร้าน", value=item.get("image", ""), width=400)
    store_preview_img = ft.Image(src=item.get("image", ""), width=320, height=200, fit="cover")

    def update_store_preview(e):
        store_preview_img.src = store_image_field.value
        page.update()

    store_image_field.on_change = update_store_preview

    # ----------------------------- [ SECTION 2 : เมนูแนะนำ ] -----------------------------
    menus = item.get("menus", [])

    def create_menu_card(menu):
        def update_preview(e):
            menu_preview.src = menu_image_field.value
            page.update()

        menu_name_field = ft.TextField(label="ชื่อเมนู", value=menu.get("name", ""), width=300)
        menu_image_field = ft.TextField(label="ลิงก์รูปภาพเมนู", value=menu.get("image", ""), width=300)
        menu_preview = ft.Image(src=menu.get("image", ""), width=200, height=150, fit="cover")

        menu_image_field.on_change = update_preview

        def delete_menu(e):
            menus.remove(menu)
            refresh_menu_list()

        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.TextField(label="ชื่อเมนู", value=menu.get("name", ""), width=300, on_change=lambda ev: menu.update({"name": ev.control.value})),
                            ft.IconButton(icon=ft.Icons.DELETE, icon_color="red", on_click=delete_menu),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.TextField(label="ลิงก์รูปภาพเมนู", value=menu.get("image", ""), width=400, on_change=lambda ev: menu.update({"image": ev.control.value})),
                    ft.Image(src=menu.get("image", ""), width=200, height=150, fit="cover"),
                ],
                spacing=8,
            ),
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10,
            padding=10,
            bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.ORANGE_100),
        )

    menu_list_column = ft.Column([create_menu_card(m) for m in menus], spacing=10)

    def refresh_menu_list():
        menu_list_column.controls = [create_menu_card(m) for m in menus]
        page.update()

    def add_menu(e):
        new_menu = {"name": "ชื่อเมนูใหม่", "image": "assets/sample.jpg"}
        menus.append(new_menu)
        refresh_menu_list()

    add_menu_btn = ft.ElevatedButton(
        "+ เพิ่มเมนูแนะนำ",
        icon=ft.Icons.ADD,
        bgcolor=AppColors.PRIMARY,
        color="white",
        on_click=add_menu,
    )

    # ----------------------------- [ SAVE FUNCTION ] -----------------------------
    def save_and_back(e):
        item["store_name"] = store_name_field.value
        item["store_detail"] = store_detail_field.value
        item["image"] = store_image_field.value
        item["menus"] = menus  # บันทึกเมนูทั้งหมด

        mapping = {
            "ร้านเด็ด": "restaurants",
            "สุ่มอาหาร": "random_foods",
            "กินตามดวง": "zodiac_foods",
            "ร้านใกล้ฉัน": "nearby_shops",
            "หมวดหมู่": "categories",
            "กินตามสีวัน": "color_day",
        }

        key = mapping[feature_name]
        items = data[key]

        # อัปเดต JSON
        updated = False
        for i, entry in enumerate(items):
            if entry["name"] == item["name"]:
                items[i] = item
                updated = True
                break
        if not updated:
            items.append(item)

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        clear_edit_data()
        page.go("/edit_features")

    # ----------------------------- [ LAYOUT ทั้งหมด ] -----------------------------
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(f"แก้ไขข้อมูล ({feature_name})", size=22, weight=ft.FontWeight.BOLD),

                # SECTION 1: ข้อมูลร้าน
                ft.Text("ข้อมูลร้าน", size=18, weight=ft.FontWeight.BOLD, color=AppColors.SECONDARY),
                ft.Divider(),
                store_name_field,
                store_detail_field,
                store_image_field,
                ft.Text("ตัวอย่างรูปภาพร้าน", size=14, color="#888888"),
                store_preview_img,
                ft.Divider(),

                # SECTION 2: เมนูแนะนำ
                ft.Text("เมนูแนะนำ", size=18, weight=ft.FontWeight.BOLD, color=AppColors.SECONDARY),
                ft.Divider(),
                menu_list_column,
                add_menu_btn,

                ft.Container(height=20),
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "บันทึก",
                            icon=ft.Icons.SAVE,
                            bgcolor=AppColors.PRIMARY,
                            color="white",
                            on_click=save_and_back,
                        ),
                        ft.OutlinedButton(
                            "ย้อนกลับ",
                            icon=ft.Icons.ARROW_BACK,
                            on_click=lambda e: page.go("/edit_features"),
                        ),
                    ],
                    spacing=10,
                ),
            ],
            spacing=15,
        ),
        padding=20,
        expand=True,
    )
