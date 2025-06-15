from django.contrib.auth.models import User
from ..models import UserPreference
from ..exceptions import UserPreferenceException

class UserPreferenceService:
    @classmethod
    def toggle_dark_mode(cls, user: User) -> bool:
        """
        다크모드 토글
        Returns:
            bool: 토글 후 다크모드 상태
        Raises:
            UserPreferenceException: 설정 변경 중 오류 발생 시
        """
        try:
            preference, created = UserPreference.objects.get_or_create(user=user)
            preference.dark_mode = not preference.dark_mode
            preference.save()
            return preference.dark_mode
        except Exception as e:
            raise UserPreferenceException(f"다크모드 설정 변경 중 오류 발생: {str(e)}")

    @classmethod
    def get_dark_mode(cls, user: User) -> bool:
        """
        사용자의 다크모드 설정 조회
        Raises:
            UserPreferenceException: 설정 조회 중 오류 발생 시
        """
        try:
            preference = UserPreference.objects.filter(user=user).first()
            return preference.dark_mode if preference else False
        except Exception as e:
            raise UserPreferenceException(f"다크모드 설정 조회 중 오류 발생: {str(e)}") 