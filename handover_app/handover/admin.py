from django.contrib import admin
from .models import Tag, Comment, Handover


class TagAdmin(admin.ModelAdmin):
    list_display = ['tag_no',
                    'tag',
                    ]


class CommentAdmin(admin.ModelAdmin):
    list_display = ['comment_no',
                    'comment',
                    'created_at',
                    ]


class HandoverAdmin(admin.ModelAdmin):
    list_display = ['handover_no',
                    'user_name',
                    'created_at',
                    ]


admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Handover, HandoverAdmin)
