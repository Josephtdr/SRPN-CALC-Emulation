from functions import saturation
from math import floor

class Stack:
    def __init__(self):
        self.stack = []

    def peek(self):
        if self.is_empty():
            return "Stack empty."
        else:
            return floor(self.stack[-1])

    def push(self, operand):
        if not self.is_full():
            self.stack.append(saturation(operand))
        else:
            print("Stack overflow.")

    def pop(self):
        return self.stack.pop()

    def display(self): #d updates everything in regards to operator stackings
        if self.is_empty():
            print("-2147483648")
        else:
            for operand in self.stack:
                print(floor(operand))

    def get_len(self):
        return len(self.stack)
    def is_full(self):
        return self.get_len() > 22
    def is_empty(self):
        return self.get_len() == 0

class OperatorStack(Stack):
    def __init__(self):
        super().__init__()
        self.ranking = {'=': 0, 'd': 0, '-': 1, '+': 2,
                        '*': 3, '/': 4, '^': 5, '%': 6}
        self.accum = {'-': 0, '+': 0, '*': 0,
                        '/': 0, '^': 0, '%': 0}

    def get_rank(self, operator):
        return self.ranking[operator]
        
    def push(self, operator):
        rank = self.get_rank(operator)
        if operator in ["=", 'd']:
            self.stack.append([operator, rank, 0, False])
        else:
            update = any(rank < op_rank for op_rank in [x[1] for x in self.stack])
            accum = self.accum[operator]
            self.accum[operator] -= 1
            self.stack.append([operator, rank, accum, update])

    def get_sort(self):
        """ sorts the ranking list by their relative ranking while keeping '=' static"""
        y = [op for op in self.stack if op[0] != '=']
        y.sort(key=lambda x:(x[1], x[2]))

        sorted_stack = [op if op[0]=='=' else y.pop() for op in self.stack]
        self.stack = []
        return sorted_stack
        #this maybe workey

        #self.stack.sort(key=lambda x:(x[1], x[2])) #to sort both
