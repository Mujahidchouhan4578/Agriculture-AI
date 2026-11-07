from llm.client import llm

class LLMServices:
    
    def __init__(self):
        self.llm=llm
        
    def ask(self,prompt):
        
        try:
            
            response=self.llm.invoke(prompt)
        
            return response.content
        
        except Exception as e:
            print(e)
            
            return None