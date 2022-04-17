from requests_html import HTMLSession


def save_html(html, path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)


def scrape(url, path):
    """
    Scrapes the given website and saves it in a file located by the given path.

    :param url: the website to be scraped
    :param path: path of the file where the scraped HTML is stored
    """
    url = url
    file_path = path
    session = HTMLSession()
    resp = session.get(url)
    resp.html.render(sleep=1)
    save_html(resp.html.html, file_path)
