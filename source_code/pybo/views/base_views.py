from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.http import JsonResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import csv
import io
import json
import re
import uuid
from datetime import datetime

from ..models import Question, UploadedFile, Book, BookDiscussion, DiscussionReply, BorrowHistory
from pybo.forms import QuestionForm, AnswerForm


class IndexView(ListView):
    model = Question
    template_name = 'pybo/question_list.html'
    context_object_name = 'question_list'
    paginate_by = 10

    def get_queryset(self):
        question_list = Question.objects.annotate(
            num_voter=Count('voter')).order_by('-create_date')
        return question_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page', '1')
        kw = self.request.GET.get('kw', '')
        so = self.request.GET.get('so', 'recent')
        
        question_list = Question.objects.annotate(
            num_voter=Count('voter'))
        if kw:
            question_list = question_list.filter(
                Q(subject__icontains=kw) |  # 제목 검색
                Q(content__icontains=kw) |  # 내용 검색
                Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
                Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
            ).distinct()
        
        if so == 'recommend':
            question_list = question_list.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
        elif so == 'popular':
            question_list = question_list.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
        else:  # recent
            question_list = question_list.order_by('-create_date')
        
        paginator = Paginator(question_list, 10)
        page_obj = paginator.get_page(page)
        context['question_list'] = page_obj
        context['page'] = page
        context['kw'] = kw
        context['so'] = so
        return context


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'pybo/question_detail.html'
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_object()
        context['answer_list'] = question.answer_set.all()
        return context


class BookQAIndexView(ListView):
    model = BookDiscussion
    template_name = 'pybo/book_qa_list.html'
    context_object_name = 'discussion_list'
    paginate_by = 10

    def get_queryset(self):
        discussion_list = BookDiscussion.objects.select_related('book', 'author').annotate(
            num_voter=Count('voter')).order_by('-create_date')
        return discussion_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page', '1')
        kw = self.request.GET.get('kw', '')
        so = self.request.GET.get('so', 'recent')
        
        discussion_list = BookDiscussion.objects.select_related('book', 'author').annotate(
            num_voter=Count('voter'))
        if kw:
            discussion_list = discussion_list.filter(
                Q(subject__icontains=kw) |  # 제목 검색
                Q(content__icontains=kw) |  # 내용 검색
                Q(author__username__icontains=kw) |  # 글쓴이 검색
                Q(book__title__icontains=kw) |  # 책 제목 검색
                Q(book__author__icontains=kw)  # 책 저자 검색
            ).distinct()
        
        if so == 'recommend':
            discussion_list = discussion_list.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
        elif so == 'popular':
            discussion_list = discussion_list.annotate(num_replies=Count('replies')).order_by('-num_replies', '-create_date')
        else:  # recent
            discussion_list = discussion_list.order_by('-create_date')
        
        paginator = Paginator(discussion_list, 10)
        page_obj = paginator.get_page(page)
        context['discussion_list'] = page_obj
        context['page'] = page
        context['kw'] = kw
        context['so'] = so
        return context


class BookQADetailView(DetailView):
    model = BookDiscussion
    template_name = 'pybo/book_qa_detail.html'
    context_object_name = 'discussion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        discussion = self.get_object()
        context['reply_list'] = discussion.replies.all().order_by('create_date')
        return context


