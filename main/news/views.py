from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView

from .models import News, Category
from .forms import NewsForms, NewsFormsModel, UserRegisterForm, UserLoginForm
from django.contrib.auth import login, logout
from django.contrib import messages


class IndexView(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')

# def index(request):
#     cont = {
#         'news': News.objects.all(),
#         'title': 'Список новостей',
#     }
#     return render(request, 'news/index.html', context=cont)


class CategoryNews(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 4
    #queryset = News.objects.select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # ТАК неправильно!!!
        # if self.object_list:
        #     context['title'] = f'Категория: {self.object_list[0].category}'
        # else:
        #     context['title'] = f'Категория: не имеет статей!'
        context['title'] = f'Категория: {Category.objects.get(pk=self.kwargs["category_id"])}'
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')


# def get_category(request, category_id):
#     cont = {
#         'news': News.objects.filter(category_id=category_id),
#         'category': Category.objects.get(pk=category_id),
#         'title': 'Статьи по категориям',
#         }
#     return render(request, 'news/category.html', context=cont)


def view_news(request, news_id):
    # news_item = News.objects.get(pk=news_id)
    news_item = get_object_or_404(News, pk=news_id)
    return render(request, 'news/view_news.html', {'news_item': news_item})


def add_news(request):
    if request.method == 'POST':
        form = NewsForms(request.POST)
        if form.is_valid():
            #print(form.cleaned_data)
            new = News.objects.create(**form.cleaned_data)
            return redirect(new)
    else:
        form = NewsForms()
    return render(request, 'news/add_news.html', {'form': form})


def add_news_1(request):
    if request.method == 'POST':
        form = NewsFormsModel(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = NewsFormsModel()
    return render(request, 'news/add_news_1.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Вы успешно зарегистрировались!")
            return redirect('index')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html',  {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')
