from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from ..services import (
    BookmarkService, NotificationService, UserBlockService,
    DraftPostService, UserPreferenceService
)
from ..models import Question, Comment

@login_required
@require_POST
def toggle_bookmark(request, post_id):
    try:
        is_bookmarked = BookmarkService.toggle_bookmark(request, post_id)
        return JsonResponse({
            'status': 'success',
            'is_bookmarked': is_bookmarked
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
def notifications(request):
    notifications = NotificationService.get_unread_notifications(request.user)
    return render(request, 'pybo/notifications.html', {
        'notifications': notifications
    })

@login_required
@require_POST
def mark_notification_read(request, notification_id):
    try:
        NotificationService.mark_as_read(notification_id)
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@require_POST
def block_user(request, user_id):
    try:
        user_to_block = get_object_or_404(User, id=user_id)
        UserBlockService.block_user(request.user, user_to_block)
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@require_POST
def unblock_user(request, user_id):
    try:
        user_to_unblock = get_object_or_404(User, id=user_id)
        UserBlockService.unblock_user(request.user, user_to_unblock)
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@require_POST
def save_draft(request):
    try:
        title = request.POST.get('title')
        content = request.POST.get('content')
        draft = DraftPostService.save_draft(request, title, content)
        return JsonResponse({
            'status': 'success',
            'draft_id': draft.id
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
def drafts(request):
    drafts = DraftPostService.get_drafts(request.user)
    return render(request, 'pybo/drafts.html', {
        'drafts': drafts
    })

@login_required
@require_POST
def toggle_dark_mode(request):
    try:
        is_dark_mode = UserPreferenceService.toggle_dark_mode(request.user)
        return JsonResponse({
            'status': 'success',
            'is_dark_mode': is_dark_mode
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400) 