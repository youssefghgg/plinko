class MathFunctions:
    """Class containing mathematical function implementations using Taylor series"""

    def __init__(self):
        self.PI = 3.14159265359
        self.E = 2.71828182846

    def _factorial(self, n):
        """Calculate factorial of n"""
        if n == 0:
            return 1
        result = 1
        for i in range(1, n + 1):
            result *= i
        return result

    def _power(self, x, n):
        """Calculate x raised to power n"""
        if n == 0:
            return 1
        if isinstance(n, float):
            if n == 0.5:  # Square root
                return self._sqrt(x)
            # For other fractional powers, use exp and ln
            return self.exp(n * self.ln(x))

        # Fix: Handle negative numbers properly
        if x == 0 and n < 0:
            raise ValueError("Cannot divide by zero (negative power with zero base)")

        result = 1
        abs_n = abs(n)
        for _ in range(abs_n):
            result *= x
        return result if n > 0 else 1 / result

    def _sqrt(self, x):
        """Calculate square root using Newton's method"""
        if x < 0:
            raise ValueError("Cannot calculate square root of negative number")
        if x == 0:
            return 0

        guess = x / 2
        for _ in range(10):  # 10 iterations for good precision
            guess = (guess + x / guess) / 2
        return guess

    def sin(self, x):
        """Calculate sine using Taylor series"""
        # Normalize x to be between -2π and 2π
        x = x % (2 * self.PI)
        result = 0
        # Fix: Increase terms for better precision
        for n in range(15):  # Using 15 terms for better precision
            term = (-1) ** n * self._power(x, 2 * n + 1) / self._factorial(2 * n + 1)
            # Fix: Add precision check
            if abs(term) < 1e-15:  # Stop if term becomes negligible
                break
            result += term
        return result

    def cos(self, x):
        """Calculate cosine using Taylor series"""
        # Normalize x to be between -2π and 2π
        x = x % (2 * self.PI)
        result = 0
        for n in range(10):  # Using 10 terms for good precision
            term = (-1) ** n * self._power(x, 2 * n) / self._factorial(2 * n)
            result += term
        return result

    def tan(self, x):
        """Calculate tangent"""
        cos_x = self.cos(x)
        if abs(cos_x) < 1e-10:
            raise ValueError("Tangent undefined at this point")
        return self.sin(x) / cos_x

    def exp(self, x):
        """Calculate e^x using Taylor series"""
        result = 0
        for n in range(20):  # Using 20 terms for good precision
            result += self._power(x, n) / self._factorial(n)
        return result

    def ln(self, x):
        """Calculate natural logarithm using Taylor series"""
        if x <= 0:
            raise ValueError("Logarithm undefined for non-positive numbers")

        # Use the formula ln(x) = ln((1+y)/(1-y)) = 2*arctanh(y)
        # where y = (x-1)/(x+1)
        y = (x - 1) / (x + 1)
        result = 0
        for n in range(20):  # Using 20 terms
            result += 2 * self._power(y, 2 * n + 1) / (2 * n + 1)
        return result


class Node:
    """Node class for expression tree"""

    def __init__(self, type, value, left=None, right=None):
        self.type = type  # 'number', 'variable', 'operator', 'function'
        self.value = value  # actual value/operator/function name
        self.left = left  # left child
        self.right = right  # right child


