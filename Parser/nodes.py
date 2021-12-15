from Lexer.tokens import *
from Parser.functions import *
import inspect


class ProgramNode:
    def __init__(self, expressions):
        self.type = PROGRAM_NODE
        self.expressions = expressions

    def eval(self, environment, display=False):
        for expr in self.expressions:
            result = eval_base(expr, environment)

            if isinstance(result, ErrorNode):
                return result.eval(environment)

            if display:
                print(result)

    def __repr__(self):
        return "PROGRAM_NODE:" + ",".join(str(exp) for exp in self.expressions)


class VarAssignNode:
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression
        self.type = VAR_ASSIGN_NODE

    def eval(self, environment):
        result = eval_base(self.expression)
        environment.variables[self.identifier] = result
        return result

    def __repr__(self):
        return (
            "VAR_ACCESS:"
            + self.identifier.__repr__()
            + "="
            + self.expression.__repr__()
        )


class ArrayNode:
    def __init__(self, nodes):
        self.type = ARRAY_NODE
        self.nodes = nodes

    def eval(self, environment):
        array = []
        for node in self.nodes:
            array.append(node.eval(environment))
        return array

    def __repr__(self):
        return "ARRAY NODE:" + "[" + ",".join(str(exp) for exp in self.nodes) + "]"


class BinOpNode:
    def __init__(self, left, op, right):
        self.type = BIN_OP_NODE
        self.left = left
        self.op = op
        self.right = right

    def eval(self, environment):
        left = eval_base(self.left, environment)
        right = eval_base(self.right, environment)

        if isinstance(left, ErrorNode):
            return left
        elif isinstance(right, ErrorNode):
            return right
        try:
            if self.op == ADD:
                return left + right
            elif self.op == SUB:
                return left - right
            elif self.op == DIV:
                return left / right
            elif self.op == MUL:
                return left * right
            elif self.op == MOD:
                return left % right
            elif self.op == POW:
                return left ** right

            elif self.op == EE:
                return 1 if left == right else 0
            elif self.op == NE:
                return 1 if left != right else 0
            elif self.op == GT:
                return 1 if left > right else 0
            elif self.op == GTE:
                return 1 if left >= right else 0
            elif self.op == LT:
                return 1 if left < right else 0
            elif self.op == LTE:
                return 1 if left <= right else 0
        except TypeError:
            return ErrorNode(
                "Binary Operation Error: "
                + str(left)
                + ":"
                + self.op
                + ":"
                + str(right)
            )

    def __repr__(self):
        return (
            "("
            + self.left.__repr__()
            + ":"
            + self.op
            + ":"
            + self.right.__repr__()
            + ")"
        )


class UnaryOpNode:
    def __init__(self, op, right):
        self.type = UNARY_OP_NODE
        self.op = op
        self.right = right

    def eval(self, environment):
        right = eval_base(self.right, environment)
        if isinstance(right, ErrorNode):
            return right
        if self.op == SUB:
            return -(right)
        elif self.op == NOT:
            return 1 if right == 0 else 0

    def __repr__(self):
        return self.op + "(" + self.right.__repr__() + ")"


class VarAccessNode:
    def __init__(self, identifier):
        self.type = VAR_ACCESS_NODE
        self.identifier = identifier

    def eval(self, environment):
        return environment.variables[self.identifier]

    def __repr__(self):
        return "VAR_ACCESS:" + self.identifier


class StringNode:
    def __init__(self, value):
        self.type = STRING_NODE
        self.value = value

    def eval(self, environment):
        return self.value

    def __repr__(self):
        return "STRING:" + self.value


class IntNode:
    def __init__(self, value):
        self.type = INT_NODE
        self.value = value

    def eval(self, environment):
        return self.value

    def __repr__(self):
        return "INT:" + str(self.value)


class ErrorNode:
    def __init__(self, message):
        self.message = message
        self.type = ERROR

    def eval(self, environment):
        if self.message != "":
            print(self.message)
        return None

    def __repr__(self):
        return "ERROR:" + self.message


class FunctionCallNode:
    def __init__(self, identifier, configurations, parameters):
        self.identifier = identifier
        self.configurations = configurations
        self.parameters = parameters
        self.type = FUNCTION_CALL_NODE

        self.functions = {
            "print": handle_print,
            "input": handle_input,
            "intInput": handle_int_input,
            "random": handle_random,
            "join": handle_join,
        }

    def __repr__(self):
        return (
            self.identifier
            + "["
            + ",".join(str(exp) for exp in self.configurations)
            + "]"
            + "{"
            + ",".join(str(exp) for exp in self.parameters)
            + "}"
        )

    def eval(self, environment):
        if self.identifier in self.functions:
            return self.functions[self.identifier](self, environment)
            # TODO CUSTOM DEFENITIONS
        else:
            return ErrorNode("Function Not Defined")


def eval_base(node, environment):
    if isinstance(node, (int, str, list, float, ErrorNode)):
        return node
    return eval_base(node.eval(environment), environment)
