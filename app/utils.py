import os
from unicodedata import normalize

from services.quillbot import rewrite_paragraph


def create_article_html(article_dict: dict) -> str:
    """Function to create HTML from article dict

    Args:
        article_dict (dict): Article

    Returns:
        str: HTML
    """
    videos_used_counter = 0
    paragraph_list = article_dict["full_article_text"].split("\n")
    html = ""

    # add css | this line can be removed if you don't want to add css
    html += add_css_to_html() + "\n\n"

    title = rewrite_paragraph(article_dict["article_title"])
    html += f"<h1>{title}</h1>\n\n"
    description = rewrite_paragraph(article_dict["article_description"])
    html += f"<h3>{description}</h3>\n\n"
    if article_dict["image_url"]:
        html += f'<img src="{article_dict["image_url"]}" alt="{article_dict["main_image_description"]}">\n\n'
    for paragraph in paragraph_list:
        if article_dict["videos_ids"]:
            if paragraph.startswith("'") and paragraph.endswith("'"):
                html += f"<h2>{paragraph[1:-1]}</h2>\n\n"
                html += f'<iframe class="centered-iframe" width="100%" height="50%" src="https://www.youtube.com/embed/{article_dict["videos_ids"][videos_used_counter]}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>\n\n'
                videos_used_counter += 1
            else:
                paragraph = rewrite_paragraph(paragraph)
                html += f"<p>{paragraph}</p>\n\n"
        else:
            paragraph = rewrite_paragraph(paragraph)
            html += f"<p>{paragraph}</p>\n\n"
    return html


def save_html_to_file(html_text: str) -> str:
    """Function to save HTML to file and return file name

    Args:
        html_text (str): HTML text
    """
    file_name = (
        html_text.split("<h1>")[1]
        .replace(" ", "_")
        .replace(",", "")
        .replace(":", "")
        .replace("'", "")
        .lower()
        .split("</h1>")[0]
    )
    file_name = remove_accents(file_name)
    with open(f"./tmp/{file_name}.html", "w") as file:
        file.write(html_text)
    return file_name


def delete_html_file(file_name: str) -> None:
    """Function to delete HTML file

    Args:
        file_name (str): File name
    """
    os.remove(f"./tmp/{file_name}.html")


def remove_accents(input_string):
    normalized_string = normalize("NFKD", input_string)
    ascii_string = normalized_string.encode("ASCII", "ignore").decode("utf-8")
    return ascii_string


def add_css_to_html() -> str:
    """Function to add CSS to HTML

    Returns:
        str: HTML with CSS
    """
    style = r"""
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0 auto;
            max-width: 800px;
            padding: 20px;
        }

        h1, h2, h3, h4, h5, h6 {
            font-weight: 700;
            margin-top: 30px;
            margin-bottom: 15px;
            text-align: center;
        }

        p {
            margin-bottom: 15px;
        }

        img {
            max-width: 100%;
            height: auto;
            margin-bottom: 20px;
        }

        .centered-iframe {
            display: block;
            margin: 0 auto;
        }
        </style>
        """
    return style