def parse_text_books(text_data):
    """텍스트 데이터를 파싱하여 도서 정보 리스트로 변환"""
    books = []
    lines = text_data.strip().split('\n')
    
    for line_num, line in enumerate(lines, start=1):
        line = line.strip()
        if not line:
            continue
            
        # 다양한 구분자로 파싱 시도
        separators = ['|', ',', '\t', ' - ', ' / ']
        parts = None
        
        for sep in separators:
            if sep in line:
                parts = [part.strip() for part in line.split(sep)]
                break
        
        if not parts:
            # 구분자가 없으면 첫 번째 공백을 기준으로 분리
            parts = line.split(' ', 1)
            if len(parts) == 1:
                parts.append('')
        
        # 최소 2개, 최대 4개의 부분이 있어야 함
        if len(parts) < 2:
            continue
            
        # 부분이 4개 미만이면 빈 문자열로 채움
        while len(parts) < 4:
            parts.append('')
        
        book_info = {
            'title': parts[0],
            'author': parts[1],
            'publisher': parts[2] if len(parts) > 2 else '',
            'publication_year': parts[3] if len(parts) > 3 else ''
        }
        
        # 출판년도가 숫자인지 확인
        if book_info['publication_year']:
            try:
                int(book_info['publication_year'])
            except ValueError:
                book_info['publication_year'] = ''
        
        books.append(book_info)
    
    return books


def book_upload_view(request):
    uploaded_file_url = None
    title = None
    success_count = 0
    error_count = 0
    errors = []
    text_data = ''
    
    if request.method == 'POST':
        # 텍스트 입력 처리
        if request.POST.get('text_data'):
            text_data = request.POST.get('text_data', '').strip()
            title = request.POST.get('title', '텍스트 입력')
            
            if text_data:
                try:
                    books_data = parse_text_books(text_data)
                    
                    for book_info in books_data:
                        try:
                            # 필수 필드 확인
                            if not book_info['title'] or not book_info['author']:
                                continue
                            
                            # 도서 생성 (Pybo Book 사용)
                            book = Book.objects.create(
                                title=book_info['title'],
                                author=book_info['author'],
                                publisher=book_info['publisher'],
                                publication_year=int(book_info['publication_year']) if book_info['publication_year'] else None
                            )
                            success_count += 1
                            
                        except ValueError as e:
                            error_count += 1
                        except Exception as e:
                            error_count += 1
                    
                    if success_count > 0:
                        messages.success(request, f'{success_count}개의 도서가 성공적으로 등록되었습니다.')
                    if error_count > 0:
                        messages.warning(request, f'{error_count}개의 도서 등록에 실패했습니다.')
                        
                except Exception as e:
                    messages.error(request, f'텍스트 처리 중 오류가 발생했습니다: {str(e)}')
        
        # 파일 업로드 처리
        elif request.FILES.get('file'):
            file = request.FILES['file']
            file_extension = file.name.split('.')[-1].lower()
            
            if file_extension not in ['csv', 'json']:
                messages.error(request, 'CSV 또는 JSON 파일만 업로드 가능합니다.')
                return render(request, 'pybo/book_upload.html', {
                    'uploaded_file_url': uploaded_file_url,
                    'title': title,
                    'success_count': success_count,
                    'error_count': error_count,
                    'errors': errors,
                    'text_data': text_data
                })
            
            try:
                if file_extension == 'csv':
                    # CSV 파일 처리
                    decoded_file = file.read().decode('utf-8')
                    csv_reader = csv.DictReader(io.StringIO(decoded_file))
                    
                    for row_num, row in enumerate(csv_reader, start=2):  # 헤더 제외하고 2부터 시작
                        try:
                            # 필수 필드 확인
                            if not row.get('title') or not row.get('author'):
                                errors.append(f"행 {row_num}: 제목과 저자는 필수입니다.")
                                error_count += 1
                                continue
                            
                            # 도서 생성 (Pybo Book 사용)
                            book = Book.objects.create(
                                title=row['title'].strip(),
                                author=row['author'].strip(),
                                publisher=row.get('publisher', '').strip(),
                                publication_year=int(row.get('publication_year', 0)) if row.get('publication_year') else None
                            )
                            success_count += 1
                            
                        except ValueError as e:
                            errors.append(f"행 {row_num}: 출판년도는 숫자여야 합니다.")
                            error_count += 1
                        except Exception as e:
                            errors.append(f"행 {row_num}: {str(e)}")
                            error_count += 1
                            
                elif file_extension == 'json':
                    # JSON 파일 처리
                    decoded_file = file.read().decode('utf-8')
                    data = json.loads(decoded_file)
                    
                    if isinstance(data, list):
                        for item_num, item in enumerate(data, start=1):
                            try:
                                if not item.get('title') or not item.get('author'):
                                    errors.append(f"항목 {item_num}: 제목과 저자는 필수입니다.")
                                    error_count += 1
                                    continue
                                
                                book = Book.objects.create(
                                    title=item['title'].strip(),
                                    author=item['author'].strip(),
                                    publisher=item.get('publisher', '').strip(),
                                    publication_year=int(item.get('publication_year', 0)) if item.get('publication_year') else None
                                )
                                success_count += 1
                                
                            except ValueError as e:
                                errors.append(f"항목 {item_num}: 출판년도는 숫자여야 합니다.")
                                error_count += 1
                            except Exception as e:
                                errors.append(f"항목 {item_num}: {str(e)}")
                                error_count += 1
                    else:
                        errors.append("JSON 파일은 배열 형태여야 합니다.")
                        error_count += 1
                
                if success_count > 0:
                    messages.success(request, f'{success_count}개의 도서가 성공적으로 등록되었습니다.')
                if error_count > 0:
                    messages.warning(request, f'{error_count}개의 도서 등록에 실패했습니다.')
                    
            except Exception as e:
                messages.error(request, f'파일 처리 중 오류가 발생했습니다: {str(e)}')
    
    return render(request, 'pybo/book_upload.html', {
        'uploaded_file_url': uploaded_file_url,
        'title': title,
        'success_count': success_count,
        'error_count': error_count,
        'errors': errors,
        'text_data': text_data
    })


