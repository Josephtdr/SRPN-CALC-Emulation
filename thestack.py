from functions import saturation

class Stack:
    def __init__(self):
        self.stack = []

    def peek(self):
        if self.is_empty():
            print("Stack empty.")
        else:
            print(self.stack[-1])

    def push(self, operand):
        if not self.is_full():
            self.stack.append(saturation(operand))
        else:
            print("Stack overflow.")

    def pop(self):
        return self.stack.pop()

    def display(self):
        if self.is_empty():
            print("-2147483648")
        else:
            for operand in self.stack:
                print(operand)

    def get_len(self):
        return len(self.stack)
    def is_full(self):
        return self.get_len() > 22
    def is_empty(self):
        return self.get_len() == 0
