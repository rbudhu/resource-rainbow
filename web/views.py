from django.db import IntegrityError
from django.db.models import Q
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import (Http404, JsonResponse, HttpResponse,
                         HttpResponseRedirect)
from django.shortcuts import render
from django.views.generic import View, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, FormView

from haystack.views import SearchView

from resource_rainbow.mixins import LoginRequiredMixin

from web.models import User, Status, UserStatus, WorkGroup
from web.forms import UserCreationForm, UserUpdateForm

# Create your views here.
class UserCreate(CreateView):
    template_name = 'web/create.html'
    form_class = UserCreationForm
    model = User

    def get_success_url(self):
        return reverse('web:status-create')


class UserUpdate(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm

    def get(self, request, *args, **kwargs):
        response = super(UserUpdate, self).get(request, args, kwargs)
        pk = kwargs.get('pk')
        if request.user.pk != int(pk):
            raise Http404
        return response

    def get_success_url(self):
        return reverse('web:status-create')


class DispatchView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        if user.skills.exists():
            return HttpResponseRedirect(reverse('web:status-create'))
        return HttpResponseRedirect(reverse(
                'web:user-update',
                kwargs={'pk': request.user.pk}))


class WorkGroupList(LoginRequiredMixin, ListView):
    template_name = 'web/workgroup_list.html'
    context_object_name = 'workgroup_list'

    def get_queryset(self):
        queryset = WorkGroup.objects.filter(created_by=self.request.user)
        return queryset


class WorkGroupDetail(LoginRequiredMixin, DetailView):
    template_name = 'web/workgroup_detail.html'
    context_object_name = 'workgroup'
    
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        queryset = WorkGroup.objects.filter(pk=pk).prefetch_related('user_set')
        return queryset


class WorkGroupUserAdd(LoginRequiredMixin, View):
    def post(self, request):
        response = {
            'status': 'error'
            }
        try:
            group_pk = request.POST.get('group_id')
            user_pk = request.POST.get('user_id')
            q = Q(pk=group_pk) & Q(created_by=request.user)
            work_group = WorkGroup.objects.get(q)
            user = User.objects.get(pk=user_pk)
            user.work_groups.add(work_group)
            response = {
                'status': 'success',
                'group': work_group.pk,
                'user': user.pk
                }
        except(WorkGroup.DoesNotExist, User.DoesNotExist):
            pass
        return JsonResponse(response)


class WorkGroupCreate(LoginRequiredMixin, CreateView):
    template_name = 'web/workgroup_create.html'
    model = WorkGroup
    fields = ['name']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        try:
            return super(WorkGroupCreate, self).form_valid(form)
        except IntegrityError:
            form.add_error('name',
                           'A Workgroup already exists with that name.')
            return self.form_invalid(form)


class StatusCreate(LoginRequiredMixin, View):
    template_name = 'web/user_status.html'

    def get(self, request):
        statuses = Status.objects.all().order_by('priority')
        work_groups = WorkGroup.objects.filter(created_by=request.user)
        return render(request, self.template_name, {
                'statuses': statuses,
                'work_groups': work_groups,
                })

    def post(self, request):
        try:
            status_pk = request.POST.get('status-id');
            status = Status.objects.get(pk=status_pk)
            user_status = UserStatus.objects.create(
                user=request.user,
                status=status
                )
            response = {
                'user': request.user.pk,
                'status': status.pk,
                'user_status': user_status.pk
                }
            return JsonResponse(response)
        except Status.DoesNotExist:
            raise Http404


class UserSearch(SearchView):
    def extra_context(self):
        print(self.request)
        context = super(UserSearch, self).extra_context()
        work_groups = WorkGroup.objects.filter(created_by=self.request.user)
        context['work_groups'] = work_groups
        active_work_group_pk = self.request.GET.get('wg')
        q = Q(pk=active_work_group_pk) & Q(created_by=self.request.user)
        try:
            active_work_group = WorkGroup.objects.get(q)
            context['active_work_group'] = active_work_group
        except WorkGroup.DoesNotExist:
            pass
        return context
