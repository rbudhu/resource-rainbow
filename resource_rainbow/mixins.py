from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class LoginProfileRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginProfileRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.skills.exists():
            kwargs = {'pk': request.user.pk}
            return HttpResponseRedirect(reverse_lazy('web:user-update',
                                                     kwargs=kwargs))
        return super(LoginProfileRequiredMixin, self).dispatch(request, *args,
                                                               **kwargs)
            
