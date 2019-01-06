from data_loader import DataLoader
from result_evaluator import ResultEvaluator
from simple_solver import SimpleSolver
from naive import Naive
from switch_set import SwitchSet
from full_switch_set import FullSwitchSet

from random import random, choice, randint
import datetime

def eval_penelty_for_two(item_left, item_right, current_time, due_date):
  penelty = 0
  for item in [item_left, item_right]:
    current_time += item[0]
    if current_time < due_date:
      penelty += item[1] * (due_date - current_time)
    else:
      penelty += item[2] * (current_time - due_date)
  return penelty

def generate_strong_population(set, due_date, accept_max, evaluated_results):
  current_time = 0
  strong_parents = []
  parents = []

  for idx in range(len(set) - 1):
    copy = [item[:] for item in set]
    pen_without_swap = eval_penelty_for_two(copy[idx], copy[idx+1], current_time, due_date)
    pen_with_swap = eval_penelty_for_two(copy[idx+1], copy[idx], current_time, due_date)
    copy[idx], copy[idx+1] = copy[idx+1], copy[idx]

    current_time += set[idx][0]
    if copy not in evaluated_results:
      if pen_with_swap < pen_without_swap:
        strong_parents.append(copy)
        evaluated_results.append(copy)

  return strong_parents

def generate_population(set, due_date, accept_max, evaluated_results):
  current_time = 0
  strong_parents = []
  parents = []

  for idx in range(len(set) - 1):
    copy = [item[:] for item in set]
    pen_without_swap = eval_penelty_for_two(copy[idx], copy[idx+1], current_time, due_date)
    pen_with_swap = eval_penelty_for_two(copy[idx+1], copy[idx], current_time, due_date)
    copy[idx], copy[idx+1] = copy[idx+1], copy[idx]

    current_time += set[idx][0]
    if copy not in evaluated_results:
      if pen_with_swap < pen_without_swap:
        strong_parents.append(copy)
        evaluated_results.append(copy)
      elif pen_without_swap - pen_with_swap < accept_max:
        parents.append(copy)
        evaluated_results.append(copy)

  return strong_parents, parents

def genetic_iter(strong, medium, weak, due_date, accept_max, evaluated_results):
  EXIT_STRONG = 150
  EXIT_MEDIUM = 10
  EXIT_WEAK = 5
  EVALUATED_RESULTS_TS_MEDIUM = 1000
  EVALUATED_RESULTS_TS_WEAK = 500

  strong_new = []
  medium_new = []
  weak_new = []

  for idx, item in enumerate(strong):
    sp, p = generate_population(item, due_date, accept_max, evaluated_results)
    strong_new += sp
    medium_new += p
    strong += sp
    medium += p

    if idx > EXIT_STRONG:
      break

  for idx, item in enumerate(medium):
    sp, p = generate_population(item, due_date, accept_max, evaluated_results)
    medium_new += sp
    weak_new += p
    medium += sp
    weak += p

    if idx > EXIT_MEDIUM or len(evaluated_results) > EVALUATED_RESULTS_TS_MEDIUM:
      break

  for idx, item in enumerate(weak):
    sp = generate_strong_population(item, due_date, accept_max, evaluated_results)
    weak += sp
    weak_new += sp

    if idx > EXIT_WEAK or len(evaluated_results) > EVALUATED_RESULTS_TS_WEAK:
      break

  return strong_new, medium_new, weak_new


def genetic(set, due_date, accept_max, n):
  evaluated_results = []
  results = []
  strong, medium, weak = [set], [], []
  for i in range(n):
    s, m, w = genetic_iter(strong, medium, weak, due_date, accept_max, evaluated_results)
    results += strong
    strong = medium
    medium = weak
    weak = []

  return results

ACCEPT_FACTOR = 0.05
FILES = [
  'data/sch20.txt', 'data/sch50.txt',
  'data/sch100.txt', 'data/sch200.txt', 'data/sch500.txt',
  'data/sch1000.txt'
]
Hs = [0.2, 0.4, 0.6, 0.8]

# FILE = 'data/sch10.txt'
# all_instances = DataLoader.call(FILE)
# total_results = []
# for inst in all_instances:
#   inst_results = []
#   for h in Hs:
#     result = FullSwitchSet.call(inst, h)
#     inst_results.append(result)
#   print([x[0] for x in inst_results])

for file in FILES:
  all_instances = DataLoader.call(file)
  res_array = []
  for idx, inst in enumerate(all_instances):
    inst_array = []
    for h in Hs:
      due_date = int(h * sum([x[0] for x in inst]))

      #(cost, set) tuple
      ss = SimpleSolver.call(inst, h)
      nv = Naive.call(inst, h)
      results = [
        ss,
        nv,
        SwitchSet.call(ss[1], due_date, 0.01, 5),
        SwitchSet.call(nv[1], due_date, 0.01, 5),
      ]

      accept_max = ACCEPT_FACTOR * results[0][0]
      length = len(inst)

      n = {
        20: 5,
        50: 2,
        100: 1,
        200: 0,
        500: 0,
        1000: 0
      }[length]

      (cost, base) = min(results)
      for result in genetic(base, due_date, accept_max, n):
        results.append((ResultEvaluator.call(result, h), result))

      best_set = min(results)[1]
      best_after_ss = SwitchSet.call(best_set, due_date, 0.05, 5)


      inst_array.append(min(results))
    print([x[0] for x in inst_array])
