from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from django.views.generic import ListView, DetailView

from ..models import Question, UploadedFile


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


def request_info_view(request):
    context = {
        'method': request.method,
        'get_data': request.GET,
        'post_data': request.POST,
        'user': request.user,
        'is_logged_in': request.user.is_authenticated,
        'path': request.path,
        'full_url': request.build_absolute_uri(),
        'session_value': request.session.get('demo', '없음'),
        'user_agent': request.META.get('HTTP_USER_AGENT', '알 수 없음'),
        'client_ip': request.META.get('REMOTE_ADDR', '알 수 없음'),
    }
    request.session['demo'] = '세션에서 저장한 값입니다.'
    return render(request, 'pybo/request_info.html', context)


def file_upload_view(request):
    uploaded_file_url = None
    title = None
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        title = request.POST.get('title', '')
        uploaded = UploadedFile.objects.create(title=title, file=file)
        uploaded_file_url = uploaded.file.url
    return render(request, 'pybo/upload_file.html', {
        'uploaded_file_url': uploaded_file_url,
        'title': title
    })
