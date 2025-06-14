from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from ..services import BookmarkService


@login_required(login_url='common:login')
def toggle_bookmark(request, question_id):
    """
    북마크 토글 API
    """
    try:
        is_bookmarked = BookmarkService.toggle_bookmark(request, question_id)
        return JsonResponse({
            'status': 'success',
            'is_bookmarked': is_bookmarked
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@login_required(login_url='common:login')
def bookmark_list(request):
    """
    북마크 목록 페이지
    """
    bookmarks = BookmarkService.get_user_bookmarks(request.user)
    return render(request, 'pybo/bookmark_list.html', {
        'bookmarks': bookmarks
    }) 