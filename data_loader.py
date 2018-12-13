class DataLoader:
  # file_path string -> task_set [[_, _, _], [_, _, _]]
  @static_method
  def call(file_path):
    with open(file_path, "r") as f:
      sets_number = int(f.readline().strip())
      sets = []
      for _ in range(sets_number):
        set_length = int(f.readline().strip())
        set = [[int(x) for x in f.readline().strip().split()] for _ in range(set_length)]
        sets.append(set)
      return sets
