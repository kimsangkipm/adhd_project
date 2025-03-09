from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm
from .models import User, SurveyQuestion
from django.contrib.auth.decorators import login_required



def index(request):
    template_name = 'index.html'
    return render(request, template_name)

# 회원가입
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # 가입 후 비활성화 상태 (관리자 승인 필요)
            user.save()
            messages.success(request, "회원가입 신청 완료! 관리자의 승인을 기다려주세요.")
            return redirect("survey/login")
    else:
        form = RegisterForm()
    return render(request, "survey/register.html", {"form": form})

# 로그인
def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                if user.is_approved:
                    login(request, user)
                    template_name = 'index.html'
                    return render(request, template_name)
                else:
                    messages.error(request, "관리자의 승인이 필요합니다.")
            else:
                messages.error(request, "아이디 또는 비밀번호가 올바르지 않습니다.")
        except User.DoesNotExist:
            messages.error(request, "아이디 또는 비밀번호가 올바르지 않습니다.")
    return render(request, "survey/login.html")

# 로그아웃
def user_logout(request):
    logout(request)
    return redirect('survey:index')
#    template_name = 'index.html'
#    return render(request, template_name)


# @login_required
def survey(request):
    # if not request.user.is_approved:
    #     return render(request, "survey/not_approved.html")
        
    questions = SurveyQuestion.objects.all()
    context = {
        'questions': questions
    }
    return render(request, "survey/survey.html", context)