class DerivativeCalculator:
    def __init__(self):
        self.math = MathFunctions()
        self.precedence = {
            '+': 1, '-': 1,
            '*': 2, '/': 2,
            '^': 3
        }

    def _tokenize(self, expression):
        """Convert expression string into tokens"""
        tokens = []
        current = ""
        operators = {'+', '-', '*', '/', '^', '(', ')'}

        i = 0
        while i < len(expression):
            char = expression[i]

            if char.isspace():
                i += 1
                continue

            # Special handling for 'e' as Euler's number
            if char == 'e' and (i + 1 < len(expression) and expression[i + 1] == '^'):
                tokens.append(str(self.math.E))  # Add e as its numerical value
                i += 1
                continue

            if char in operators:
                if current:
                    tokens.append(current)
                    current = ""
                tokens.append(char)
                i += 1
                continue

            if char.isalnum() or char == '.':
                current += char
                i += 1
                continue

            if char.isalpha():
                func = char
                j = i + 1
                while j < len(expression) and expression[j].isalpha():
                    func += expression[j]
                    j += 1
                if func in {'sin', 'cos', 'tan', 'ln', 'log', 'exp'}:
                    tokens.append(func)
                    i = j
                    continue
                elif func == 'e':  # Handle standalone 'e'
                    tokens.append(str(self.math.E))
                    i = j
                    continue

            i += 1

        if current:
            tokens.append(current)

        return tokens

    def _parse(self, tokens):
        """Parse tokens into an expression tree using Shunting Yard algorithm"""
        output = []
        operators = []

        for token in tokens:
            if token.replace('.', '').isdigit() or token == str(self.math.E):
                # Convert e to its numerical value if it's Euler's number
                value = float(token)
                output.append(Node('number', value))
            elif token == 'x':
                output.append(Node('variable', 'x'))
            elif token in {'sin', 'cos', 'tan', 'ln', 'log', 'exp'}:
                operators.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    self._process_operator(operators, output)
                if operators:
                    operators.pop()  # Remove '('
                if operators and operators[-1] in {'sin', 'cos', 'tan', 'ln', 'log', 'exp'}:
                    func = operators.pop()
                    if output:  # Add this check
                        arg = output.pop()
                        output.append(Node('function', func, arg))
            elif token in self.precedence:
                while (operators and operators[-1] != '(' and
                       operators[-1] not in {'sin', 'cos', 'tan', 'ln', 'log', 'exp'} and
                       self.precedence[operators[-1]] >= self.precedence[token]):
                    self._process_operator(operators, output)
                operators.append(token)

        while operators:
            self._process_operator(operators, output)

        return output[0] if output else None

    def _process_operator(self, operators, output):
        """Helper function for parsing"""
        op = operators.pop()
        if op in {'sin', 'cos', 'tan', 'ln', 'log', 'exp'}:
            arg = output.pop()
            output.append(Node('function', op, arg))
        else:
            right = output.pop()
            left = output.pop()
            output.append(Node('operator', op, left, right))

    def differentiate(self, node):
        if not node:
            return None

        if node.type == 'number':
            return Node('number', 0)

        if node.type == 'variable':
            return Node('number', 1)

        if node.type == 'operator':
            # Fix: Handle division by zero cases
            if node.value == '/':
                denominator = node.right
                if denominator.type == 'number' and denominator.value == 0:
                    raise ValueError("Division by zero in derivative")
        """Calculate the derivative of the expression tree"""
        if not node:
            return None

        if node.type == 'number':
            return Node('number', 0)

        if node.type == 'variable':
            return Node('number', 1)

        if node.type == 'operator':
            if node.value in {'+', '-'}:
                return Node('operator', node.value,
                            self.differentiate(node.left),
                            self.differentiate(node.right))

            if node.value == '*':  # Product rule
                return Node('operator', '+',
                            Node('operator', '*',
                                 self.differentiate(node.left),
                                 node.right),
                            Node('operator', '*',
                                 node.left,
                                 self.differentiate(node.right)))

            if node.value == '/':  # Quotient rule
                return Node('operator', '/',
                            Node('operator', '-',
                                 Node('operator', '*',
                                      self.differentiate(node.left),
                                      node.right),
                                 Node('operator', '*',
                                      node.left,
                                      self.differentiate(node.right))),
                            Node('operator', '^',
                                 node.right,
                                 Node('number', 2)))

            if node.value == '^':  # Power rule and chain rule
                if node.right.type == 'number':  # Simple power rule
                    power = node.right.value
                    return Node('operator', '*',
                                Node('number', power),
                                Node('operator', '^',
                                     node.left,
                                     Node('number', power - 1)))
                else:  # General case: d/dx(u^v) = u^v * (v*ln(u))′
                    return Node('operator', '*',
                                node,
                                Node('operator', '+',
                                     Node('operator', '*',
                                          node.right,
                                          Node('operator', '/',
                                               self.differentiate(node.left),
                                               node.left)),
                                     Node('operator', '*',
                                          Node('function', 'ln', node.left),
                                          self.differentiate(node.right))))

        if node.type == 'function':
            # Chain rule: d/dx(f(g(x))) = f'(g(x)) * g'(x)
            if node.value == 'sin':
                return Node('operator', '*',
                            Node('function', 'cos', node.left),
                            self.differentiate(node.left))
            elif node.value == 'cos':
                return Node('operator', '*',
                            Node('operator', '*',
                                 Node('number', -1),
                                 Node('function', 'sin', node.left)),
                            self.differentiate(node.left))
            elif node.value == 'tan':
                return Node('operator', '*',
                            Node('operator', '^',
                                 Node('function', 'sec', node.left),
                                 Node('number', 2)),
                            self.differentiate(node.left))
            elif node.value in {'ln', 'log'}:
                return Node('operator', '*',
                            Node('operator', '/',
                                 Node('number', 1),
                                 node.left),
                            self.differentiate(node.left))
            elif node.value == 'exp':
                return Node('operator', '*',
                            Node('function', 'exp', node.left),
                            self.differentiate(node.left))

        return Node('number', 0)

    def _simplify(self, node):
        """Simplify the expression tree"""
        if not node:
            return None

        # Recursively simplify children
        if node.left:
            node.left = self._simplify(node.left)
        if node.right:
            node.right = self._simplify(node.right)

        # Basic arithmetic simplifications
        if node.type == 'operator':
            # Multiplication by 0
            if node.value == '*' and (
                    (node.left.type == 'number' and node.left.value == 0) or
                    (node.right.type == 'number' and node.right.value == 0)):
                return Node('number', 0)

            # Multiplication by 1
            if node.value == '*' and node.left.type == 'number' and node.left.value == 1:
                return node.right
            if node.value == '*' and node.right.type == 'number' and node.right.value == 1:
                return node.left

            # Addition/subtraction with 0
            if node.value in {'+', '-'} and node.right.type == 'number' and node.right.value == 0:
                return node.left

            # Power of 1
            if node.value == '^' and node.right.type == 'number' and node.right.value == 1:
                return node.left

            # Power of 0
            if node.value == '^' and node.right.type == 'number' and node.right.value == 0:
                return Node('number', 1)

        return node

    def _to_string(self, node):
        """Convert expression tree to string"""
        if not node:
            return ""

        if node.type == 'number':
            return str(float(node.value)) if float(node.value).is_integer() else f"{node.value:.3f}"

        if node.type == 'variable':
            return node.value

        if node.type == 'function':
            return f"{node.value}({self._to_string(node.left)})"

        if node.type == 'operator':
            left = self._to_string(node.left)
            right = self._to_string(node.right)

            if node.value in {'+', '-'}:
                return f"{left} {node.value} {right}"
            elif node.value in {'*', '/'}:
                # Add parentheses for proper precedence
                if node.left.type == 'operator' and node.left.value in {'+', '-'}:
                    left = f"({left})"
                if node.right.type == 'operator' and node.right.value in {'+', '-'}:
                    right = f"({right})"
                return f"{left}{node.value}{right}"
            else:  # power
                if node.left.type == 'operator':
                    left = f"({left})"
                if node.right.type == 'operator':
                    right = f"({right})"
                return f"{left}^{right}"


