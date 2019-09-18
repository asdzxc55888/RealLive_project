from django import template
from django.contrib.auth.models import Group
from livePage.models import UserSetting

register = template.Library()

@register.filter(name='is_in')
def is_in(user, groupName):
    group = Group.objects.get(name=groupName)
    return True if group in user.groups.all() else False

@register.filter(name='is_living')
def is_living(user):
    data = UserSetting.objects.get(userId=user)
    return data.isLive
