from PIL import Image


image_path = "C:/Users/softr/OneDrive/Desktop/Hero Battle/assets/warrior3_1.PNG"

image = Image.open(image_path)


left = 1056
top = 928
right = left + 104
bottom = top + 152

cropped_frame = image.crop((left, top, right, bottom))

cropped_path = "C:/Users/softr/OneDrive/Desktop/characters/warrior3/attack/4.png"

cropped_frame.save(cropped_path)

cropped_path
