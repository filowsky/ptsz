from data_loader import DataLoader
from itertools import permutations

class FullSwitchSet:
  @staticmethod
  def call(set, h):
    total_time = sum(x[0] for x in set)
    due_date = int(h * total_time)
    return min([
      (FullSwitchSet.eval_result(perm, due_date), perm) for perm in permutations(set)
    ])

  @staticmethod
  def eval_result(set, due_date):
    current_time = 0
    total_penelty = 0
    for [len, early, late] in set:
      current_time += len
      if current_time < due_date:
        total_penelty += early * (due_date - current_time)
      else:
        total_penelty += late * (current_time - due_date)
    return total_penelty
