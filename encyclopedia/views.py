from django.shortcuts import render
from django import forms
import markdown2
import random
from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    content = forms.CharField(widget=forms.Textarea, label="")
class NewEditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="")

def get_randomPage():    
    import random
    pages = util.list_entries()
    random_page= random.choice(pages)
    return random_page

#This is the homepage
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "randomPage": get_randomPage()
    })
#This is the page that shows a single entry
def entry(request,pagename):
    get_entry_page =  util.get_entry(pagename)
    if get_entry_page is None:
        doesPageExist = False
        entry = ""
    else:
        entry = markdown2.markdown(util.get_entry(pagename))
        doesPageExist = True
    return render(request,"encyclopedia/entry.html",{
        "doesPageExist" : doesPageExist,
        "pagename": pagename,
        "entries": util.list_entries(),
        "entry": entry,
        "randomPage": get_randomPage()
    })


#This is the page that creates a new entry
def create(request):
    #if there is an entry
    if request.method == 'POST':  
        #get data of said entry        
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = f"# {title}\n{form.cleaned_data['content']}"
            if util.get_entry(title):
                #if the entry already exists make pop up error message or something
                return render(request,"encyclopedia/create.html",{
                    "form": form,
                    "isDupe" : True,
                    "randomPage": get_randomPage()
                })
            else:
                util.save_entry(title, content)
                return render(request,"encyclopedia/entry.html",{
                    "pagename": title,
                    "entries": util.list_entries(),
                    "doesPageExist" : True,
                    "entry" : markdown2.markdown(util.get_entry(title)),
                    "randomPage": get_randomPage()
                })
        else: 
            return render(request,"encyclopedia/create.html", {
            "form": form,
            "randomPage": get_randomPage()
        })
    return render(request,"encyclopedia/create.html",{
        "form" : NewEntryForm(),
        "isDupe" : False,
        "randomPage": get_randomPage()
    })


#This is the page that searches for a particular entry
def search(request):
    if request.method == 'POST':
        form = request.POST
        search_term = form['q'].lower()
        search_results= []
        entry_list = util.list_entries()
        for entry in entry_list:
            if search_term == entry.lower():
                return render(request, 'encyclopedia/entry.html', {
                    "pagename": search_term,
                    "entries": util.list_entries(),
                    "doesPageExist" : True,
                    "entry" : markdown2.markdown(util.get_entry(search_term)),
                    "randomPage": get_randomPage()
                })
            elif str(search_term) in entry.lower():
                search_results.append(entry)
        hasResults = len(search_results) > 0
        return render(request, 'encyclopedia/search.html',{
            "search_term" : search_term,
            "search_results": search_results,
            "hasResults": hasResults,
            "randomPage": get_randomPage()
        })
    
def edit(request,page):
    if request.method == 'POST':  
        form = NewEditForm(request.POST)
        if form.is_valid():
            title = page
            content = f"# {title}\n {form.cleaned_data['content']}"
            util.save_entry(title, bytes(content, 'utf8'))
            return render(request,"encyclopedia/entry.html",{
                "pagename": page,
                "entries": util.list_entries(),
                "doesPageExist" : True,
                "entry" : markdown2.markdown(util.get_entry(page)),
                "randomPage": get_randomPage()
            })
    content = util.get_entry(page)
    intro = f"# {page}"
    final_content = content.replace(intro,"",1).replace("\n","",1).replace("\r","")
    form = NewEditForm(initial={'content':final_content, 'title':page})
    return render(request, 'encyclopedia/edit.html',{
        "page": page,
        "content" : final_content,
        "form": form,
        "randomPage": get_randomPage()
    })

def random(request):
    entries = util.list_entries()
    random_page = random.choice(entries)
    return render(request, "encyclopedia/index.html",{
        "randomPage": get_randomPage()
    })