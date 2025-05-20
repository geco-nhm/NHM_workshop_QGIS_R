from googletrans import Translator
import time

INPUT_FILE = "QGIS_2025_nhm_images.md"
OUTPUT_FILE = "QGIS_2025_nhm_images_EN.md"
MAX_CHARS = 4500  # Google has a limit of ~5000 chars per request

translator = Translator()

def split_text(text, max_chars):
    lines = text.splitlines()
    chunks = []
    chunk = []
    current_len = 0

    for line in lines:
        line_len = len(line) + 1
        if current_len + line_len > max_chars:
            chunks.append("\n".join(chunk))
            chunk = []
            current_len = 0
        chunk.append(line)
        current_len += line_len
    if chunk:
        chunks.append("\n".join(chunk))
    return chunks

def translate_chunk(chunk):
    try:
        result = translator.translate(chunk, src='no', dest='en')
        return result.text
    except Exception as e:
        print("Error:", e)
        return f"[Translation error: {e}]"

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        text = f.read()

    chunks = split_text(text, MAX_CHARS)
    print(f"📝 Translating {len(chunks)} chunks...")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f_out:
        for i, chunk in enumerate(chunks):
            print(f"🔁 Translating chunk {i+1}/{len(chunks)}...")
            translated = translate_chunk(chunk)
            f_out.write(translated + "\n\n")
            time.sleep(1.0)  # Optional: be nice to the server
    print(f"\n✅ Translation complete! Output written to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
