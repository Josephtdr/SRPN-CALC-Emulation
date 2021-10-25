""" SRPN CALCULATOR """
from thestack import Stack, OperatorStack
from functions import is_int
import consts

class SRPN:
    """ Calculator Object """
    operand_stack = Stack()
    operator_stack = OperatorStack()
    randpos = 0
    foundhash = False
    regeq = ''

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
        """ for processing any input of multiple commands """
        def process_temp_operand(temp_operand):
            """ processes the temp stored operand onto the stack """
            if temp_operand: self.process_operand(temp_operand)
            return ''
        def process_operator_stack():
            """ computes the operators in sorted order """
            sorted_operators = self.operator_stack.get_sort()
            for operator, _, _, update in sorted_operators:
                if update: #update value
                    self.regeq = self.operand_stack.peek()
                self.process_operator(operator)
            self.regeq = self.operand_stack.peek()

        temp_operand = '' #reset for each set of commands
        for i, cha in enumerate(chars):
            if is_int(cha) or (temp_operand=='' and cha=='-' and len(chars)>i+1
                and is_int(chars[i+1]) and ((i>0) == (chars[i-1]!='-'))):
                temp_operand+= cha
            else:
                temp_operand = process_temp_operand(temp_operand)
                if cha=='r': #treat r like another int
                    self.process_operand(cha)
                elif cha in consts.OPERATOR_LIST: #cha an operator
                    self.operator_stack.push(cha)
                    if cha=='d':
                        process_operator_stack()
                else: #cha is not a operator nor an operand
                    self.process_unknown(cha)

        process_temp_operand(temp_operand)
        process_operator_stack()

    def process_command_singular(self, char):
        """ for processing any input of just a singular command """
        if is_int(char) or char=='r':
            self.process_operand(char)
        elif char=='=': #different for multi/singular commands
            print(self.operand_stack.peek())
        elif char in consts.OPERATOR_LIST:
            self.process_operator(char)
        else:
            self.process_unknown(char)

    def process_unknown(self, char):
        """ processes an unidentified char """
        if char!=' ':
            print('Unrecognised operator or operand "{}".'.format(char))

    def process_operator(self, operator):
        """ processes an operator """
        if operator=='=': #only '=' from commmand_multi sent here
            print(self.regeq if self.regeq else self.operand_stack.peek())

        elif operator=='d':
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
        self.regeq = operand
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


#This is the entry point for the program.
#Do not edit the below
#slightly edited, hopefully fine
if __name__ == "__main__":
    srpn = SRPN()
    while True:
        try:
            cmd = input()
            srpn.process_command(cmd)
        except:
            exit()
