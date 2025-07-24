import ollama

class SmartAgent:
    def __init__(self, model, system_prompt):
        self.model_name = model
        self.chat_log = []
        if system_prompt:
            self.chat_log.append({'role': 'user', 'content': system_prompt})
        print("Agent is ready")

    def chat(self, message):
        self.chat_log.append({'role':'user', 'content': message})
        response = ollama.chat(model = self.model_name, messages=self.chat_log)

        answer_text = response['message']['content']
        self.chat_log.append({'role':'agent', 'content':answer_text})
    
        return answer_text
    
