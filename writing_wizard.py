import openai
from utils import get_configs, get_env, write_to_file, cache
from types import SimpleNamespace

DEFAULT_SYSTEM_PROMPT = """Question Answering Mode. Instructions:
- Provide factual and concise answers to each question.
- Strive for accuracy and stay relevant to the specific question asked.
- Absoultely no conversational elements or elaboration.
- All answers should be straight to point.
- Article needs to be elaborate with Examples. It should be well formatted in Markdown and should be atleast 350 words. Maximum 1000 words.
- File name needs to be short and expressive. It should be one to three words long.
- When asked for file name, provide only one file name.
"""

class WritingWizard:
    def __init__(self, messages=[], system_prompt=DEFAULT_SYSTEM_PROMPT):
        self._messages = messages
        self._system_prompt = {
            'role' : 'system',
            'content' : system_prompt
        }
            
    @property
    @cache
    def configs(self):
        all_configs = get_configs()
        all_configs.openai.api.key = get_env(all_configs.openai.api.key_var)
        all_configs.llm.selected = SimpleNamespace(**all_configs.llm.available[all_configs.llm.selected])
        return all_configs
    
    @property
    @cache
    def model(self):
        return self.configs.llm.selected
    
    @property
    @cache
    def server(self) -> openai.OpenAI:
        configs = self.configs
        return openai.OpenAI(
            api_key  = configs.openai.api.key,
            base_url = configs.openai.api.url,
        )
    
    @property    
    def system_prompt(self):
        return self._system_prompt
    
    @system_prompt.setter
    def system_prompt(self, msg:dict):
        self._system_prompt = {
            'role' : 'system',
            'content' : msg
        }
    
    @property    
    def messages(self):
        return self._messages
    
    @messages.setter
    def messages(self, msg:dict):
        self._messages.append(msg)
        
        if len(self.messages) > 3:
            self._messages.pop(0)
    
    def chat(self, prompt:str):
        self.messages = {
            'role' : 'user',
            'content' : prompt
        }
        response = self.server.chat.completions.create(
            model    = self.model.model,
            messages = [self.system_prompt] + self.messages
        ).choices[0]
        self.messages = {
            'role' : response.message.role,
            'content' : response.message.content
        }
    
    def save_to_file(self, filename = None):
        if len(self.messages) < 3 and filename == None:
            print("Cannot write to file, atleast three messages are needed, currently are",len(self.messages))
        
        if not filename:
            filename = self.messages[-1]["content"] + '.md'
        
        return write_to_file(
            output_folder   = self.configs.output_folder, 
            filename        = filename,
            data            = self.messages[0]["content"]
        )

WritingWizard = WritingWizard()

if __name__ == '__main__':
    from sys import argv
    def test():
        WritingWizard.chat("Write an article on the topic Article-Writing Generative AI ChatBots.")
        # print(WritingWizard.messages)
        print("--- Article Fetched ---")
        
        WritingWizard.chat("Suggest one file name which can contain this article.")
        # print(WritingWizard.messages)
        print("--- Title Fetched --- ")
        
        print(WritingWizard.save_to_file())
        print("--- File saved --- ")
    
    if len(argv) > 1:
        if argv[1] == "--test":
            test()
