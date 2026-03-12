from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # Create a new image with a transparent background
    size = (256, 256)
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw a rounded rectangle (like an app icon)
    # Background color: Blue-ish (Google Material Design Blue 500: #2196F3)
    bg_color = (33, 150, 243, 255)
    
    # Draw a circle/rounded rect
    margin = 20
    draw.ellipse([margin, margin, size[0]-margin, size[1]-margin], fill=bg_color)

    # Draw Text "DTC"
    try:
        # Try to use a default font
        font = ImageFont.truetype("arial.ttf", 80)
    except IOError:
        font = ImageFont.load_default()

    text = "DTC"
    
    # Calculate text position to center it
    # getbbox returns (left, top, right, bottom)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size[0] - text_width) / 2
    y = (size[1] - text_height) / 2 - 10 # Slightly adjust up

    draw.text((x, y), text, fill="white", font=font)

    # Save as .ico
    # Windows icons usually contain multiple sizes
    icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    img.save('app_icon.ico', format='ICO', sizes=icon_sizes)
    print(f"Icon created: {os.path.abspath('app_icon.ico')}")

if __name__ == "__main__":
    create_icon()
