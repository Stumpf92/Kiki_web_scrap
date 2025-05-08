import ollama

class Ai:


    def __init__(self, name, seed):        
        self.client = ollama.Client()
        self.model = name
        self.seed = seed
        self.history = []
        
    def prompt(self, request):
        self.request = request 
        self.response = ollama.chat(model=self.model,
                                    messages=[{    
                                        'role': 'user',
                                        'content': self.request,
                                        },],
                                    options={'seed': self.seed}
                                        )
        self.history.append({"request": self.request, "response": self.response['message']['content']})
        return self.response['message']['content']
