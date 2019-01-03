from data_loader import DataLoader
from result_evaluator import ResultEvaluator
from simple_solver import SimpleSolver
from naive import Naive
from base_picker import BasePicker
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

def fast_switch_set(set, due_date, accept_max, evaluated_results):
  copy = [item[:] for item in set]
  current_time = 0
  for idx in range(len(copy) - 1):
    pen_without_swap = eval_penelty_for_two(copy[idx], copy[idx+1], current_time, due_date)
    pen_with_swap = eval_penelty_for_two(copy[idx+1], copy[idx], current_time, due_date)
    if pen_with_swap < pen_without_swap:
      copy[idx], copy[idx+1] = copy[idx+1], copy[idx]

    current_time += copy[idx][0]

  return [copy]
  # return [copy], [[item[:] for item in copy]]


def genetic_iter(strong, medium, weak, due_date, accept_max, evaluated_results):
  EXIT_STRONG = 50
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


def genetic(set, due_date, accept_max):
  length = len(set)
  fss = False
  if length <= 100:
    n = 2
  if length <= 50:
    n = 5
  if length <= 20:
    n = 10
  else:
    fss = True

  if fss:
    return fast_switch_set(set, due_date, accept_max, [])
  else:
    evaluated_results = []
    results = []
    strong, medium, weak = genetic_iter([set], [], [], due_date, accept_max, evaluated_results)
    for i in range(n):
      s, m, w = genetic_iter(strong, medium, weak, due_date, accept_max, evaluated_results)
      results += strong
      strong = medium
      medium = weak
      weak = []

    return results

ACCEPT_FACTOR = 0.05
MUTATION_FACTOR = 0.005
ITER_TRESHHOLD = 100
FILES = [
  'data/sch10.txt', 'data/sch20.txt', 'data/sch50.txt',
  'data/sch100.txt', 'data/sch200.txt', 'data/sch500.txt',
  'data/sch1000.txt'
]
Hs = [0.2, 0.4, 0.6, 0.8]
for file in FILES:
  all_instances = DataLoader.call(file)
  print(datetime.datetime.now().time())
  print(file)
  res_array = []
  for idx, inst in enumerate(all_instances):
    inst_array = []
    for h in Hs:
      cost, set = SimpleSolver.call(inst, h)
      if h == 0.8 and BasePicker.call(inst, idx) == 'Naive':
        set = Naive.call(inst, h)

      due_date = int(h * sum([x[0] for x in set]))
      accept_max = ACCEPT_FACTOR * cost

      results = [(set, cost)]
      for result in genetic(set, due_date, accept_max):
        results.append((result, ResultEvaluator.call(result, h)))

      x = min(results, key = lambda t: t[1])

      inst_array.append(x[1])
    res_array.append([x for x in inst_array])

  for x in res_array:
    print(x)
