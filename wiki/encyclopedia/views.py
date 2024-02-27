from django.shortcuts import render

from . import util

from markdown2 import Markdown

from django import forms

from random import choice

# class NewSearchForm(forms.Form):
#     search = forms.CharField(label="Search")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, name):

    mkdwn = Markdown()

    if content:= util.get_entry(name):

        return render(request, "encyclopedia/page.html", {
            "title": name,
            "content": mkdwn.convert(content),
        } )
    
    else:

        return render(request, "encyclopedia/404.html", status=404)

# def search(request):

#     return render(request, "encyclopedia/layout.html", {
#         "form" : NewSearchForm()
#     })


def search(request):

    query = request.POST.get('query')

    if util.get_entry(query):
        return title(request, query)
    
    else:
        entries = util.list_entries()
        out = []

        for entry in entries:

            if query.lower() in entry.lower():
                out.append(entry)

        return render(request, "encyclopedia/search.html", {
            "results": out,
            "query": query
        })


def random(request):

    entries = util.list_entries()

    return title(request, choice(entries))