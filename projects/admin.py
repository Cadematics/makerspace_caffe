from django.contrib import admin
from .models import Project  # Ensure you import the correct model
from .models import Reward, Pledge, Petition, UserProfile
# from .models import Event

admin.site.register(Project)  # Correct model name (singular)


@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'project', 'crowdfunding_event')
    list_filter = ('project', 'crowdfunding_event')
    search_fields = ('title',)



@admin.register(Pledge)
class PledgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'event', 'reward', 'amount', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('user__username', 'project__title', 'event__title')



admin.site.register(Petition)

admin.site.register(UserProfile)


