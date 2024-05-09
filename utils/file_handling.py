import os, hashlib, random, re

def sanitize_filename(filename:str):
    if '\n' in filename:
        filename = filename.replace('\n', ' ')
    if '`' in filename:
        filename = filename.replace('`', ' ')
    if ' Explanation:' in filename:
        filename = filename.split(' Explanation:')[0]
    if ' or ' in filename:
        filename = filename.split(' or ')[0]
    filename = filename.strip()
    
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)
    filename = filename.replace(" ", "_")
    return filename


def write_to_file(output_folder, filename, data):
    filename = sanitize_filename(filename)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    file_path = os.path.join(output_folder, filename)
    if os.path.isfile(file_path):
        random_hash = hashlib.md5(str(random.random()).encode()).hexdigest()[:6]
        filename = f"{filename}_{random_hash}"

    with open(os.path.join(output_folder, filename), 'w') as f:
        f.write(data)
        
    return f"File was created and saved at: {os.path.join(output_folder, filename)}"
