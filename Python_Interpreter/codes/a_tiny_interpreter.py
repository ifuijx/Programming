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


if __name__ == "__main__":
    what_to_execute = {
        "instructions": [("LOAD_VALUE", 0),
                        ("LOAD_VALUE", 1),
                        ("ADD_TWO_VALUES", None),
                        ("PRINT_ANSWER", None)],
        "numbers": [7, 5]
    }

    interpreter = Interpreter()
    interpreter.run_code(what_to_execute)
