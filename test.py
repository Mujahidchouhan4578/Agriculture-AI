from services.pdf_reader import PDFReader

def test():
    reader=PDFReader()
    text=reader.read("reports/sample.pdf")
    print(text)
    
    
test()