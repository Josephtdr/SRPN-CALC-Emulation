""" ADVANCED SRPN CALCULATOR """
from srpnbasic import SRPN
from thestack import OperatorStack
from functions import is_int
import consts

class SRPNADV(SRPN):
    """ ADVANCED Calculator Object """
    def __init__(self):
        super().__init__()
        self.operator_stack = OperatorStack()
        self.regeq = ''

    def process_command_multi(self, chars):
        """ for processing any input of multiple commands """
        def process_temp_operand(temp_operand):
            """ processes the temp stored operand onto the stack """
            if temp_operand: self.process_operand(temp_operand)
            return ''
        def process_operator_stack():
            """ computes the operators in sorted order """
            sorted_operators = self.operator_stack.get_sort()
            for operator, _, update in sorted_operators:
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

    def process_operator(self, operator):
        if operator=='=': #only '=' from _commmand_multi sent here
            print(self.regeq if self.regeq else self.operand_stack.peek())
        else:
            super().process_operator(operator)

    def process_operand(self, operand):
        """ pushes an operand to the stack """
        if operand=='r':
            operand = self.get_randint()
        self.regeq = operand
        self.operand_stack.push(operand)

    def process_unknown(self, char):
        """ processes an unidentified char """
        if char!=' ':
            print('Unrecognised operator or operand "{}".'.format(char))


if __name__ == "__main__":
    srpncalc = SRPNADV()
    while True:
        try:
            cmd = input()
            srpncalc.process_command(cmd)
        except:
            exit()
