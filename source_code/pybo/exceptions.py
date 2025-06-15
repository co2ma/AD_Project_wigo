class PyboException(Exception):
    """기본 예외 클래스"""
    pass

class BookmarkException(PyboException):
    """북마크 관련 예외"""
    pass

class UserPreferenceException(PyboException):
    """사용자 설정 관련 예외"""
    pass

class QuestionException(PyboException):
    """질문 관련 예외"""
    pass

class AnswerException(PyboException):
    """답변 관련 예외"""
    pass 