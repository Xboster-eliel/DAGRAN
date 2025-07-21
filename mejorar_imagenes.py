# archivo: mejorar_imagenes.py

from PIL import Image, ImageEnhance

def upscale_image(img: Image.Image, scale_factor: float = 2.0) -> Image.Image:
    """
    Aumenta la resolución de la imagen multiplicando sus dimensiones
    por `scale_factor` usando remuestreo de alta calidad (LANCZOS).
    """
    w, h = img.size
    new_size = (int(w * scale_factor), int(h * scale_factor))
    return img.resize(new_size, resample=Image.LANCZOS)

def enhance_image(
    img: Image.Image,
    contrast: float = 1.2,
    brightness: float = 1.1,
    color: float = 1.3,
    sharpness: float = 1.5
) -> Image.Image:
    """
    Ajusta la imagen aumentando:
      - contraste
      - brillo
      - saturación (color)
      - nitidez
    según los factores proporcionados.
    """
    img = ImageEnhance.Contrast(img).enhance(contrast)
    img = ImageEnhance.Brightness(img).enhance(brightness)
    img = ImageEnhance.Color(img).enhance(color)
    img = ImageEnhance.Sharpness(img).enhance(sharpness)
    return img

def process_image(
    img_path: str,
    scale_factor: float = 2.0,
    contrast: float = 1.2,
    brightness: float = 1.1,
    color: float = 1.3,
    sharpness: float = 1.5
) -> Image.Image:
    """
    Carga la imagen desde `img_path`, la remuestrea para aumentar
    resolución y luego aplica mejoras de contraste, brillo, color y nitidez.
    Retorna un objeto PIL.Image listo para mostrar.
    """
    img = Image.open(img_path)
    img = upscale_image(img, scale_factor=scale_factor)
    img = enhance_image(
        img,
        contrast=contrast,
        brightness=brightness,
        color=color,
        sharpness=sharpness
    )
    return img
