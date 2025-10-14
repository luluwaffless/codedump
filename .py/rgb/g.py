from PIL import Image
for g in range(256):
    img = Image.new("RGB", (256, 256))
    for r in range(256):
        for b in range(256):
            img.putpixel((r, b), (r, g, b))
    img.save(f"g/{g}.png")
    img.close()
    print(g)