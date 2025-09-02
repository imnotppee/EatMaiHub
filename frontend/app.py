import flet as ft

def main(page: ft.Page):
    page.title = "Flet Navigation Demo"
    page.theme_mode = "light"

    def route_change(e):
        page.views.clear()

        # หน้าแรก
        if page.route == "/":
            page.views.append(
                ft.View(
                    "/",
                    controls=[
                        ft.AppBar(title=ft.Text("Home"), bgcolor="blue"),
                        ft.Text("นี่คือหน้าแรก"),
                        ft.IconButton(ft.Icons.ARROW_FORWARD, on_click=lambda _: page.go("/second"))
                    ],
                )
            )

        # หน้าที่สอง
        elif page.route == "/second":
            page.views.append(
                ft.View(
                    "/second",
                    controls=[
                        ft.AppBar(title=ft.Text("Second Page"), bgcolor="green"),
                        ft.Text("หน้านี้คือ Second Page"),
                        ft.IconButton(ft.Icons.HOME, on_click=lambda _: page.go("/"))
                    ],
                )
            )

        page.update()

    # callback เมื่อกดปุ่ม back (เช่นในมือถือ/เว็บ browser)
    def view_pop(e):
        page.views.pop()
        page.go(page.views[-1].route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # เริ่มต้นไปหน้าแรก
    page.go(page.route)

ft.app(target=main)
