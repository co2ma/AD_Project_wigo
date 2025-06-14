from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count

from ..models import Question
from ..services import BookmarkService, UserPreferenceService


def index(request):
    """
    pybo 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')       # 검색어
    so = request.GET.get('so', 'recent') # 정렬 기준

    # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(
            num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(
            num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:
        question_list = Question.objects.order_by('-create_date')
    # 조회
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()

    # 페이징처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    # 다크모드 상태 추가
    is_dark_mode = False
    if request.user.is_authenticated:
        is_dark_mode = UserPreferenceService.get_dark_mode(request.user)

    context = {
        'question_list': page_obj,
        'page': page,
        'kw': kw,
        'is_dark_mode': is_dark_mode
    }
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    is_bookmarked = False
    is_dark_mode = False
    
    if request.user.is_authenticated:
        is_bookmarked = BookmarkService.is_bookmarked(request.user, question)
        is_dark_mode = UserPreferenceService.get_dark_mode(request.user)
    
    context = {
        'question': question,
        'is_bookmarked': is_bookmarked,
        'is_dark_mode': is_dark_mode
    }
    return render(request, 'pybo/question_detail.html', context)
