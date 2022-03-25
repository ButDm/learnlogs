"""Определяет схемы URL для learning_logs."""

from django.urls import path
from . import views

app_name = 'learning_logs'
urlpatterns = [
    # Домашняя страница
    path('', views.index, name='index'),
    # Страница приветствия
    path('greet/', views.greet, name='greet'),
    # Страница с дополнительной информацией
    path('extra_info/', views.extra_info, name='extra_info'),
    # Страница со списком всех тем.
    path('topics/', views.topics, name='topics'),
    # Страница со списком всех тем.
    path('public_topics/', views.public_topics, name='public_topics'),
    # Страница с подробной информацией по отдельной теме
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    # Страница с подробной информацией по отдельной теме
    path('public_topics/<int:topic_id>/', views.public_topic,
            name='public_topic'),
    # Страница для добавления новой темы
    path('new_topic/', views.new_topic, name='new_topic'),
    # Страница для добавления новой записи.
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    # Страница для редактирования записи
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    ]
