from django.template import Library

register=Library()
@register.filter
def stu_count(answers):
    stu_l=[]
    for answer in answers:
        stu=answer.stu
        stu_l.append(stu)

    stu_l=set(stu_l)

    return len(stu_l)

