from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreationForm
from .models import User


class MyUserAdmin(UserAdmin):
    add_form = UserCreationForm

    list_display = ('user_ID', 'username', 'is_staff', 'user_image')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    fieldsets = (
        (None, {'fields': ('username', 'password', 'user_ID',)}),
        ('個人情報', {'fields': ('first_name', 'last_name', 'email', 'user_image')}),
        ('権限', {'fields': ('is_active', 'is_staff', 'is_superuser',
                           'groups', 'user_permissions'
                           )
                }
         ),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'user_ID', 'password1', 'password2')}
         ),
    )
    search_fields = ('user_ID',)
    ordering = ('user_ID',)
    filter_horizontal = ()


admin.site.register(User, MyUserAdmin)



