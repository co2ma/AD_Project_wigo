from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout
from .forms import UserForm


def signup(request):
    """
    계정생성
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})

@api_view(['POST'])
def api_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({'success': True, 'username': user.username})
    else:
        return Response({'success': False, 'error': '아이디 또는 비밀번호가 올바르지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def api_logout(request):
    logout(request)
    return Response({'success': True})
