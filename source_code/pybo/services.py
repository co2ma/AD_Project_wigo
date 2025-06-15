from typing import List
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Bookmark, Question, UserPreference

class BookmarkService:
    @classmethod
    def toggle_bookmark(cls, request: HttpRequest, question_id: int) -> bool:
        """
        북마크 토글 기능
        Returns:
            bool: 북마크 상태 (True: 북마크됨, False: 북마크 해제됨)
        """
        question = get_object_or_404(Question, pk=question_id)
        bookmark, created = Bookmark.objects.get_or_create(
            user=request.user,
            question=question
        )
        
        if not created:
            bookmark.delete()
            return False
        return True

    @classmethod
    def get_user_bookmarks(cls, user: User) -> List[Bookmark]:
        """
        사용자의 북마크 목록 조회
        """
        return Bookmark.objects.filter(user=user).select_related('question')

    @classmethod
    def is_bookmarked(cls, user: User, question: Question) -> bool:
        """
        특정 게시글의 북마크 여부 확인
        """
        return Bookmark.objects.filter(user=user, question=question).exists()

class UserPreferenceService:
    @classmethod
    def toggle_dark_mode(cls, user: User) -> bool:
        """
        다크모드 토글
        Returns:
            bool: 토글 후 다크모드 상태
        """
        preference, created = UserPreference.objects.get_or_create(user=user)
        preference.dark_mode = not preference.dark_mode
        preference.save()
        return preference.dark_mode

    @classmethod
    def get_dark_mode(cls, user: User) -> bool:
        """
        사용자의 다크모드 설정 조회
        """
        preference = UserPreference.objects.filter(user=user).first()
        return preference.dark_mode if preference else False 