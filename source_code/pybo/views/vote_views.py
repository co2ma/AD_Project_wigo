from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from ..models import Question, Answer, BookDiscussion, DiscussionReply


@login_required(login_url='common:login')
def vote_question(request, pk):
    """
    pybo 질문추천등록
    """
    question = get_object_or_404(Question, pk=pk)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        if request.user in question.voter.all():
            question.voter.remove(request.user)
            messages.success(request, '추천을 취소했습니다.')
        else:
            question.voter.add(request.user)
            messages.success(request, '추천했습니다.')
    return redirect('pybo:detail', pk=question.id)


@login_required(login_url='common:login')
def vote_answer(request, pk):
    """
    pybo 답글추천등록
    """
    answer = get_object_or_404(Answer, pk=pk)
    if request.user == answer.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        if request.user in answer.voter.all():
            answer.voter.remove(request.user)
            messages.success(request, '추천을 취소했습니다.')
        else:
            answer.voter.add(request.user)
            messages.success(request, '추천했습니다.')
    return redirect('pybo:detail', pk=answer.question.id)


@login_required(login_url='common:login')
def vote_discussion(request, pk):
    """
    책 토론 추천등록
    """
    discussion = get_object_or_404(BookDiscussion, pk=pk)
    if request.user == discussion.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        if request.user in discussion.voter.all():
            discussion.voter.remove(request.user)
            messages.success(request, '추천을 취소했습니다.')
        else:
            discussion.voter.add(request.user)
            messages.success(request, '추천했습니다.')
    return redirect('pybo:book_qa_detail', pk=discussion.id)


@login_required(login_url='common:login')
def vote_reply(request, pk):
    """
    책 토론 답글 추천등록
    """
    reply = get_object_or_404(DiscussionReply, pk=pk)
    if request.user == reply.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        if request.user in reply.voter.all():
            reply.voter.remove(request.user)
            messages.success(request, '추천을 취소했습니다.')
        else:
            reply.voter.add(request.user)
            messages.success(request, '추천했습니다.')
    return redirect('pybo:book_qa_detail', pk=reply.discussion.id)
