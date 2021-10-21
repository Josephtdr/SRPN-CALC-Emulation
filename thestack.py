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
    ranking = {'-': 1, '+': 2, '*': 3, '/': 4, '^': 5, '%': 6}#, '=': 7}
    #d updates everything

    def pop(self):
        return self.stack.pop()[0] #as they are stored as lists (see fn push)

    def get(self):
        return [self.pop() for i in range(len(self.stack))]

    def push(self, opertor):
        rank = self.ranking[opertor]
        self.stack.append([opertor, rank, 1])
        self.sort()

    def sort(self):
        """ sorts the ranking list by their relative ranking """
        self.stack.sort(key=lambda x:x[1])
        #self.ranking.sort(key=lambda x:(x[1],x[2])) to sort both
        #sort by ranking then by reverse index within ranking