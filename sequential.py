import os
import concurrent.futures
from bs4 import BeautifulSoup
from google_trans_new import google_translator
import threading
import resource
from deep_translator import GoogleTranslator

# Set the source and target languages
src_lang = 'auto'
target_lang = 'hi'

# Set the root directory of HTML files
root_dir = 'classcentral_web/www.classcentral.com/deneme'


def translate_text(text, translator):
    """Translate the given text to the target language."""
    try:
        result =GoogleTranslator(source='auto', target='hi').translate(text)
        print(result)
        return result
    except Exception as e:
        print(f"Error translating {text}: {e}")
        return None


def translate_tag(tag, translator):
    """Translate the contents of the given tag to the target language."""
    if tag.string:
        print(tag.string)
        translated_text = translate_text(tag.string, translator)
        if translated_text:
            print(f"Translated: {tag.string} -> {translated_text}")
            tag.string.replace_with(translated_text)


def translate_file(file_path):
    """Translate the contents of the given HTML file to the target language."""
    # Initialize the translator for each file
    print(file_path)
    translator = google_translator()
    print(file_path)

    with open(file_path, 'r') as f:
        contents = f.read()

    # Parse the HTML and extract the body contents
    soup = BeautifulSoup(contents, 'html.parser')
    body = soup.find('body')

    # Translate the contents within the body tag
    if body:
        for tag in body.find_all():
            translate_tag(tag, translator)

        # Overwrite the original HTML file with the translated contents
        print(file_path)
        with open(file_path, 'w') as f:
            f.write(str(soup))
    print(f"Translated {file_path}")


# Loop through the root directory and its subdirectories
html_files = []
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        # Check if the file is an HTML file
        if filename.endswith('.html'):
            file_path = os.path.join(dirpath, filename)
            html_files.append(file_path)
for file_path in html_files:
    try:
        translate_file(file_path)
    except Exception as e:
        print(f"Error translating file: {e}")

