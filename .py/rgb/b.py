from PIL import Image
for b in range(256):
    img = Image.new("RGB", (256, 256))
    for g in range(256):
        for r in range(256):
            img.putpixel((r, g), (r, g, b))
    img.save(f"b/{b}.png")
    img.close()
    print(b)