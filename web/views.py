from datetime import date, timedelta
from random import randrange

from django.db import IntegrityError
from django.db.models import Q, F
from django.core.urlresolvers import reverse
from django.http import (Http404, JsonResponse, HttpResponseRedirect)
from django.shortcuts import render
from django.views.generic import View, ListView, DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from haystack.views import SearchView
from taggit.models import Tag

from resource_rainbow.mixins import (LoginRequiredMixin,
                                     LoginProfileRequiredMixin)

from web.mixins import WorkGroupListMixin
from web.models import User, Status, UserStatus, WorkGroup
from web.forms import UserCreationForm, UserUpdateForm


# Create your views here.
class UserCreate(WorkGroupListMixin, CreateView):
    template_name = 'web/create.html'
    form_class = UserCreationForm
    model = User

    def get_success_url(self):
        return reverse('web:status-create')


class UserDetail(LoginRequiredMixin, WorkGroupListMixin, DetailView):
    template_name = 'web/user_detail.html'
    context_object_name = 'person'

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        queryset = User.objects.filter(pk=pk)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(UserDetail, self).get_context_data(**kwargs)
        past = date.today() - timedelta(days=7)
        user_statuses = UserStatus.objects.filter(user=kwargs.get('object'),
                                                  created__gte=past)
        user_statuses = user_statuses.order_by('created')
        context['user_statuses'] = user_statuses
        return context


class UserUpdate(LoginRequiredMixin, WorkGroupListMixin, UpdateView):
    model = User
    form_class = UserUpdateForm

    def get(self, request, *args, **kwargs):
        response = super(UserUpdate, self).get(request, args, kwargs)
        pk = kwargs.get('pk')
        if request.user.pk != int(pk):
            raise Http404
        return response

    def get_context_data(self, **kwargs):
        context = super(UserUpdate, self).get_context_data(**kwargs)
        if not self.request.user.skills.exists():
            adjectives = ['awesome', 'sweet', 'mad', 'rad', 'fantastic']
            adjective = adjectives[randrange(0, 5)]
            msg = 'You need to enter some {} skills before you can proceed.'
            context['message'] = msg.format(adjective)
        return context

    def get_success_url(self):
        return reverse('web:status-create')


class StatusCreate(LoginProfileRequiredMixin, View):
    template_name = 'web/user_status.html'

    def get(self, request):
        statuses = Status.objects.all().order_by('priority')
        work_groups = WorkGroup.objects.filter(created_by=request.user)
        past = date.today() - timedelta(days=7)
        user_statuses = UserStatus.objects.filter(user=request.user,
                                                  created__gte=past)
        user_statuses = user_statuses.order_by('created')
        return render(request, self.template_name, {
            'statuses': statuses,
            'work_groups': work_groups[:6],
            'user_statuses': user_statuses,
        })

    def post(self, request):
        today = date.today()
        adjectives = ['Nice!', 'Awesome!', 'Great!', 'Stellar!',
                      'Good job!', 'Sweet!', 'Good!']
        try:
            status_pk = request.POST.get('status-id')
            status = Status.objects.get(pk=status_pk)
            user_status, created = UserStatus.objects.update_or_create(
                user=request.user, created__year=today.year,
                created__month=today.month, created__day=today.day,
                defaults={'status': status})
            message = '{} You\'ve recorded your status for today as {}.'
            message = message.format(adjectives[randrange(0, len(adjectives))],
                                     status.name)
            response = {
                'user': request.user.pk,
                'status': status.pk,
                'user_status': user_status.pk,
                'user_status_name': status.name,
                'message': message,
            }
            return JsonResponse(response)
        except Status.DoesNotExist:
            raise Http404


class WorkGroupList(LoginRequiredMixin, ListView):
    template_name = 'web/workgroup_list.html'
    context_object_name = 'workgroup_list'

    def get_queryset(self):
        queryset = WorkGroup.objects.filter(created_by=self.request.user)
        return queryset


class WorkGroupDetail(LoginRequiredMixin, WorkGroupListMixin, DetailView):
    template_name = 'web/workgroup_detail.html'
    context_object_name = 'workgroup'

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        queryset = WorkGroup.objects.filter(pk=pk).prefetch_related('user_set')
        return queryset


class WorkGroupUserRemove(LoginRequiredMixin, View):
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
            user.work_groups.remove(work_group)
            response = {
                'status': 'success',
                'group': work_group.pk,
                'user': user.pk
            }
        except(WorkGroup.DoesNotExist, User.DoesNotExist):
            pass
        return JsonResponse(response)


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


class WorkGroupCreate(LoginRequiredMixin, WorkGroupListMixin, CreateView):
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


class UserSearch(SearchView):
    def extra_context(self):
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


class SkillSearch(View):
    def get(self, request):
        q = request.GET.get('q')
        items = Tag.objects.filter(name__istartswith=q)
        items = items.annotate(text=F('name'))
        items = items.values('id', 'text')
        results = {
            'items': list(items)
        }
        return JsonResponse(results)


class DispatchView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        if user.skills.exists():
            return HttpResponseRedirect(reverse('web:status-create'))
        return HttpResponseRedirect(reverse(
            'web:user-update',
            kwargs={'pk': request.user.pk}))


class URLView(TemplateView):
    template_name = 'web/urls.js'
