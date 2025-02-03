import markdown
import os
from tkinter import filedialog, Tk
from tkinter import messagebox, ttk

class MarkdownConverterGUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("Markdown to HTML Converter")
        self.root.geometry("400x200")

        style = ttk.Style()
        style.configure('TButton', padding=6)
        style.configure('TLabel', padding=6)

        # Create and pack widgets
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill='both', expand=True)

        title_label = ttk.Label(main_frame, text="Markdown to HTML Converter", font=('Arial', 14, 'bold'))
        title_label.pack(pady=10)

        convert_button = ttk.Button(main_frame, text="Select Markdown File", command=self.convert_file)
        convert_button.pack(pady=20)

    def start(self):
        self.root.mainloop()

    def convert_file(self):
        try:
            convert_markdown_to_html()
            messagebox.showinfo("Success", "Conversion completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def convert_markdown_to_html():
    # Hide the main tkinter window
    root = Tk()
    root.withdraw()

    # Open file dialog to select markdown file
    input_file = filedialog.askopenfilename(
        title="Select Markdown file",
        filetypes=[("Markdown files", "*.md")]
    )

    if input_file:
        # Read the markdown content
        with open(input_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()

        # Convert markdown to HTML
        html_content = markdown.markdown(markdown_content)

        # Create HTML document with basic styling
        html_document = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Converted Markdown</title>
    <style>
        body {{ 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px;
            font-family: Arial, sans-serif;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>
"""

        # Get output filename
        output_file = os.path.splitext(input_file)[0] + '.html'

        # Write the HTML content to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_document)

        print(f"Conversion complete! HTML file saved as: {output_file}")
    else:
        print("No file selected.")

if __name__ == "__main__":
    try:
        convert_markdown_to_html()
    except Exception as e:
        print(f"An error occurred: {str(e)}")