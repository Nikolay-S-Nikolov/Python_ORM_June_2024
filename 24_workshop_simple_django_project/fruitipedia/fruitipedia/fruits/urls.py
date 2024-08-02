from django.urls import path, include

from fruitipedia.fruits import views

urlpatterns = (
    path('', views.index, name="index"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('create-fruit/', views.CreateFruitView.as_view(), name="create_fruit"),
    path('create-category/', views.create_category, name="create_category"),
    path('<int:pk>/', include([
        path('details-fruit/', views.details_view, name="details_view"),
        path('edit-fruit/', views.edit_view, name="edit_view"),
        path('delete-fruit/', views.DeleteFruitView.as_view(), name="delete_view")
    ]))
)
