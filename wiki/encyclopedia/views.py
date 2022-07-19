from http.client import HTTPResponse
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from . import util
from encyclopedia.forms import PageForm

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
        "title": title, "content": content
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

        
        


def new_page(request):

    if request.method == 'POST':

        # Make form from request post data
        form = PageForm(request.POST)

        # Check form valid
        if form.is_valid():
            
            # Get cleaned data
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')

            # if true create new page and redirect to new page, otherwise add error message
            if util.save_entry(title, content):
                return HttpResponseRedirect(reverse('entry_page', args=(title,)))
            else:
                messages.add_message(request, messages.ERROR, "A page with that title exists already!", extra_tags='danger')


    return render(request, "encyclopedia/new_page.html", { "form": PageForm()})


def edit_page(request):

    if request.method == 'POST':
        # Make form from request post data
        form = PageForm(request.POST)

        if form.is_valid():
            # Get cleaned data
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            
            # Edit entry
            util.edit_entry(title, content)

            return HttpResponseRedirect(reverse('entry_page', args=(title, )))
    
    # if title doesnt exists
    if 't' not in request.GET:
        return HttpResponseRedirect(reverse('index'))

    # Get title data
    title = request.GET.get('t').strip()

    # if title is empty
    if len(title) == 0:
        return HttpResponseRedirect(reverse('index'))

    # Get content data
    content = util.get_entry(title)

    # Check if content exists
    if content is None:
        return HttpResponseNotFound("Not found")

    # Make form with initial title and content
    form = PageForm(initial={'title': title, 'content': content})
    # Set title disabled = True
    form.disable_title()
    

    # return form with initial title and content
    return render(request, "encyclopedia/edit_page.html", {
        'form': form
        })