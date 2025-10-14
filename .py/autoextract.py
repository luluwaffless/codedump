import win32clipboard
import pyperclip
import pytesseract
from PIL import Image
import io
import time

def extract_text_from_image(image):
    text = pytesseract.image_to_string(image, lang='por')
    return text

def get_image_from_clipboard():
    with io.BytesIO() as output:
        try:
            win32clipboard.OpenClipboard()
            if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_DIB):
                data = win32clipboard.GetClipboardData(win32clipboard.CF_DIB)
                output.write(data)
                image = Image.open(output)
                image = image.convert("L")
                return image
            else:
                return None
        except Exception as e:
            print(str(e))
            return None
        finally:
            win32clipboard.CloseClipboard()

def main():
    print("Ctrl+C para sair.")
    try:
        while True:
            try:
                image = get_image_from_clipboard()
                if image is not None:
                    text = extract_text_from_image(image)
                    pyperclip.copy(text)
                    print("Copiado!")
            except Exception as e:
                print(str(e))
            time.sleep(1)
    except KeyboardInterrupt:
        print("Parando.")

if __name__ == "__main__":
    main()