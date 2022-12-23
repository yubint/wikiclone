from random import randint

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
import markdown2

from . import util


def index(request):
    """
    Main page of the Website. Renders the index page
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entries(request, title):
    """
    Returns rendered page of the title provided if it exists
    and returns error page if it doesn't."""
    entry = util.get_entry(title)
    if entry:
        html = markdown2.markdown(entry)
        return util.render_entry(request, title, html)
    return util.render_error(request, 'Page not Found')

def search(request):
    """
    Searches for an entry and returns that page if it exists.
    If it doesn't then it returs an index page with the entries
    that are similar to the search query.
    """
    query = request.GET.get('q')
    if not query:
        return util.render_error(request, "Search Query not provided.")
    entry = util.get_entry(query)
    if entry:
        return util.render_entry(request, query, markdown2.markdown(entry))

    # Using list comprehension to return the only entries that match the query
    return render(request, 'encyclopedia/index.html', {
        'entries': [x for x in util.list_entries() if query.lower() in x.lower()]
    })

def add_entry(request):
    """
    Returns the New entry page if the request is GET and adds the entry if
    it's a POST request. Returns an error if that page already exists.
    """
    if request.method == 'GET':
        return render(request, 'encyclopedia/new.html')
    title = request.POST.get('title')
    entry_text = request.POST.get('entry')
    if not title or not entry_text:
        return util.render_error(request, "Error Occured.Title/Description was not provided")
    if util.get_entry(title) is not  None:
        return util.render_error(request,
                                "Error Occured. A page with that title already exists. Go to that page to edit or enter a new title.")
    util.save_entry(title, entry_text)
    return HttpResponseRedirect(reverse('entries', kwargs= {"title":title}))

def edit_entry(request, title):
    """
    Returns the edit page if it's a GET request and edits the entry if it's a POST
    request.
    """
    if request.method == "GET":
        entry = util.get_entry(title)
        if entry:
            return render(request, 'encyclopedia/edit.html', {
                'title': title,
                'entry': entry
            })
        return util.render_error(request, "Error Occured. No such entry to edit")
    entry_text = request.POST.get('entry')
    if not entry_text:
        return util.render_error(request, "Error Occures. No entry provided.")
    util.save_entry(title, entry_text)
    return HttpResponseRedirect(reverse('entries', kwargs = {'title' : title}))

def random_entry(request):
    """
    Redirects the user to a random entry.
    """
    entries_list = util.list_entries()
    length = len(entries_list)
    return HttpResponseRedirect(reverse('entries',
                                 kwargs={'title': entries_list[randint(0, length -1 )]}))
