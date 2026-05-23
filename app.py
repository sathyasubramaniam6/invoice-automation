import tkinter as tk
from tkinter import filedialog
import pytesseract
from PIL import Image
import pandas as pd
import sys
import os

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def process_image():
    try:
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
        )

        if not file_path:
            return

        # Load image safely
        try:
            with Image.open(file_path) as img:
                image = img.copy()
        except Exception as e:
            status_label.config(text=f"❌ Image Error: {str(e)}")
            return

        status_label.config(text=f"Processing...")

        text = pytesseract.image_to_string(image)

        data = {}
        for line in text.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                data[key.strip()] = value.strip()

        df = pd.DataFrame([data])

        # Get EXE folder path
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(__file__)

        output_path = os.path.join(base_path, "output.xlsx")

        df.to_excel(output_path, index=False)

        status_label.config(text=f"✅ Saved at: {output_path}")

    except Exception as e:
        status_label.config(text=f"❌ Error: {str(e)}")


# UI Window
root = tk.Tk()
root.title("Image to Excel Converter")
root.geometry("300x200")

btn = tk.Button(root, text="Upload Image", command=process_image)
btn.pack(pady=20)

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()