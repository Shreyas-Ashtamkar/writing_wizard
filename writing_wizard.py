import openai
from utils import get_configs, get_env, write_to_file, cache
from types import SimpleNamespace

DEFAULT_SYSTEM_PROMPT = """Question Answering Mode. Follow each of the below instructions carefully and strictly.:
- Provide factual and concise answers to each question.
- Strive for accuracy and stay relevant to the specific question asked.
- Absoultely no conversational elements or elaboration.
- All answers should be straight to point.
- Article needs to be elaborate with Examples. It should be well formatted in Markdown and should be atleast 350 words.
- File name needs to be short and expressive. It should be one to three words long.
- When asked for file name, provide only one file name. Do not provide explaination.
"""

class _WritingWizard:
    def __init__(self, messages=[], system_prompt=DEFAULT_SYSTEM_PROMPT):
        """Initialize the class with the given messages and system prompt.
        
        Args:
            messages (list, optional): List of messages to initialize the class with. Defaults to an empty list.
            system_prompt (str, optional): System prompt to initialize the class with. Defaults to DEFAULT_SYSTEM_PROMPT.
        """
        self._messages = messages
        self._system_prompt = {
            'role' : 'system',
            'content' : system_prompt
        }
        
    @property
    @cache
    def configs(self):
        """Retrieve and update configurations for the current environment.
        
        Returns:
            dict: A dictionary containing all configurations after updating API key and selected LLM.
        """
        all_configs = []
        all_configs = get_configs()
        all_configs.openai.api.key = get_env(all_configs.openai.api.key_var)
        all_configs.llm.selected = SimpleNamespace(**all_configs.llm.available[all_configs.llm.selected])
        return all_configs
    
    def reload(self):
        get_configs.cache_clear()
        self.__class__.configs.fget.cache_clear()
        self.__class__.server.fget.cache_clear()
    
    @property
    @cache
    def model(self):
        """Return the selected model from the configs for the Language Model."""
        return self.configs.llm.selected
    
    @property
    @cache
    def server(self) -> openai.OpenAI:
        """Return an instance of OpenAI using the configurations provided."""
        configs = self.configs
        server = None
        try:
            server  = openai.OpenAI(
                api_key  = configs.openai.api.key,
                base_url = configs.openai.api.url,
            )
        except openai.OpenAIError as e:
            print("Error : Cannot initialize server (60) : " + e.__str__())
            
        return server
    
    @property    
    def system_prompt(self):
        """Return the system prompt."""
        return self._system_prompt
    
    @system_prompt.setter
    def system_prompt(self, msg:dict):
        """Set system prompt message for the chatbot.
        
        Args:
            msg (dict): The message content to be set.
        
        Returns:
            None
        """
        self._system_prompt = {
            'role' : 'system',
            'content' : msg
        }
    
    @property    
    def messages(self):
        """Return the messages stored in the instance."""
        return self._messages
    
    @messages.setter
    def messages(self, msg:dict):
        """Append a message to the list of messages and keep only the last 3 messages.
        
        Args:
            msg (dict): The message to be appended to the list of messages.
        """
        if not isinstance(msg, dict):
            raise ValueError("Please use WritingWizard.add_messages to add custom messages with roles else assign dictionary {role:str, content:str}")
        
        self._messages.append(msg)
        
        # if len(self.messages) > 4:
        #     self._messages.pop(0)
    
    def clear_messages(self):
        """Clears the messages stored in the object."""
        self._messages = []
    
    def create_message(self, content:str, role:str="user"):
        """Add a message to the object.
        
        Args:
            content (str): The content of the message.
            role (str, optional): The role of the user sending the message. Defaults to "user".
        """
        return {
            "role": role,
            "content" : content
        }
    
    def generate_response(self, test=False) -> dict[str,str]:
        """Generates a response using the server's chat completions.
        
        Returns:
            dict: A dictionary containing the role and content of the response.
        """
        
        if test:
            response = {
                'role' : "test-role",
                'content' : "test-content"
            }
        else:
            try:
                response = self.server.chat.completions.create(
                    model    = self.model.model,
                    messages = [self.system_prompt] + self.messages,
                    max_tokens = 4096,
                    # stream   = True
                ).choices[0]
                response = {
                    'role' : response.message.role,
                    'content' : response.message.content
                }
            except AttributeError as e:
                print("Error : Cannot generate completions (125) : " + e.__str__())
                exit(1)
        
        return response
    
    def chat(self, prompt:str):
        """Updates the chat messages with the user prompt and generates a response."""
        self.messages = {
            'role' : 'user',
            'content' : prompt
        }
        self.messages = self.generate_response()
        return self.messages
    
    def save_to_file(self, filename = None, output_folder:str=None):
        """Save messages to a file.
        
        Args:
            filename (str, optional): The name of the file to save the messages to. If not provided, a filename will be generated with a '.md' extension. Defaults to None.
            output_folder (str, optional): The folder where the file will be saved. If not provided, the default output folder from config.yaml will be used. Defaults to None.
        
        Returns:
            bool: True if the messages were successfully saved to the file, False otherwise.
        """
        if len(self.messages) < 2:
            print("Cannot write to file, atleast 2 messages are needed, currently are", len(self.messages))
        
        if not filename:
            print("\nGenerating Filename... \n")
            self.chat("Suggest one file name which can contain this article.")
            
            filename = self.messages[-1]["content"]
            
        if not output_folder:
            output_folder = self.configs.output_folder
        
        filename += '.md'
        
        print(f"--- Saving File : {filename} --- ")
        
        return write_to_file(
            output_folder   = output_folder,
            filename        = filename,
            data            = self.messages[1]["content"]
        )
    
    def write_article(self, topic:str):
        """Write an article on the given topic.
        
        Args:
            topic (str): The topic on which the article needs to be written.
        
        Returns:
            str: The article generated using AI.
        """
        print("\nWriting Article... \n")
        self.chat(f"Write an article on the topic {topic}.")
        
        return self.messages[-1]

WritingWizard:_WritingWizard = _WritingWizard()

if __name__ == '__main__':
    from sys import argv
    def test():
        WritingWizard.chat("Write an article on the topic Article-Writing Generative AI ChatBots.")
        # print(WritingWizard.messages)
        print("\nArticle Fetched... \n")
        
        WritingWizard.chat("Suggest one file name which can contain this article.")
        # print(WritingWizard.messages)
        print("\nTitle Fetched... \n")
        
        print(WritingWizard.save_to_file())
        print("\nFile saved... \n")
    
    if len(argv) > 1:
        if argv[1] == "--test":
            test()
