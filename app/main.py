from services.g1 import get_g1_articles, create_markdown, save_markdown_to_file, delete_markdown_file

if __name__ == "__main__":
    g1_articles = get_g1_articles()
    markdown = create_markdown(g1_articles[1])
    markdown_file_name = save_markdown_to_file(markdown)
    delete_markdown_file(markdown_file_name)