from bs4 import BeautifulSoup
import bs4
from bs4 import Comment

def html_remover(html,full=False):
    soup = BeautifulSoup(html, 'html.parser')
    if full:
        # for tag in soup.find_all(['meta', 'style']):
        #     tag.decompose()
        # for tag in soup.find_all(True):  # True means all tags
        #     tag.attrs = {}
        
        # tag_list = soup.findAll(lambda tag: len(tag.attrs) > 0)
        # for t in tag_list:
        #     for attr, val in t.attrs:
        #         del t[attr]
        # return soup
        KEEP_ATTRIBUTES = ['href']

        # doc = '''<html><head><title>Page title</title></head><body><p id="firstpara" align="center">This is <i>paragraph</i> <a onmouseout="">one</a>.<p id="secondpara" align="blah">This is <i>paragraph</i> <b>two</b>.</html>'''
        # soup = bs4.BeautifulSoup(doc)
        

        for child in soup.descendants:
            if isinstance(child,Comment):
                child.extract()
        for tag in soup.descendants:
            if isinstance(tag, bs4.element.Tag):
                tag.attrs = {key: value for key, value in tag.attrs.items()
                            if key in KEEP_ATTRIBUTES}
        for div in soup.find_all('div'):
            if not div.attrs:
                div.unwrap()

    cleaned_html = soup.prettify()
    return cleaned_html