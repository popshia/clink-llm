import os
import tkinter as tk
from tkinter import filedialog, messagebox

import fitz  # PyMuPDF
import markdownify
from docx import Document


# Function to convert Word to Markdown
def convert_word_to_md(file_path):
    try:
        doc = Document(file_path)
        md_text = ""
        for para in doc.paragraphs:
            md_text += para.text + "\n\n"
        return md_text
    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert Word document: {str(e)}")
        return None


# Function to convert PDF to Markdown (text-based)
def convert_pdf_to_md(file_path):
    try:
        pdf_doc = fitz.open(file_path)
        md_text = ""
        for page_num in range(pdf_doc.page_count):
            page = pdf_doc.load_page(page_num)
            text = page.get_text("text")
            md_text += text + "\n\n"
        return md_text
    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert PDF: {str(e)}")
        return None


# Function to save Markdown to file
def save_markdown(md_text, output_path):
    try:
        with open(output_path, "w", encoding="utf-8") as md_file:
            md_file.write(md_text)
        messagebox.showinfo(
            "Success",
            f"File successfully converted to Markdown!\nSaved at: {output_path}",
        )
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save Markdown file: {str(e)}")


# Function to handle file selection and conversion
def convert_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Word Files", "*.docx"), ("PDF Files", "*.pdf")]
    )

    if not file_path:
        return

    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == ".docx":
        md_text = convert_word_to_md(file_path)
    elif file_extension == ".pdf":
        md_text = convert_pdf_to_md(file_path)
    else:
        messagebox.showerror(
            "Error", "Unsupported file format. Please select a .docx or .pdf file."
        )
        return

    if md_text:
        output_path = filedialog.asksaveasfilename(
            defaultextension=".md", filetypes=[("Markdown Files", "*.md")]
        )
        if output_path:
            save_markdown(md_text, output_path)


# Create the GUI interface
def create_gui():
    root = tk.Tk()
    root.title("File to Markdown Converter")
    root.geometry("400x200")

    label = tk.Label(
        root,
        text="Select a Word (.docx) or PDF (.pdf) file to convert to Markdown",
        wraplength=300,
        justify="center",
    )
    label.pack(pady=20)

    convert_button = tk.Button(
        root, text="Select File", command=convert_file, width=20, height=2
    )
    convert_button.pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
