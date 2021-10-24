from django import forms
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
import markdown2
from django.urls import reverse
from . import forms
from random import randint

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_entry(request, title):
    entry = util.get_entry(title)
    if entry == None:
        return render(request, "encyclopedia\entry_not_found.html")
    article_in_html = markdown2.markdown(entry)
    return render(request, "encyclopedia\entry.html", {
        "entry": article_in_html,
        "title": title
    })

def search(request):
    #request.GET is basically a query dict so you can access it like any other dict
    #The default method for forms that are not specified is GET. We use a GET request in search because it does not change the state of the application
    potential_filename = request.GET.get('q','')
    if util.get_entry(potential_filename) is not None:
        return HttpResponseRedirect(reverse('get_entry', args=[potential_filename]))
    all_entries = util.list_entries()
    subEntries = []
    for entry in all_entries:
        if potential_filename.upper() in entry.upper():
            subEntries.append(entry)
    return render(request, "encyclopedia\search_results.html", {
        "entries": subEntries,
        "search_param": potential_filename
    })

def create_page(request):
    if request.method == "POST":
        form = forms.NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            if util.get_entry(title) is None:
                return render(request, "encyclopedia\entry_not_found.html")
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('get_entry', args=[title]))
    return render(request, "encyclopedia/create_page.html", {
        "form": forms.NewEntryForm()
    })

def edit(request, title):
    entry_in_markdown = util.get_entry(title)
    return render(request, "encyclopedia/create_page.html", {
        "form": forms.NewEntryForm(initial={'title': title, 'content': entry_in_markdown})
    })

def random(request):
    all_entries = util.list_entries()
    random_entry_name = all_entries[randint(0, len(all_entries) - 1)]
    return HttpResponseRedirect(reverse('get_entry', args=[random_entry_name]))