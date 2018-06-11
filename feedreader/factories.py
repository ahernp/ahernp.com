import factory

from .models import Group, Feed, Entry


class GroupFactory(factory.DjangoModelFactory):
    class Meta:
        model = Group

    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: "Group %s" % n)


class FeedFactory(factory.DjangoModelFactory):
    class Meta:
        model = Feed

    id = factory.Sequence(lambda n: n)
    title = factory.Sequence(lambda n: "Feed %s" % n)
    xml_url = factory.Sequence(lambda n: "https://feed-%s-xml-url" % n)
    link = factory.Sequence(lambda n: "https://feed-%s-link" % n)
    description = factory.Sequence(lambda n: "Feed %s description" % n)


class EntryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Entry

    id = factory.Sequence(lambda n: n)
    feed = factory.SubFactory(FeedFactory)
    title = factory.Sequence(lambda n: "Entry %s" % n)
    link = factory.Sequence(lambda n: "https://entry-%s-link" % n)
    description = factory.Sequence(lambda n: "Entry %s description" % n)
