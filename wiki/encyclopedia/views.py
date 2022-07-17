from django.http import HttpResponseNotFound
from django.shortcuts import render

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