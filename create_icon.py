from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # Create a new image with a transparent background
    size = 256
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Draw a blue circle for the background
    draw.ellipse((10, 10, size-10, size-10), fill=(52, 152, 219, 255))
    
    # Draw a magnifying glass
    draw.ellipse((80, 80, 176, 176), outline=(255, 255, 255, 255), width=15)
    draw.line((160, 160, 200, 200), fill=(255, 255, 255, 255), width=15)
    
    # Draw the letter "E" for EUROPA
    try:
        font = ImageFont.truetype("arial.ttf", 120)
    except:
        font = ImageFont.load_default()
    
    draw.text((90, 70), "E", fill=(255, 255, 255, 255), font=font)
    
    # Save the image as ICO
    image.save("icon.ico", format="ICO")
    
    print("Icon created successfully!")

if __name__ == "__main__":
    create_icon() 