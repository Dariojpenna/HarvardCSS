from urllib import request
from django import forms
from tkinter import Entry
from django.shortcuts import render
import  markdown
from  random import choice


from . import util

def MDConvert(name):
    entry= util.get_entry(name)
    markdowner = markdown.Markdown()
    
    if entry == None:
        return None
    else:
        return markdowner.convert(entry)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entries(request,name):
    entry=MDConvert(name)
    if entry == None:
        return render (request,'encyclopedia/error.html')
    else:
        return render (request,'encyclopedia/entry.html',{
            'title': name,
            'entry': entry
        })


def Searcher (request):
    S = request.GET['q']
      
    if MDConvert(S) is  None:
       
        list= []
        for Ent in util.list_entries ():
            if S.lower () in Ent.lower():
                list.append(Ent)
        return render (request,'encyclopedia/Search.html',{
                    'list':list

        })     
             
    else:
         return render (request,'encyclopedia/entry.html',{
            'entry': MDConvert(S)
         })

class NewEntryForm (forms.Form):
    entry=forms.CharField(label='New Entry')


def newpage(request):
    if request.method =='GET':
        return render (request, 'encyclopedia/newpage.html')

    else:
        t=request.POST['title']
        c=request.POST['content']
        Checkentry= util.get_entry(t)
        if Checkentry is None:
            util.save_entry(t,c)
            addentry=MDConvert(t)
            return render (request,'encyclopedia/entry.html',{
                'entry':addentry,
                'title': t
            })
        else:
            return render (request,'encyclopedia/error.html')

def modify(request):
    if request.method == 'POST':
            entryTitle= request.POST['newtitle']
            entryContent= util.get_entry(entryTitle)
            return render (request, 'encyclopedia/modifyentry.html',{
            'entryTitle': entryTitle,
            'entryContent':entryContent
        })

def editentry(request):
    t=request.POST['title']
    c=request.POST['content']
    util.save_entry(t,c)
    return render (request,'encyclopedia/entry.html',{
        'entry': MDConvert(t),
        'title': t

    })     

def random(request):
    entry= util.list_entries()
    aleatory = choice(entry)
    aleatoryEntry = MDConvert(aleatory)
    return render (request, 'encyclopedia/entry.html',{
        'entry': aleatoryEntry,
        'title': aleatory
    })
    