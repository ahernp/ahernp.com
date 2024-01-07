import factory
from django.utils import timezone

from .models import Timer


class TimerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Timer

    target = factory.LazyFunction(timezone.now)
    label = factory.Sequence(lambda n: "Timer %s" % n)
    slug = factory.Sequence(lambda n: "timer-%s" % n)
