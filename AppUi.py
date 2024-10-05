import tkinter as tk
from tkinter import filedialog, messagebox
import requests

def upload_pdf():
    pdf_file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if pdf_file_path:
        with open(pdf_file_path, 'D:\Chatbot.Ranju.pdf') as pdf_file:
            try:
                response = requests.post('http://127.0.0.1:5000/convert_pdf', files={'file': pdf_file})
                if response.status_code == 200:
                    messagebox.showinfo("Success", "PDF uploaded and processed successfully!")
                else:
                    messagebox.showerror("Error", "Failed to process the PDF.")
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("Chatbot PDF Uploader")

# Create a button to upload PDF
upload_button = tk.Button(root, text="Upload PDF", command=upload_pdf)
upload_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
