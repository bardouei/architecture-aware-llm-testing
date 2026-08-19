import tempfile
import unittest
from pathlib import Path

from evaluation.mutation_testing import MutationTesting


SWIFT_SOURCE = """final class LoginViewModel {
    var user: User?
    var username = ""
    var password = ""

    func login() async {
        do {
            user = try await loginUseCase.execute(username: username, password: password)
        } catch {
            user = nil
        }
    }
}
"""


class MutationTestingTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.source_file = Path(self.temporary_directory.name) / "LoginViewModel.swift"
        self.source_file.write_text(SWIFT_SOURCE)

    def tearDown(self):
        self.temporary_directory.cleanup()

    def test_discovers_targeted_login_mutants(self):
        mutants = MutationTesting(self.source_file).discover_mutants()

        self.assertEqual(len(mutants), 3)
        self.assertEqual(
            {mutant.operator for mutant in mutants},
            {
                "remove_async_result_assignment",
                "remove_nil_assignment",
                "swap_credential_arguments",
            },
        )
        self.assertTrue(all(mutant.line > 0 for mutant in mutants))

    def test_executes_classifies_and_restores(self):
        def compile_source():
            return {"success": "_ = user" not in self.source_file.read_text()}

        def run_tests():
            killed = "_ = try await" in self.source_file.read_text()
            return {"success": not killed}

        result = MutationTesting(
            self.source_file, compile_source, run_tests
        ).run()

        self.assertTrue(result["success"])
        self.assertEqual(result["mutations_created"], 3)
        self.assertEqual(result["mutations_killed"], 1)
        self.assertEqual(result["mutations_survived"], 1)
        self.assertEqual(result["invalid_mutants"], 1)
        self.assertEqual(result["mutation_score"], 50.0)
        self.assertEqual(self.source_file.read_text(), SWIFT_SOURCE)

    def test_stops_when_baseline_fails(self):
        result = MutationTesting(
            self.source_file,
            lambda: {"success": True},
            lambda: {"success": False, "output": "baseline failed"},
        ).run()

        self.assertFalse(result["success"])
        self.assertEqual(result["mutations_tested"], 0)
        self.assertEqual(self.source_file.read_text(), SWIFT_SOURCE)

    def test_restores_source_when_runner_raises(self):
        calls = 0

        def run_tests():
            nonlocal calls
            calls += 1
            if calls > 1:
                raise RuntimeError("runner crashed")
            return {"success": True}

        mutation = MutationTesting(
            self.source_file, lambda: {"success": True}, run_tests
        )
        with self.assertRaisesRegex(RuntimeError, "runner crashed"):
            mutation.run()

        self.assertEqual(self.source_file.read_text(), SWIFT_SOURCE)


if __name__ == "__main__":
    unittest.main()
