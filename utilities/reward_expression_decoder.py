# Example expression: (((unit_completed / allocated_unit) * allocated_point) * 0.8 - 5)

# db te time_completed, allocated_time, allocted_point ei 3 ta variable string akare save thakbe. 
# python e ese replace kore amra baki kaj korbo.

def decode_reward_expression(working_expression: str, unit_completed: int, allocated_unit: int, allocated_point: int):
   
    if "unit_completed" in working_expression:
        working_expression = working_expression.replace("unit_completed", str(unit_completed))
    if "allocated_unit" in working_expression:
        working_expression = working_expression.replace("allocated_unit", str(allocated_unit))
    if "allocated_point" in working_expression:
        working_expression = working_expression.replace("allocated_point", str(allocated_point))

    print(working_expression)

    evaluated_value = eval(working_expression)
    return "{:.2f}".format(evaluated_value) if evaluated_value > 0 else 0



print(decode_reward_expression("(((unit_completed / allocated_unit) * allocated_point) * .8 - 5)", 20, 40, 530))