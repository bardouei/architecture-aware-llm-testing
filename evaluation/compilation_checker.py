import subprocess
from pathlib import Path



class CompilationChecker:


    def __init__(
        self,
        project_path,
        scheme="SwiftSampleApp",
        destination="platform=iOS Simulator,name=iPhone 17"
    ):

        self.project_path = Path(
            project_path
        )

        self.scheme = scheme

        self.destination = destination



    def check(self):


        command = [

            "xcodebuild",

            "-project",

            str(self.project_path),

            "-scheme",

            self.scheme,

            "-destination",

            self.destination,

            "CODE_SIGNING_ALLOWED=NO"

        ]


        try:

            result = subprocess.run(

                command,

                capture_output=True,

                text=True,

                timeout=300

            )


            return {

                "success":

                    result.returncode == 0,


                "output":
                    (
                        result.stdout +
                        "\n" +
                        result.stderr
                    )[-5000:]

            }



        except Exception as error:


            return {

                "success": False,

                "error": str(error)

            }
