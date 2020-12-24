"""
Data processing module.
"""

from dragnet import extract_content

def clean_wiki_page(html_content):
    """
    Remove the noise from the page and simplify the resultant HTML.
    Using the dragnet library (https://github.com/dragnet-org/dragnet/).
    """
    return extract_content(html_content)