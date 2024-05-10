import fire, json, datetime

from writing_wizard import WritingWizard
from utils import write_to_file, set_env

def write_article(topic:str=None, create_file:bool=True, output_filename:str=None, output_folder:str=None, interactive:bool=False):
    """Generate an article based on the given topic.
    
    Args:
        topic (str, optional): The topic for the article. If not provided, the user will be prompted to input a topic. Defaults to None.
        create_file (bool, optional): Determines whether to save the article to a file. Defaults to True.
        output_filename (str, optional): The name of the file to save the article to. If not provided, a name will be auto-generated. Defaults to None.
        output_folder (str, optional): The folder to save the article file to. If not provided, the file will be saved to the default folder. Defaults to None.
        interactive (bool, optional): Determines whether to run the function in interactive mode. If True, the user will be prompted for inputs. Defaults to False.
    
    Returns:
        None
    
    Example:
        write_article(topic="Python Programming", create_file=True, output_folder="articles", interactive=False)
    """
    
    if interactive:
        print("     Welcome to Writing-Wizard")
        print("-----------------------------------")
        
        if WritingWizard.server == None:
            if (API_KEY := input("Please enter the API key (or leave blank to exit) : ")) != "":
                if create_file := (input("Do you wish to save this key? ").lower() in ('y', 'yes', 'ye', 'ya', 'yaa', 'sure')):
                    write_to_file(
                        data = f"API_KEY={API_KEY}",
                        output_folder=".",
                        filename=".env"
                    )
                else:
                    set_env('API_KEY', API_KEY)
                
                WritingWizard.reload()
                if WritingWizard.server == None:
                    print("ERROR : Key invalid or .env not found")
                    exit(1)
            else:
                print("No key provided... Exiting...")
                exit(1)
    
    if not topic:
        topic = input("Please enter a topic : ")
    
    article = WritingWizard.write_article(topic)
    
    print("\n--------------- Generated Article --------------------\n")
    print(article['content'])
    print("\n------------------- Article End ----------------------\n")
    
    if create_file:
        if interactive:
            if (output_folder := input("Do you want the output to be created in a specific folder? (leave blank for default)")) == "":
                output_folder = None
                
            if (output_filename := input("Please enter the file name to save in or leave blank for to auto-generate it :")) == "":
                output_filename = None
            
            print(output_filename)
            
        print(WritingWizard.save_to_file( filename=output_filename, output_folder=output_folder ))
    else:
        if interactive:
            if create_file := input("Do you wish to save this article? ").lower() in ('y', 'yes', 'ye', 'ya', 'yaa', 'sure'):
                if (output_folder := input("Do you want the output to be created in a specific folder? (leave blank for default)")) == "":
                    output_folder = None
                
                if (output_filename := input("Please enter the file name to save in or leave blank for to auto-generate it :")) == "":
                    output_filename = None
                    
                WritingWizard.save_to_file(
                    filename      = output_filename,
                    output_folder = output_folder
                )
    
    write_to_file(
        data            =   json.dumps([WritingWizard.system_prompt] + WritingWizard.messages),
        output_folder   =   '.log',
        filename        =   f"messages.{datetime.datetime.timestamp(datetime.datetime.now())}.json"
    )
    
    print("\nDone.")

if __name__ == '__main__':
    fire.Fire(write_article)
