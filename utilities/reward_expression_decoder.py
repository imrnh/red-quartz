# Example expression: (((time_completed / allocated_time) * allocated_point) * 80% - 5)

# db te time_completed, allocated_time, allocted_point ei 3 ta variable string akare save thakbe. 
# python e ese replace kore amra baki kaj korbo.

def decode_reward_expression(workingexpression : str, time_cmpltd: int, alloc_time : int, alloc_point : int):
   
    if "time_completed" in workingexpression:
        workingexpression = workingexpression.replace("time_completed", str(time_cmpltd))
    if "allocated_time" in workingexpression:
        workingexpression = workingexpression.replace("allocated_time", str(alloc_time))
    if "allocated_point" in workingexpression:
        workingexpression = workingexpression.replace("allocated_point", str(alloc_point))
    
    evaluatedValue = eval(workingexpression)
    return "{:.2f}".format(evaluatedValue) if evaluatedValue > 0 else 0

    

print(decode_reward_expression("((50 / allocated_time) * allocated_point) * 0.97 - 2", 30, 60, 20))