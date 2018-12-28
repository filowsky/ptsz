from data_loader import DataLoader
from result_evaluator import ResultEvaluator

class SimpleSolver:
  def solve(self, problem, h_coeff):
    due_date = self.__compute_due_date(problem, h_coeff)
    #TODO algorithm for scheduling
    tasks_before_due_date = []
    tasks_after_due_date = []

    tasks_by_duration_earliness_ratio = sorted(problem, key=lambda t: t[0]/t[1])
    tasks_by_duration_tardiness_ratio = sorted(problem, key=lambda t: t[0]/t[2])

    for task in problem:
      tde_head = tasks_by_duration_earliness_ratio[0]
      tdt_head = tasks_by_duration_tardiness_ratio[0]

      if ((sum(list(map(lambda t: t[0], tasks_before_due_date))) + tde_head[0] > due_date) and
        ((sum(list(map(lambda t: t[0], tasks_after_due_date))) < (sum(list(map(lambda t: t[0], problem))) - due_date)) or
        (tde_head[0] / tde_head[1] < tde_head[0] / tdt_head[2]))):
        tasks_after_due_date.append(tde_head)
        tasks_by_duration_earliness_ratio.remove(tde_head)
        tasks_by_duration_tardiness_ratio.remove(tde_head)
      else:
        tasks_before_due_date.insert(0, tdt_head)
        tasks_by_duration_earliness_ratio.remove(tdt_head)
        tasks_by_duration_tardiness_ratio.remove(tdt_head)

    tasks_before_due_date_sorted = sorted(tasks_before_due_date, key=lambda t: t[0]/t[1], reverse = True)
    tasks_after_due_date_sorted = sorted(tasks_after_due_date, key=lambda t: t[0]/t[2])

    scheduled_tasks = tasks_before_due_date_sorted + tasks_after_due_date_sorted

    cost = self.__compute_cost(scheduled_tasks, due_date)
    return (cost, scheduled_tasks)
        

  def __compute_due_date(self, instance, h_coeff):
    durations = list(map(lambda x: x[0], instance))
    return int(sum(durations) * h_coeff)

  def __compute_cost(self, scheduled_tasks, due_date):
    current_time = 0
    def cost(task):
      nonlocal current_time
      current_time += task[0]
      delay = current_time - due_date

      if delay > 0:
        return delay * task[2]
      else:
        return -delay * task[1]

    return sum(list(map(lambda t: cost(t), scheduled_tasks)))



all_instances = DataLoader.call('data/sch10.txt')
simple_solver = SimpleSolver()
print(simple_solver.solve(all_instances[0], 0.4))