from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment, News


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, form_data, news):
    COMMENT_BEFORE_REQUEST = Comment.objects.count()
    url = reverse("news:detail", args=(news.id,))
    response = client.post(url, data=form_data)
    login_url = reverse("users:login")
    expected_url = f"{login_url}?next={url}"
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == COMMENT_BEFORE_REQUEST


@pytest.mark.django_db
def test_auth_user_can_create_comment(author_client, form_data, news):
    COMMENT_BEFORE_REQUEST = Comment.objects.count()
    url = reverse("news:detail", args=(news.id,))
    response = author_client.post(url, data=form_data)
    new_comment = Comment.objects.last()
    assert Comment.objects.count() == COMMENT_BEFORE_REQUEST + 1
    assert new_comment.text == form_data["text"]


def test_user_cant_use_bad_words(author_client, news):
    COMMENT_BEFORE_REQUEST = Comment.objects.count()
    url = reverse("news:detail", args=(news.id,))
    bad_words_data = {"text": f"Какой-то текст, {BAD_WORDS[0]}, еще текст"}
    response = author_client.post(url, data=bad_words_data)
    assertFormError(response, form="form", field="text", errors=WARNING)
    assert Comment.objects.count() == COMMENT_BEFORE_REQUEST


def test_author_can_edit_comment(author_client, form_data, comment, news):
    url = reverse("news:edit", args=(comment.id,))
    response = author_client.post(url, data=form_data)
    assertRedirects(
        response, (reverse("news:detail", args=(news.id,)) + "#comments")
    )
    comment.refresh_from_db()
    assert comment.text == form_data["text"]


def test_user_cant_edit_comment_of_another_user(
    reader_client, form_data, comment
):
    url = reverse("news:edit", args=(comment.id,))
    response = reader_client.post(url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment = Comment.objects.last()
    comment.refresh_from_db()
    assert comment.text != form_data["text"]
