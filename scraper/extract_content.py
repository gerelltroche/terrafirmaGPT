import os
from bs4 import BeautifulSoup

def extract_main_content(html_file_path):
    with open(html_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')

    # Replace <br> and </p> tags with newline characters to preserve line breaks
    for br_tag in soup.find_all('br'):
        br_tag.replace_with('\n')

    for p_tag in soup.find_all('p'):
        p_tag.append('\n')

    # You can modify the following line to target a more specific element if needed, e.g., soup.find(id='main-content')
    main_content = soup.body

    # Get text content with newline characters
    text_content = main_content.get_text(separator='\n', strip=True)
    return text_content

def save_to_txt_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

input_folder = 'pages'
output_folder = 'content'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for file_name in os.listdir(input_folder):
    if file_name.endswith('.html'):
        input_file_path = os.path.join(input_folder, file_name)
        output_file_path = os.path.join(output_folder, file_name.replace('.html', '.txt'))

        main_content = extract_main_content(input_file_path)
        save_to_txt_file(output_file_path, main_content)

        print(f"Processed {input_file_path} and saved content to {output_file_path}")