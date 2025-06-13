from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from ..models import Question, Answer
from ..forms import AnswerForm

class AnswerCreateView(LoginRequiredMixin, CreateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'pybo/answer_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.create_date = timezone.now()
        form.instance.question = get_object_or_404(Question, pk=self.kwargs['question_id'])
        messages.success(self.request, '답변이 등록되었습니다.')
        return super().form_valid(form)

    def get_success_url(self):
        return resolve_url('pybo:detail', question_id=self.kwargs['question_id'])

class AnswerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'pybo/answer_form.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def form_valid(self, form):
        form.instance.modify_date = timezone.now()
        messages.success(self.request, '답변이 수정되었습니다.')
        return super().form_valid(form)

    def get_success_url(self):
        return resolve_url('pybo:detail', question_id=self.object.question.id)

class AnswerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Answer
    template_name = 'pybo/answer_confirm_delete.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(request, '답변이 삭제되었습니다.')
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return resolve_url('pybo:detail', question_id=self.object.question.id)
