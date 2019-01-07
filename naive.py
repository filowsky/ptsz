from result_evaluator import ResultEvaluator
class Naive:
  @staticmethod
  def call(set, h):
    due_date = int(sum([x[0] for x in set]) * h)
    copy = sorted(set, key=lambda t: -t[0]) #desc sort
    result = []
    rangee = range(len(copy))
    current_time = 0
    while current_time <= due_date:
      item = copy.pop(0)
      result.append(item)
      current_time += item[0]
    copy = sorted(copy, key=lambda t: t[0])
    result += copy
    return ResultEvaluator.call(result, h), result
