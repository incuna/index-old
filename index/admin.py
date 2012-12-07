from django.contrib import admin

from .models import Tag, IndexCard, CardImage


class CardImageInline(admin.StackedInline):
    model = CardImage
    extra = 1


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class IndexCardAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = (CardImageInline,)


class CardImageAdmin(admin.ModelAdmin):
    list_filter = ('indexcard',)


admin.site.register(Tag, TagAdmin)
admin.site.register(IndexCard, IndexCardAdmin)
admin.site.register(CardImage, CardImageAdmin)
