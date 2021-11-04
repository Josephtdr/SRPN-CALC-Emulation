""" BASIC SRPN CALCULATOR """
from thestack import Stack
from functions import is_int
import consts

class SRPN:
    """ Calculator Object """
    def __init__(self):
        self.operand_stack = Stack()
        self.randpos = 0
        self.foundhash = False

    def process_command(self, command):
        """ parses a command and runs the relavent functions """
        for char in command.split(' '):
            if char == '#':
                self.foundhash = not self.foundhash
            elif not self.foundhash:
                if is_int(char) or len(char)==1:
                    self.process_command_singular(char)
                elif len(char)>1:
                    self.process_command_multi(list(char))

    def process_command_multi(self, chars):
        """ parses multi char commands char by char"""
        for char in chars:
            self.process_command_singular(char)

    def process_command_singular(self, char):
        """ for processing any input of just a singular command """
        if is_int(char) or char=='r':
            self.process_operand(char)
        elif char=='=':
            print(self.operand_stack.peek())
        elif char in consts.OPERATOR_LIST:
            self.process_operator(char)
        else:
            self.process_unknown(char)

    def process_unknown(self, char):
        """ processes an unidentified char """
        if char!=' ':
            self.process_operand(0)

    def process_operator(self, operator):
        """ processes an operator """
        if operator=='d':
            self.operand_stack.display()
        else:
            c,b,a = None,None,None
            try:
                b = self.operand_stack.pop()
                a = self.operand_stack.pop()
                c = self.compute(operator, a, b)
            except IndexError:
                print("Stack underflow.")
            #in the case of a failed compution return unused values to the stack
            if c is None:
                if a is not None:
                    self.process_operand(a)
                if b is not None:
                    self.process_operand(b)
            else:
                self.operand_stack.push(c)

    def process_operand(self, operand):
        """ processes an operand """
        if operand=='r':
            operand = self.get_randint()
        self.operand_stack.push(operand)

    def compute(self, operator, a, b):
        """ computes the currently stored operand """
        if operator=="+":
            return a+b
        elif operator=="-":
            return a-b
        elif operator=="*":
            return a*b
        elif operator=="/":
            try:
                return a/b
            except ZeroDivisionError:
                print("Divide by 0.")
        elif operator=="%":
            try:
                return int(a)%int(b)
            except ZeroDivisionError:
                print("Divide by 0.")
        elif operator=="^":
            if b >= 0:
                return a**b
            else:
                print("Negative power.")

    def get_randint(self):
        """ gets the next int from the list of 'random' ints """
        randint = consts.RANDLIST[self.randpos]
        self.randpos = (self.randpos + 1) % len(consts.RANDLIST)
        return randint


if __name__ == "__main__":
    srpncalc = SRPN()
    while True:
        try:
            cmd = input()
            srpncalc.process_command(cmd)
        except:
            exit()
