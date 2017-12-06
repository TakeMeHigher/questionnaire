from django.forms import Form, fields, widgets as wd, ModelForm
from app01 import models


class QuestionForm(Form):
    title = fields.CharField(error_messages={"required": "问题不能为空"},
                             widget=wd.Textarea(attrs={"style": "width:600px;height:50px"})
                             )
    type = fields.ChoiceField(choices=((1, "单选"), (2, "打分(0-10分)"), (3, "建议")),
                              widget=wd.Select(attrs={"style": "width:200px;height:30px", "class": "type"}))

    option_ids = fields.ChoiceField(choices=[], widget=wd.RadioSelect())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["option_ids"].choices = models.Option.objects.all().values_list("id", "title")


class AnswerForm(Form):
    value = fields.IntegerField()
    content = fields.CharField()
    options = fields.ChoiceField(choices=[], widget=wd.RadioSelect())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["options"].choices = models.Option.objects.all().values_list("id", "title", "value")


class QuestionModleForm(ModelForm):
    class Meta:
        model = models.Question
        fields = ["title", 'type']

        error_messages = {
            "title": {"required": "名称不能为空"}
        }

        widgets = {
            "title":wd.Textarea(attrs={"class": "question_title","style":"width:600px;height:40px"}),
            "type":wd.Select(attrs={"class":"type","style":"width:300px;height:30px"})
        }

class OptionModelForm(ModelForm):
    class Meta:
        model=models.Option
        fields=["title","value"]

        widgets={
            "title":wd.TextInput(),
            "value":wd.TextInput(),
        }


