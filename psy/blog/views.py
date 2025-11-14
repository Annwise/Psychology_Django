from django.shortcuts import render
from django.http import HttpResponseNotFound
import os
from django.conf import settings
from django.core.paginator import Paginator


def blog(request):
    # Список статей (можно добавить дату и автора)
    articles = [
        {
            'id': 1,
            'title': 'Тревога или паническая атака? Разбираемся',
            'excerpt': 'Достаточно часто ко мне обращаются клиенты, думая что у них паническая атака, а на самом деле тревога или наоборот, думая ...',
            'author': 'Мария Ондрушка',
            'published_date': '2025-01-01',
            'image': 'blog/images/11.jpg',
            'url': '/blog/article/1/'
        },
        {
            'id': 2,
            'title': '4 способа пережить паническую атаку',
            'excerpt': 'Если вы хотите спросить, что такое панические атаки, значит вы совершенно точно ими не страдаете. Самое главное это ...',
            'author': 'Мария Ондрушка',
            'published_date': '2025-01-05',
            'image': 'blog/images/22.jpg',
            'url': '/blog/article/2/'
        },
        {
            'id': 3,
            'title': 'Пассивная агрессия. В чём она проявляется?',
            'excerpt': '"Да ты без меня никто!", "Что бы ты без меня делала". Замечали за знакомыми? Или может за собой? Это признаки пассивной агрессии ...',
            'author': 'Мария Ондрушка',
            'published_date': '2025-01-10',
            'image': 'blog/images/33.jpg',
            'url': '/blog/article/3/'
        },
        {
            'id': 4,
            'title': 'Как снизить тревожность? Полезные лайфхаки',
            'excerpt': 'Повышенная тревожность, может возникнуть в жизни каждого, но при систематическом повторении, может оказаться негативное ...',
            'author': 'Мария Ондрушка',
            'published_date': '2025-01-15',
            'image': 'blog/images/44.jpg',
            'url': '/blog/article/4/'
        },
    ]

    # Получаем параметры
    sort = request.GET.get('sort', '-published_date')  # по умолчанию — новые первыми
    author_filter = request.GET.get('author', '')

    # Фильтруем статьи
    filtered_articles = articles

    if author_filter:
        filtered_articles = [a for a in filtered_articles if author_filter.lower() in a['author'].lower()]

    # Сортируем
    if sort == 'title':
        filtered_articles.sort(key=lambda x: x['title'])
    elif sort == '-title':
        filtered_articles.sort(key=lambda x: x['title'], reverse=True)
    elif sort == 'author':
        filtered_articles.sort(key=lambda x: x['author'])
    elif sort == '-author':
        filtered_articles.sort(key=lambda x: x['author'], reverse=True)
    elif sort == 'published_date':
        filtered_articles.sort(key=lambda x: x['published_date'])
    elif sort == '-published_date':
        filtered_articles.sort(key=lambda x: x['published_date'], reverse=True)

    # Пагинация
    paginator = Paginator(filtered_articles, 2)  # 2 статьи на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Получаем всех авторов для фильтра
    authors = list(set([a['author'] for a in articles]))

    return render(request, 'blog/blog.html', {
        'page_obj': page_obj,
        'sort': sort,
        'author_filter': author_filter,
        'authors': authors
    })


def article(request, article_id):
    # Путь к файлу статьи
    article_path = os.path.join(settings.BASE_DIR, 'blog', 'articles', f'article{article_id}.html')

    # Проверяем, существует ли файл
    if not os.path.exists(article_path):
        return HttpResponseNotFound("Статья не найдена")

    # Читаем содержимое файла
    with open(article_path, 'r', encoding='utf-8') as f:
        content = f.read()

    context = {
        'article_id': article_id,
        'content': content
    }

    return render(request, 'blog/article.html', context)
