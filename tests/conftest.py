import os
import pytest


def pytest_addoption(parser):
    parser.addoption("--module-file", action="store", default="default name")
    parser.addoption("--name", action="store", default="default name")


def pytest_sessionstart(session):
    session.results = dict()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    if result.when == 'call' or result.when == 'setup':
        item.session.results[item] = result


def pytest_sessionfinish(session, exitstatus):
    results_by_test = dict()
    for result in session.results.values():
        # name_parts = result.nodeid.split('::')
        # test_name: str = f"{name_parts[1]}: {name_parts[2]}"
        test_name: str = result.nodeid.split("::")[1]
        index = test_name.find("[")
        if index > -1:
            key = test_name[:index]
        else:
            key = test_name

        if key in results_by_test.keys():
            results_by_test[key]["total"] += 1
            if result.outcome == "passed":
                results_by_test[key]["passed"] += 1
        else:
            results_by_test[key] = {"total": 1, "passed": 1 if result.outcome == "passed" else 0}

    report_file_name = session.config.getoption('--name')[:-3]

    # check if results folder exists, if not, create it
    if not os.path.exists(f".{os.sep}results"):
        os.makedirs(f".{os.sep}results")

    with open(f".{os.sep}results{os.sep}{report_file_name}.txt", mode="w", encoding='utf8') as file:
        total_tests = len(results_by_test)
        score_sum = 0
        line_char = u'\u2500' * 108
        c_char = u'\u2502'
        header = f"{line_char}\n{c_char}{'#':^3}{c_char}{' Prueba':<93}{c_char}{'Puntos':^8}{c_char}\n{line_char}\n"
        file.write(header)
        grand_total = 0
        grand_passed = 0
        for count, item in enumerate(results_by_test.items(), start=1):
            key, value = item
            test_score = value["passed"] / value["total"]
            grand_total += value["total"]
            grand_passed += value["passed"]
            score_sum += test_score
            inter_test = f"({value['passed']}/{value['total']})"
            line = f"{c_char}{count:<3}{c_char} {key:<85}{inter_test:<7}{c_char}{test_score:^8.1f}{c_char}\n"
            file.write(line)

        file.write(f"{line_char}\n")
        footer = f"{c_char}{'TOTAL':<97}{c_char}{score_sum:^8.1f}{c_char}\n{line_char}\n"
        file.write(footer)
        score = score_sum / total_tests * 5
        # grand_score = grand_passed / grand_total * 5
        file.write(f"NOTA: {score_sum:.1f} / {total_tests} = {score: .1f}")
        # file.write(f"NOTA: {grand_passed} / {grand_total} = {grand_score: .1f}")
