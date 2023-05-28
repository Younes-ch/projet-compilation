import unittest
from main import tokenize, check_order

class TestTokenize(unittest.TestCase):
    def test_valid_string(self):
        string = 'sin(3.14)+cos(2*pi)'
        tokens = tokenize(string)
        expected_tokens = [
            ('KEYWORD', 'sin'),
            ('LEFT_PARENTHESIS', '('),
            ('NUMBER', '3.14'),
            ('RIGHT_PARENTHESIS', ')'),
            ('OPERATOR', '+'),
            ('KEYWORD', 'cos'),
            ('LEFT_PARENTHESIS', '('),
            ('NUMBER', '2'),
            ('OPERATOR', '*'),
            ('PI', 'pi'),
            ('RIGHT_PARENTHESIS', ')'),
        ]
        self.assertEqual(tokens, expected_tokens)

    def test_invalid_string(self):
        string = 'sin(3.14)+$cos(2*pi)'
        with self.assertRaises(ValueError):
            tokenize(string)

    def test_valid_string_with_spaces(self):
        string = 'sin ( 3.14 ) + cos ( 2 * pi )'
        tokens = tokenize(string)
        expected_tokens = [
            ('KEYWORD', 'sin'),
            ('LEFT_PARENTHESIS', '('),
            ('NUMBER', '3.14'),
            ('RIGHT_PARENTHESIS', ')'),
            ('OPERATOR', '+'),
            ('KEYWORD', 'cos'),
            ('LEFT_PARENTHESIS', '('),
            ('NUMBER', '2'),
            ('OPERATOR', '*'),
            ('PI', 'pi'),
            ('RIGHT_PARENTHESIS', ')'),
        ]
        self.assertEqual(tokens, expected_tokens)

    def test_valid_string_with_unsupported_keyword(self):
        string = 'tan(3.14) + cos(2*pi)'
        tokens = tokenize(string)
        expected_tokens = [
            ('KEYWORD', 'tan'),
            ('LEFT_PARENTHESIS', '('),
            ('NUMBER', '3.14'),
            ('RIGHT_PARENTHESIS', ')'),
            ('OPERATOR', '+'),
            ('KEYWORD', 'cos'),
            ('LEFT_PARENTHESIS', '('),
            ('NUMBER', '2'),
            ('OPERATOR', '*'),
            ('PI', 'pi'),
            ('RIGHT_PARENTHESIS', ')'),
        ]
        self.assertEqual(tokens, expected_tokens)


class TestCheckOrder(unittest.TestCase):
    def test_invalid_order_with_missing_operand(self):
        tokens = [
            ('NUMBER', '2'),
            ('OPERATOR', '+'),
        ]
        self.assertFalse(check_order(tokens))

    def test_invalid_order_with_missing_operator(self):
        tokens = [
            ('NUMBER', '2'),
            ('NUMBER', '3'),
        ]
        self.assertFalse(check_order(tokens))

    def test_invalid_order_with_missing_left_parenthesis(self):
        tokens = [
            ('KEYWORD', 'sin'),
            ('NUMBER', '3.14'),
            ('RIGHT_PARENTHESIS', ')'),
        ]
        self.assertFalse(check_order(tokens))

    def test_invalid_order_with_missing_right_parenthesis(self):
        tokens = [
            ('KEYWORD', 'sin'),
            ('LEFT_PARENTHESIS', '('),
            ('NUMBER', '3.14'),
        ]
        self.assertFalse(check_order(tokens))

    def test_valid_order(self):
        tokens = [
            ('KEYWORD', 'sin'),
            ('LEFT_PARENTHESIS', '('),
            ('NUMBER', '3.14'),
            ('RIGHT_PARENTHESIS', ')'),
            ('OPERATOR', '+'),
            ('KEYWORD', 'cos'),
            ('LEFT_PARENTHESIS', '('),
            ('NUMBER', '2'),
            ('OPERATOR', '*'),
            ('PI', 'pi'),
            ('RIGHT_PARENTHESIS', ')'),
        ]
        self.assertTrue(check_order(tokens))

    def test_invalid_order(self):
        tokens = [
            ('KEYWORD', 'sin'),
            ('NUMBER', '3.14'),
            ('OPERATOR', '+'),
            ('KEYWORD', 'cos'),
            ('LEFT_PARENTHESIS', '('),
            ('NUMBER', '2'),
            ('OPERATOR', '*'),
            ('PI', 'pi'),
            ('RIGHT_PARENTHESIS', ')'),
        ]
        self.assertFalse(check_order(tokens))

    def test_invalid_parenthesis_count(self):
        tokens = [
            ('KEYWORD', 'sin'),
            ('LEFT_PARENTHESIS', '('),
            ('NUMBER', '3.14'),
            ('RIGHT_PARENTHESIS', ')'),
            ('OPERATOR', '+'),
            ('KEYWORD', 'cos'),
            ('LEFT_PARENTHESIS', '('),
            ('NUMBER', '2'),
            ('OPERATOR', '*'),
            ('PI', 'pi'),
        ]
        self.assertFalse(check_order(tokens))

if __name__ == '__main__':
    unittest.main()
