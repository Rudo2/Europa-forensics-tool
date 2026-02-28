import base64
import os

# Create the directory if it doesn't exist
os.makedirs('src/ui/assets', exist_ok=True)

# Save the image
with open('src/ui/assets/turtle_detective.png', 'wb') as f:
    f.write(base64.b64decode('YOUR_BASE64_IMAGE_DATA_HERE')) 