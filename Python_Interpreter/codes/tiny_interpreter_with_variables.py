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
            
            # if instruction_name == "LOAD_VALUE":
            #     self.LOAD_VALUE(val)
            # elif instruction_name == "ADD_TWO_VALUES":
            #     self.ADD_TWO_VALUES()
            # elif instruction_name == "PRINT_ANSWER":
            #     self.PRINT_ANSWER()
            # elif instruction_name == "STORE_NAME":
            #     self.STORE_NAME(val)
            # elif instruction_name == "LOAD_NAME":
            #     self.LOAD_NAME(val)

            correct_method = getattr(self, instruction_name)
            if val is None:
                correct_method()
            else:
                correct_method(val)


if __name__ == "__main__":
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

    interpreter = Interpreter()
    interpreter.run_code(what_to_execute)
