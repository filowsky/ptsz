from data_loader import DataLoader
from result_evaluator import ResultEvaluator
from simple_solver import SimpleSolver

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
    copy = [[x for x in item] for item in set]
    pen_without_swap = eval_penelty_for_two(copy[idx], copy[idx+1], current_time, due_date)
    pen_with_swap = eval_penelty_for_two(copy[idx+1], copy[idx], current_time, due_date)
    copy[idx], copy[idx+1] = copy[idx+1], copy[idx]

    # print(len(evaluated_results))

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
    copy = [[x for x in item] for item in set]
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

def genetic_iter(set, h, best, accept_factor, mutation_factor, evaluated_results):
  due_date = int(h * sum([x[0] for x in set]))
  accept_max = accept_factor * best

  strong_parents, parents = generate_population(set, due_date, accept_max, evaluated_results)
  print(len(strong_parents))
  print(len(parents))
  print(len(evaluated_results))

  for item in strong_parents:
    print(len(strong_parents))
    sp, p = generate_population(item, due_date, accept_max, evaluated_results)
    strong_parents += sp
    parents += p

  if len(evaluated_results) > 500:
    parents = []

  for item in parents:
    sp = generate_strong_population(item, due_date, accept_max, evaluated_results)
    parents += sp

  last_elements_num = int(len(parents) / 10)
  strong_parents += parents[-last_elements_num:]  # take 10% of best parents
  return strong_parents

def genetic_iter_sp_only(set, h, best, accept_factor, mutation_factor, evaluated_results):
  due_date = int(h * sum([x[0] for x in set]))
  accept_max = accept_factor * best

  strong_parents, parents = generate_population(set, due_date, accept_max, evaluated_results)

  for item in strong_parents:
    sp, _ = generate_population(item, due_date, accept_max, evaluated_results)
    strong_parents += sp
    # strong_parents += p

  return strong_parents

ACCEPT_FACTOR = 0.1
MUTATION_FACTOR = 0.005
ITER_TRESHHOLD = 100
Hs = [0.4] #[0.2, 0.4, 0.6, 0.8]
all_instances = [DataLoader.call('data/sch100.txt')[0]]

res_array = []
for inst in all_instances:
  inst_array = []
  for h in Hs:
    cost, set = SimpleSolver.call(inst, h)

    evaluated_results = [] # used as ref
    items = [[[field for field in item] for item in set]]

    results = []
    for item in items:
      cost = ResultEvaluator.call(item, h)
      if len(items) > ITER_TRESHHOLD:
        items += genetic_iter_sp_only(item, h, cost, ACCEPT_FACTOR, MUTATION_FACTOR, evaluated_results)
      else:
        items += genetic_iter(item, h, cost, ACCEPT_FACTOR, MUTATION_FACTOR, evaluated_results)
      results.append((item, cost))

    x = min(results, key = lambda t: t[1])

    inst_array.append(x[1])
    print(x[1])
  res_array.append([x for x in inst_array])

for x in res_array:
  print(x)
