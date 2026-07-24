"""
wallpaper_engine.py - Motor de fondo de pantalla de KALMIYA
Genera y aplica un fondo de pantalla personalizado estilo HUD militar.
"""

import ctypes
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_OK = True
except ImportError:
    PIL_OK = False
    print("[WALLPAPER] Pillow no disponible.")
    sys.exit(1)

try:
    import psutil
    PSUTIL_OK = True
except ImportError:
    PSUTIL_OK = False

WALLPAPER_W = 1920
WALLPAPER_H = 1080
OUTPUT_PATH = Path(__file__).parent / "kalmiya_wallpaper.png"

C_BG          = (10, 10, 26)
C_SECONDARY   = (0, 26, 46)
C_ACCENT      = (0, 242, 255)
C_ACCENT_DIM  = (0, 77, 85)
C_WHITE       = (255, 255, 255)
C_DIM         = (136, 136, 136)
C_SUCCESS     = (0, 255, 136)
C_WARNING     = (255, 170, 0)
C_DANGER      = (255, 68, 68)


def _load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "C:/Windows/Fonts/consolab.ttf" if bold else "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/courbd.ttf" if bold else "C:/Windows/Fonts/cour.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except (IOError, OSError):
            continue
    return ImageFont.load_default()


def _draw_grid(draw: ImageDraw.Draw, w: int, h: int):
    for x in range(0, w, 80):
        draw.line([(x, 0), (x, h)], fill=(5, 15, 25), width=1)
    for y in range(0, h, 80):
        draw.line([(0, y), (w, y)], fill=(5, 15, 25), width=1)
    for x in range(0, w, 400):
        draw.line([(x, 0), (x, h)], fill=(0, 40, 55), width=1)
    for y in range(0, h, 400):
        draw.line([(0, y), (w, y)], fill=(0, 40, 55), width=1)


