import os, hashlib, random, re

def fix_encoding(s:str):
    """Fixes the encoding of a string by encoding it to UTF-8 and then decoding it back to UTF-8.
    
        Args:
            s (str): The input string to fix the encoding.
    
        Returns:
            str: The fixed string with correct encoding.
    """
    return s.encode("utf-8").decode("utf-8")

def sanitize_filename(filename:str):
    """Sanitize the given filename by fixing encoding issues, removing special characters, and replacing spaces with underscores.
    
    Args:
        filename (str): The original filename to be sanitized.
    
    Returns:
        str: The sanitized filename.
    """
    filename = fix_encoding(filename)
    filename = filename.replace('*', '')
    filename = filename.replace('`', '')

    if '\n' in filename:
        filename = filename.split('\n')[0]

    filename = filename.replace("1. ", '')

    if ' Explanation:' in filename:
        filename = filename.split(' Explanation:')[0]

    if ' or ' in filename:
        filename = filename.split()[0]
    
    filename = filename.strip()
    
    filename = filename.replace(" ", "_")
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)

    return filename


def write_to_file(output_folder, filename, data):
    """Write data to a file in the specified output folder.
    
    Args:
        output_folder (str): The path to the output folder where the file will be saved.
        filename (str): The name of the file to be created.
        data (str): The data to be written to the file.
    
    Returns:
        str: The full path to the created file.
    """
    data = fix_encoding(data)
    
    filename = sanitize_filename(filename)
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    file_path = os.path.join(output_folder, filename)
    if os.path.isfile(file_path):
        ext = filename.split(".")[-1]
        filename.replace("." + ext, '')
        random_hash = hashlib.md5(str(random.random()).encode()).hexdigest()[:6]
        filename = f"{filename}_{random_hash}"
        filename += "." + ext

    with open(os.path.join(output_folder, filename), 'w', encoding='utf-8') as f:
        f.write(data)
        
    # return f"File was created and saved at: {os.path.join(output_folder, filename)}"
    return os.path.join(output_folder, filename)
