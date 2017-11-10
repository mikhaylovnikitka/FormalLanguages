import unittest
import copy

class BadInputException(Exception):
    def __init__(self, message_):
        Exception.__init__(self)
        self.message = message_


class TestForProblem(unittest.TestCase):
    def test_bad_input(self):
        with self.assertRaises(BadInputException):
            test("a+*", "aaba")
            test("a+*2z", "aaba")

    def test_my(self):
        self.assertEqual(test("ab+*", "aaba"), True)
        self.assertEqual(test("ab+*", "1"), True)
        self.assertEqual(test("a*b+", "b"), True)
        self.assertEqual(test("abc..", "abc"), True)
        self.assertEqual(test("1111", "1"), True)
        self.assertEqual(test("ab.bb.a.+ab.c.*.", "cabc"), False)
        self.assertEqual(test("ab.bb.a.+ab.c.*.", "ababcabc"), True)
        self.assertEqual(test("ab.bb.a.+ab.c.*.", "bbaabc"), True)
        self.assertEqual(test("aab.a.*.aab.+*.ba.1+.", "aababbb"), False)
        self.assertEqual(test("aab.a.*.aab.+*.ba.1+.", "aabaaaaba"), True)
        self.assertEqual(test("aab.a.*.aab.+*.ba.1+.", "a"), True)

    def tests_from_condition(self):
        self.assertEqual(test("aab.a.*.aab.+*.ba.1+.", "aabaabab"), True)
        self.assertEqual(test("bba.ab.+*b..*", "babaabbab"), False)


def epsilon_accounting(n, m):
    matrix = [['-'] * m for i in range(n)]
    for i in range(m):
        matrix[0][i] = '+'
    return matrix


def pre_accounting(char, word, n, m):
    matrix = [['-'] * m for i in range(n)]
    for i in range(m):
        if word[i] == char:
            matrix[1][i] = '+'
    return matrix


def star_accounting(current, n, m):
    matrix = copy.deepcopy(current);
    for i in range(m):
        matrix[0][i] = '+'
    for i in range(1, n):
        for j in range(m):
            if matrix[i][j] == '+':
                if i + j < m:
                    for second_i in range(n):
                        if matrix[second_i][i + j] == '+' and second_i + i < n:
                            matrix[second_i + i][j] = '+'
    return matrix


def concat_accounting(first, second, n, m):
    matrix = [['-'] * m for i in range(n)]
    for i in range(n):
        for j in range(m):
            if first[i][j] == '+':
                if i + j < m:
                    for second_i in range(n):
                        if second[second_i][i + j] == '+' and second_i + i < n:
                            matrix[second_i + i][j] = '+'
            if second[0][0] == '+' and first[n-1][0] == '+':
                matrix[n-1][0] = '+'
    return matrix


def plus_accounting(first, second, n, m):
    matrix = copy.deepcopy(first);
    for i in range(n):
        for j in range(m):
            if second[i][j] == '+':
                matrix[i][j] = '+'
    return matrix

def test(expression, word):
    n = len(word) + 1
    m = len(word)
    a_matrix = pre_accounting("a", word, n, m)
    b_matrix = pre_accounting("b", word, n, m)
    c_matrix = pre_accounting("c", word, n, m)
    epsilon_matrix = epsilon_accounting(n, m)
    stack = []
    for char in expression:
        if char == '.':
            if len(stack) < 2:
                raise BadInputException("Невозможно выполнить операцию .")
            second = stack.pop()
            first = stack.pop()
            to_push = concat_accounting(first, second, n, m)
            stack.append(to_push)
            continue
        if char == '+':
            if len(stack) < 2:
                raise BadInputException("Невозможно выполнить операцию +")
            second = stack.pop()
            first = stack.pop()
            to_push = plus_accounting(first, second, n, m)
            stack.append(to_push)
            continue
        if char == '*':
            if len(stack) == 0:
                raise BadInputException("Невозможно выполнить операцию *")
            first = stack.pop()
            to_push = star_accounting(first, n, m)
            stack.append(to_push)
            continue
        if char == 'a':
            stack.append(a_matrix)
            continue
        if char == 'b':
            stack.append(b_matrix)
            continue
        if char == 'c':
            stack.append(c_matrix)
            continue
        if char == '1':
            stack.append(epsilon_matrix)
            continue
        raise BadInputException("В выражении присутсвуют недопустимые символы")
    if len(stack) == 0:
        raise BadInputException("Невозможно выдать ответ")
    answer = stack.pop()
    if word == '1':
        if answer[0][0] == '+':
            return True
        else:
            return False
    if answer[-1][0] == '+':
        return True
    else:
        return False


def read_from_file():
    fin = open("input.txt", 'r')
    regular_expression, word = fin.readline().split()
    print(regular_expression, word)
    print(test(regular_expression, word))
    fin.close()

if __name__ == '__main__':
    unittest.main()
    #read_from_file()
