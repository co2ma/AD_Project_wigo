from django import forms

from pybo.models import Question, Answer, Comment, Book, BookDiscussion, DiscussionReply


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'content', 'book']
        labels = {
            'subject': '제목',
            'content': '내용',
            'book': '관련 도서',
        }
        widgets = {
            'book': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 책 선택 필드를 선택사항으로 설정
        self.fields['book'].required = False
        self.fields['book'].empty_label = "도서를 선택하세요 (선택사항)"


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }


class BookDiscussionForm(forms.ModelForm):
    class Meta:
        model = BookDiscussion
        fields = ['book', 'subject', 'content']
        labels = {
            'book': '토론 대상 도서',
            'subject': '토론 제목',
            'content': '토론 내용',
        }
        widgets = {
            'book': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from library.models import Book as LibraryBook
        self.fields['book'].queryset = LibraryBook.objects.all()
        self.fields['book'].empty_label = "토론할 도서를 선택하세요"


class ReplyForm(forms.ModelForm):
    class Meta:
        model = DiscussionReply
        fields = ['content']
        labels = {
            'content': '답글 내용',
        }
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
