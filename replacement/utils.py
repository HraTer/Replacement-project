"""
Tools

"""
from django.db.models import Q
from django.urls import reverse_lazy

from replacement.models import Brand


def is_member_of_group(user, group_names):
    """
    Checks if a user belongs to a specific group or groups.

    :param user: The user object.
    :param group_names: A string or a list of group names to check membership.
    :return: True if the user is a member of the specified group(s), False otherwise.
    """
    if isinstance(group_names, str):
        # Check if the user belongs to a single group.
        rights_exist = user.groups.filter(name=group_names).exists()
    else:
        # Check if the user belongs to any group in a list of groups.
        rights_exist = user.groups.filter(name__in=group_names).exists()
    return rights_exist

class RedirectToCorrectBrandMixin:
    """
    Mixin to redirect users to the correct brand page or the default homepage if no specific URL is provided.
    """
    def get_success_url(self):
        """
        Determines the correct URL to redirect to after a successful operation.

        :return: The next URL to redirect to, or the homepage if no specific URL is provided.
        """
        next_url = self.request.POST.get('next') or self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('replacement:home-page')


