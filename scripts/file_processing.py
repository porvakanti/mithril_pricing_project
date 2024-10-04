
import os
import re
from scripts.tokenizer import num_tokens_from_string

def clean_markdown_content(content: str) -> str:
    # Remove links
    link_pattern = r'\[([^\[]+)\]\(([^\)]+)\)'
    content = re.sub(link_pattern, r'\1', content)

    # Remove images
    image_pattern = r'\!\[([^\[]*)\]\(([^\)]+)\)'
    content = re.sub(image_pattern, '', content)

    # Remove all occurrences of **
    content = content.replace('**', '')
    content = content.replace('\n', '')

    return content

def process_markdown_files(input_directory: str):
    i = 0
    for filename in os.listdir(input_directory):
        if filename.endswith('.md'):
            file_path = os.path.join(input_directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                tokens = num_tokens_from_string(content)
                if tokens > 8191:
                    print(f'File {filename} has {tokens} tokens which is more than 8191 (max) tokens')

# Example usage:
# process_markdown_files('./data/azure-ai-docs/')
