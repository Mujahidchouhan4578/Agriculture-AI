from services.pdf_reader import PDFReader

class PDFAgent:
    
    def __init__(self):
        self.reader=PDFReader()
        
    def execute(self,state):
        pdf_text=self.reader.read(state["pdf_path"])
        state["pdf_text"]=pdf_text
        
        return state
    