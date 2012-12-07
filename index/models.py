import datetime
import re

from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _
from feincms.content.richtext.models import RichTextContent
from feincms.module.medialibrary.models import MediaFile
from feincms.module.page.models import Page
from incunafein.content.medialibrary.models import MediaFileContent

class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.name

class IndexCard(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, default='')
    created = models.DateTimeField(default=datetime.datetime.now, editable=False)
    tags = models.ManyToManyField(Tag)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug': self.slug})

    @staticmethod
    def all_tags(self):
        return self.tags.prefetch_related()

class CardImage(models.Model):
    indexcard = models.ForeignKey(IndexCard)
    imagefile = models.FileField(upload_to='images/')
    created = models.DateTimeField(default=datetime.datetime.now, editable=False)
    downloaded = models.IntegerField(default=0)

    @property
    def popular(self):
        return CardImage.objects.filter(indexcard=self.indexcard).\
            aggregate(Sum('downloaded'))['downloaded__sum']

    @property
    def get_tags(self):
        return [x.name.lower() for x in self.indexcard.all_tags()]

    def __unicode__(self):
        return 'Image {0} for Index Card "{1}"'.format(self.id, self.indexcard)


Page.register_extensions('changedate', 'datepublisher', 'seo', 'titles')
Page.register_templates(
    {
        'key': '1col',
        'title': _('One column'),
        'path': 'base.html',
        'regions': (
            ('main', _('Main content')),
        ),
    },
)
Page.create_content_type(RichTextContent)
Page.create_content_type(MediaFileContent, TYPE_CHOICES=(('default', _('Default')),))

MediaFile.register_filetypes(
    ('image', _('Image'), lambda f: re.compile(r'\.(bmp|jpe?g|jp2|jxr|gif|png|tiff?)$', re.IGNORECASE).search(f)),
    ('video', _('Video'), lambda f: re.compile(r'\.(mov|m[14]v|mp4|avi|mpe?g|qt|ogv|wmv|flv)$', re.IGNORECASE).search(f)),
    ('audio', _('Audio'), lambda f: re.compile(r'\.(au|mp3|m4a|wma|oga|ram|wav)$', re.IGNORECASE).search(f)),
    ('pdf', _('PDF document'), lambda f: f.lower().endswith('.pdf')),
    ('swf', _('Flash'), lambda f: f.lower().endswith('.swf')),
    ('txt', _('Text'), lambda f: f.lower().endswith('.txt')),
    ('flv', _('Flash Video'), lambda f: f.lower().endswith('.flv')),
    ('rtf', _('Rich Text'), lambda f: f.lower().endswith('.rtf')),
    ('zip', _('Zip archive'), lambda f: f.lower().endswith('.zip')),
    ('doc', _('Microsoft Word'), lambda f: re.compile(r'\.docx?$', re.IGNORECASE).search(f)),
    ('xls', _('Microsoft Excel'), lambda f: re.compile(r'\.xlsx?$', re.IGNORECASE).search(f)),
    ('ppt', _('Microsoft PowerPoint'), lambda f: re.compile(r'\.pptx?$', re.IGNORECASE).search(f)),
    ('other', _('Binary'), lambda f: True),  # Must be last
)

