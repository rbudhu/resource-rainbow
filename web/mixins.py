from django.views.generic import View
from web.models import WorkGroup


class WorkGroupListMixin(View):
    def get_context_data(self, **kwargs):
        context = super(WorkGroupListMixin, self).get_context_data(**kwargs)
        workgroups = WorkGroup.objects.filter(created_by=self.request.user)
        context['work_groups'] = workgroups
        return context
