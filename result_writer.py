class ResultWriter:
  @staticmethod
  def call(inst, min, k, h):
    inst = [item[:] for item in inst]
    if k == 0:
      k = 4
    else:
      k = 9
    h = int(h * 10)
    cost = min[0]
    sorted = min[1]
    file = "sch_127277_" + str(len(inst)) + "_" + str(k) + "_" + str(h) + ".txt"
    with open(file, "w+") as f:
      f.write(str(cost) + "\n")
      solution_array = []
      for item in sorted:
          index = inst.index(item)
          solution_array.append(str(index))
          inst[index] = False
      print((k, h, cost, sorted))
      f.write(" ".join(solution_array))
