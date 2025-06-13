from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True, blank=True, related_name='questions')

    def __str__(self):
        return self.subject


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100, blank=True, default='')
    publication_year = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    
    @classmethod
    def get_all_books(cls) -> QuerySet['Book']:
        """
        전체 책 목록 반환
        """
        return cls.objects.all()
    
    @classmethod
    def get_books_by_author(cls, author_name: str) -> QuerySet['Book']:
        """
        특정 저자의 책만 반환
        """
        return cls.objects.filter(author__iexact=author_name)
    
    @classmethod
    def get_books_by_title_keyword(cls, keyword: str) -> QuerySet['Book']:
        """
        제목에 키워드가 포함된 책 반환 (대소문자 구분 없이)
        """
        return cls.objects.filter(title__icontains=keyword)
    
    @classmethod
    def get_books_ordered_by_title(cls) -> QuerySet['Book']:
        """
        제목 순으로 정렬된 책 목록 반환
        """
        return cls.objects.all().order_by('title')


class UploadedFile(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
