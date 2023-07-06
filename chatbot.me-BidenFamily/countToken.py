import os
import chardet

def count_tokens_in_file(file_path):
    with open(file_path, 'rb') as file:
        content_bytes = file.read()
    detected = chardet.detect(content_bytes)
    encoding = detected['encoding']
    content = content_bytes.decode(encoding, errors='ignore')
    tokens = content.split()
    return len(tokens)

def count_tokens_in_directory(directory_path):
    total_tokens = 0
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        total_tokens += count_tokens_in_file(file_path)
    return total_tokens

directory_path = "/Users/philipperaymondjb/Documents/GitHub/fine-tune/Biden Laptop emails/biden-laptop-emlxs"
total_tokens = count_tokens_in_directory(directory_path)
print(f"Total tokens: {total_tokens}")
