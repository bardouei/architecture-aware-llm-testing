import json
from pathlib import Path




class ComparisonEngine:



    def __init__(
        self,
        baseline,
        architecture
    ):

        self.baseline = baseline

        self.architecture = architecture




    def compare(
        self
    ):


        report = {



            "comparison":

            {



                "baseline":

                    self.baseline,



                "architecture_aware":

                    self.architecture

            },



            "improvements":

                self.calculate_improvements()

        }



        return report





    def calculate_improvements(
        self
    ):


        result = {}



        for metric in self.baseline:


            before = self.baseline[metric]

            after = self.architecture.get(

                metric,

                0

            )


            result[metric] = {


                "baseline":

                    before,


                "architecture_aware":

                    after,


                "improvement":

                    round(

                        after - before,

                        2

                    )

            }



        return result





    def save(
        self,
        path
    ):


        path = Path(
            path
        )


        path.parent.mkdir(

            exist_ok=True

        )


        with open(

            path,

            "w"

        ) as file:


            json.dump(

                self.compare(),

                file,

                indent=4

            )