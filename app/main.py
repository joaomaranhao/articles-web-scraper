from services.g1 import get_g1_articles, create_markdown

if __name__ == "__main__":
    g1_articles = get_g1_articles()
    markdown = create_markdown(g1_articles[1])
    print(markdown)
    