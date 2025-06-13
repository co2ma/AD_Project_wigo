from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from ..models import Question, BookDiscussion
from ..forms import QuestionForm, BookDiscussionForm

class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'pybo/question_form.html'
    success_url = reverse_lazy('pybo:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.create_date = timezone.now()
        messages.success(self.request, '질문이 등록되었습니다.')
        return super().form_valid(form)

class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'pybo/question_form.html'
    success_url = reverse_lazy('pybo:index')

    def test_func(self):
        return self.get_object().author == self.request.user

    def form_valid(self, form):
        form.instance.modify_date = timezone.now()
        messages.success(self.request, '질문이 수정되었습니다.')
        return super().form_valid(form)

class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    success_url = reverse_lazy('pybo:index')
    template_name = 'pybo/question_confirm_delete.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(request, '질문이 삭제되었습니다.')
        return super().delete(request, *args, **kwargs)


# 책 Q&A 관련 뷰들
class BookQuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'pybo/book_question_form.html'
    success_url = reverse_lazy('pybo:book_qa_index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.create_date = timezone.now()
        messages.success(self.request, '책에 대한 질문이 등록되었습니다.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Question.objects.values_list('book', flat=True).distinct()
        return context

class BookQuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'pybo/book_question_form.html'
    success_url = reverse_lazy('pybo:book_qa_index')

    def test_func(self):
        return self.get_object().author == self.request.user

    def form_valid(self, form):
        form.instance.modify_date = timezone.now()
        messages.success(self.request, '질문이 수정되었습니다.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Question.objects.values_list('book', flat=True).distinct()
        return context

class BookQuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    success_url = reverse_lazy('pybo:book_qa_index')
    template_name = 'pybo/book_question_confirm_delete.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(request, '질문이 삭제되었습니다.')
        return super().delete(request, *args, **kwargs)


# 책 토론 관련 뷰들
class BookDiscussionCreateView(LoginRequiredMixin, CreateView):
    model = BookDiscussion
    form_class = BookDiscussionForm
    template_name = 'pybo/book_discussion_form.html'
    success_url = reverse_lazy('pybo:book_qa_index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, '도서 토론이 등록되었습니다.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from library.models import Book as LibraryBook
        context['books'] = LibraryBook.objects.all()
        return context

class BookDiscussionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BookDiscussion
    form_class = BookDiscussionForm
    template_name = 'pybo/book_discussion_form.html'
    success_url = reverse_lazy('pybo:book_qa_index')

    def test_func(self):
        return self.get_object().author == self.request.user

    def form_valid(self, form):
        form.instance.modify_date = timezone.now()
        messages.success(self.request, '토론이 수정되었습니다.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from library.models import Book as LibraryBook
        context['books'] = LibraryBook.objects.all()
        return context

class BookDiscussionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BookDiscussion
    success_url = reverse_lazy('pybo:book_qa_index')
    template_name = 'pybo/book_discussion_confirm_delete.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(request, '토론이 삭제되었습니다.')
        return super().delete(request, *args, **kwargs)
