from random import randint

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entries(request, title):
    entry = util.get_entry(title)
    if entry:
        html = markdown2.markdown(entry)
        return util.render_entry(request, title, html)
    return util.render_error(request, 'Page not Found')

def search(request):
    query = request.GET.get('q')
    if not query:
        return util.render_error(request, "Search Query not provided.")
    entry = util.get_entry(query)
    if entry:
        return util.render_entry(request, query, markdown2.markdown(entry))
    
    return render(request, 'encyclopedia/index.html', {
        'entries': [x for x in util.list_entries() if query.lower() in x.lower()]
    })

def add_entry(request):
    if request.method == 'GET':
        return render(request, 'encyclopedia/new.html')
    title = request.POST.get('title')
    entry_text = request.POST.get('entry')
    if not title or not entry_text:
        return util.render_error(request, "Error Occured.Title/Description was not provided")
    if util.get_entry(title) != None:
        return util.render_error(request, "Error Occured. A page with that title already exists. Go to that page to edit or enter a new title.")
    util.save_entry(title, entry_text)
    return HttpResponseRedirect(reverse('entries', kwargs= {"title":title}))

def edit_entry(request, title):
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
    entries_list = util.list_entries()
    length = len(entries_list)
    return HttpResponseRedirect(reverse('entries', kwargs={'title': entries_list[randint(0, length -1 )]}))