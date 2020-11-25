from django.urls import path

from trains.views import home, TrainCreateView

urlpatterns = [
    # path('update/<int:pk>/', CityUpdateView.as_view(), name='update'),
    # path('delete/<int:pk>/', CityDeleteView.as_view(), name='delete'),
    path('add/', TrainCreateView.as_view(), name='add'),
    # path('detail/<int:pk>/', CityDetailView.as_view(), name='detail'),
    path('', home, name='home'),
]
