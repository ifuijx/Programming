# 简单的 Python 解释器

---

[回到仓库](../README.md)

## 工具

Python 3.6(64-bit), VS Code

## 简介

该例子来自一篇文章。
[原文地址（英文）](http://www.aosabook.org/en/500L/a-python-interpreter-written-in-python.html)
[原文地址（中文译）](https://mp.weixin.qq.com/s/lN53nSnmI1VcPtOTb24PGA)

本例只为实现 Python 解释器的部分内容，忽略了 Python 代码的词法分析，语法分析和编译，并且没有进行任何优化。

在例子中，使用的虚拟机为栈虚拟机。

## 小型的解释器

这个解释器只能理解三个指令，分别是：

* `LOAD_VALUE`
* `ADD_TWO_VALUES`
* `PRINT_ANSWER`

为什么是这三个指令呢？因为在这个例子中，示范的解释器是一个栈机器，在执行指令时，对操作数进行入栈出栈的操作。因此，这三个指令的功能分别是：

* `LOAD_VALUE`: 将一个操作数入栈
* `ADD_TWO_VALUES`：从操作数栈中取出两个操作数，相加后将结果入栈
* `PRINT_ANSWER`：从操作数栈中取出一个数，输出

假设程序代码是 `7 + 5`，而经过解释前的各种步骤得到了如下的指令集：

```python
what_to_execute = {
    # 解析代码得到的指令
    "instructions": [("LOAD_VALUE", 0), # 第二个值为操作数在操作数列表中的序号
                     ("LOAD_VALUE", 1),
                     ("ADD_TWO_VALUES", None), # None 表示不需要从操作数列表中取出操作数
                     ("PRINT_ANSWER", None)],
    # 解析代码得到的操作数
    "numbers": [7, 5]
}
```

为什么要把 `7` 和 `5` 放入操作数列表中，而不是直接放到指令内呢？因为有可能要相加的是两个字符串，比如 `"abc" + "def"`，这样的话操作数就是不定长的，放到指令中并不合适。而且，如果要做的是 `7 + 7`，就能省去一个操作数。

现在开始编写解释器：

```python
class Interpreter:
    def __init__(self):
        self.stack = []
    
    def LOAD_VALUE(self, val):
        self.stack.append(val)
    
    def PRINT_ANSWER(self):
        answer = self.stack.pop()
        print(answer)
    
    def ADD_TWO_VALUES(self):
        first_val = self.stack.pop()
        second_val = self.stack.pop()
        answer = first_val + second_val
        self.stack.append(answer)
```

现在已经定义了一个可以执行指令的解释器，还需要完成的是输入指令，然后执行这些指令，可以编写一个方法：

```python
def run_code(self, what_to_execute):
    instructions = what_to_execute["instructions"]
    numbers= what_to_execute["numbers"]
    for each_step in instructions:
        instruction_name, operand = each_step
        
        if instruction_name == "LOAD_VALUE":
            val = numbers[operand]
            self.LOAD_VALUE(val)
        elif instruction_name == "ADD_TWO_VALUES":
            self.ADD_TWO_VALUES()
        elif instruction_name == "PRINT_ANSWER":
            self.PRINT_ANSWER()
```

执行如下：

```python
what_to_execute = {
    "instructions": [("LOAD_VALUE", 0),
                        ("LOAD_VALUE", 1),
                        ("ADD_TWO_VALUES", None),
                        ("PRINT_ANSWER", None)],
    "numbers": [7, 5]
}

interpreter = Interpreter()
interpreter.run_code(what_to_execute)
```

代码在 [示例代码](./codes/a_tiny_interpreter.py)

## 增加变量

要增加对变量的支持，就要再次添加两条指令，`STORE_NAME` 和 `LOAD_NAME`。另外，还需要添加变量名到值的映射关系。为了简单起见，先忽略命名空间和作用域的影响，因此可以把值和变量的映射保存到解释器中。

代码：

```python
def sample():
    a = 1
    b = 2
    print(a + b)
```

解析之后：

```python
what_to_execute = {
    "instructions": [("LOAD_VALUE", 0),
                     ("STORE_NAME", 0),
                     ("LOAD_VALUE", 1),
                     ("STORE_NAME", 1),
                     ("LOAD_NAME", 0),
                     ("LOAD_NAME", 1),
                     ("ADD_TWO_VALUES", None),
                     ("PRINT_ANSWER", None)],
    "numbers": [1, 2],
    "names": ["a", "b"]
}
```

在解释器中，为了保存变量名到值的映射关系，在解释器中添加一个 `environment` 字典。另外，为了完成指令，还需要添加 `STORE_NAME` 和 `LOAD_NAME` 方法。

貌似所有的工作已经完成了，但是出现了新的问题。现在，已有的指令格式为 `指令名, 序号`，显然，有两个变量列表 `numbers` 和 `names`，而序号指的是哪一个列表中的序号和指令有关。

可以把这种指令和列表的对应关系编写到 `run_code` 方法中，但是可扩展性不好，如果要添加新的指令，就需要在 `run_code` 中添加更多的逻辑。因此，可以尝试把这种对应关系分离出来，写入到新的方法中。

（省略了未修改/添加的方法）

```python
class Interpreter:
    def __init__(self):
        self.stack = []
        self.environment = {}

    def STORE_NAME(self, name):
        val = self.stack.pop()
        self.environment[name] = val

    def LOAD_NAME(self, name):
        val = self.environment[name]
        self.stack.append(val)

    def parse_operand(self, instruction_name, operand, what_to_execute):
        numbers_instructions = ["LOAD_VALUE"]
        names_instructions = ["LOAD_NAME", "STORE_NAME"]

        if operand is None:
            return None

        if instruction_name in numbers_instructions:
            val = what_to_execute["numbers"][operand]
        elif instruction_name in names_instructions:
            val = what_to_execute["names"][operand]

        return val

    def run_code(self, what_to_execute):
        instructions = what_to_execute["instructions"]

        for each_step in instructions:
            instruction_name, operand = each_step

            val = self.parse_operand(instruction_name, operand, what_to_execute)
            
            if instruction_name == "LOAD_VALUE":
                self.LOAD_VALUE(val)
            elif instruction_name == "ADD_TWO_VALUES":
                self.ADD_TWO_VALUES()
            elif instruction_name == "PRINT_ANSWER":
                self.PRINT_ANSWER()
            elif instruction_name == "STORE_NAME":
                self.STORE_NAME(val)
            elif instruction_name == "LOAD_NAME":
                self.LOAD_NAME(val)
```

现在可以看到，`run_code` 方法已经很长了，每添加一个指令，都需要添加一个 `elif` 分支。因此可以使用指令名直接动态调用合适的方法，这也是指令名和方法名写得一致的原因。

```python
def parse_operand(self, instruction_name, operand, what_to_execute):
    numbers_instructions = ["LOAD_VALUE"]
    names_instructions = ["LOAD_NAME", "STORE_NAME"]

    if operand is None:
        return None

    if instruction_name in numbers_instructions:
        val = what_to_execute["numbers"][operand]
    elif instruction_name in names_instructions:
        val = what_to_execute["names"][operand]

    return val

def run_code(self, what_to_execute):
    instructions = what_to_execute["instructions"]

    for each_step in instructions:
        instruction_name, operand = each_step

        val = self.parse_operand(instruction_name, operand, what_to_execute)

        correct_method = getattr(self, instruction_name)
        if val is None:
            correct_method()
        else:
            correct_method(val)
```

代码在 [示例代码](./codes/tiny_interpreter_with_variables.py)

## 结尾

该例就进行到这里，已经可以看到这个解释器的可扩展性和可用性了。文章的其余部分将在以后编写。
