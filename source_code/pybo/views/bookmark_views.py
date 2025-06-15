from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from ..models import Question, Bookmark

from ..services import BookmarkService


@login_required
def toggle_bookmark(request, question_id):
    """
    북마크 토글 API
    """
    question = get_object_or_404(Question, pk=question_id)
    bookmark, created = Bookmark.objects.get_or_create(
        user=request.user,
        question=question
    )
    
    if not created:
        bookmark.delete()
        return JsonResponse({
            'status': 'success',
            'message': '북마크가 해제되었습니다.',
            'is_bookmarked': False
        })
    
    return JsonResponse({
        'status': 'success',
        'message': '북마크가 추가되었습니다.',
        'is_bookmarked': True
    })


@login_required
def bookmark_list(request):
    """
    북마크 목록 페이지
    """
    bookmarks = Bookmark.objects.filter(user=request.user)
    return render(request, 'pybo/bookmark_list.html', {
        'bookmarks': bookmarks
    }) 