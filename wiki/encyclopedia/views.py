from django.shortcuts import render
from django import forms
from markdown2 import Markdown

import random



from . import util

class SearchForm(forms.Form):
    q = forms.CharField(label="Search Encyclopedia")

class CreateForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content")
  
def index(request):
    """
    Displays the index page.
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def create(request):
    """
    Displays the create page.
    """
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = CreateForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the title and content from the 'cleaned' version of form data
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            # Check if the title already exists
            if util.get_entry(title) is None:
                util.save_entry(title, content)
                return render(request, "encyclopedia/entry.html", {
                    "title": title,
                    "content": util.get_entry(title)
                })
            else:
                return render(request, "encyclopedia/error.html", {
                    "message": "Entry already exists"
                })
            
        else:

            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/error.html", {
                "message": "Invalid form"
            })
    else:

        # If the request method is not POST, render the page with a blank form.
        return render(request, "encyclopedia/create.html", {
            "form": CreateForm()
        })

def entry(request, title):
    """
    Displays the requested entry.
    """
    # If the entry does not exist, display an error message
    entry_content = util.get_entry(title)
    if entry_content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "Entry not found"
        })
    else:
        # If the entry exists, display it
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": Markdown().convert(entry_content),
        })
    
def edit(request, title):
    """
    Displays the edit page.
    """
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = CreateForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the title and content from the 'cleaned' version of form data
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            util.save_entry(title, content)

            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": util.get_entry(title)
            })
            
        else:

            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/error.html", {
                "message": "Invalid form"
            })
    else:

        # If the request method is not POST, render the page with a blank form.
        return render(request, "encyclopedia/edit.html", {
            "form": CreateForm(initial={'title': title, 'content': util.get_entry(title)}),
            "title": title,
            "content": util.get_entry(title),
        })
    
def random_page(request):
    """
    Displays a random entry.
    """    

    entries = util.list_entries()
    if not entries:
        return render(request, "encyclopedia/error.html", {
            "message": "No entries found"
        })
    title = random.choice(entries)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": util.get_entry(title)
    })

    
def search(request):
    """
    Displays the search results.
    """
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = SearchForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the q from the 'cleaned' version of form data
            q = form.cleaned_data["q"]

            # Search for the q in the list of entries
            entries = util.list_entries()

            results = []

            # If the q is in the entry, add it to the results list
            for entry in entries:
                if q.lower() in entry.lower():
                    results.append(entry)

            # If the q is an exact match for an entry, redirect to that entry page
            if q in results:
                return render(request, "encyclopedia/entry.html", {
                    "title": q,
                    "content": util.get_entry(q)
                })
            
            # If the q does not match any entries, display a message
            elif len(results) == 0:
                return render(request, "encyclopedia/error.html", {
                    "message": "No results found"
                })
            
            # If the q matches multiple entries, display a list of those entries
            else:
                return render(request, "encyclopedia/search.html", {
                    "results": results
                })
            
        else:

            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/error.html", {
                "message": "Invalid form"
            })
    else:

        # If the request method is not POST, re-render the page with existing information.
        return render(request, "encyclopedia/error.html", {
            "message": "Invalid request"
        })
    

