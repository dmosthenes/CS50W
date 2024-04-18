from django.shortcuts import render, redirect

from . import util

from markdown2 import Markdown

from django import forms

from random import choice

mkdwn = Markdown()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def edit(request, page):

    content = util.get_entry(page)

    if request.method == "POST":
        
        new_text = request.POST.get("body")
        page = request.POST.get("title")

        util.save_entry(page, new_text)

        return redirect(title, page)

    else:
        return render(request, "encyclopedia/edit_page.html", {
            "title": page,
            "content": content
        })
    

def create(request):

    if request.method == "POST":

        page = request.POST.get("title")
        content = request.POST.get("content")

        util.save_entry(page, content)

        return redirect(title, page)

    return render(request, "encyclopedia/new_page.html", {

    })

def title(request, name):

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