import subprocess
import re
from pathlib import Path



class CoverageAnalyzer:


    def __init__(
        self,
        result_bundle,
        source_file=None
    ):

        self.result_bundle = Path(
            result_bundle
        )

        self.source_file = source_file



    def analyze(self):


        if not self.result_bundle.exists():

            return {

                "success": False,

                "coverage": 0,

                "error":
                    f"Result bundle not found: {self.result_bundle}"

            }



        command = [

            "xcrun",

            "xccov",

            "view",

            "--report",

            str(self.result_bundle)

        ]



        try:


            result = subprocess.run(

                command,

                capture_output=True,

                text=True

            )


            output = (

                result.stdout +

                result.stderr

            )


            if result.returncode != 0:

                return {

                    "success": False,

                    "coverage": 0,

                    "error": output[-3000:]

                }



            coverage = (
                self.extract_file_percentage(
                    output,
                    self.source_file
                )

                if self.source_file

                else self.extract_percentage(
                    output
                )
            )


            return {


                "success": True,


                "coverage":

                    coverage,


                "raw":

                    output[-3000:]

            }



        except Exception as error:


            return {


                "success": False,


                "coverage": 0,


                "error":
                    str(error)

            }




    def extract_percentage(
        self,
        text
    ):


        match = re.search(

            r"(\d+\.\d+)%",

            text

        )


        if match:

            return float(
                match.group(1)
            )


        return 0


    def extract_file_percentage(
        self,
        text,
        source_file
    ):

        filename = Path(source_file).name

        for line in text.splitlines():

            if filename in line:

                return self.extract_percentage(line)

        return 0
