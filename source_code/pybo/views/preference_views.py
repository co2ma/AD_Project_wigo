from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from ..services import UserPreferenceService


@login_required(login_url='common:login')
def toggle_dark_mode(request):
    """
    다크모드 토글 API
    """
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