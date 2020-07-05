from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import markdown2
from random import randrange
from . import util

encyc = util.list_entries()

class SearchForm(forms.Form):
    q = forms.CharField(min_length = 1)
class EditForm(forms.Form):
    edited = forms.CharField()
class CreateForm(forms.Form):
    title = forms.CharField(min_length = 1)
    content = forms.CharField(min_length = 1)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def title(request, entry_name):
    term = entry_name
    entry = util.get_entry(entry_name)
    if not entry:
        return render(request, "encyclopedia/error.html", {
            "cause":f"{entry_name} doesn't exist"
        })
    else:
        return render(request, "encyclopedia/title.html", {
            "entry": markdown2.markdown(entry), "term":term
        })

def search(request):
    results = list()
    if request.method == "GET":
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["q"]
            for entry in util.list_entries():
                if query == entry:
                    return HttpResponseRedirect(f"wiki/{query}")
                if query.lower() in entry.lower():
                    results.append(entry)
            if not results:
                return render(request, "encyclopedia/search.html",{
                    "q":"No Results Found"
                    })
            else:
                return render(request, "encyclopedia/search.html",{
                            "q": results, "term": query
                            })
        else:
            return index(request)

def aleator(request):
    index = randrange(len(encyc))
    result = util.list_entries()[index].lower()
    return HttpResponseRedirect(f"wiki/{result}")

def edit(request, entry_name):
    term = entry_name
    entry = util.get_entry(entry_name)
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            fin = form.cleaned_data["edited"]
            for dic in util.list_entries():
                if term.lower() == dic.lower():
                    util.save_entry(dic, fin)
            return HttpResponseRedirect(reverse("wiki:title",  kwargs={'entry_name':term}))

    return render(request, "encyclopedia/edit.html",{
        "entry":entry, "term":term
    })

def add(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if title in util.list_entries():
                return render(request, "encyclopedia/error.html", {
                    "cause":f"{title} already Exists"
                })
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("wiki:title", kwargs={'entry_name':title}))
        else:
            return render(request, "encyclopedia/error.html",{
                "cause":"Entry not valid"
            })
    return render(request, "encyclopedia/add.html")
