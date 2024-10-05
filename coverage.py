from typing import Self, Callable, Any
from trace import Trace
from inspect import getsourcelines, getfile


class CoverageTracker:
    def __init__(
        self: Self,
        function: Callable[..., Any],
        *args,
        **kwargs,
    ) -> None:
        self.function = function

        self._lines = set()
        self.covered_lines = set()

    def reset(self: Self) -> None:
        self.lines.clear()
        self.covered_lines.clear()

    @property
    def lines(self: Self) -> set[int]:
        if self._lines:
            return self._lines

        source_lines, starting_line_number = getsourcelines(self.function)
        self.source_lines = source_lines

        function_declaration_offset = 0
        for index, line in enumerate(source_lines):
            if line.strip().endswith(":"):
                function_declaration_offset += index
                break

        start = starting_line_number + function_declaration_offset + 1
        end = len(source_lines) + starting_line_number

        return set(range(start, end))

    def __call__(self: Self, trace: Trace) -> None:
        self.reset()

        tracer_results = trace.results()
        executed_lines = tracer_results.counts
        module = getfile(self.function)

        for line in self.lines:
            if (module, line) in executed_lines:
                self.covered_lines.add(line)