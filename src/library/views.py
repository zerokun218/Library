from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from book.models import Book
from django.db.models import Q

def index(request):
    return render(request, 'index.html')


@login_required
def search_view(request):
    user = request.user
    search = request.GET.get('q')
    obj = Book.objects.filter(
        Q(name__contains=search)|
        Q(author__contains=search)|
        Q(description__contains=search)
    )
    return render(request, "search.html", {'book_list': obj, "query": search})
