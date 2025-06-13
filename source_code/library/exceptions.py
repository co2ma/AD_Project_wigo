class BookNotFound(Exception):
    """요청한 책이 존재하지 않을 경우"""
    pass

class BookHasNoBorrowHistory(Exception):
    """책에 대출 이력이 없을 경우"""
    pass 