from http import HTTPStatus

import pytest
from django.conf import settings
from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
def test_news_list_for_different_users(client, news_bulk):
    url = reverse("news:home")
    response = client.get(url)
    object_list = response.context["object_list"]
    assert object_list.count() == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, news_bulk):
    url = reverse("news:home")
    response = client.get(url)
    object_list = response.context["object_list"]
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comment_order(client, comments_bulk, news):
    url = reverse("news:detail", args=(news.id,))
    response = client.get(url)
    object_list = (response.context["news"]).comment_set.all()
    all_comments = [comments.created for comments in object_list]
    sorted_comments = sorted(all_comments, reverse=False)
    assert all_comments == sorted_comments


@pytest.mark.parametrize(
    "parametrized_client, expected",
    ((pytest.lazy_fixture("author_client"), "form"),),
)
def test_authorized_client_has_form(news, parametrized_client, expected):
    url = reverse("news:detail", args=(news.id,))
    response = parametrized_client.get(url)
    assert expected in response.context


@pytest.mark.parametrize(
    "parametrized_client, expected",
    ((pytest.lazy_fixture("client"), "form"),),
)
def test_authorized_client_has_form(news, parametrized_client, expected):
    url = reverse("news:detail", args=(news.id,))
    response = parametrized_client.get(url)
    assert expected not in response.context
