import flet as ft
from utils.colors import AppColors
import json, os
from utils.global_state import set_edit_data

def edit_features_view(page: ft.Page):
    """หน้า Edit Features"""

    # ---------- โหลดข้อมูลจาก JSON ----------
    json_path = os.path.join(os.path.dirname(__file__), "../data/features_data.json")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # ---------- ดึงข้อมูลแต่ละฟีเจอร์ ----------
    features = {
        "ร้านเด็ด": data.get("restaurants", []),
        "สุ่มอาหาร": data.get("random_foods", []),
        "กินตามดวง": data.get("zodiac_foods", []),
        "ร้านใกล้ฉัน": data.get("nearby_shops", []),
        "หมวดหมู่": data.get("categories", []),
        "กินตามสีวัน": data.get("color_day", []),
    }

    # ---------- ฟังก์ชันบันทึก JSON ----------
    def save_json():
        data.update({
            "restaurants": features["ร้านเด็ด"],
            "random_foods": features["สุ่มอาหาร"],
            "zodiac_foods": features["กินตามดวง"],
            "nearby_shops": features["ร้านใกล้ฉัน"],
            "categories": features["หมวดหมู่"],
            "color_day": features["กินตามสีวัน"],
        })
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # ---------- ฟังก์ชันเปิดหน้าแก้ไข ----------
    def open_edit_page(item, feature_name):
        """เปิดหน้าใหม่เพื่อแก้ไขรายละเอียด"""
        set_edit_data(item, feature_name)
        page.go("/edit_feature_detail")

    # ---------- ฟังก์ชันสร้างการ์ด ----------
    def create_card(item, feature_name):
        def delete_item(e):
            confirm = ft.AlertDialog(
                title=ft.Text("ยืนยันการลบ"),
                content=ft.Text(f"ต้องการลบ '{item['name']}' ใช่หรือไม่?"),
                actions=[
                    ft.TextButton("ยกเลิก", on_click=lambda ev: close_confirm()),
                    ft.TextButton("ลบ", on_click=lambda ev: confirm_delete()),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )

            def close_confirm():
                confirm.open = False
                page.update()

            def confirm_delete():
                features[feature_name].remove(item)
                save_json()
                confirm.open = False
                show_tab(feature_name)
                page.update()

            page.dialog = confirm
            confirm.open = True
            page.update()

        return ft.Container(
            content=ft.Row(
                [
                    ft.Image(
                        src=item.get("image", "assets/sample.jpg"),
                        width=180,
                        height=140,
                        fit="cover",
                        border_radius=10,
                    ),
                    ft.Container(width=15),
                    ft.Column(
                        [
                            ft.Text(item["name"], size=16, weight=ft.FontWeight.BOLD, color=AppColors.SECONDARY),
                            ft.Text(item["detail"], size=13, color=AppColors.TEXT_SECONDARY),
                            ft.Row(
                                [
                                    ft.ElevatedButton(
                                        "แก้ไข", icon=ft.Icons.EDIT, height=35,
                                        bgcolor=ft.Colors.BLUE_100,
                                        color=AppColors.SECONDARY,
                                        on_click=lambda e: open_edit_page(item, feature_name),
                                    ),
                                    ft.ElevatedButton(
                                        "ลบ", icon=ft.Icons.DELETE,
                                        bgcolor=ft.Colors.RED_200, height=35,
                                        on_click=delete_item
                                    ),
                                ],
                                spacing=10,
                            ),
                        ],
                        spacing=6,
                    ),
                ],
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            padding=20,
            border=ft.border.all(1, ft.Colors.GREY_300),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=6,
                color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
        )

    # ---------- เพิ่มข้อมูลใหม่ ----------
    def add_new_item(e):
        new_item = {"name": "ชื่อใหม่", "detail": "รายละเอียดใหม่", "image": "assets/sample.jpg"}
        features[current_feature.value].append(new_item)
        save_json()
        show_tab(current_feature.value)

    # ---------- ฟังก์ชันสลับแท็บ ----------
    current_feature = ft.Ref[str]()
    current_feature.value = "ร้านเด็ด"
    current_tab = ft.Ref[ft.Column]()

    def show_tab(feature_name):
        current_feature.value = feature_name
        for btn in tab_buttons.controls:
            is_active = btn.data == feature_name
            btn.style = ft.ButtonStyle(
                bgcolor=ft.Colors.ORANGE_100 if is_active else ft.Colors.WHITE,
                color=AppColors.SECONDARY if is_active else "#666666",
                shape=ft.RoundedRectangleBorder(radius=10),
            )
        current_tab.current.controls = [create_card(r, feature_name) for r in features[feature_name]]
        page.update()

    # ---------- ปุ่มแท็บ ----------
    tab_buttons = ft.Row(
        controls=[
            ft.ElevatedButton(
                content=ft.Text(name, size=14),
                data=name,
                on_click=lambda e, n=name: show_tab(n),
                style=ft.ButtonStyle(
                    padding=ft.padding.symmetric(horizontal=20, vertical=10),
                    bgcolor=ft.Colors.WHITE,
                    color="#666666",
                    shape=ft.RoundedRectangleBorder(radius=10),
                ),
            )
            for name in features.keys()
        ],
        spacing=12,
    )

    # ---------- ปุ่มเพิ่ม ----------
    add_button = ft.ElevatedButton(
        "+ เพิ่มข้อมูลใหม่",
        icon=ft.Icons.ADD,
        bgcolor=AppColors.PRIMARY,
        color=ft.Colors.WHITE,
        height=45,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
        ),
        on_click=add_new_item,
    )

    # ---------- พื้นที่เนื้อหา ----------
    tab_content = ft.Column(ref=current_tab, spacing=10)
    show_tab("ร้านเด็ด")

    # ---------- Layout ----------
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Edit Features", size=22, weight=ft.FontWeight.BOLD),
                tab_buttons,
                ft.Container(height=10),
                add_button,
                ft.Container(height=10),
                tab_content,
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        ),
        padding=20,
        expand=True,
    )
