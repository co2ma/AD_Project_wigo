from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from ..models import Question, Answer, BookDiscussion, DiscussionReply
from ..forms import AnswerForm, DiscussionReplyForm

class AnswerCreateView(LoginRequiredMixin, CreateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'pybo/answer_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.create_date = timezone.now()
        form.instance.question = get_object_or_404(Question, pk=self.kwargs['pk'])
        messages.success(self.request, '답변이 등록되었습니다.')
        return super().form_valid(form)

    def get_success_url(self):
        return resolve_url('pybo:detail', pk=self.kwargs['pk'])

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
        return resolve_url('pybo:detail', pk=self.object.question.id)

class AnswerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Answer
    template_name = 'pybo/answer_confirm_delete.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(request, '답변이 삭제되었습니다.')
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return resolve_url('pybo:detail', pk=self.object.question.id)


# 책 Q&A 관련 답변 뷰들
class BookAnswerCreateView(LoginRequiredMixin, CreateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'pybo/book_answer_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.create_date = timezone.now()
        form.instance.question = get_object_or_404(Question, pk=self.kwargs['pk'])
        messages.success(self.request, '답변이 등록되었습니다.')
        return super().form_valid(form)

    def get_success_url(self):
        return resolve_url('pybo:book_qa_detail', pk=self.kwargs['pk'])

class BookAnswerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'pybo/book_answer_form.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def form_valid(self, form):
        form.instance.modify_date = timezone.now()
        messages.success(self.request, '답변이 수정되었습니다.')
        return super().form_valid(form)

    def get_success_url(self):
        return resolve_url('pybo:book_qa_detail', pk=self.object.question.id)

class BookAnswerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Answer
    template_name = 'pybo/book_answer_confirm_delete.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(request, '답변이 삭제되었습니다.')
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return resolve_url('pybo:book_qa_detail', pk=self.object.question.id)


# 책 토론 답글 관련 뷰들
class ReplyCreateView(LoginRequiredMixin, CreateView):
    model = DiscussionReply
    form_class = DiscussionReplyForm
    template_name = 'pybo/reply_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.discussion = get_object_or_404(BookDiscussion, pk=self.kwargs['pk'])
        messages.success(self.request, '답글이 등록되었습니다.')
        return super().form_valid(form)

    def get_success_url(self):
        return resolve_url('pybo:book_qa_detail', pk=self.kwargs['pk'])

class ReplyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = DiscussionReply
    form_class = DiscussionReplyForm
    template_name = 'pybo/reply_form.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def form_valid(self, form):
        form.instance.modify_date = timezone.now()
        messages.success(self.request, '답글이 수정되었습니다.')
        return super().form_valid(form)

    def get_success_url(self):
        return resolve_url('pybo:book_qa_detail', pk=self.object.discussion.id)

class ReplyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = DiscussionReply
    template_name = 'pybo/reply_confirm_delete.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(request, '답글이 삭제되었습니다.')
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return resolve_url('pybo:book_qa_detail', pk=self.object.discussion.id)
