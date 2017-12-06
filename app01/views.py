from django.shortcuts import render,HttpResponse,redirect
from app01 import models
from app01.forms import QuestionForm,QuestionModleForm,OptionModelForm
#   滑动验证码
from app01.geetest import GeetestLib

import json
# Create your views here.

pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"
mobile_geetest_id = "7c25da6fe21944cfe507d2f9876775a9"
mobile_geetest_key = "f5883f4ee3bd4fa8caec67941de1b903"


def pcgetcaptcha(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)

#滑动验证码登录
def pcajax_validate(request):
    if request.method == "POST":
        login_response = {"is_login": False, "error_msg": None}
        #  验证验证码
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        # 扩充 验证用户名密码
        if result:
            username = request.POST.get("username")
            password = request.POST.get("password")

            user =models.UserInfo.objects.filter(username=username,pwd=password).first()
            if user:
                login_response["is_login"] = True
                request.session["user"]={"username":username,"id":user.id}

            else:
                login_response["error_msg"] = "username or password error"

        else:
            login_response["error_msg"] = "验证码错误"

        return HttpResponse(json.dumps(login_response))

    return HttpResponse("error")


def index(request):
    questionSuvs=models.QuestionSuv.objects.all()
    return render(request,"index.html",{"questionSuvs":questionSuvs})


def login(request):
    return render(request,"login.html")


def addQuestionSuv(request):
    if request.method=="POST":
        title=request.POST.get("title")
        class_id=request.POST.get("classlist")
        models.QuestionSuv.objects.create(title=title,classobj_id=class_id,userInfoobj_id=request.session["user"].get("id"))
        return redirect("/index/")
    classlist=models.ClassList.objects.all()
    return render(request,"addQuestionSuv.html",{"classlist":classlist})



def editQuestionSuv(request,questionSuv_id):
   def inner():
       questions=models.Question.objects.filter(questionSuv__id=questionSuv_id).all()

       if not questions:
           form=QuestionModleForm()

           yield {"form":form,"question":None,"options":None,"option_class":"hide"}
       else:

           for question in questions:
               tem = {"form": None, "question": None, "options": None, "option_class": "hide"}
               form=QuestionModleForm(instance=question)
               tem["form"]=form
               tem["question"]=question
               if question.type==1:
                   tem["option_class"]=''
                   def inner_option(question):
                       options=models.Option.objects.filter(question=question).all()
                       for option in options:
                           optionform=OptionModelForm(instance=option)
                           yield  {"form":optionform,"option":option}
                   tem["options"]=inner_option(question)
               yield tem

   return render(request,"questionList.html",{"tem":inner()})


