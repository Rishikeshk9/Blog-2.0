from django.contrib.auth.models import User
from django.db import models
from django.db.models import F
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation



from django.utils import timezone

from hitcount.models import HitCount, HitCountMixin

# Create your models here.


class Post(models.Model, HitCountMixin):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    visit = GenericRelation(HitCount, object_id_field='object_pk',
                            related_query_name='hit_count_generic_relation', default=0)
    likes = models.ManyToManyField(User, related_name = "likes",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
