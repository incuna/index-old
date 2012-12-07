from django.template.defaultfilters import slugify


def generate_slug(cls, value):
    count = 1
    slug = slugify(value)
    if not isinstance(cls, type):
        cls = cls.__class__

    def _get_query(cls, **kwargs):
        if cls.objects.filter(**kwargs).count():
            return True

    while _get_query(cls, slug=slug):
        slug = slugify(u'{0}-{1}'.format(value, count))
        # make sure the slug is not too long
        while len(slug) > cls._meta.get_field('slug').max_length:
            value = value[:-1]
            slug = slugify(u'{0}-{1}'.format(value, count))
        count = count + 1
    return slug

