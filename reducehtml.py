from bs4 import BeautifulSoup
import bs4
from bs4 import Comment
from bs4 import NavigableString
empty_tag_finder=lambda x: (len(x.contents) == 0) and ('href' not in x.attrs.keys())


def html_remover(html,full=False):
    soup = BeautifulSoup(html, 'html.parser')
    if full:
        for tag in soup.find_all(['meta','style','code']):
            tag.decompose()
        KEEP_ATTRIBUTES = ['href']
        
        for tag in soup.descendants:
            if isinstance(tag, bs4.element.Tag):
                tag.attrs = {key: value for key, value in tag.attrs.items()
                            if key in KEEP_ATTRIBUTES}
        for div in soup.find_all('div'):
            if not div.attrs:
                div.unwrap()

        any_more_empty_tags=True
        while any_more_empty_tags:
            all_empty_tags=soup.find_all(empty_tag_finder)
            if len(all_empty_tags)==0:
                any_more_empty_tags=False
            for tag in all_empty_tags:
                tag.extract()
        # print(soup.find_all('svg'))
        for element in soup.find_all(text=lambda text: isinstance(text, Comment)):
            element.extract()
  

 
            
            


    cleaned_html = soup.prettify()
    # print(repr(cleaned_html))
    return cleaned_html



# with open('example.html', 'r') as file:  # r to open file in READ mode
#     html = file.read()
# print(len(html))
# cleaned=html_remover(html,full=True)
# print(len(cleaned))
# with open("cleaned.html", "w") as file:
#         file.write(cleaned)