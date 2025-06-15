from .services import UserPreferenceService

def dark_mode(request):
    """
    모든 템플릿에 다크모드 상태를 전달하는 컨텍스트 프로세서
    """
    is_dark_mode = False
    if request.user.is_authenticated:
        is_dark_mode = UserPreferenceService.get_dark_mode(request.user)
    return {'is_dark_mode': is_dark_mode} 