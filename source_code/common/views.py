from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserForm, ProfileUpdateForm

def login_view(request):
    """
    로그인
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('pybo:index')
    else:
        form = AuthenticationForm()
    return render(request, 'common/login.html', {'form': form})

def logout_view(request):
    """
    로그아웃
    """
    from django.contrib.auth import logout
    logout(request)
    return redirect('pybo:index')

def signup(request):
    """
    회원가입
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('pybo:index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})

@login_required(login_url='common:login')
def profile(request):
    """
    마이 페이지
    """
    return render(request, 'common/profile.html')

@login_required(login_url='common:login')
def profile_update(request):
    """
    프로필 수정
    """
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            # 닉네임 업데이트
            user.username = form.cleaned_data['username']
            
            # 비밀번호 업데이트 (새 비밀번호가 입력된 경우에만)
            new_password = form.cleaned_data['password1']
            if new_password:
                user.set_password(new_password)
                update_session_auth_hash(request, user)  # 세션 유지
            
            user.save()
            messages.success(request, '프로필이 성공적으로 수정되었습니다.')
            return redirect('common:profile')
    else:
        form = ProfileUpdateForm(user=request.user)
    
    return render(request, 'common/profile.html', {'form': form})
