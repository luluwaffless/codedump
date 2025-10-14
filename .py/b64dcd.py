import base64

def decode_base64_multicharset(string):
    string = string.strip()
    try:
        raw_bytes = base64.b64decode(string)
    except Exception as e:
        print(f"❌ invalid base64 input: {e}")
        return
    print(f"decoded {len(raw_bytes)} raw bytes")
    for enc in ["utf-8", "ascii", "latin-1" "iso-8859-1", "windows-1252", "utf-16", "utf-16le", "utf-16be", "utf-32"]:
        try:
            decoded = raw_bytes.decode(enc)
            print(f"✅ {enc} -> {decoded!r}")
        except Exception as e:
            print(f"❌ {enc}: {e}")

b64_input = input("enter base64 string: ").strip()
decode_base64_multicharset(b64_input)