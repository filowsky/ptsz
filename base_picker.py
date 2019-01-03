class BasePicker:
  def call(inst, idx):
    id = len(inst) + idx

    if id in [11, 12, 16, 17, 27]:
      return 'Naive'

    return 'SimpleSolver'
