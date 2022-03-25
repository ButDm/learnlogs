from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404


from .models import Topic, Entry
from .forms import TopicForm, EntryForm
# Create your views here.


def index(request):
    """Домашняя страница приложения Learning Log"""
    return render(request, 'learning_logs/index.html')


def greet(request):
    """Домашняя страница приложения Learning Log"""
    return render(request, 'learning_logs/greet.html')


def extra_info(request):
    """Домашняя страница приложения Learning Log"""
    return render(request, 'learning_logs/extra_info.html')


@login_required
def topics(request):
    """Выводит список тем."""
    public_topics = Topic.objects.filter(public=True).order_by('date_added')
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics, 'public_topics': public_topics}
    return render(request, 'learning_logs/topics.html', context)


def public_topics(request):
    """Выводит список тем."""
    public_topics = Topic.objects.filter(public=True).order_by('date_added')
    context = {'public_topics': public_topics}
    return render(request, 'learning_logs/public_topics.html', context)


@login_required
def topic(request, topic_id):
    """Выводит одну тему и все ее записи."""
    topic = get_object_or_404(Topic, id=topic_id)
    # Проверка того, что тема принадлежит текущему пользователю.
    check_topic_onwer(request, topic)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


def public_topic(request, topic_id):
    """Выводит одну тему и все ее записи."""
    print(111)
    topic = get_object_or_404(Topic, id=topic_id)
    # Проверка того, что тема принадлежит текущему пользователю.
    check_topic_public(topic)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/public_topic.html', context)


@login_required
def new_topic(request):
    """Определяет новую тему."""
    if request.method != 'POST':
        # Данные не отправлялись; создаётся пустая форма.
        form = TopicForm()
    else:
        # Отправлены данные POST; обработать данные.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            if request.POST["public"]:
                # Checkbox was checked
                new_topic.public = request.POST.get("public")
            new_topic.save()

            return redirect('learning_logs:topics')

    # Вывести пустую или недействительную форму.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Создаёт новую запись."""
    topic = get_object_or_404(Topic, id=topic_id)
    check_topic_onwer(request, topic)
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        form = EntryForm()
    else:
        # Оправлены данные POST; обработать данные.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.owner = request.user
            new_entry.save()
            if topic.owner == new_entry.owner and not topic.public:
                return redirect('learning_logs:topic', topic_id=topic.id)
            else:
                return redirect('learning_logs:public_topic',
                                topic_id=topic.id)
    # Вывести пустую или недействительную фоаму.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Редактирует существующую запись."""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    check_topic_onwer(request, topic)
    if request.method != 'POST':
        # Исходный запрос; форма заполняется данными текущей записи.
        form = EntryForm(instance=entry)
    else:
        # Отправка данных POST; обработать данные.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            if topic.owner == entry.owner and not topic.public:
                return redirect('learning_logs:topic', topic_id=topic.id)
            else:
                return redirect('learning_logs:public_topic',
                                topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


def check_topic_onwer(request, topic):
    if topic.owner != request.user:
        if topic.public is not True:
            raise Http404


def check_topic_public(topic):
    if topic.public is not True:
        raise Http404
