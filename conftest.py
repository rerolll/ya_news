from datetime import timedelta
from random import randint
import pytest

# Импортируем модель заметки, чтобы создать экземпляр.
from news.models import News, Comment

from django.conf import settings
from django.utils import timezone


@pytest.fixture
def author(django_user_model):  
    return django_user_model.objects.create(username='Автор')

@pytest.fixture
def reader(django_user_model):  
    return django_user_model.objects.create(username='Читатель')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client

@pytest.fixture
def reader_client(reader, client):
    client.force_login(reader)
    return client

@pytest.fixture
def news(author):
    return News.objects.create(
        title='Заголовок',
        text='Текст заметки',
    )

@pytest.fixture
def id_note_for_arg(news):  
    return news.id,

@pytest.fixture
def comment(news, author):
    return Comment.objects.create(
        news= news,
        author= author,
        text="Текст комментария",
    )
    
@pytest.fixture
def id_comment_for_args(comment):  
    return comment.id,

@pytest.fixture
def news_bulk():
    today = timezone.now()
    news = []
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
        news.append(News(
            title=f'Title {index}',
            text ='Text',
            date=today - timedelta(days=randint(1, 100))
        ))
        News.objects.bulk_create(news)

@pytest.fixture
def comments_bulk(news, author):
    today = timezone.now()
    comments = []
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
        comments.append(Comment(
            news= news,
            author= author,
            text="Текст комментария",
            
        ))
        comment.created =today - timedelta(days=randint(1, 100))
        Comment.objects.bulk_create(comments)

@pytest.fixture
def form_data():
    return {
        'text': 'Новый Текст комментария',
    }