def main():
    calc = DerivativeCalculator()

    print("\nDerivative Calculator (No Imports)")
    print("==================================")
    print("Supported functions:")
    print("  - Basic: +, -, *, /, ^")
    print("  - Constants: e (Euler's number)")
    print("  - Trig: sin(x), cos(x), tan(x)")
    print("  - Exp/Log: exp(x), ln(x)")
    print("  - Composition: sin(x^2), ln(x^3), e^x")
    print("Enter 'quit' to exit")
    print("==================================\n")

    while True:
        try:
            expr = input("\nEnter a function: ").strip()
            if not expr:
                print("Please enter a valid expression")
                continue

            if expr.lower() == 'quit':
                break

            tokens = calc._tokenize(expr)
            if not tokens:
                print("Invalid expression: could not tokenize")
                continue

            tree = calc._parse(tokens)
            if not tree:
                print("Invalid expression: could not parse")
                continue

            derivative = calc.differentiate(tree)
            simplified = calc._simplify(derivative)
            result = calc._to_string(simplified)

            print(f"The derivative of {expr} is:")
            print(f"f'(x) = {result}")

        except IndexError:
            print("Error: Invalid expression format")
        except ValueError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"Error: {str(e)}")
            print("Please check your expression format")

def _validate_expression(self, expr):
    """Validate input expression"""
    # Check for balanced parentheses
    stack = []
    for char in expr:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                return False
            stack.pop()
    if stack:
        return False

    # Check for invalid operator sequences
    operators = {'+', '-', '*', '/', '^'}
    prev_char = None
    for char in expr:
        if char in operators and prev_char in operators:
            return False
        prev_char = char

    return True

if __name__ == "__main__":
    main()