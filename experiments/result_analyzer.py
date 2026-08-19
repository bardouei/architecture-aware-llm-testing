import json
from pathlib import Path




class ResultAnalyzer:



    def __init__(
        self,
        result_file
    ):

        self.result_file = Path(
            result_file
        )



    def load(self):

        with open(
            self.result_file
        ) as file:

            return json.load(
                file
            )



    def calculate_metrics(
        self
    ):

        data = self.load()



        metrics = {



            "compilation_success":

                self.boolean_metric(

                    data.get(
                        "compilation",
                        {}
                    )

                ),



            "test_success":

                self.boolean_metric(

                    data.get(
                        "tests",
                        {}
                    )

                ),



            "coverage":

                data.get(
                    "coverage",
                    {}
                )
                .get(
                    "coverage",
                    0
                ),



            "mutation_score":

                self.calculate_mutation_score(

                    data.get(
                        "mutation",
                        {}

                    )

                )

        }



        return metrics




    def boolean_metric(
        self,
        data
    ):

        return (

            1

            if data.get(
                "success",
                False
            )

            else 0

        )




    def calculate_mutation_score(
        self,
        mutation
    ):


        if "mutation_score" in mutation:

            return mutation["mutation_score"]


        created = mutation.get(

            "mutations_created",

            0

        )


        killed = mutation.get(

            "mutations_killed",

            0

        )


        invalid = mutation.get(

            "invalid_mutants",

            0

        )


        valid = created - invalid


        if valid <= 0:

            return 0



        return round(

            (killed / valid) * 100,

            2

        )




if __name__ == "__main__":


    analyzer = ResultAnalyzer(

        "results/evaluation_results.json"

    )


    print(

        analyzer.calculate_metrics()

    )
