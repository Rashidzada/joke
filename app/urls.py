from django.urls import path
from .import views
urlpatterns = [
    path('',views.index,name='index'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('register/',views.register,name='register'),
    path('login_view/',views.login_view,name='login_view'),
    path('logout/',views.logout_view,name='logout_view'),
    path('add_joke/',views.add_joke,name='add_joke'),
    path('edit_joke/<int:joke_id>/',views.edit_joke,name='edit_joke'),
    path('delete_joke/<int:joke_id>/',views.delete_joke,name='delete_joke'),
    path('view_joke/<int:joke_id>/',views.view_joke,name='view_joke'),
]