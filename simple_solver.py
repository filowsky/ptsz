from data_loader import DataLoader
from result_evaluator import ResultEvaluator

class SimpleSolver:
  @staticmethod
  def call(problem):
    return problem

all_instances = DataLoader.call('data/sch10.txt')
print(SimpleSolver.call(all_instances[0]))
