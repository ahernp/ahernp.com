from .factories import EntryFactory


def test_entry_feed_group_structure():
    entry = EntryFactory.build()

    assert entry.feed.title == "Feed 0"
    assert entry.feed.group == None
