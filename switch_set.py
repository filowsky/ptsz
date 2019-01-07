from itertools import permutations
from random import random, randint
from result_evaluator import ResultEvaluator

class SwitchSet:
  @staticmethod
  def call(set, due_date, mutation_factor, iters):
    if iters == 1:
      set = SwitchSet.perform_iteration(set, due_date, mutation_factor)
    else:
      for i in range(iters):
        set = SwitchSet.perform_iteration(set, due_date, mutation_factor)
      for i in range(iters):
        set = SwitchSet.perform_iteration(set, due_date, 0)

    return (ResultEvaluator.call_with_dd(set, due_date), set)


  @staticmethod
  def perform_iteration(set, due_date, mutation_factor):
    copy = [item[:] for item in set]

    if random() < mutation_factor:
      idx = randint(0, len(copy) - 1)
      idx2 = randint(0, len(copy) - 1)
      copy[idx], copy[idx2] = copy[idx2], copy[idx]

    current_time = 0
    for idx in range(len(copy) - 1):
      pen_without_swap = SwitchSet.eval_penelty_for_two(copy[idx], copy[idx+1], current_time, due_date)
      pen_with_swap = SwitchSet.eval_penelty_for_two(copy[idx+1], copy[idx], current_time, due_date)
      copy[idx], copy[idx+1] = copy[idx+1], copy[idx]

      if pen_with_swap < pen_without_swap:
        copy[idx], copy[idx+1] = copy[idx+1], copy[idx]

      current_time += set[idx][0]

    return copy


  @staticmethod
  def eval_penelty_for_two(item_left, item_right, current_time, due_date):
    penelty = 0
    for item in [item_left, item_right]:
      current_time += item[0]
      if current_time < due_date:
        penelty += item[1] * (due_date - current_time)
      else:
        penelty += item[2] * (current_time - due_date)
    return penelty
