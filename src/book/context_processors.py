from .models import Category, Book, SpecifyBook
from django.db.models.functions import Length
# context_processors
def context_processors_category(request):
    category_list = Category.objects.all()
    book_list = Book.objects.all()
    receipt = SpecifyBook.objects.all().order_by('is_charge','charge_time','-id')
    populate = Book.objects.all()
    populate = sorted(populate, key = lambda x: len(x.specifybook_set.all()))
    populate = populate[::-1]
    return {'context_processors_category': category_list,
                'context_processors_book': book_list,
                    'context_processors_specifybook': receipt,
                    'context_processors_popular_book': populate,
                    }
