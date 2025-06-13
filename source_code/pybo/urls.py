from django.urls import path

from .views import base_views, question_views, answer_views, comment_views, vote_views
from .views.api_views import receive_post

app_name = 'pybo'

urlpatterns = [
    # base_views.py
    path('', base_views.IndexView.as_view(), name='index'),
    path('<int:pk>/', base_views.QuestionDetailView.as_view(), name='detail'),
    path('book-upload/', base_views.book_upload_view, name='book_upload'),

    # 도서 관리
    path('books/', base_views.BookListView.as_view(), name='book_list'),
    path('books/<int:book_id>/history/', base_views.BookHistoryView.as_view(), name='book_history'),
    path('books/<int:book_id>/borrow/', base_views.borrow_book, name='borrow_book'),
    path('books/<int:book_id>/return/', base_views.return_book, name='return_book'),

    # book_qa_views.py (새로운 책 Q&A 기능)
    path('book-qa/', base_views.BookQAIndexView.as_view(), name='book_qa_index'),
    path('book-qa/<int:pk>/', base_views.BookQADetailView.as_view(), name='book_qa_detail'),
    path('book-qa/question/create/', question_views.BookQuestionCreateView.as_view(), name='book_question_create'),
    path('book-qa/question/modify/<int:pk>/', question_views.BookQuestionUpdateView.as_view(), name='book_question_modify'),
    path('book-qa/question/delete/<int:pk>/', question_views.BookQuestionDeleteView.as_view(), name='book_question_delete'),
    path('book-qa/answer/create/<int:pk>/', answer_views.BookAnswerCreateView.as_view(), name='book_answer_create'),
    path('book-qa/answer/modify/<int:pk>/', answer_views.BookAnswerUpdateView.as_view(), name='book_answer_modify'),
    path('book-qa/answer/delete/<int:pk>/', answer_views.BookAnswerDeleteView.as_view(), name='book_answer_delete'),

    # book_discussion_views.py (새로운 책 토론 기능)
    path('book-discussion/create/', question_views.BookDiscussionCreateView.as_view(), name='book_discussion_create'),
    path('book-discussion/modify/<int:pk>/', question_views.BookDiscussionUpdateView.as_view(), name='book_discussion_modify'),
    path('book-discussion/delete/<int:pk>/', question_views.BookDiscussionDeleteView.as_view(), name='book_discussion_delete'),
    path('reply/create/<int:pk>/', answer_views.ReplyCreateView.as_view(), name='reply_create'),
    path('reply/modify/<int:pk>/', answer_views.ReplyUpdateView.as_view(), name='reply_modify'),
    path('reply/delete/<int:pk>/', answer_views.ReplyDeleteView.as_view(), name='reply_delete'),
    path('vote/discussion/<int:pk>/', vote_views.vote_discussion, name='book_discussion_vote'),
    path('vote/reply/<int:pk>/', vote_views.vote_reply, name='reply_vote'),

    # question_views.py
    path('question/create/', question_views.QuestionCreateView.as_view(), name='question_create'),
    path('question/modify/<int:pk>/', question_views.QuestionUpdateView.as_view(), name='question_modify'),
    path('question/delete/<int:pk>/', question_views.QuestionDeleteView.as_view(), name='question_delete'),

    # answer_views.py
    path('answer/create/<int:pk>/', answer_views.AnswerCreateView.as_view(), name='answer_create'),
    path('answer/modify/<int:pk>/', answer_views.AnswerUpdateView.as_view(), name='answer_modify'),
    path('answer/delete/<int:pk>/', answer_views.AnswerDeleteView.as_view(), name='answer_delete'),

    # comment_views.py
    path('comment/create/question/<int:pk>/', comment_views.comment_create_question, name='comment_create_question'),
    path('comment/modify/question/<int:pk>/', comment_views.comment_modify_question, name='comment_modify_question'),
    path('comment/delete/question/<int:pk>/', comment_views.comment_delete_question, name='comment_delete_question'),
    path('comment/create/answer/<int:pk>/', comment_views.comment_create_answer, name='comment_create_answer'),
    path('comment/modify/answer/<int:pk>/', comment_views.comment_modify_answer, name='comment_modify_answer'),
    path('comment/delete/answer/<int:pk>/', comment_views.comment_delete_answer, name='comment_delete_answer'),

    # vote_views.py
    path('vote/question/<int:pk>/', vote_views.vote_question, name='vote_question'),
    path('vote/answer/<int:pk>/', vote_views.vote_answer, name='vote_answer'),

    path('api/post/', receive_post, name='receive_post'),
]
