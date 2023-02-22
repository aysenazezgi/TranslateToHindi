from googletrans import Translator
import os
from bs4 import BeautifulSoup
import concurrent.futures

# Set the source and target languages
src_lang = 'en'
target_lang = 'hi'

# Set the root directory of HTML files
root_dir = '/home/aysenazezgi/classcentral_web/www.classcentral.com'

# Initialize the translator
translator = Translator()

# Initialize a list to store the lines that could not be translated
not_translated_lines = []

# Define a function to translate the contents of an HTML file
def translate_html_file(file_path):
    with open(file_path, 'r') as f:
        contents = f.read()

    # Parse the HTML and extract the body contents
    soup = BeautifulSoup(contents, 'html.parser')
    body = soup.find('body')

    # Translate the contents within the body tag
    if body:
        for tag in body.find_all():
            if tag.string:
                try:
                    translated_text = translator.translate(tag.string, src=src_lang, dest=target_lang).text
                    print(f"Translated: {tag.string} -> {translated_text}")
                    tag.string.replace_with(translated_text)
                except Exception as e:
                    print(f"Error translating {tag.string}: {e}")
                    not_translated_lines.append((file_path, tag.string))

        # Write the translated HTML contents to the file
        with open(file_path, 'w') as f:
            f.write(str(soup))

# Use multithreading to translate the contents of HTML files
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            # Check if the file is an HTML file
            if filename.endswith('.html'):
                file_path = os.path.join(dirpath, filename)
                print(filename)
                executor.submit(translate_html_file, file_path)

# Write the lines that could not be translated to a text file
if not_translated_lines:
    with open('/home/aysenazezgi/classcentral_web/nottranslatedmultithread.txt', 'w') as f:
        for file_path, line in not_translated_lines:
            f.write(f"{file_path}: {line}\n")

