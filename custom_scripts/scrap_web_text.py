import requests
from bs4 import BeautifulSoup
import re
import nltk

# Download the NER model for English
nltk.download('maxent_ne_chunker')
nltk.download('words')

def get_person_info(text, person):
    # Tokenize the text into words
    words = nltk.word_tokenize(text)

    # Apply POS tagging to identify parts of speech
    tagged_words = nltk.pos_tag(words)

    # Apply NER to identify named entities
    named_entities = nltk.ne_chunk(tagged_words, binary=False)

    # Loop through the named entities and extract information about the requested person
    for entity in named_entities:
        if hasattr(entity, 'label') and entity.label() == 'PERSON':
            name = ' '.join([word for word, tag in entity.leaves()]).lower()
            if person.lower() in name:
                return f"{name.capitalize()} is mentioned in the text."
    

def main():
  

    url = 'https://www.upf.edu/web/iis/professors'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all links in the page
    links = []
    for link in soup.find_all('a', href=True):
        links.append(link['href'])

    # Find all PDF links in the page
    pdf_links = []
    for link in soup.find_all('a', href=True):
        if link['href'].endswith('.pdf'):
            pdf_links.append(link['href'])

    # Find all text in the page
    text = ''
    for p in soup.find_all('p'):
        text += p.text.strip()

    print('All links in the page:')
    print(links)
    print('PDF links in the page:')
    print(pdf_links)
    print('Text in the page:')
    print(text)


if __name__ == '__main__':
    main()