def _draw_corner_decorations(draw: ImageDraw.Draw, w: int, h: int):
    margin = 40
    arm = 120
    color = C_ACCENT
    dim = C_ACCENT_DIM
    for (ox, oy, dx, dy) in [(margin, margin, 1, 1), (w - margin, margin, -1, 1),
                              (margin, h - margin, 1, -1), (w - margin, h - margin, -1, -1)]:
        draw.line([(ox, oy), (ox + dx * arm, oy)], fill=color, width=2)
        draw.line([(ox, oy), (ox, oy + dy * arm)], fill=color, width=2)
        sq = 6
        draw.rectangle([(ox - sq // 2, oy - sq // 2), (ox + sq // 2, oy + sq // 2)], fill=color)
        for i in range(1, 4):
            tx = ox + dx * (arm * i // 4)
            ty = oy + dy * (arm * i // 4)
            draw.line([(tx, oy - 4 * dy), (tx, oy + 4 * dy)], fill=dim, width=1)
            draw.line([(ox - 4 * dx, ty), (ox + 4 * dx, ty)], fill=dim, width=1)


def _draw_center_watermark(draw: ImageDraw.Draw, w: int, h: int):
    font = _load_font(220, bold=True)
    text = "KALMIYA"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (w - tw) // 2
    y = (h - th) // 2 - 40
    for offset in range(6, 0, -1):
        draw.text((x + offset, y + offset), text, font=font, fill=(0, 60, 70))
        draw.text((x - offset, y + offset), text, font=font, fill=(0, 60, 70))
    draw.text((x, y), text, font=font, fill=(0, 80, 90))


def _draw_hud_frame(draw: ImageDraw.Draw, w: int, h: int):
    mx, my = 60, 50
    draw.rectangle([(mx, my), (w - mx, h - my)], outline=C_ACCENT_DIM, width=1)
    arm = 80
    for (x1, y1, x2, y2, x3, y3) in [
        (mx, my, mx + arm, my, mx, my + arm),
        (w - mx, my, w - mx - arm, my, w - mx, my + arm),
        (mx, h - my, mx + arm, h - my, mx, h - my - arm),
        (w - mx, h - my, w - mx - arm, h - my, w - mx, h - my - arm),
    ]:
        draw.line([(x1, y1), (x2, y2)], fill=C_ACCENT, width=2)
        draw.line([(x1, y1), (x3, y3)], fill=C_ACCENT, width=2)


def _draw_top_bar(draw: ImageDraw.Draw, w: int, h: int, now: datetime):
    bar_y, bar_h = 50, 36
    draw.rectangle([(60, bar_y), (w - 60, bar_y + bar_h)], fill=(0, 15, 25))
    font_bar = _load_font(14, bold=True)
    font_small = _load_font(11)
    draw.text((80, bar_y + 10), "KALMIYA NEURAL CORE v3.5", font=font_bar, fill=C_ACCENT)
    full_str = now.strftime("%A, %d de %B de %Y").upper() + "  " + now.strftime("%H:%M:%S")
    bbox = draw.textbbox((0, 0), full_str, font=font_small)
    tw = bbox[2] - bbox[0]
    draw.text((w - 80 - tw, bar_y + 12), full_str, font=font_small, fill=C_DIM)
    draw.line([(60, bar_y + bar_h), (w - 60, bar_y + bar_h)], fill=C_ACCENT_DIM, width=1)


def _draw_bottom_bar(draw: ImageDraw.Draw, w: int, h: int):
    bar_y, bar_h = h - 86, 36
    draw.rectangle([(60, bar_y), (w - 60, bar_y + bar_h)], fill=(0, 15, 25))
    draw.line([(60, bar_y), (w - 60, bar_y)], fill=C_ACCENT_DIM, width=1)
    font_bar = _load_font(13, bold=True)
    font_small = _load_font(11)
    draw.text((80, bar_y + 10),
              "SARA KERRIGAN  -  USUARIO AUTORIZADO  NIVEL DE ACCESO: CLASE S",
              font=font_bar, fill=C_ACCENT)
    status = "TODOS LOS SISTEMAS OPERATIVOS  CIFRADO ACTIVO  CANAL SEGURO"
    bbox = draw.textbbox((0, 0), status, font=font_small)
    tw = bbox[2] - bbox[0]
    draw.text((w - 80 - tw, bar_y + 12), status, font=font_small, fill=C_DIM)


def _get_system_stats() -> dict:
    stats = {"cpu": 0.0, "ram": 0.0, "ram_used": 0.0, "ram_total": 0.0,
             "disk": 0.0, "disk_used": 0.0, "disk_total": 0.0}
    if not PSUTIL_OK:
        return stats
    try:
        stats["cpu"] = psutil.cpu_percent(interval=0.5)
        vm = psutil.virtual_memory()
        stats["ram"] = vm.percent
        stats["ram_used"] = vm.used / (1024 ** 3)
        stats["ram_total"] = vm.total / (1024 ** 3)
        drive = "C:\\" if sys.platform == "win32" else "/"
        du = psutil.disk_usage(drive)
        stats["disk"] = du.percent
        stats["disk_used"] = du.used / (1024 ** 3)
        stats["disk_total"] = du.total / (1024 ** 3)
    except Exception as e:
        print(f"[WALLPAPER] Error stats: {e}")
    return stats


def _draw_stats_panel(draw: ImageDraw.Draw, w: int, h: int, stats: dict):
    px, py, pw, ph = 80, h - 260, 340, 160
    draw.rectangle([(px, py), (px + pw, py + ph)], fill=(0, 10, 20), outline=C_ACCENT_DIM, width=1)
    font_title = _load_font(11, bold=True)
    font_label = _load_font(10)
    draw.text((px + 10, py + 8), "ESTADO DEL SISTEMA", font=font_title, fill=C_ACCENT_DIM)
    draw.line([(px + 10, py + 24), (px + pw - 10, py + 24)], fill=C_ACCENT_DIM, width=1)
    rows = [
        ("CPU", f"{stats['cpu']:.1f}%", stats['cpu'] / 100),
        ("RAM", f"{stats['ram']:.1f}%  ({stats['ram_used']:.1f}/{stats['ram_total']:.1f} GB)", stats['ram'] / 100),
        ("DISCO", f"{stats['disk']:.1f}%  ({stats['disk_used']:.0f}/{stats['disk_total']:.0f} GB)", stats['disk'] / 100),
    ]
    bar_w, bar_h_px, row_h = 160, 8, 38
    for i, (label, value_str, fraction) in enumerate(rows):
        ry = py + 32 + i * row_h
        draw.text((px + 10, ry), label + ":", font=font_label, fill=C_DIM)
        bx, by = px + 70, ry + 2
        draw.rectangle([(bx, by), (bx + bar_w, by + bar_h_px)], fill=(0, 20, 30))
        fw = int(bar_w * min(fraction, 1.0))
        if fw > 0:
            bc = C_DANGER if fraction > 0.85 else C_WARNING if fraction > 0.70 else C_ACCENT
            draw.rectangle([(bx, by), (bx + fw, by + bar_h_px)], fill=bc)
        draw.text((bx + bar_w + 8, ry), value_str, font=font_label, fill=C_ACCENT)


def _draw_right_panel(draw: ImageDraw.Draw, w: int, h: int, now: datetime):
    pw, ph = 340, 160
    px, py = w - 80 - pw, h - 260
    draw.rectangle([(px, py), (px + pw, py + ph)], fill=(0, 10, 20), outline=C_ACCENT_DIM, width=1)
    font_title = _load_font(11, bold=True)
    font_val = _load_font(12, bold=True)
    font_label = _load_font(10)
    draw.text((px + 10, py + 8), "INFORMACION DE SESION", font=font_title, fill=C_ACCENT_DIM)
    draw.line([(px + 10, py + 24), (px + pw - 10, py + 24)], fill=C_ACCENT_DIM, width=1)
    for i, (label, value) in enumerate([
        ("USUARIO", "Sara Kerrigan"),
        ("SISTEMA", "KALMIYA v3.5"),
        ("ESTADO", "OPERATIVO"),
        ("SESION", now.strftime("%d/%m/%Y %H:%M")),
    ]):
        ry = py + 32 + i * 28
        draw.text((px + 10, ry), f"{label}:", font=font_label, fill=C_DIM)
        vc = C_SUCCESS if value == "OPERATIVO" else C_ACCENT
        draw.text((px + 110, ry), value, font=font_val, fill=vc)


def generate_wallpaper(output_path: Optional[str] = None) -> str:
    if output_path is None:
        output_path = str(OUTPUT_PATH)
    print(f"[WALLPAPER] Generando fondo ({WALLPAPER_W}x{WALLPAPER_H})...")
    now = datetime.now()
    stats = _get_system_stats()
    img = Image.new("RGB", (WALLPAPER_W, WALLPAPER_H), C_BG)
    draw = ImageDraw.Draw(img)
    _draw_grid(draw, WALLPAPER_W, WALLPAPER_H)
    _draw_center_watermark(draw, WALLPAPER_W, WALLPAPER_H)
    _draw_hud_frame(draw, WALLPAPER_W, WALLPAPER_H)
    _draw_corner_decorations(draw, WALLPAPER_W, WALLPAPER_H)
    _draw_top_bar(draw, WALLPAPER_W, WALLPAPER_H, now)
    _draw_bottom_bar(draw, WALLPAPER_W, WALLPAPER_H)
    _draw_stats_panel(draw, WALLPAPER_W, WALLPAPER_H, stats)
    _draw_right_panel(draw, WALLPAPER_W, WALLPAPER_H, now)
    img.save(output_path, "PNG")
    print(f"[WALLPAPER] Guardado en: {output_path}")
    return output_path


def set_wallpaper(image_path: str) -> bool:
    if sys.platform != "win32":
        print("[WALLPAPER] Solo compatible con Windows.")
        return False
    try:
        abs_path = str(Path(image_path).resolve())
        result = ctypes.windll.user32.SystemParametersInfoW(0x0014, 0, abs_path, 0x0003)
        if result:
            print(f"[WALLPAPER] Fondo aplicado: {abs_path}")
            return True
        print("[WALLPAPER] Error al aplicar el fondo.")
        return False
    except Exception as e:
        print(f"[WALLPAPER] Excepcion: {e}")
        return False


def update_wallpaper(output_path: Optional[str] = None) -> bool:
    try:
        path = generate_wallpaper(output_path)
        return set_wallpaper(path)
    except Exception as e:
        print(f"[WALLPAPER] Error: {e}")
        return False


if __name__ == "__main__":
    print("\n  KALMIYA WALLPAPER ENGINE\n")
    success = update_wallpaper()
    if success:
        print("[WALLPAPER] Fondo de pantalla actualizado correctamente.")
    else:
        print(f"[WALLPAPER] Imagen guardada en: {OUTPUT_PATH}")
