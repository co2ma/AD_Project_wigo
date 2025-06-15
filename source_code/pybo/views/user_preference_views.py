from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ..services import UserPreferenceService
from ..exceptions import UserPreferenceException

@login_required(login_url='common:login')
def toggle_dark_mode(request):
    """
    다크모드 토글 뷰
    """
    try:
        is_dark_mode = UserPreferenceService.toggle_dark_mode(request.user)
        return JsonResponse({'is_dark_mode': is_dark_mode})
    except UserPreferenceException as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required(login_url='common:login')
def get_dark_mode(request):
    """
    다크모드 설정 조회 뷰
    """
    try:
        is_dark_mode = UserPreferenceService.get_dark_mode(request.user)
        return JsonResponse({'is_dark_mode': is_dark_mode})
    except UserPreferenceException as e:
        return JsonResponse({'error': str(e)}, status=400) 