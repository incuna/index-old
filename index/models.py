from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Sum
from django.utils import timezone

from .utils import generate_slug


class CardImage(models.Model):
    indexcard = models.ForeignKey('IndexCard')
    imagefile = models.FileField(upload_to='images/')
    created = models.DateTimeField(default=timezone.now, editable=False)
    downloaded = models.IntegerField(default=0)

    def __unicode__(self):
        return 'Image {0} for Index Card "{1}"'.format(self.pk, self.indexcard)

    @property
    def popular(self):
        card_images = CardImage.objects.filter(indexcard=self.indexcard)
        return card_images.aggregate(Sum('downloaded'))['downloaded__sum']

    @property
    def get_tags(self):
        return [x.name.lower() for x in self.indexcard.all_tags()]


class IndexCard(models.Model):
    tags = models.ManyToManyField('Tag')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, default='')
    created = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'index cards'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = generate_slug(IndexCard, self.name)
        return super(IndexCard, self).save(*args, **kwargs)

    @staticmethod
    def all_tags(self):
        return self.tags.prefetch_related()


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = generate_slug(Tag, self.name)
        return super(Tag, self).save(*args, **kwargs)

