from django.contrib import admin
from .models import Question, Answer, Comment, Book, BookDiscussion, DiscussionReply, BorrowHistory


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Comment)
admin.site.register(Book)
admin.site.register(BookDiscussion)
admin.site.register(DiscussionReply)
admin.site.register(BorrowHistory)
