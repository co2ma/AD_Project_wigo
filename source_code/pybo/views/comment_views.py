from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import CommentForm
from ..models import Question, Answer, Comment


@login_required(login_url='common:login')
def comment_create_question(request, pk):
    """
    pybo 질문댓글등록
    """
    question = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.question = question
            comment.save()
            return redirect('pybo:detail', pk=comment.question_id)
    else:
        form = CommentForm()
    context = {'form': form, 'question': question}
    return render(request, 'pybo/comment_form.html', context)


@login_required(login_url='common:login')
def comment_modify_question(request, pk):
    """
    pybo 질문댓글수정
    """
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('pybo:detail', pk=comment.question_id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('pybo:detail', pk=comment.question_id)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form, 'comment': comment}
    return render(request, 'pybo/comment_form.html', context)


@login_required(login_url='common:login')
def comment_delete_question(request, pk):
    """
    pybo 질문댓글삭제
    """
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('pybo:detail', pk=comment.question_id)
    else:
        comment.delete()
    return redirect('pybo:detail', pk=comment.question_id)


@login_required(login_url='common:login')
def comment_create_answer(request, pk):
    """
    pybo 답글댓글등록
    """
    answer = get_object_or_404(Answer, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.answer = answer
            comment.save()
            return redirect('pybo:detail', pk=comment.answer.question.id)
    else:
        form = CommentForm()
    context = {'form': form, 'answer': answer}
    return render(request, 'pybo/comment_form.html', context)


@login_required(login_url='common:login')
def comment_modify_answer(request, pk):
    """
    pybo 답글댓글수정
    """
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('pybo:detail', pk=comment.answer.question.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('pybo:detail', pk=comment.answer.question.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form, 'comment': comment}
    return render(request, 'pybo/comment_form.html', context)


@login_required(login_url='common:login')
def comment_delete_answer(request, pk):
    """
    pybo 답글댓글삭제
    """
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('pybo:detail', pk=comment.answer.question.id)
    else:
        comment.delete()
    return redirect('pybo:detail', pk=comment.answer.question.id)
