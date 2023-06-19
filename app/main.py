from services.g1 import get_g1_articles
from utils import create_article_html, delete_html_file, save_html_to_file

if __name__ == "__main__":
    g1_articles = get_g1_articles()
    # html = create_article_html(g1_articles[1])
    # html_file_name = save_html_to_file(html)
    # print(f"HTML file saved: {html_file_name}")
    for article in g1_articles:
        html = create_article_html(article)
        html_file_name = save_html_to_file(html)
        print(f"HTML file saved: {html_file_name}")
