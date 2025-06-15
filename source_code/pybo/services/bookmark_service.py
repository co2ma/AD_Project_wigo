from typing import List
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from ..models import Bookmark, Question
from ..exceptions import BookmarkException

class BookmarkService:
    @classmethod
    def toggle_bookmark(cls, request: HttpRequest, question_id: int) -> bool:
        """
        북마크 토글 기능
        Returns:
            bool: 북마크 상태 (True: 북마크됨, False: 북마크 해제됨)
        Raises:
            BookmarkException: 북마크 처리 중 오류 발생 시
        """
        try:
            question = get_object_or_404(Question, pk=question_id)
            bookmark, created = Bookmark.objects.get_or_create(
                user=request.user,
                question=question
            )
            
            if not created:
                bookmark.delete()
                return False
            return True
        except Exception as e:
            raise BookmarkException(f"북마크 처리 중 오류 발생: {str(e)}")

    @classmethod
    def get_user_bookmarks(cls, user: User) -> List[Bookmark]:
        """
        사용자의 북마크 목록 조회
        Raises:
            BookmarkException: 북마크 조회 중 오류 발생 시
        """
        try:
            return Bookmark.objects.filter(user=user).select_related('question')
        except Exception as e:
            raise BookmarkException(f"북마크 목록 조회 중 오류 발생: {str(e)}")

    @classmethod
    def is_bookmarked(cls, user: User, question: Question) -> bool:
        """
        특정 게시글의 북마크 여부 확인
        Raises:
            BookmarkException: 북마크 확인 중 오류 발생 시
        """
        try:
            return Bookmark.objects.filter(user=user, question=question).exists()
        except Exception as e:
            raise BookmarkException(f"북마크 여부 확인 중 오류 발생: {str(e)}") 