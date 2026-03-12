
import flet as ft
from dtc_helper import hex_to_dtc, dtc_to_hex

def main(page: ft.Page):
    page.title = "DTC Tool (beta)"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 500
    page.window_height = 600
    page.window_resizable = True  # Allow resizing
    page.padding = 10
    page.update()  # Force update to apply window settings immediately

    # --- About Dialog ---
    def show_about(e):
        print("About button clicked")
        
        def close_dlg(e):
            print("Closing dialog")
            dlg.open = False
            page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("About DTC Tool"),
            content=ft.Column([
                ft.Text("Fault Code Converter"),
                ft.Divider(),
                ft.Row([ft.Text("Version:", color=ft.Colors.GREY), ft.Text("beta")]),
                ft.Row([ft.Text("Author:", color=ft.Colors.GREY), ft.Text("YangZL", weight=ft.FontWeight.BOLD)]),
                ft.Divider(),
                ft.Text("Based on SAE J2012 Standard", size=12, color=ft.Colors.GREY_600)
            ], tight=True, spacing=10, width=300),
            actions=[
                ft.TextButton("Close", on_click=close_dlg)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dlg)
        dlg.open = True
        page.update()
        print("Dialog opened via overlay")

    # --- AppBar ---
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.Icons.BUILD),
        leading_width=40,
        title=ft.Text("DTC Tool", weight=ft.FontWeight.BOLD),
        center_title=False,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        actions=[
            ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Text("beta", size=10, color=ft.Colors.ON_PRIMARY_CONTAINER),
                        bgcolor=ft.Colors.PRIMARY_CONTAINER,
                        border_radius=4,
                        padding=ft.Padding.symmetric(horizontal=4, vertical=2)
                    ),
                    ft.IconButton(ft.Icons.INFO_OUTLINE, tooltip="About", on_click=show_about)
                ], spacing=10),
                padding=ft.Padding.only(right=10)
            )
        ]
    )

    # --- DTC Converter Logic ---
    hex_input = ft.TextField(label="Internal Code (Hex)", hint_text="e.g. 0120", width=200)
    dtc_input = ft.TextField(label="Standard DTC", hint_text="e.g. P0120", width=200)
    result_text = ft.Text(value="", size=20, weight=ft.FontWeight.BOLD)
    result_container = ft.Container(
        content=result_text,
        padding=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER,
        border_radius=5,
        visible=False
    )

    def convert_to_dtc(e):
        res = hex_to_dtc(hex_input.value)
        result_text.value = f"DTC: {res}"
        result_container.visible = True
        dtc_input.value = res if "Error" not in res else ""
        page.update()

    def convert_to_hex(e):
        res = dtc_to_hex(dtc_input.value)
        result_text.value = f"Hex: {res}"
        result_container.visible = True
        hex_input.value = res if "Error" not in res else ""
        page.update()

    dtc_content = ft.Column([
        ft.Text("Fault Code Converter", size=24, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        ft.Row([
            hex_input,
            ft.FilledButton("Convert to DTC ->", on_click=convert_to_dtc)
        ]),
        ft.Row([
            dtc_input,
            ft.FilledButton("<- Convert to Hex", on_click=convert_to_hex)
        ]),
        ft.Divider(),
        result_container,
        ft.Text("Note: Supports SAE J2012 Standard Conversion (P/C/B/U codes)", color=ft.Colors.GREY)
    ], spacing=20, expand=True)

    page.add(ft.Container(content=dtc_content, padding=20, expand=True))
    
    # Footer (Simple, unobtrusive)
    page.add(
        ft.Container(
            content=ft.Row(
                [
                    ft.Text("v: beta", size=11, color=ft.Colors.GREY_400),
                    ft.Text("•", size=11, color=ft.Colors.GREY_300),
                    ft.Text("YangZL", size=11, color=ft.Colors.GREY_400, tooltip="Author"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8
            ),
            padding=ft.Padding.only(bottom=5)
        )
    )

if __name__ == "__main__":
    ft.run(main)
