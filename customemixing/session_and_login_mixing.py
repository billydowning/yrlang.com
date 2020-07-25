from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


class UserSessionAndLoginCheckMixing(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        elif not request.session.get('user_role'):
            return redirect('user-role-select')
        return super(UserSessionAndLoginCheckMixing, self).dispatch(request, *args, **kwargs)



       
