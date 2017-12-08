from django.shortcuts import render,HttpResponse,redirect
from app01 import models
from app01.forms import QuestionForm,QuestionModleForm,OptionModelForm
#   滑动验证码
from app01.geetest import GeetestLib

from django.forms import Form
from django.forms import fields
from django.forms import widgets

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
            stu=models.Student.objects.filter(username=username,pwd=password).first()
            user =models.UserInfo.objects.filter(username=username,pwd=password).first()
            if user :
                request.session.flush()
                login_response["is_login"] = True
                request.session["user"]={"username":username,"id":user.id}
            elif stu:
                request.session.flush()
                login_response["is_login"] = True
                request.session["stu"] = {"username": username, "id": stu.id}

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


#编辑问题 传值
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

   return render(request,"questionList.html",{"tem":inner(),"questionSuv_id":questionSuv_id})

#保存
def saveQuestionSuv(request):
    question_list=request.body
    question_list=question_list.decode("utf-8")
    question_list=json.loads(question_list)
    question_l=question_list.get("question_list")
    questionSuv_id=question_list.get('questionSuv_id')
    qid_l=[]
    for question in question_l:
        qid=question.get('qid')
        print(qid,'------------')
        qtitle=question.get('qtitle')
        qtype=question.get('qtype')
        options=question.get('options')
        if  qid:
            print(qid,'------')
            qid_l.append(int(qid))
        if not qid:
            question=models.Question.objects.create(title=qtitle,type=qtype)
            question.questionSuv.add(questionSuv_id)
            qid_l.append(question.id)
            if options:
                for option in options:
                    oid = option.get('oid')
                    otitle = option.get('otitle')
                    ovalue = option.get('ovalue')
                    models.Option.objects.create(title=otitle,value=ovalue,question=question)
        else:
            models.Question.objects.filter(id=qid).update(title=qtitle,type=qtype)
            y_options=models.Option.objects.filter(question_id=qid).all()
            y_option_ids=[option.id for option in y_options]

            now_optionids=[]
            if options:

                for option in options:
                    oid = option.get('oid')
                    now_optionids.append(int(oid))
                    otitle = option.get('otitle')
                    ovalue = option.get('ovalue')
                    if not oid:
                        models.Option.objects.create(title=otitle, value=ovalue, question_id=qid)
                    else:
                        models.Option.objects.filter(id=oid).update(title=otitle, value=ovalue)
                del_optionid = list(set(y_option_ids).difference(now_optionids))
                for id in del_optionid:
                    models.Option.objects.filter(id=id).delete()

            else:
                models.Option.objects.filter(question_id=qid).delete()
    model_question_ids=[]
    questions=models.Question.objects.filter(questionSuv__id=questionSuv_id).all()
    for question in questions:
        model_question_ids.append(question.id)
    l=list(set(model_question_ids).difference(qid_l))
    for id in l:
        models.Question.objects.filter(id=id).delete()

    return HttpResponse("ok")

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
def fun(value):
    if len(value)<15:
        raise ValidationError("必须超过15字")
#参与问卷调查
def joinQuestionSuv(request,questionSuv_id,class_id):
    stu_id=request.session.get("stu").get("id")

    if not models.ClassList.objects.filter(student__id=stu_id,id=class_id):
        return HttpResponse("你只可以填写本班的调查问卷")
    answer=models.Answer.objects.filter(questionSuv_id=questionSuv_id,stu_id=stu_id)
    if answer:
        return HttpResponse("你已经参与过这次调查问卷了")

    dic = {}
    questions=models.Question.objects.filter(questionSuv__id=questionSuv_id).all()

    for question in questions:

        if question.type==1:
            dic['option_id_%s'%question.id]=fields.ChoiceField(
               label=question.title,
               widget=widgets.RadioSelect,
               choices=models.Option.objects.filter(question=question).values_list("id","title"),
               error_messages={"required": "必选"},
             )
        elif question.type ==2:
            dic['value_%s'%question.id]=fields.ChoiceField(
               label=question.title,
               widget=widgets.RadioSelect,
               choices=[(i,i) for i in range(1,11)],
               error_messages={"required":'必选'},
            )

        else:
            dic["content_%s"%question.id]=fields.CharField(
               label=question.title,
               widget=widgets.Textarea,
               error_messages={"required":'必填'},
               validators=[fun,],
            )




    #创建对象的另一种方法 这是动态生成form
    JoinQuestionSuvForm = type('JoinQuestionSuvForm', (Form,), dic)

    if request.method=='GET':
        form =JoinQuestionSuvForm()
        return render(request,"JoinQuestionSuv.html",{"form":form})
    else:
        form =JoinQuestionSuvForm(request.POST)

        if form.is_valid():
            data=form.cleaned_data
            print(data)
            for k,v in data.items():
                key,qid=k.rsplit("_",1)
                answer_dic={"question_id":qid,"stu_id":stu_id,key:v,'questionSuv_id':questionSuv_id}
                models.Answer.objects.create(**answer_dic)
            return redirect("/index/")
        else:
            return render(request,'JoinQuestionSuv.html',{'form':form})





