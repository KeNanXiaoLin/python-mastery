x = 10
y = 20

print(globals())
def func(m:int,n:int)->int:
    "this is my func"
    global x  # 声明x是全局变量
    x = 37
    b = 29
    print(locals())
    return m+n
    
f = func
f.name = "myfunc"
print(f.name)
print(f.__doc__)
print(f.__annotations__)
print(f.__dict__)
print(dir(f))
import inspect
print(inspect.signature(f))
args = 1,2
sig = inspect.signature(f)
bound = sig.bind(*args)
print(bound.arguments)
print(eval("f(1,2)"))
print(exec("result = f(3,4)"))
