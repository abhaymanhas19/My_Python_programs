def read_pdf(dat):
    # from pymupdf4llm import PyMuPDFParser
    import pymupdf4llm
    try:
        # parser = PyMuPDFParser()
        text = pymupdf4llm.to_markdown(dat)
        return text
    except Exception as e:
        print(f"An error occurred while reading the PDF: {e}")
        return ""


with open('/home/jarvis/Documents/7.pdf', 'rb') as file_obj:
        extracted_text = read_pdf(file_obj)
        print(extracted_text)