from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.http import JsonResponse
import csv
import io
import json
import re

from ..models import Question, UploadedFile, Book
from library.models import Book as LibraryBook


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
    model = Question
    template_name = 'pybo/book_qa_list.html'
    context_object_name = 'question_list'
    paginate_by = 10

    def get_queryset(self):
        question_list = Question.objects.filter(book__isnull=False).annotate(
            num_voter=Count('voter')).order_by('-create_date')
        return question_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page', '1')
        kw = self.request.GET.get('kw', '')
        so = self.request.GET.get('so', 'recent')
        
        question_list = Question.objects.filter(book__isnull=False).annotate(
            num_voter=Count('voter'))
        if kw:
            question_list = question_list.filter(
                Q(subject__icontains=kw) |  # 제목 검색
                Q(content__icontains=kw) |  # 내용 검색
                Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
                Q(answer__author__username__icontains=kw) |  # 답변 글쓴이 검색
                Q(book__title__icontains=kw)  # 책 제목 검색
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


class BookQADetailView(DetailView):
    model = Question
    template_name = 'pybo/book_qa_detail.html'
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_object()
        context['answer_list'] = question.answer_set.all()
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
                            
                            # 도서 생성
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
                        messages.warning(request, f'{error_count}개의 항목에서 오류가 발생했습니다.')
                    if success_count == 0 and error_count == 0:
                        messages.warning(request, '유효한 도서 정보를 찾을 수 없습니다.')
                        
                except Exception as e:
                    messages.error(request, f'텍스트 처리 중 오류가 발생했습니다: {str(e)}')
        
        # 파일 업로드 처리
        elif request.FILES.get('file'):
            file = request.FILES['file']
            title = request.POST.get('title', '')
            
            # 파일 저장
            uploaded = UploadedFile.objects.create(title=title, file=file)
            uploaded_file_url = uploaded.file.url
            
            # 파일 확장자 확인
            file_extension = file.name.split('.')[-1].lower()
            
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
                            
                            # 도서 생성
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
                else:
                    errors.append("지원하지 않는 파일 형식입니다. CSV 또는 JSON 파일을 업로드해주세요.")
                    error_count += 1
                    
            except Exception as e:
                errors.append(f"파일 처리 중 오류가 발생했습니다: {str(e)}")
                error_count += 1
            
            # 결과 메시지 표시
            if success_count > 0:
                messages.success(request, f'{success_count}개의 도서가 성공적으로 등록되었습니다.')
            if error_count > 0:
                messages.error(request, f'{error_count}개의 항목에서 오류가 발생했습니다.')
                for error in errors[:5]:  # 최대 5개 오류만 표시
                    messages.warning(request, error)
    
    return render(request, 'pybo/book_upload.html', {
        'uploaded_file_url': uploaded_file_url,
        'title': title,
        'success_count': success_count,
        'error_count': error_count,
        'errors': errors,
        'text_data': text_data
    })
