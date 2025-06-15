from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from ..models import Question, Bookmark

from ..services import BookmarkService
from ..exceptions import BookmarkException


@login_required(login_url='common:login')
def bookmark_toggle(request, question_id):
    """
    북마크 토글 뷰
    """
    try:
        is_bookmarked = BookmarkService.toggle_bookmark(request, question_id)
        return JsonResponse({
            'status': 'success',
            'message': '북마크가 추가되었습니다.' if is_bookmarked else '북마크가 해제되었습니다.',
            'is_bookmarked': is_bookmarked
        })
    except BookmarkException as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@login_required(login_url='common:login')
def bookmark_list(request):
    """
    북마크 목록 뷰
    """
    try:
        bookmarks = BookmarkService.get_user_bookmarks(request.user)
        return render(request, 'pybo/bookmark_list.html', {
            'bookmarks': bookmarks
        })
    except BookmarkException as e:
        return render(request, 'pybo/bookmark_list.html', {
            'error': str(e)
        }) 