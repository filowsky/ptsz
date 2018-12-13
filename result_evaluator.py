class ResultEvaluator:
  # task_set [[_, _, _], [_, _, _]] -> total_time integer
  @staticmethod
  def call(set):
    total_time = sum(item[0] for item in set)
    due_date = floor(h * total_time)
    current_time = 0
    total_penelty = 0
    for [len, early, late] in set:
      current_time += len
      if current_time < due_date:
        total_penelty += early * (due_date - current_time)
      else:
        total_penelty += late * (current_time - due_date)
    return total_penelty
