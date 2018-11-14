import pytest

from unittest.mock import patch

from django.urls import reverse

from .factories import EntryFactory, FeedFactory, GroupFactory
from .views import count_entries


def test_entry_feed_group_structure():
    entry = EntryFactory.build()

    assert entry.feed.title == "Feed 0"
    assert entry.feed.group is None


@patch("feedreader.views.Group.objects")
@patch("feedreader.views.Feed.objects")
def test_counting_entries(mock_feed_qs, mock_group_qs):
    group_1 = GroupFactory.build()
    group_2 = GroupFactory.build()

    feed_1 = FeedFactory.build(group=group_1)
    feed_11 = FeedFactory.build(group=group_1)
    feed_3 = FeedFactory.build()
    entries = [
        EntryFactory.build(feed=feed_1),
        EntryFactory.build(feed=feed_1, read_flag=True),
        EntryFactory.build(feed=feed_11),
        EntryFactory.build(feed=feed_3),
    ]

    mock_feed_qs.all.return_value = [feed_1, feed_11, feed_3]
    mock_group_qs.all.return_value = [group_1, group_2]

    counts = count_entries(entries)

    assert len(counts) == 3, "Expected counts to have 3 attributes"
    assert "group_counts" in counts
    assert len(counts["group_counts"]) == 2

    assert counts["group_counts"][0].group.name == group_1.name
    assert counts["group_counts"][0].total_count == 3
    assert len(counts["group_counts"][0].feed_counts) == 2

    assert counts["group_counts"][0].feed_counts[0].feed.title == feed_1.title
    assert counts["group_counts"][0].feed_counts[0].total_count == 2
    assert counts["group_counts"][0].feed_counts[1].feed.title == feed_11.title
    assert counts["group_counts"][0].feed_counts[1].total_count == 1

    assert counts["group_counts"][1].group.name == group_2.name
    assert counts["group_counts"][1].total_count == 0
    assert len(counts["group_counts"][1].feed_counts) == 0

    assert "non_group_feed_counts" in counts
    assert len(counts["non_group_feed_counts"]) == 1

    assert counts["non_group_feed_counts"][0].feed.title == feed_3.title
    assert counts["non_group_feed_counts"][0].total_count == 1

    assert "total_entries" in counts
    assert counts["total_entries"] == 4


@pytest.mark.django_db
def test_mark_all_read_requires_login(client, admin_client):
    entry = EntryFactory.create()
    post_data = {}
    response = client.post(reverse("mark-all-entry-read"), post_data, follow=True)
    assert response.status_code == 200
    assert b"<title>Log in | Django site admin</title>" in response.content

    response = admin_client.post(reverse("mark-all-entry-read"), post_data, follow=True)
    assert response.status_code == 200
    assert b"<title>Feedreader (1)</title>" in response.content


@pytest.mark.django_db
def test_mark_entry_read_requires_login(client, admin_client):
    entry = EntryFactory.create()
    post_data = {"entry_id": entry.id}
    response = client.post(reverse("mark-entry-read"), post_data, follow=True)
    assert response.status_code == 200
    assert b"<title>Log in | Django site admin</title>" in response.content

    response = admin_client.post(reverse("mark-entry-read"), post_data, follow=True)
    assert response.status_code == 200
    assert b"<title>Feedreader (1)</title>" in response.content
