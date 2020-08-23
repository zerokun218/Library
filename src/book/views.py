from django.shortcuts import render,redirect, get_object_or_404
from django.utils import timezone
from .models import Book,Test, SpecifyBook, Category
from . import forms
from account.models import Profile

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from datetime import date, timedelta
# Create your views here.
import re

def book_list(request):
    obj = Book.objects.all()

    template_name = 'book/book_list.html'

    context = {'book_list':obj}
    return render(request, template_name, context)

def book_page_list(request, page):
    obj = Book.objects.all()
    template_name = 'book/book_list.html'
    pages = len(obj)
    p = pages//4
    if p*4 != pages:
        p += 1
    page_list = [i for i in range(1,p+1)]
    context = {'book_list': obj[0+4*(page-1):4+4*(page-1)],
                'pages': page_list,
                'page_active': page,
                }
    return render(request, template_name, context)

def detail_book(request, id):
    obj = get_object_or_404(Book, id = id)
    template_name = 'book/detail_book.html'

    comment = obj.commentbook_set.all()
    amount_comment = len(comment)
    context = {'object': obj, 'comment':comment, 'amount_comment':amount_comment}

    return render(request, template_name, context)



@login_required
def create_book(request):
    form = forms.BookForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        name = form.cleaned_data.get('name')
        name = re.sub('\s+',' ', name)
        name = name.capitalize()
        obj.name = name
        obj.author = obj.author.capitalize()

        # ----just testing multiple choices-----
        # ----conclusion: no need comment section------

        # choices = form.cleaned_data.get('category')
        # # in testing-acepted
        # print(choices)
        # for i in choices:
        #     obj.category.add(i)
        obj.save()
        return redirect('/book/page/1')
    template_name = 'book/form.html'
    context = {'form': form}
    return render(request, template_name, context)

@login_required
def update_book(request, id):
    obj = get_object_or_404(Book, id = id)
    form = forms.BookForm(request.POST or None, instance=obj)
    if form.is_valid():
        obj = form.save(commit=False)
        name = form.cleaned_data.get('name')
        name = re.sub('\s+',' ', name)
        name = name.capitalize()
        obj.name = name
        obj.author = obj.author.capitalize()
        # ----just testing multiple choices-----
        # ----conclusion: no need comment section------

        # if form.cleaned_data.get('category'):
        #     for i in obj.category.all():
        #         obj.category.remove(i)
        #     for i in form.cleaned_data.get('category'):
        #         obj.category.add(i)
        obj.save()
        return redirect('/book/page/1')
    template_name = 'book/update_book.html'
    context = {'form': form, 'object': obj}
    return render(request, template_name, context)

@login_required
def delete_book(request, id):
    obj = get_object_or_404(Book, id = id)
    if request.POST: # request.method = 'post'
        obj.delete()
        return redirect('/book/page/1')
    template_name = 'book/delete_book.html'
    context = {'object': obj}
    return render(request, template_name, context)

@login_required
def add_book_to_profile(request, id):
    obj = get_object_or_404(Book, id = id)
    is_existed = obj.specifybook_set.filter(user=request.user)
    if request.POST:
        user = request.user
        user.profile.books.add(obj)

        if is_existed:
            # new_obj = get_object_or_404(SpecifyBook, user = user, book = obj)
            new_obj = SpecifyBook.objects.get(user = user, book = obj)
            new_obj.borrow_time = date.today()
            new_obj.charge_time = new_obj.borrow_time + timedelta(days=25)
            new_obj.is_charge = False
            new_obj.save()
        else:
            new_spec_book = obj.specifybook_set.create(user=user, is_charge = False, borrow_time=date.today(), charge_time=date.today() + timedelta(days=15))
            new_spec_book.save()
        obj.amount -= 1
        obj.save()
        user.save()
        return redirect('/book/user_list/' + user.username)
    existing = True
    if is_existed and obj.specifybook_set.filter(user=request.user)[0].is_charge == False:
        existing = False
    context = {'object': obj, "is_existed": existing}
    template_name = 'book/add_book_to_profile.html'
    return render(request, template_name, context)



