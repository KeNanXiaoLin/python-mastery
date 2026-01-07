def func():
    x = 10
    # exec('x = 15; print(x)')  # 输出: 15
    loc = {}
    exec('x = 15', None, loc)          # 输出: 10
    x = loc['x']
    print(x)                   # 输出: 15 ✅
func()


def dynamic_variable_creation():
    var_names = ['var1', 'var2', 'var3']
    for i, name in enumerate(var_names):
        locals()[name] = i
    print(locals())
 
dynamic_variable_creation()

x = 100
exec('x = 15', globals(), None)  
print(x)

