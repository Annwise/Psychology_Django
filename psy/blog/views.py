from django.shortcuts import render
from django.http import HttpResponseNotFound
import os
from django.conf import settings


def blog(request):
    return render(request, 'blog/blog.html')


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
