import re


class Conversion:
    def __init__(self, capacity):
        self.top = -1
        self.capacity = capacity
        self.array = []
        self.output = []
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

    @property
    def isEmpty(self):
        return self.top == -1

    def peek(self):
        return self.array[-1]

    def pop(self):
        if not self.isEmpty:
            self.top -= 1
            return self.array.pop()
        else:
            return "$"

    def push(self, op):
        self.top += 1
        self.array.append(op)

    def isOperand(self, ch):
        return ch.isdigit()

    def notGreater(self, i):
        try:
            a = self.precedence[i]
            b = self.precedence[self.peek()]
            return True if a <= b else False
        except KeyError:
            return False

    def infixToPostfix(self, exp):
        for i in exp:
            if self.isOperand(i):
                self.output.append(i)
            elif i == '(':
                self.push(i)
            elif i == ')':
                while ((not self.isEmpty) and
                       self.peek() != '('):
                    a = self.pop()
                    self.output.append(a)
                if not self.isEmpty and self.peek() != '(':
                    return -1
                else:
                    self.pop()
            else:
                while not self.isEmpty and self.notGreater(i):
                    self.output.append(self.pop())
                self.push(i)
        while not self.isEmpty:
            self.output.append(self.pop())
        return self.output


def evaluation(list):
    #print(list)
    stack = []
    for i in range(len(list)):
        try:
            stack.append(int(list[i]))
        except ValueError:
            if list[i] == '+':
                stack[-2] = stack[-1] + stack[-2]
                stack.pop(-1)
            elif list[i] == '-':
                stack[-2] = stack[-2] - stack[-1]
                stack.pop(-1)
            elif list[i] == '*':
                stack[-2] = stack[-2] * stack[-1]
                stack.pop(-1)
            elif list[i] == '/':
                stack[-2] = stack[-2] / stack[-1]
                stack.pop(-1)
            elif list[i] == '^':
                stack[-2] = stack[-2] ^ stack[-1]
                stack.pop(-1)
        #print(stack)
    return int(stack[0])


def check(numbers):
    if numbers.count('(') != numbers.count(')'):
        return 'Invalid expression'
    for i in range(len(numbers)):
        try:
            int(numbers[i])
        except ValueError:
            if numbers[i] in variables.keys():
                numbers[i] = variables[numbers[i]]
            elif numbers[i] in ['*', '/', '(', ')', '^']:
                pass
            else:
                if '+' in numbers[i]:
                    numbers[i] = '+'
                elif '-' in numbers[i]:
                    if numbers[i].count('-') % 2:
                        numbers[i] = '-'
                    else:
                        numbers[i] = '+'
                else:
                    return 'Invalid expression'
    obj = Conversion(len(numbers))
    return evaluation(obj.infixToPostfix(numbers))


def variable_check(string):
    expration = string.split('=')
    if len(expration) > 2:
        print('Invalid assignment')
    else:
        a = ''.join(expration[0].split())
        b = ''.join(expration[1].split())
        if a.isalpha() and b.isalpha():
            if b in variables.keys():
                variables[a] = variables[b]
            else:
                print('Unknown variable')
        elif a.isalpha() and b.isdigit():
            variables[a] = b
        elif not a.isalpha():
            print('Invalid identifier')
        else:
            print('Invalid assignment')


def main():
    while True:
        string = input()
        if string == '/exit':
            print('Bye!')
            exit()
        elif string == '/help':
            print('The program calculates the sum of numbers')
        elif string.startswith('/'):
            print('Unknown command')
        elif string != '':
            if '=' in string:
                variable_check(string)
            else:
                numbers = re.findall(r'\++|\*+|/+|\(|\)|-+|\^+|[0-9]+|[a-z]+', string)
                if len(numbers) == 1 and numbers[0].isalpha():
                    if numbers[0] in variables.keys():
                        print(variables[numbers[0]])
                    else:
                        print('Unknown variable')
                else:
                    print(check(numbers))


variables = dict()
if __name__ == '__main__':
    main()