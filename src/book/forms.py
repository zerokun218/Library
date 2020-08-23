from django import forms
from .models import Book,Test, CommentBook, Category



class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name','author','category', 'url','image','description']
        labels = {
            'url': 'Link to Book'
        }

    # multiplechoices ManyToManyField in Django
    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields["category"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["category"].queryset = Category.objects.all()

    def clean_name(self, *args, **kwargs):
        instance = self.instance
        name = self.cleaned_data.get('name')
        author = self.cleaned_data.get('author')
        qs = Book.objects.filter(name__iexact=name, author__iexact=author)
        if instance is not None:
            qs = qs.exclude(id=instance.id)
        if qs.exists():
            raise forms.ValidationError('This Book has already been used with the same name and author')
        return name

# class TestForm(forms.ModelForm):
#     class Meta:
#         model = Test
#         fields = ['name', 'date_create']

class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentBook
        fields = ['content']
        labels = {
            'content': 'Comment'
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
