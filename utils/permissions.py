import logging
from django.contrib.auth.mixins import UserPassesTestMixin


class GroupCheckMixin(UserPassesTestMixin):
    groups_to_check = []
    access_denied_url = 'access_denied'

    def get_login_url(self):
        # pylint: disable=R1705
        if not self.request.user.is_authenticated:
            return super(GroupCheckMixin, self).get_login_url()
        else:
            return self.access_denied_url

    def test_func(self):
        if len(self.groups_to_check) == 0:
            logging.warning(
                'No groups to check - Group check will always fail!')
        user_groups = {g.name for g in self.request.user.groups.all()}
        return len(user_groups.intersection(set(self.groups_to_check))) > 0
