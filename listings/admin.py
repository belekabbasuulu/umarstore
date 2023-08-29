from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Product, Category, Review, Size, Color, Season


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')


admin.site.register(Size)


class OrderReviewInline(admin.TabularInline):
    model = Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug',
                    'price', 'get_image', 'available')
    list_filter = ('category', 'available')
    list_editable = ('price', 'available')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="85" height="60">')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [OrderReviewInline]
