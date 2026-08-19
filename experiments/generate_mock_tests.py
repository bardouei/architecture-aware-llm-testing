import sys
from pathlib import Path


# Add project root to python path

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

sys.path.append(
    str(PROJECT_ROOT)
)



from prototype.llm.runners.baseline_runner import (
    BaselineRunner
)

from prototype.llm.runners.architecture_runner import (
    ArchitectureRunner
)
from prototype.run_pipeline import run as build_context





def load_source_code():


    source_path = (

        PROJECT_ROOT /

        "datasets" /

        "fixtures" /

        "swift-sample-app" /

        "SwiftSampleApp" /

        "Feature" /

        "Login" /

        "LoginViewModel.swift"

    )


    with open(source_path) as file:

        return file.read()





def load_context():

    return build_context(
        PROJECT_ROOT / "datasets/fixtures/swift-sample-app",
        "LoginViewModel",
        PROJECT_ROOT / "artifacts/context/swift-sample-app/LoginViewModel",
    )






def save_result(
    content,
    path
):

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    with open(
        path,
        "w"
    ) as file:

        file.write(
            content
        )



def run():


    print(
        "Generating deterministic mock fixtures"
    )


    source_code = load_source_code()


    context = load_context()



    # -------------------------
    # Baseline
    # -------------------------


    print(
        "\nRunning Baseline..."
    )


    baseline_runner = BaselineRunner()


    baseline_result = (
        baseline_runner.run(
            source_code
        )
    )


    baseline_path = (

        PROJECT_ROOT /

        "experiments" /

        "fixtures" /

        "generated-tests" /

        "baseline" /

        "LoginViewModelTests.swift"

    )


    save_result(

        baseline_result,

        baseline_path

    )


    print(
        "Baseline saved"
    )





    # -------------------------
    # Architecture Aware
    # -------------------------


    print(
        "\nRunning Architecture-aware..."
    )


    architecture_runner = ArchitectureRunner()


    architecture_result = (

        architecture_runner.run(

            context,

            source_code

        )

    )


    architecture_path = (

        PROJECT_ROOT /

        "experiments" /

        "fixtures" /

        "generated-tests" /

        "architecture" /

        "LoginViewModelTests.swift"

    )


    save_result(

        architecture_result,

        architecture_path

    )


    print(
        "Architecture-aware saved"
    )





    print(
        "\nExperiment completed"
    )





if __name__ == "__main__":

    run()
