from django.db import models

# Create your models here.
class UserInfo(models.Model):
    '''
    用户表
    '''
    username=models.CharField(max_length=32,verbose_name="用户名")
    pwd=models.CharField(max_length=32,verbose_name="密码")


    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural="用户表"


class ClassList(models.Model):
    '''
    班级表
    '''
    title=models.CharField(max_length=64,verbose_name="班级名称")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural="班级表"

class Student(models.Model):
    '''
    学生表
    '''
    username = models.CharField(max_length=32,verbose_name="姓名")
    pwd=models.CharField(max_length=32,verbose_name="姓名")
    cls = models.ForeignKey(to=ClassList,verbose_name="所属班级")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural="学生表"

class QuestionSuv(models.Model):
    '''
    问卷表
    '''
    title=models.CharField(max_length=32,verbose_name="问卷名称")
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    end_time = models.DateTimeField(verbose_name="结束时间",null=True)
    classobj=models.ForeignKey(to=ClassList,verbose_name="班级")
    userInfoobj=models.ForeignKey(to=UserInfo,verbose_name="创建人")


    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural="问卷表"

class Question(models.Model):
    '''
    问题表
    '''
    title=models.CharField(max_length=32,verbose_name="问题名称")
    question_type=(
        (1,"单选"),
        (2,"打分"),
        (3,"建议")
    )
    type=models.IntegerField(choices=question_type,verbose_name="问题类型")
    questionSuv=models.ManyToManyField(to=QuestionSuv,verbose_name="所属问卷")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural="问题表"


class Option(models.Model):
    '''
    单选表
    '''
    title=models.CharField(max_length=32,verbose_name="选项名称")
    value=models.IntegerField(verbose_name="选项所对应的分值")
    question = models.ForeignKey(to=Question,verbose_name="所属问题")


    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural="单选表"

class Answer(models.Model):
    '''
    答案表
    '''
    stu=models.ForeignKey(to=Student,verbose_name="所属学生")
    question=models.ForeignKey(to=Question,verbose_name="所属问题")
    option=models.ForeignKey(to=Option,null=True,blank=True,verbose_name="所属单选表")
    value=models.IntegerField(null=True,blank=True,verbose_name="打分表的分值")
    content=models.CharField(max_length=255,null=True,blank=True,verbose_name="建议表的内容")
    questionSuv=models.ForeignKey(to=QuestionSuv,null=True)

    class Meta:
        verbose_name_plural="答案表"

