import openai
import time
import os
from dotenv import load_dotenv

# Set your API key (or use an environment variable)
load_dotenv()  # Load variables from .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


INPUT_FILE = "QGIS_2025_nhm_images.md"
OUTPUT_FILE = "QGIS_2025_nhm_images_EN.md"
MODEL = "gpt-3.5-turbo"
MAX_CHARS = 2000

def split_text(text, max_chars):
    lines = text.splitlines()
    chunks = []
    chunk = []
    current_len = 0

    for line in lines:
        if current_len + len(line) + 1 > max_chars and chunk:
            chunks.append("\n".join(chunk))
            chunk = []
            current_len = 0
        chunk.append(line)
        current_len += len(line) + 1
    if chunk:
        chunks.append("\n".join(chunk))
    return chunks

def translate_chunk(chunk):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Translate the following Markdown content from Norwegian to English. "
                        "Preserve all formatting including headers, bullet points, code blocks, images, and links:\n\n"
                        + chunk
                    ),
                }
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception as e:
        print("Error:", e)
        return f"\n\n[Translation error: {e}]\n\n"

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
            time.sleep(1.5)  # Rate limiting
    print(f"\n✅ Translation complete! Output written to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