# def test_form_view(request):
#     form = forms.TestForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         form = forms.TestForm()
#     return render(request, 'book/test_form_time.html', {'form': form})
#
# def test_view(request):
#     obj = Test.objects.all()
#
#     return render(request, 'book/test_time.html', {'object': obj})


@login_required
def user_book_view(request, username):
    user = get_object_or_404(User, username__iexact=username)
    spec_book =  SpecifyBook.objects.filter(user = user).order_by('-borrow_time','-id')
    context = {
        'object': spec_book,
        'username':user.username
    }
    return render(request, "book/user_list_book.html", context)


@login_required
def comment_book(request, id):
    user = request.user
    form = forms.CommentForm(request.POST or None)
    book = get_object_or_404(Book, id = id)
    if request.POST:
        obj = form.save(commit=False)
        obj.user = request.user
        obj.book = book
        obj.save()
        return redirect('/book/' + str(id))
    context = {'form': form, 'title': book.name}
    template_name = 'book/comment_book.html'
    return render(request, template_name, context)


@login_required
def create_category(request):
    form = forms.CategoryForm(request.POST or None)
    if request.POST:
        form.save()
        return redirect('/book/page/1')
    return render(request, 'book/new_category.html', {'form':form})

def category_list_view(request, title):
    obj = Category.objects.get(name__iexact = title)
    book_list = obj.book_set.all()
    return render(request, 'book/category_book_list.html', {'object': book_list, 'title': title})


# --------Charge Book by current User----------------
# @login_required
# def charge_book(request, id):
#     obj = get_object_or_404(Book, id = id)
#     if request.POST:
#         user = request.user
#         spec_book = SpecifyBook.objects.get(user = user, book = obj)
#         spec_book.is_charge = True
#         spec_book.save()
#         obj.amount += 1
#         obj.save()
#         return redirect("/book/user_list")
#
#     charged = False
#     if SpecifyBook.objects.filter(user = request.user, book = obj) and SpecifyBook.objects.get(user = request.user, book = obj).is_charge == False:
#         charged = True
#     context = {'object': obj,
#                 "charged": charged,
#                     'spec_book':SpecifyBook.objects.get(user = request.user, book = obj)
#                     }
#     return render(request, 'book/charge_book.html', context)



@login_required
def charge_book(request, id, username):
    user = get_object_or_404(User, username__iexact=username)
    obj = get_object_or_404(Book, id = id)
    if request.POST:
        spec_book = SpecifyBook.objects.get(user = user, book = obj)
        spec_book.is_charge = True
        spec_book.save()
        obj.amount += 1
        obj.save()
        return redirect("/book/user_list/"+user.username)
    charged = False
    if SpecifyBook.objects.filter(user = user, book = obj) and SpecifyBook.objects.get(user =user, book = obj).is_charge == False:
        charged = True
    context = {'object': obj,
                "charged": charged,
                    'spec_book':SpecifyBook.objects.get(user = user, book = obj),
                        'username': user.username
                    }
    return render(request, 'book/charge_book.html', context)


# confirm Student return book by Librarian or admin(staff)---completed
# need to select specify user's list book to confirm
@login_required
def charge_book_confirm_view(request):
    obj = SpecifyBook.objects.filter(is_charge=False)
    name = request.GET.get('qStudent')
    title = request.GET.get('qBook')
    announce = ''
    if title:
        title = re.sub('\s+', ' ', title)
    if not (name and title):
        announce = 'Not allow blank Field!!'
        return render(request, 'book/charge_book_confirm.html',{'announce': announce})
    if request.GET:
        if User.objects.filter(username__iexact=name):
            user = User.objects.get(username__iexact=name)
            if Book.objects.filter(name__iexact=title):
                book =Book.objects.get(name__iexact=title)
                if obj.filter(user=user, book=book):
                    charge_book = obj.get(user=user, book=book)
                    return redirect('/book/'+str(book.id)+'/' + str(user.username)+'/charge_book')
            else:
                announce = 'Book ' + title + ' is not exit!!'
                return redirect('/book/user_list/'+user.username)
        else:
            announce = 'User ' + name + ' is not exit!!'
    context = {
            'announce': announce,
        }
    return render(request, 'book/charge_book_confirm.html', context)


def report_view(request):
    return render(request, 'book/report.html')
