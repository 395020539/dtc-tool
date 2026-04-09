
import flet as ft
import asyncio
from dtc_helper import hex_to_dtc, dtc_to_hex

def main(page: ft.Page):
    page.title = "DTC Tool (beta)"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 600
    page.window_height = 800
    page.window_resizable = True  # Allow resizing
    page.padding = 0
    page.update()  # Force update to apply window settings immediately

    async def show_toast(msg: str, duration: float = 1.2):
        box = ft.Container(
            content=ft.Text(msg, color=ft.Colors.ON_PRIMARY),
            bgcolor=ft.Colors.PRIMARY,
            padding=ft.Padding.symmetric(horizontal=12, vertical=8),
            border_radius=8,
            opacity=0.0,
            animate_opacity=300,
        )
        overlay = ft.Column(
            [ft.Row([box], alignment=ft.MainAxisAlignment.CENTER)],
            alignment=ft.MainAxisAlignment.END,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )
        page.overlay.append(overlay)
        box.opacity = 1.0
        page.update()
        await asyncio.sleep(duration)
        box.opacity = 0.0
        page.update()
        await asyncio.sleep(0.3)
        page.overlay.remove(overlay)
        page.update()

    # --- About Dialog ---
    def show_about(e):
        def close_dlg(e):
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
                ft.Text("基于 SAE J2012 标准的故障码转换工具，支持 【2 字节/3 字节十六进制内码】与 【5 位/7 位 DTC显示码】 之间的双向转换。", size=12, color=ft.Colors.GREY_600, selectable=True)
            ], tight=True, spacing=10, width=300),
            actions=[
                ft.TextButton("Close", on_click=close_dlg)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    # --- AppBar ---
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.Icons.AUTO_FIX_HIGH),
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

    # --- Single Conversion Tab ---
    hex_input = ft.TextField(label="Internal Code (Hex)", hint_text="e.g. 0120 or 0120FF", expand=True)
    dtc_input = ft.TextField(label="Standard DTC", hint_text="e.g. P0120 or P0120FF", expand=True)
    single_result_source = ft.Text(value="", size=12, color=ft.Colors.GREY_600)
    single_result_kind_text = ft.Text(value="", size=12, color=ft.Colors.ON_PRIMARY_CONTAINER)
    single_result_kind = ft.Container(
        content=single_result_kind_text,
        bgcolor=ft.Colors.PRIMARY_CONTAINER,
        border_radius=6,
        padding=ft.Padding.symmetric(horizontal=8, vertical=4),
        visible=False
    )
    single_result_text = ft.Text(value="", size=24, weight=ft.FontWeight.BOLD)
    single_result_container = ft.Container(
        content=ft.Column([
            single_result_source,
            ft.Row([single_result_text, single_result_kind], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
        ], spacing=6, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=15,
        bgcolor=ft.Colors.SURFACE_CONTAINER,
        border_radius=8,
        visible=False,
        alignment=ft.alignment.Alignment(0, 0),
        animate_opacity=300
    )

    def convert_to_dtc_single(e):
        if not hex_input.value: return
        res = hex_to_dtc(hex_input.value)
        single_result_source.value = "Source: Hex"
        single_result_kind_text.value = "DTC"
        single_result_kind.visible = True
        single_result_text.value = f"{res}"
        single_result_container.visible = True
        dtc_input.value = res if "Error" not in res else ""
        page.update()

    def convert_to_hex_single(e):
        if not dtc_input.value: return
        res = dtc_to_hex(dtc_input.value)
        single_result_source.value = "Source: DTC"
        single_result_kind_text.value = "HEX"
        single_result_kind.visible = True
        single_result_text.value = f"{res}"
        single_result_container.visible = True
        hex_input.value = res if "Error" not in res else ""
        page.update()

    single_tab_content = ft.Container(
        content=ft.Column([
            ft.Text("Single Conversion", size=20, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Row([
                hex_input,
                ft.IconButton(ft.Icons.ARROW_FORWARD, on_click=convert_to_dtc_single, tooltip="Convert to DTC")
            ]),
            ft.Row([
                dtc_input,
                ft.IconButton(ft.Icons.ARROW_BACK, on_click=convert_to_hex_single, tooltip="Convert to Hex")
            ]),
            ft.Container(height=20),
            single_result_container,
        ], spacing=20),
        padding=20
    )

    # --- Batch Conversion Tab ---
    batch_input = ft.TextField(
        label="Input Codes (One per line)",
        hint_text="e.g.\n0120\n4123AB\nP0120FF",
        multiline=True,
        min_lines=3,
        max_lines=8,
        expand=True
    )
    batch_output = ft.TextField(
        label="Results",
        multiline=True,
        min_lines=3,
        max_lines=8,
        read_only=True,
        expand=True
    )

    def process_batch(mode):
        lines = batch_input.value.strip().split("\n")
        results = []
        for line in lines:
            line = line.strip()
            if not line: continue
            if mode == "to_dtc":
                res = hex_to_dtc(line)
                results.append(f"{res}")
            else:
                res = dtc_to_hex(line)
                results.append(f"{res}")
        batch_output.value = "\n".join(results)
        page.update()

    async def copy_results(e):
        msg = "已复制到剪贴板" if batch_output.value else "没有可复制的结果"
        if batch_output.value:
            await ft.Clipboard().set(batch_output.value)
        await show_toast(msg)

    batch_tab_content = ft.Container(
        content=ft.Column([
            ft.Text("Batch Conversion", size=20, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            batch_input,
            ft.Row([
                ft.FilledButton("Batch Hex -> DTC", icon=ft.Icons.PLAY_ARROW, on_click=lambda _: process_batch("to_dtc"), expand=True),
                ft.FilledButton("Batch DTC -> Hex", icon=ft.Icons.PLAY_ARROW, on_click=lambda _: process_batch("to_hex"), expand=True),
            ], spacing=10),
            batch_output,
            ft.OutlinedButton("Copy All Results", icon=ft.Icons.COPY, on_click=copy_results, width=200),
        ], spacing=15, scroll=ft.ScrollMode.ADAPTIVE),
        padding=20
    )

    # --- Main Layout with Tabs ---
    single_btn = ft.FilledButton("Single Mode", icon=ft.Icons.LOOKS_ONE, on_click=lambda _: switch_mode(0), style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)))
    batch_btn = ft.FilledButton("Batch Mode", icon=ft.Icons.REORDER, on_click=lambda _: switch_mode(1), style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)))
    
    mode_row = ft.Row([single_btn, batch_btn], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
    content_container = ft.Container(content=single_tab_content, expand=True)

    def switch_mode(index):
        def apply_selected(btn, selected: bool):
            if selected:
                btn.bgcolor = ft.Colors.PRIMARY
                btn.color = ft.Colors.ON_PRIMARY
            else:
                btn.bgcolor = None
                btn.color = None

        if index == 0:
            content_container.content = single_tab_content
            apply_selected(single_btn, True)
            apply_selected(batch_btn, False)
        else:
            content_container.content = batch_tab_content
            apply_selected(single_btn, False)
            apply_selected(batch_btn, True)
        page.update()

    # Initial state
    switch_mode(0)

    page.add(
        ft.Container(content=mode_row, padding=10, bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
        content_container,
        ft.Container(
            content=ft.Row(
                [
                    ft.Text("v: beta", size=11, color=ft.Colors.GREY_400),
                    ft.Text("•", size=11, color=ft.Colors.GREY_300),
                    ft.Text("YangZL", size=11, color=ft.Colors.GREY_400),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8
            ),
            padding=ft.Padding.only(bottom=10)
        )
    )

if __name__ == "__main__":
    ft.run(main)
