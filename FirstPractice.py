import unittest


class TestUM(unittest.TestCase):
    def test_my(self):
        self.assertEqual(test("ab+*", "aaba"), True)
        self.assertEqual(test("a*b+", "b"), True)
        self.assertEqual(test("abc..", "abc"), True)

    def tests_from_condition(self):
        self.assertEqual(test("aab.a. ∗ .aab.+∗.ba.1+.", "aabaabab"), True)
        self.assertEqual(test("bba.ab.+∗b..∗", "babaabbab"), False)


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


def star_accounting(matrix, n, m):
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
    return matrix


def plus_accounting(first, second, n, m):
    for i in range(n):
        for j in range(m):
            if second[i][j] == '+':
                first[i][j] = '+'
    return first


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
            second = stack.pop()
            first = stack.pop()
            to_push = concat_accounting(first, second, n, m)
            #print('first', first)
            #print('second', second)
            #print('dot', to_push)
            stack.append(to_push)
        if char == '+':
            second = stack.pop()
            first = stack.pop()
            to_push = plus_accounting(first, second, n, m)
            #print('first', first)
            #print('second', second)
            #print('plus', to_push)
            stack.append(to_push)
        if char == '*':
            first = stack.pop()
            #print('first', first)
            to_push = star_accounting(first, n, m)
            #print('star', to_push)
            stack.append(to_push)
        if char == 'a':
            stack.append(a_matrix)
        if char == 'b':
            stack.append(b_matrix)
        if char == 'c':
            stack.append(c_matrix)
        if char == '1':
            stack.append(epsilon_matrix)
    answer = stack.pop()
    if word == '1':
        if answer[0][0] == '+':
            return True
        else:
            return False
        return
    if answer[-1][0] == '+':
        return True
    else:
        return False


def read_from_file():
    fin = open("input.txt", 'r')
    regular_expression, word = fin.readline().split()
    print(regular_expression, word)
    print(test(regular_expression, word))

if __name__ == '__main__':
    unittest.main()
