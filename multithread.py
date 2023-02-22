import os
import concurrent.futures
from bs4 import BeautifulSoup
from googletrans import Translator
import threading
import resource
from deep_translator import GoogleTranslator
soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
resource.setrlimit(resource.RLIMIT_NOFILE, (hard, hard))
from textblob import TextBlob
import pycld2 as cld2

# Set the source and target languages
src_lang = 'auto'
target_lang = 'hi'

# Set the root directory of HTML files
#root_dir = '/home/aysenazezgi/classcentral_web/www.classcentral.com'

root_dir = '/home/aysenazezgi/classcentral_web/www.classcentral.com'

# Initialize a list to store the lines that could not be translated
not_translated_lines = []

# Set the maximum number of worker threads to use for multithreading
max_workers = 10

# Set the maximum number of open files at any given time
max_open_files = 5

# Create a semaphore to limit the number of open files
file_semaphore = threading.BoundedSemaphore(value=max_open_files)

def translate_text(text):
    """Translate the given text to the target language."""
    try:
        if not text.isdigit():
            _, _, _, detected_languages = cld2.detect(text, returnVectors=True)
            detected_language= list(sum(detected_languages, ()))
            if 'hi' not in detected_language and 'un' not in detected_language :
                p#rint(detected_language)
                result = GoogleTranslator(source='auto', target='hi').translate(text)
            #print(result)
                return result
    except Exception as e:
            print(f"Error translating {text}: {e}")
            return None

def translate_tag(tag, file_path):
    """Translate the contents of the given tag to the target language."""
    if tag.string:
        translated_text = translate_text(tag.string)
        if translated_text:
            #print(f"Translated: {tag.string} -> {file_path}")
            tag.string.replace_with(translated_text)
        else:
            not_translated_lines.append((file_path, tag.string))

def translate_file(file_path):
    """Translate the contents of the given HTML file to the target language."""
    # Initialize the translator for each file
    translator = Translator()
    print(file_path)

    with file_semaphore:
        with open(file_path, 'r') as f:
            contents = f.read()

        # Parse the HTML and extract the body contents
        soup = BeautifulSoup(contents, 'html.parser')
        body = soup.find('body')

        # Translate the contents within the body tag
        if body:
            for tag in body.find_all():
                translate_tag(tag, file_path)

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

# Translate the HTML files in parallel using multiple worker threads
with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = [executor.submit(translate_file, file_path) for file_path in html_files]
    for future in concurrent.futures.as_completed(futures):
        try:
            future.result()
        except Exception as e:
            print(f"Error translating file: {e}")

# Write the lines that could not be translated to a text file

with open('/home/aysenazezgi/classcentral_web/nottranslatedmultithread.txt', 'w') as f:
        for file_path, line in not_translated_lines:
            f.write(f"{file_path}: {line}\n")
