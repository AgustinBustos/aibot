from bs4 import BeautifulSoup
import bs4
import re
from bs4 import Comment
from bs4 import NavigableString
empty_tag_finder=lambda x: (len(x.contents) == 0) and ('href' not in x.attrs.keys())
tag_replacer_finder=lambda x: x.name in ['section','g','span','label']

def html_remover(html):
    soup = BeautifulSoup(html, 'html.parser')
   
    for tag in soup.find_all(['meta','style','code']):
        tag.decompose()
    KEEP_ATTRIBUTES = ['href']
    
    for tag in soup.descendants:
        if isinstance(tag, bs4.element.Tag):
            tag.attrs = {key: value for key, value in tag.attrs.items()
                        if key in KEEP_ATTRIBUTES}
    for tag in soup.find_all(tag_replacer_finder):
        tag.name='div'
    for div in soup.find_all('div'):
        if not div.attrs:
            div.unwrap()
    for div in soup.find_all('div'):
        div.name='d'
    any_more_empty_tags=True
    while any_more_empty_tags:
        all_empty_tags=soup.find_all(empty_tag_finder)
        if len(all_empty_tags)==0:
            any_more_empty_tags=False
        for tag in all_empty_tags:
            tag.extract()
        # print(soup.find_all('svg'))
    for element in soup.find_all(string=lambda text: isinstance(text, Comment)):
        element.extract()
  

 
            
            


    cleaned_html = re.sub(r'[\t\r\n]', '', str(soup)) #.prettify()
    # print(repr(cleaned_html))

    before=len(cleaned_html)+1
    after=len(cleaned_html)
    while before>after:  
        before=len(cleaned_html)
        cleaned_html=cleaned_html.replace("> ",'>')
        cleaned_html=cleaned_html.replace(" <",'<')
        cleaned_html=cleaned_html.replace("  ",' ')
        after=len(cleaned_html)



    return   cleaned_html 



# with open('example.html', 'r',encoding="utf-8") as file:  # r to open file in READ mode
#     html = file.read()
# print(len(html))
# cleaned=html_remover(html)
# print(len(cleaned))
# with open("cleaned.html", "w",encoding="utf-8") as file:
#         file.write(cleaned)