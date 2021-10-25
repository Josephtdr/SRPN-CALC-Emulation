from functions import saturation

class Stack:
    """ Custom Stack for operands """
    def __init__(self):
        self.stack = []

    def peek(self):
        if self.is_empty():
            return "Stack empty."
        else:
            return int(self.stack[-1])

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
                print(int(operand))

    def get_len(self):
        return len(self.stack)
    def is_full(self):
        return self.get_len() > 22
    def is_empty(self):
        return self.get_len() == 0

class OperatorStack(Stack):
    """ Modified from above custom Stack for operators """
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
        """ sorts the stack by their relative rankings while keeping '=' static"""
        templist = [op for op in self.stack if op[0] != '=']
        templist.sort(key=lambda x:(x[1], x[2]))

        sorted_stack = [op if op[0]=='=' else templist.pop() for op in self.stack]
        self.stack = []
        return sorted_stack
