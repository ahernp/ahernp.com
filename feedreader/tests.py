from .factories import EntryFactory, FeedFactory, GroupFactory
from .views import count_entries


def test_entry_feed_group_structure():
    entry = EntryFactory.build()

    assert entry.feed.title == "Feed 0"
    assert entry.feed.group is None


def test_counting_entries():
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

    counts = count_entries([group_1, group_2], [feed_1, feed_11, feed_3], entries)

    assert len(counts) == 4
    assert "group_counts" in counts
    assert len(counts["group_counts"]) == 2

    import pdb

    pdb.set_trace()  # Start debugging
    assert counts["group_counts"][0].group.name == group_1.name
    assert counts["group_counts"][0].total_count == 3
    assert counts["group_counts"][0].unread_count == 2
    assert len(counts["group_counts"][0].feed_counts) == 2

    assert counts["group_counts"][0].feed_counts[0].feed.title == feed_1.title
    assert counts["group_counts"][0].feed_counts[0].total_count == 2
    assert counts["group_counts"][0].feed_counts[0].unread_count == 1
    assert counts["group_counts"][0].feed_counts[1].feed.title == feed_11.title
    assert counts["group_counts"][0].feed_counts[1].total_count == 1
    assert counts["group_counts"][0].feed_counts[1].unread_count == 1

    assert counts["group_counts"][1].group.name == group_2.name
    assert counts["group_counts"][0].total_count == 0
    assert counts["group_counts"][0].unread_count == 0
    assert len(counts["group_counts"][0].feed_counts) == 0

    assert "non_group_feed_counts" in counts
    assert len(counts["non_group_feed_counts"]) == 1
    assert counts["non_group_feed_counts"][0].feed.title == feed_3.title
    assert counts["non_group_feed_counts"][0].total_count == 1
    assert counts["non_group_feed_counts"][0].unread_count == 1

    assert "total_entries" in counts
    assert "total_entries" == 3

    assert "total_unread_entries" in counts
    assert "total_unread_entries" == 2
