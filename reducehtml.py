from bs4 import BeautifulSoup

def html_remover(html,full=False):
    soup = BeautifulSoup(html, 'html.parser')
    if full:
        for tag in soup.find_all(['meta', 'style']):
            tag.decompose()

        # for tag in soup.find_all(True):  # True means all tags
        #     tag.attrs = {}

    cleaned_html = soup.prettify()
    return cleaned_html