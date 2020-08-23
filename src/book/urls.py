from django.urls import path
from . import views

# app_name='book'
# call in template: {% url 'book:all' %}

urlpatterns = [
    path('', views.book_list, name ="all"),
    path('<int:id>/',views.detail_book, name="detail_book"),
    path('<int:id>/edit/', views.update_book, name="update_book"),
    path('<int:id>/delete/', views.delete_book, name="delete_book"),
    path('new/', views.create_book, name = "new_book"),
    path('<int:id>/add-book-to-profile', views.add_book_to_profile, name="add_book_to_profile"),
    path('<int:id>/<str:username>/charge_book', views.charge_book, name="charge_book"),
    path('user_list/<str:username>', views.user_book_view, name="user_list"),
    path('page/<int:page>/', views.book_page_list, name="book_page_list"),
    path('<int:id>/comment/', views.comment_book, name='comment_book'),
    path('new_category/', views.create_category, name='new_category'),
    path('category/<str:title>', views.category_list_view, name='category_book_list'),
    path('test/',views.charge_book_confirm_view, name = 'charge_book_confirm'),
    path('report/', views.report_view, name= 'report'),

    # path('test/', views.test_view, name='test_view'),
    # path('test/new/', views.test_form_view, name = 'test_form_view')
]