class BookListView(ListView):
    """도서 목록 뷰"""
    model = Book
    template_name = 'pybo/book_list.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        queryset = Book.objects.all().order_by('title')
        return queryset


class BookHistoryView(DetailView):
    """도서 대여 기록 뷰"""
    model = Book
    template_name = 'pybo/book_history.html'
    context_object_name = 'book'
    pk_url_kwarg = 'book_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        histories = BorrowHistory.objects.filter(book=book).order_by('-borrowed_at')
        context['histories'] = histories
        
        # 현재 사용자가 대여 중인지 확인
        if self.request.user.is_authenticated:
            user_has_borrowed = BorrowHistory.objects.filter(
                book=book,
                user=self.request.user,
                returned_at__isnull=True
            ).exists()
            context['user_has_borrowed'] = user_has_borrowed
        
        return context


@login_required(login_url='common:login')
def borrow_book(request, book_id):
    """도서 대여"""
    book = get_object_or_404(Book, pk=book_id)
    
    # 이미 대여 중인지 확인
    active_borrow = BorrowHistory.objects.filter(
        book=book, 
        user=request.user, 
        returned_at__isnull=True
    ).first()
    
    if active_borrow:
        messages.warning(request, '이미 대여 중인 도서입니다.')
    else:
        BorrowHistory.objects.create(book=book, user=request.user)
        messages.success(request, f'"{book.title}" 도서를 대여했습니다.')
    
    return redirect('pybo:book_history', book_id=book_id)


@login_required(login_url='common:login')
def return_book(request, book_id):
    """도서 반납"""
    book = get_object_or_404(Book, pk=book_id)
    
    # 대여 중인 기록 찾기
    active_borrow = BorrowHistory.objects.filter(
        book=book, 
        user=request.user, 
        returned_at__isnull=True
    ).first()
    
    if active_borrow:
        active_borrow.returned_at = timezone.now()
        active_borrow.save()
        messages.success(request, f'"{book.title}" 도서를 반납했습니다.')
    else:
        messages.warning(request, '대여 중인 도서가 아닙니다.')
    
    return redirect('pybo:book_history', book_id=book_id)
