
import PyPDF2
import os

def pdf_to_text(pdf_file, save_directory):
    # Create the text file name based on the PDF file name
    base_name = os.path.splitext(os.path.basename(pdf_file))[0] + '.txt'
    text_file = os.path.join(save_directory, base_name)

    # Open the PDF file
    with open(pdf_file, 'rb') as file:
        # Create a PDF reader
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Open the text file for writing
        with open(text_file, 'w', encoding='utf-8') as output_file:
            # Iterate over each page
            for page_num in range(len(pdf_reader.pages)):
                # Extract text from the page
                page_text = pdf_reader.pages[page_num].extract_text()
                # Write the text to the text file
                output_file.write(f'Page {page_num + 1}:\n')
                output_file.write(page_text)
                output_file.write('\n\n')

    print(f'Text extracted and saved to {text_file}')

# Example usage
pdf_to_text('D:\Chatbot/Ranjupdf', 'D:\Chatbot\output') 
