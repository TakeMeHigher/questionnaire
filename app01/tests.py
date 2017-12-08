from django.test import TestCase

# Create your tests here.
# l=[]
# dic={"a":None}
# for i in range(3):
#     dic['a']=i
#     l.append(dic)
# print(l)



#
# l=[1,2,3]
#
# c=[4,5]
#
# l.append(c)
# c.append(7)
#
# print(c)
# print(l)#[1, 2, 3, [4, 5, 7]]


# d1={"name":"yuan"}
# d2={"age":12}
# d1["xxx"]=d2
#
# d2["height"]="180cm"
#
# print(d1)   # {"name":"yuan","xxx":{"age":12,"height":"180cm"}}




d1={1:{"xxx":[12,34]},2:{"xxx":[34,56,[777,888,999],[11,8238,99]]}}
d2={"xxx":[777,888,999,[11,8238,99]]}
d3={"xxx":[11,8238,99]}

d1[2]["xxx"].append(d2["xxx"])
d2["xxx"].append(d3["xxx"])

print(d1)   #  {1:{"xxx":[12,34]},2:{"xxx":[34,56,[777,888,999,[11,8238,99]]]}}
print(d2)   #  {"xxx":[777,888,999,[11,8238,99]]}
print(d3)   #  d3={"xxx":[11,8238,99]}



class User(object):
    countury='china'
    def __init__(self,args):
        self.args=args

    def get(self):
        return self.args


#类名=type('类名',(继承的类,),dict)
def ff():
    return 123
Foo = type('Foo',(object,),{'x1':8,'func':lambda self,arg:arg,"ff":ff})