from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count

from ..models import Question, BlockedUser
from ..services import BookmarkService, UserPreferenceService


def index(request):
    """
    pybo 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')       # 검색어
    so = request.GET.get('so', 'recent') # 정렬 기준

    # 차단한 사용자 목록 가져오기
    blocked_users = []
    if request.user.is_authenticated:
        blocked_users = BlockedUser.objects.filter(user=request.user).values_list('blocked_user', flat=True)
    
    # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:  # recent
        question_list = Question.objects.order_by('-create_date')
    
    # 차단한 사용자의 게시물 제외
    question_list = question_list.exclude(author_id__in=blocked_users)
    
    # 검색
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()

    # 페이징 처리
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
        'so': so,
        'is_dark_mode': is_dark_mode
    }
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    
    # 차단한 사용자의 게시물인지 확인
    if request.user.is_authenticated:
        is_blocked = BlockedUser.objects.filter(
            user=request.user,
            blocked_user=question.author
        ).exists()
        if is_blocked:
            return redirect('pybo:index')
    
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
