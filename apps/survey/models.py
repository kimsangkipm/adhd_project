# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


# 사용자 모델
class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)  # 생년월일
    age = models.IntegerField(null=True, blank=True)  # 나이
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)  # 연락처
    email = models.EmailField(unique=True)  # 이메일 (기본 제공)
    is_approved = models.BooleanField(default=False)  # 관리자가 승인해야만 True
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='survey_user_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='survey_user_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    def save(self, *args, **kwargs):
        if self.birth_date:
            from datetime import date
            today = date.today()
            self.age = today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
      
      

class SurveyCategory(models.Model):
    code = models.CharField(max_length=20, unique=True)  # inattention, hyperactivity
    title_en = models.CharField(max_length=500)
    title_ko = models.CharField(max_length=500)
    
    def get_title(self, language_mode='BOTH'):
        if language_mode == 'EN':
            return self.title_en
        elif language_mode == 'KO':
            return self.title_ko
        return f"{self.title_en} / {self.title_ko}"
    
    class Meta:
        verbose_name_plural = "Survey Categories"
        

class SurveyQuestion(models.Model):
    LANGUAGE_MODE_CHOICES = [
        ('EN', 'English Only'),
        ('KO', 'Korean Only'),
        ('BOTH', 'Both English and Korean')
    ]
    
    text_en = models.TextField()  # 영어 질문
    text_ko = models.TextField()  # 한글 질문
    category = models.ForeignKey(SurveyCategory, on_delete=models.CASCADE)

    weight_never_en = models.CharField(max_length=20, default="Never")  # 영어 라벨
    weight_never_ko = models.CharField(max_length=20, default="전혀 그렇지 않다")  # 한글 라벨
    weight_never_value = models.IntegerField(default=0)  # 점수

    weight_sometimes_en = models.CharField(max_length=20, default="Sometimes")
    weight_sometimes_ko = models.CharField(max_length=20, default="가끔 그렇다")
    weight_sometimes_value = models.IntegerField(default=1)

    weight_often_en = models.CharField(max_length=20, default="Often")
    weight_often_ko = models.CharField(max_length=20, default="자주 그렇다")
    weight_often_value = models.IntegerField(default=2)

    weight_always_en = models.CharField(max_length=20, default="Always")
    weight_always_ko = models.CharField(max_length=20, default="항상 그렇다")
    weight_always_value = models.IntegerField(default=3)

    def get_text(self, language_mode='BOTH'):
        """사용자의 언어 설정에 따라 질문을 반환"""
        if language_mode == 'EN':
            return self.text_en
        elif language_mode == 'KO':
            return self.text_ko
        else:
            return f"{self.text_en} / {self.text_ko}"  # 영어와 한글 함께 표시

    def get_weight_labels(self, language_mode='BOTH'):
        """사용자의 언어 설정에 따라 가중치 라벨 반환"""
        if language_mode == 'EN':
            return {
                "never": self.weight_never_en,
                "sometimes": self.weight_sometimes_en,
                "often": self.weight_often_en,
                "always": self.weight_always_en,
            }
        elif language_mode == 'KO':
            return {
                "never": self.weight_never_ko,
                "sometimes": self.weight_sometimes_ko,
                "often": self.weight_often_ko,
                "always": self.weight_always_ko,
            }
        else:
            return {
                "never": f"{self.weight_never_en} / {self.weight_never_ko}",
                "sometimes": f"{self.weight_sometimes_en} / {self.weight_sometimes_ko}",
                "often": f"{self.weight_often_en} / {self.weight_often_ko}",
                "always": f"{self.weight_always_en} / {self.weight_always_ko}",
            }

    def get_weight_value(self, response):
        """응답에 해당하는 가중치 점수 반환"""
        weight_map = {
            "never": self.weight_never_value,
            "sometimes": self.weight_sometimes_value,
            "often": self.weight_often_value,
            "always": self.weight_always_value
        }
        return weight_map.get(response, 0)  # 기본값 0

    def __str__(self):
        return f"{self.get_text()} ({self.category.get_title()})"



# 사용자 응답 모델
class UserResponse(models.Model):
    RESPONSE_CHOICES = [
        ('never', 'Never'),
        ('sometimes', 'Sometimes'),
        ('often', 'Often'),
        ('always', 'Always')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 사용자 연동
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)  # 설문 문항 연동
    response = models.CharField(max_length=10, choices=RESPONSE_CHOICES)  # 응답 선택지
    created_at = models.DateTimeField(auto_now_add=True)  # 응답 제출 시간

    def __str__(self):
        return f"{self.user.username} - {self.question.text} : {self.response}"