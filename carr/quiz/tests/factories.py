from django.contrib.auth.models import User
import factory


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Sequence(lambda n: "user%d" % n)
