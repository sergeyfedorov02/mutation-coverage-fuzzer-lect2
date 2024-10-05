from runner import Runner
from fuzzer import MutationFuzzer
from cgi_decoder import cgi_decode
from url_validator import http_program


def main() -> None:
    test_coverage()


def test_mutation_url_validator():
    runner = Runner(http_program)
    seed = {"http://www.google.com/search?q=fuzzing"}
    fuzzer = MutationFuzzer(
        seed=seed,
        min_mutations=2,
        max_mutations=5,
        runner=runner,
        count=100_000,
    )
    fuzzer.fuzz()


def test_mutation_cgi_decode():
    # cgi_decode("+")
    # cgi_decode("%20")
    # cgi_decode("abc")

    runner = Runner(cgi_decode)
    seed = {"2%0", "abc+"}
    fuzzer = MutationFuzzer(
        seed=seed,
        min_mutations=2,
        max_mutations=5,
        runner=runner,
        count=100_000,
    )
    fuzzer.fuzz()


def test_coverage():
    # cgi_decode("+")
    # cgi_decode("%20")
    # cgi_decode("abc")

    runner = Runner(cgi_decode)

    res = runner.run("+")
    covered_lines_set = runner.coverage_tracker.covered_lines
    covered_lines_count = len(covered_lines_set)
    lines = len(runner.coverage_tracker.lines)
    print(res[1])
    print(f"{covered_lines_count}/{lines}")
    print(f"{runner.coverage_tracker.covered_lines} \n")

    res = runner.run("%20")
    covered_lines_set = runner.coverage_tracker.covered_lines
    covered_lines_count = len(covered_lines_set)
    lines = len(runner.coverage_tracker.lines)
    print(res[1])
    print(f"{covered_lines_count}/{lines}")
    print(f"{runner.coverage_tracker.covered_lines} \n")

    res = runner.run("abc")
    covered_lines_set = runner.coverage_tracker.covered_lines
    covered_lines_count = len(covered_lines_set)
    lines = len(runner.coverage_tracker.lines)
    print(res[1])
    print(f"{covered_lines_count}/{lines}")
    print(f"{runner.coverage_tracker.covered_lines} \n")


if __name__ == "__main__":
    main()
