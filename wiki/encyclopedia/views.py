from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import util

# Main site
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, title):

    # Get content data
    content = util.get_entry(title)
    
    # Checks if entry exists
    if content is None:
        return HttpResponseNotFound("Not found")

    return render(request, "encyclopedia/content.html", { 
        "title": title.capitalize(), "content": content
        })


def search(request):

    # if query empty, redirect to home page
    if "q" not in request.GET:
        return HttpResponseRedirect(reverse('index'))

    # Get search data
    search_query = request.GET.get("q").strip()

    # if entry is empty, redirect to home page
    if len(search_query) == 0:
        return HttpResponseRedirect(reverse('index'))

    # Get entries
    entries = util.list_entries()
    
    # if entry found,redirect to entry page
    if search_query in entries:
        return HttpResponseRedirect(reverse('entry_page', args=(search_query,)))

    # Redirect filtred data
    search_query = search_query.casefold()
    return render(request, "encyclopedia/search.html", {"entries": list(filter(lambda entry: search_query in entry.casefold(), entries))})

        
        


