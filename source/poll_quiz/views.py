from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from django.urls import reverse
from django.views.generic import View, TemplateView, FormView
from .base_views import FormView as CustomFormView
from .models import Poll
from .forms import PollForm


class IndexView(View):
    def get(self, request):
        data = Poll.objects.all()
        return render(request, 'index.html', context={'polls': data})


class PollView(TemplateView):
    template_name = 'poll_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        poll = get_object_or_404(Poll, pk=pk)
        context['poll'] = poll
        return context


class PollCreateView(CustomFormView):
    template_name = 'poll_create.html'
    form_class = PollForm

    def form_valid(self, form):
        self.poll = form.save()
        return super().form_valid(form)

    def get_redirect_url(self):
        return reverse('poll_view', kwargs={'pk': self.poll.pk})


class PollEditView(FormView):
    template_name = 'poll_edit.html'
    form_class = PollForm

    def dispatch(self, request, *args, **kwargs):
        self.poll = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['poll'] = self.poll
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.poll
        return kwargs

    def form_valid(self, form):
        self.poll = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('poll_view', kwargs={'pk': self.poll.pk})

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Poll, pk=pk)

def poll_delete_view(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    if request.method == 'GET':
        return render(request, 'poll_delete.html', context={'poll': poll})
    elif request.method == 'POST':
        poll.delete()
        return redirect('home')
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])