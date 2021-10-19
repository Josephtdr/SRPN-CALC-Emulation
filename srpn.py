""" SRPN CALCULATOR """
from thestack import Stack
from functions import is_int
import consts

class SRPN:
    """ Calculator Object """
    def __init__(self):
        self.operand_stack = Stack()
        self.randpos = 0
        self.foundhash = False
        self.rega, self.regb = '',''
        self.regoperator = ''
        self.regeq = ''

    def process_command(self, command):
        """ parses a command and runs the relavent functions """
        def reg_check(temp_operand): #processes a temporary stored operand
            if temp_operand != '':
                self.regeq = temp_operand
                self.process_operand(temp_operand)
            if self.regoperator:
                self.process_operator()
            return ''

        for char in command.split(' '):
            if char == '#':
                self.foundhash = not self.foundhash
            elif not self.foundhash:
                if char=='=':
                    self.operand_stack.peek()
                else:
                    temp_operand = '' #reset for each set of commands
                    chars = list(char)
                    for i, cha in enumerate(chars):
                        if is_int(cha) or (cha=='-' and i==0 and
                            len(chars)>1 and is_int(chars[i+1])):
                            temp_operand+= cha
                        elif cha=='r': #treat r like another int
                            temp_operand = reg_check(temp_operand)
                            self.process_operand(self.get_randint())
                        elif cha in consts.OPERATOR_LIST: #cha an operator
                            temp_operand = reg_check(temp_operand)
                            self.regoperator = cha
                        else: #cha is not a operator nor an operand
                            self.process_char(cha)
                    reg_check(temp_operand)

    def process_char(self, char):
        """ processes an unidentified char """
        if char!=' ':
            print('Unrecognised operator or operand "{}".'.format(char))

    def process_operator(self):
        """ processes an operator """
        if self.regoperator=='=':
            if self.regeq != '':
                print(self.regeq)
            else:
                self.operand_stack.peek()
        elif self.regoperator=='d':
            self.operand_stack.display()
        else:
            c = None
            try:
                self.regb = self.operand_stack.pop()
                self.rega = self.operand_stack.pop()
                c = self.compute()
            except IndexError:
                print("Stack underflow.")

            if c is None:
                if self.rega != '':
                    self.process_operand(self.rega)
                if self.regb != '':
                    self.process_operand(self.regb)
            else:
                self.process_operand(c)
        self.emptyreg()

    def process_operand(self, operand):
        """ pushes a given operand to the stack """
        self.operand_stack.push(operand)

    def compute(self):
        """ computes a new operand with the currently stored operator """
        if self.regoperator=="+":
            return self.rega+self.regb
        if self.regoperator=="-":
            return self.rega-self.regb
        if self.regoperator=="*":
            return self.rega*self.regb
        if self.regoperator=="/":
            try:
                return self.rega//self.regb
            except ZeroDivisionError:
                print("Divide by 0.")
                return None
        if self.regoperator=="%":
            return self.rega%self.regb
        if self.regoperator=="^":
            if self.regb >= 0:
                return self.rega**self.regb
            else:
                print("Negative power.")
                return None

    def get_randint(self):
        """ gets the next int from the list of 'random' ints """
        randint = consts.RANDLIST[self.randpos]
        self.randpos = (self.randpos + 1) % len(consts.RANDLIST)
        return randint

    def emptyreg(self):
        """ resets the 'registry' values """
        self.rega, self.regb, self.regoperator = '','',''


#This is the entry point for the program.
#Do not edit the below
#slightly edited, should be fine lol
if __name__ == "__main__":
    srpn = SRPN()
    while True:
        try:
            cmd = input()
            srpn.process_command(cmd)
        except:
            exit()
