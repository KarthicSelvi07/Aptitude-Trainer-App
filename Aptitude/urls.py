from django.urls import path
from .views import SignInView, RegisterView, home_view, topics,topics_detail,formulas_page,test_result,practice_question,test_question,progress_page

urlpatterns = [
    path("signin/", SignInView.as_view(), name="signin"),
    path("signup/", RegisterView.as_view(), name="signup"),
    path("home/", home_view, name="home"),
    path("topics/", topics, name="topics"),  # Now correctly imported
    path('topics_detail/<int:topic_id>/', topics_detail, name='topics_detail'),
    path('formulas/<int:topic_id>/', formulas_page, name='formulas_page'),
    path('practice/<int:topic_id>/<int:question_index>/', practice_question, name='practice_question'),
    path('test/<int:topic_id>/<int:question_index>/', test_question, name='test_question'),
    path('progress/', progress_page, name='progress_page'),
    path('test_result/<int:topic_id>', test_result, name='test_result'),
]

