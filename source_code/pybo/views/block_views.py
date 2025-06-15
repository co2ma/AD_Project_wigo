from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from ..models import BlockedUser

@login_required
def toggle_block(request, user_id):
    blocked_user = get_object_or_404(User, id=user_id)
    
    if request.user == blocked_user:
        return JsonResponse({
            'status': 'error',
            'message': '자기 자신을 차단할 수 없습니다.'
        }, status=400)
    
    blocked, created = BlockedUser.objects.get_or_create(
        user=request.user,
        blocked_user=blocked_user
    )
    
    if not created:
        blocked.delete()
        return JsonResponse({
            'status': 'success',
            'message': '차단이 해제되었습니다.',
            'is_blocked': False
        })
    
    return JsonResponse({
        'status': 'success',
        'message': '차단되었습니다.',
        'is_blocked': True
    })

@login_required
def blocked_users(request):
    blocked_users = BlockedUser.objects.filter(user=request.user)
    return render(request, 'pybo/blocked_users.html', {
        'blocked_users': blocked_users
    }) 