from cvxpy.expressions.variables import Variable
from cvxpy.expressions.constants import Constant


# TODO this assumes all possible constraint sets are cones:
def canonicalize_constr(constr, canon_methods):
    arg_exprs = []
    constrs = []
    for a in constr.args:
        e, c = canonicalize_tree(a, canon_methods)
        constrs += c
        arg_exprs += [e]
    # Feed the linear expressions into a constraint of the same type (assumed a cone):
    constr = type(constr)(*arg_exprs)
    return constr, constrs


def canonicalize_tree(expr, canon_methods):
    canon_args = []
    constrs = []
    for arg in expr.args:
        canon_arg, c = canonicalize_tree(arg, canon_methods)
        canon_args += [canon_arg]
        constrs += c
    canon_expr, c = canonicalize_expr(expr, canon_args, canon_methods)
    constrs += c
    return canon_expr, constrs


def canonicalize_expr(expr, args, canon_methods):
    if isinstance(expr, Variable):
        return expr, []
    elif isinstance(expr, Constant):
        return expr, []
    elif expr.is_atom_convex() and expr.is_atom_concave():
        try:
            expr = type(expr)(*args)
        except TypeError: # Probably AddExpression
            expr = type(expr)(args)
        return expr, []
    else:
        return canon_methods[type(expr)](expr, args)
