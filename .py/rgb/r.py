from PIL import Image
for r in range(256):
    img = Image.new("RGB", (256, 256))
    for g in range(256):
        for b in range(256):
            img.putpixel((g, b), (r, g, b))
    img.save(f"r/{r}.png")
    img.close()
    print(r)