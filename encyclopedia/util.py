import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

def render_error(request, error: str):
    """
    Takes an error message and returns an response with the rendered
    error page.
    """
    return render(request, 'encyclopedia/error.html', {
        'error': error
    })

def render_entry(request, title: str, html: str):
    """
    Takes a title and html for an entry page and returns an response with
    the rendered entry page.
    """
    return render(request, 'encyclopedia/entry.html', {
        'title': title,
        'html': html
    })
    