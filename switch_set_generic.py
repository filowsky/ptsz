from itertools import permutations
from random import random, randint
from result_evaluator import ResultEvaluator


class SwitchSetGeneric:
    @staticmethod
    def call(set, due_date, mutation_factor, slice_len, iters):
        if iters == 1:
            set = SwitchSetGeneric.perform_iteration(set, slice_len, due_date, mutation_factor)
        else:
            for i in range(iters):
                set = SwitchSetGeneric.perform_iteration(set, slice_len, due_date, mutation_factor)
            for i in range(iters):
                set = SwitchSetGeneric.perform_iteration(set, slice_len, due_date, 0)

        return (ResultEvaluator.call_with_dd(set, due_date), set)

    @staticmethod
    def perform_iteration(set, slice_len, due_date, mutation_factor):
        if (len(set) <= slice_len):
            raise ValueError('len(set) must be greater than slice_len.')

        copy = [item[:] for item in set]

        if random() < mutation_factor:
            idx = randint(0, len(copy) - 1)
            idx2 = randint(0, len(copy) - 1)
            copy[idx], copy[idx2] = copy[idx2], copy[idx]

        rng = range(len(copy) - slice_len + 1)
        current_time = 0

        for idx in rng:
            best_slice = min([
                (SwitchSetGeneric.compute_cost(perm, due_date, current_time), perm)
                for perm in permutations(copy[idx:idx+slice_len])
            ])

            copy[idx:idx+slice_len] = best_slice[1]
            current_time += copy[idx][0]

        return copy

    @staticmethod
    def compute_cost(scheduled_tasks, due_date, current_time):
        def cost(task):
            nonlocal current_time
            current_time += task[0]
            delay = current_time - due_date

            if delay > 0:
                return delay * task[2]
            else:
                return -delay * task[1]

        return sum(list(map(lambda t: cost(t), scheduled_tasks)))
