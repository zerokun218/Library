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

    class trie:
        def __init__(self):
            self.root = dict()
            self.root['end'] = -1
            self.root['max'] = -1
        def add_string(self,s,priority):
            current_dict = self.root
            for letter in s:
                if letter in current_dict:
                    current_dict = current_dict[letter]
                else:
                    current_dict[letter] = {'max':-1}
                    current_dict = current_dict[letter]
            if 'end' in current_dict:
                if current_dict['end'] < priority:
                    current_dict['end'] = priority
            else:
                current_dict['end'] = priority
            if current_dict['max'] < priority:
                current_dict['max'] = priority
        def find_string(self,s):
            current_dict = self.root
            for letter in s:
                if letter in current_dict:
                    current_dict = current_dict[letter]
                else:
                    return False
            if 'end' in current_dict:
                return True
            else:
                return False
        def get_max(self,current_dict):
            curr_max = current_dict['max']
            for key in current_dict:
                if key == 'end':
                    if curr_max < current_dict['end']:
                        curr_max = current_dict['end']
                elif key == 'max':
                    if curr_max < current_dict['max']:
                        curr_max = current_dict['max']
                else:
                    k = self.get_max(current_dict[key])
                    if curr_max < k:
                        curr_max = k
            current_dict['max'] = curr_max
            return curr_max
        def find_max_weight(self,s):
            current_dict = self.root
            for letter in s:
                if letter in current_dict:
                    current_dict = current_dict[letter]
                else:
                    return -1
            if current_dict['max'] == -1:
                return self.get_max(current_dict)
            else:
                return current_dict['max']

    obj = Book.objects.filter(
        Q(name__contains=search)
    )
    return render(request, "search.html", {'book_list': obj, "query": search})
