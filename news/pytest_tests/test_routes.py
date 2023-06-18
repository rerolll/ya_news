from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    "name, args",
    (
        ("news:home", None),
        ("news:detail", pytest.lazy_fixture("id_note_for_arg")),
        ("users:login", None),
        ("users:logout", None),
        ("users:signup", None),
    ),
)
@pytest.mark.django_db
def test_pages_availability_for_anonymous_user(client, name, args):
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    "parametrized_client, expected_status",
    (
        (pytest.lazy_fixture("admin_client"), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture("author_client"), HTTPStatus.OK),
    ),
)
@pytest.mark.parametrize(
    "name",
    ("news:edit", "news:delete"),
)
@pytest.mark.django_db
def test_pages_availability_for_different_users(
    parametrized_client, name, comment, expected_status
):
    url = reverse(name, args=(comment.id,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "name",
    ("news:edit", "news:delete"),
)
def test_redirects(client, name, comment):
    login_url = reverse("users:login")
    url = reverse(name, args=(comment.id,))
    expected_url = f"{login_url}?next={url}"
    response = client.get(url)
    assertRedirects(response, expected_url)
