from django.shortcuts import render
from django import forms

from . import util

class SearchForm(forms.Form):
    q = forms.CharField(label="Search Encyclopedia")
  
def index(request):
    """
    Displays the index page.
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    """
    Displays the requested entry.
    """
    # If the entry does not exist, display an error message
    if util.get_entry(title) is None:
        return render(request, "encyclopedia/error.html", {
            "message": "Entry not found"
        })
    else:
        # If the entry exists, display it
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
