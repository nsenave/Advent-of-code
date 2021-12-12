import unittest

with open('math.txt', 'r') as inputfile :
    lines = inputfile.readlines()



def eval_simple_expr(string_expr) :
    expr = string_expr.split(' ')
    #
    last_number = int(expr[0])
    res = last_number
    #
    for c in expr[1:] :
        if c == '+' :
            last_operator = '+'
        elif c == '*' :
            last_operator = '*'
        else :
            last_number = int(c)
            if last_operator == '+' :
                res += last_number
            elif last_operator == '*' :
                res *= last_number
    #
    return res

def resolve_expr(eval_simple_function, string_expr) :

    def g(string_expr) :
        return resolve_expr(eval_simple_function, string_expr)
    
    if '(' not in string_expr :
        return str(eval_simple_function(string_expr))
    else :
        k = 0
        while string_expr[k] != '(' :
            k += 1
        k0 = k
        nb_parentheses = 0
        fin_parent = False
        while k < len(string_expr) and not fin_parent :
            if string_expr[k] == '(' :
                nb_parentheses += 1
            if string_expr[k] == ')' :
                nb_parentheses -= 1
                if nb_parentheses == 0 :
                    fin_parent = True
            k += 1
        k1 = k
        
        return g( string_expr[:k0] + g(string_expr[k0+1:k1-1]) + string_expr[k1:] )

def eval_expr(string_expr) :
    return int(resolve_expr(eval_simple_expr, string_expr))



def eval_simple_expr2(string_expr) :
    expr = string_expr.split(' ')
    #
    stack = [int(expr.pop(0))]
    # First eval + which is prioritary
    while expr != [] :
        c = expr.pop(0)
        if c == '+' :
            stack.append(stack.pop() + int(expr.pop(0)))
        elif c == '*' :
            stack.append(c)
        else :
            stack.append(int(c))
    # Then *
    res = 1
    for k in range(0, len(stack), 2) :
        res *= stack[k]
    #
    return res

def eval_expr2(string_expr) :
    return int(resolve_expr(eval_simple_expr2, string_expr))



class EvalTests(unittest.TestCase) :

    expressions = [
        '1 + 2 * 3 + 4 * 5 + 6',
        '1 + (2 * 3) + (4 * (5 + 6))',
        '2 * 3 + (4 * 5)',
        '5 + (8 * 3 + 9 + 3 * 4 * 3)', 
        '5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))',
        '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'
    ]

    results1 = [71, 51, 26, 437, 12240, 13632]
    results2 = [231, 51, 46, 1445, 669060, 23340]

    def test_eval_simple_expr(self) :
        self.assertEqual(eval_simple_expr('1 + 1'), 2)
        self.assertEqual(eval_simple_expr('2 * 1'), 2)
        self.assertEqual(eval_simple_expr('6 * 7'), 42)
        self.assertEqual(eval_simple_expr('1 + 2 * 3 + 4 * 5 + 6'), 71)

    def test_eval_expr(self):
        for k in range(len(EvalTests.expressions)) :
            e, r = EvalTests.expressions[k], EvalTests.results1[k]
            self.assertEqual(eval_expr(e), r)
    
    def test_eval_simple2(self) :
        self.assertEqual(eval_simple_expr2('1 + 2 * 3'), 9)
        self.assertEqual(eval_simple_expr2('1 * 2 + 3'), 5)
        self.assertEqual(eval_simple_expr2('1 + 2 * 3 + 4 * 5 + 6'), 231)
    
    def test_eval_expr2(self):
        for k in range(len(EvalTests.expressions)) :
            e, r = EvalTests.expressions[k], EvalTests.results2[k]
            self.assertEqual(eval_expr2(e), r)



if __name__ == "__main__":

    unittest.main(exit=False)

    print(f"Result part one: {sum(list(map(eval_expr, lines)))}")
    print(f"Result part two: {sum(list(map(eval_expr2, lines)))}")
