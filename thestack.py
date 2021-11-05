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
    """ Modified from above custom Stack for operators in SRPNADV """
    def __init__(self):
        super().__init__()
        self.ranking = {'=': 0, 'd': 0, '-': 1, '+': 2,
                        '*': 3, '/': 4, '^': 5, '%': 6}

    def get_rank(self, operator):
        return self.ranking[operator]

    def get_previous_rank(self):
        """ excludes operators '=' and 'd' """
        for op_rank in reversed([x[1] for x in self.stack]):
                if op_rank > 0:
                    return op_rank
        return 0

    def push(self, operator):
        rank = self.get_rank(operator)
        if operator in ["=", 'd']:
            self.stack.append([operator, rank, False])
        else:
            update = rank < self.get_previous_rank()
            self.stack.append([operator, rank, update])

    def get_sort(self):
        """ recursive sorter thingy"""
        def mini_sort(tbseperated):
            if len(tbseperated)<=1:
                return tbseperated

            i = len(tbseperated) - 1
            rank = tbseperated[i][1]
            comparrank = tbseperated[i-1][1]
            lowestcomprank = comparrank

            while rank>comparrank and comparrank<=lowestcomprank and i>0:
                if lowestcomprank>comparrank:
                    lowestcomprank=comparrank
                tbseperated[i], tbseperated[i-1] = tbseperated[i-1], tbseperated[i]
                i -= 1
                rank = tbseperated[i][1]
                comparrank = tbseperated[i-1][1]
                
            return mini_sort(tbseperated[:i]) + mini_sort(tbseperated[i:])

        """ sorts the stack by their relative rankings while keeping '=' static"""
        templist = [op for op in self.stack if op[0] != '=']
        othertemp = mini_sort(templist)
        othertemp.reverse()
        sorted_stack = [op if op[0]=='=' else othertemp.pop() for op in self.stack]
        self.stack = []
        return sorted_stack
