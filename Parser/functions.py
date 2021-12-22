import random
import math
from Lexer.tokens import *
import Parser.nodes as nodes


def params_to_string(params, environment):
    return "".join(
        str(param.eval(environment)) for param in flatten_list(params, environment)
    )


def handle_sqrt(node, environment):
    root = 2
    if len(node.configurations) > 0:
        root = node.configurations[0].eval(environment)
    return nodes.IntNode(
        nodes.format_result(node.parameters[0].eval(environment) ** (1 / root))
    )


def handle_print(node, environment):
    string = params_to_string(node.parameters, environment)
    print(string)
    return nodes.StringNode(string)


def handle_input(node, environment):
    string = params_to_string(node.parameters, environment)
    return nodes.StringNode(input(string))


def handle_int_input(node, environment):
    string = params_to_string(node.parameters, environment)
    return nodes.IntNode(nodes.format_float(float(input(string))))


def handle_random(node, environment):
    if len(node.configurations) < 1:
        if len(node.parameters) >= 1:
            n = node.parameters[0].eval(environment)
            return nodes.ArrayNode(
                [nodes.IntNode(nodes.format_result(random.random())) for _ in range(n)]
            )
        return nodes.IntNode(nodes.format_result(random.random()))

    if len(node.configurations) > 1:
        min_value = node.configurations[0].eval(environment)
        max_value = node.configurations[1].eval(environment)
    else:
        max_value = node.configurations[0].eval(environment)
        min_value = 0

    if len(node.parameters) >= 1:
        n = node.parameters[0].eval(environment)
        return nodes.ArrayNode(
            [nodes.IntNode(random.randint(min_value, max_value)) for _ in range(n)]
        )
    else:
        return nodes.IntNode(random.randint(min_value, max_value))


def handle_sum(node, environment):
    array = nodes.ArrayNode(flatten_list(node.parameters, environment)).eval(
        environment
    )
    print(array)


def handle_frac(node, environment):
    if len(node.parameters) < 2:
        return nodes.ErrorNode("FRAC takes at least 2 parameters")

    op_node = nodes.BinOpNode(node.parameters[0], "DIV", node.parameters[1])
    return nodes.IntNode(nodes.eval_base(op_node, environment))


def handle_join(node, environment):
    if len(node.configurations) < 1:
        string = ","
    else:
        string = params_to_string(node.configurations, environment)

    array = flatten_list(node.parameters, environment)
    return nodes.StringNode(
        string.join([str(param.eval(environment)) for param in array])
    )


def flatten_list(array, environment):
    if isinstance(array, list):
        flattened_array = []
        for item in array:
            flattened_array += flatten_list(item, environment)
        return flattened_array

    elif array.type in (INT_NODE, STRING_NODE):
        return [array]

    elif array.type == ARRAY_NODE:
        return flatten_list(array.nodes, environment)

    elif array.type == FUNCTION_CALL_NODE:
        return flatten_list(array.eval(environment), environment)

    if array.type == ARRAY_NODE:
        return flatten_list(array.nodes, environment)

    elif array.type == VAR_ACCESS_NODE:
        return flatten_list(
            flatten_list(environment.variables[array.identifier], environment),
            environment,
        )
