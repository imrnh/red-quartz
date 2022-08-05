# Example expression: (((unit_completed / allocated_unit) * allocated_point) * 0.8 - 5)

# db te time_completed, allocated_time, allocted_point ei 3 ta variable int akare save thakbe.
# function e paramemter akare pass korle eval function string e oi nam gulo pele erpor variable dhore kaj kore.

def decode_reward_expression(working_expression: str, unit_completed: int, allocated_unit: int, allocated_point: int):
    evaluated_value = eval(working_expression)
    return "{:.2f}".format(evaluated_value) if evaluated_value > 0 else 0


# Example expression: ((extra_units/3)*5)*.9

def extra_units_reward_eval(working_expression: str, extra_units: int):
    evaluated_value = eval(working_expression)
    return "{:.2f}".format(evaluated_value) if evaluated_value > 0 else 0


def negative_points(working_expression: str , neg_units: int):
    evaluated_value = eval(working_expression)
    return "{:.2f}".format(evaluated_value) if evaluated_value > 0 else 0

# print(decode_reward_expression("(((unit_completed / allocated_unit) * allocated_point) * .8 - 5)", 20, 40, 530)) --> 207

# print(over_unit_reward_eval("((extra_units/3)*5)*.9", 30)) --> 45