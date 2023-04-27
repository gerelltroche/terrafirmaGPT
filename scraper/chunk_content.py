import os

def chunk_text(text, max_length=200):
    chunks = []
    lines = text.split('\n')
    current_chunk = ''

    for line in lines:
        if len(current_chunk) + len(line) + 1 <= max_length:
            current_chunk += line + '\n'
        else:
            chunks.append(current_chunk.strip())
            current_chunk = line + '\n'
    
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def save_to_txt_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

input_folder = 'content'
output_folder = 'chunks'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for file_name in os.listdir(input_folder):
    if file_name.endswith('.txt'):
        input_file_path = os.path.join(input_folder, file_name)
        
        with open(input_file_path, 'r', encoding='utf-8') as file:
            text_content = file.read()
        
        chunks = chunk_text(text_content)

        for i, chunk in enumerate(chunks):
            output_file_name = f'{file_name[:-4]}_{i + 1}.txt'
            output_file_path = os.path.join(output_folder, output_file_name)
            save_to_txt_file(output_file_path, chunk)

            print(f"Processed {input_file_path} and saved chunk {i + 1} to {output_file_path}")