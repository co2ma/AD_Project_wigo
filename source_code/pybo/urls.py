from django.urls import path

from .views import base_views, question_views, answer_views, comment_views, vote_views
from .views.api_views import receive_post

app_name = 'pybo'

urlpatterns = [
    # base_views.py
    path('', base_views.IndexView.as_view(), name='index'),
    path('<int:pk>/', base_views.QuestionDetailView.as_view(), name='detail'),
    path('request-info/', base_views.request_info_view, name='request_info'),
    path('upload/', base_views.file_upload_view, name='upload_file'),

    # question_views.py
    path('question/create/', question_views.QuestionCreateView.as_view(), name='question_create'),
    path('question/modify/<int:pk>/', question_views.QuestionUpdateView.as_view(), name='question_modify'),
    path('question/delete/<int:pk>/', question_views.QuestionDeleteView.as_view(), name='question_delete'),

    # answer_views.py
    path('answer/create/<int:question_id>/', answer_views.AnswerCreateView.as_view(), name='answer_create'),
    path('answer/modify/<int:pk>/', answer_views.AnswerUpdateView.as_view(), name='answer_modify'),
    path('answer/delete/<int:pk>/', answer_views.AnswerDeleteView.as_view(), name='answer_delete'),

    # comment_views.py
    path('comment/create/question/<int:question_id>/', comment_views.comment_create_question, name='comment_create_question'),
    path('comment/modify/question/<int:comment_id>/', comment_views.comment_modify_question, name='comment_modify_question'),
    path('comment/delete/question/<int:comment_id>/', comment_views.comment_delete_question, name='comment_delete_question'),
    path('comment/create/answer/<int:answer_id>/', comment_views.comment_create_answer, name='comment_create_answer'),
    path('comment/modify/answer/<int:comment_id>/', comment_views.comment_modify_answer, name='comment_modify_answer'),
    path('comment/delete/answer/<int:comment_id>/', comment_views.comment_delete_answer, name='comment_delete_answer'),

    # vote_views.py
    path('vote/question/<int:question_id>/', vote_views.vote_question, name='vote_question'),
    path('vote/answer/<int:answer_id>/', vote_views.vote_answer, name='vote_answer'),

    path('api/post/', receive_post, name='receive_post'),
]
