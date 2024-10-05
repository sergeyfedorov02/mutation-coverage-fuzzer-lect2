from typing import Self
from random import choice, randint

from mutations import (
    flip_random_character,
    delete_random_character,
    insert_random_character,
    insert_random_special_character,
)
from runner import Runner, RunnerResult


class MutationFuzzer:
    def __init__(
            self: Self,
            seed: set[str],
            min_mutations: int,
            max_mutations: int,
            runner: Runner,
            count: int,
    ) -> None:
        self.seed = seed
        self.min_mutations = min_mutations
        self.max_mutations = max_mutations
        self.runner = runner
        self.count = count

        self.poplulation = self.seed
        self.line_status = {line: False for line in self.runner.coverage_tracker.lines}

    def mutate(self, individual: str) -> str:
        turn = randint(1, 4)
        match turn:
            case 1:
                return flip_random_character(individual)
            case 2:
                return delete_random_character(individual)
            case 3:
                return insert_random_character(individual)
            case 4:
                return insert_random_special_character(individual)

    def create_candidate(self: Self) -> str:
        candidate = choice(list(self.poplulation))
        trials = randint(self.min_mutations, self.max_mutations)
        for _ in range(trials):
            candidate = self.mutate(candidate)
        return candidate

    def run_candidate(self: Self, candidate: str) -> RunnerResult:
        _, result = self.runner.run(candidate)
        covered_lines = self.runner.coverage_tracker.covered_lines
        for line in covered_lines:
            if not self.line_status[line]:
                self.line_status[line] = True
                self.poplulation.add(candidate)
        return result

    def run_seed(self: Self) -> None:
        for candidate in self.seed:
            self.run_candidate(candidate)

    def run(self: Self) -> None:
        candidate = self.create_candidate()
        result = self.run_candidate(candidate)

        uncovered_lines = [
            line for line, status in self.line_status.items() if not status
        ]

        print(
            f"Candidate: {candidate}",
            f"Uncovered lines: {uncovered_lines}",
            f"Population: {self.poplulation}",
            f"Result: {result}",
        )

    def fuzz(self: Self) -> None:
        self.run_seed()
        for _ in range(self.count):
            self.run()
