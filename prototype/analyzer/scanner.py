from pathlib import Path


class RepositoryScanner:


    def __init__(self, project_path: str):
        self.project_path = Path(project_path)



    def scan_files(self):

        source_files = []
        test_files = []


        for file in self.project_path.rglob("*.swift"):

            file_path = str(file)


            if self.is_test_file(file):
                test_files.append(file_path)

            else:
                source_files.append(file_path)


        return {
            "source_files": source_files,
            "test_files": test_files
        }



    def scan_modules(self):

        modules = set()

        ignored = {
            ".git",
            ".build"
        }


        for folder in self.project_path.iterdir():

            if not folder.is_dir():
                continue


            if folder.name.endswith(
                (
                    ".xcodeproj",
                    ".xcworkspace"
                )
            ):
                continue


            if folder.name in ignored:
                continue


            modules.add(folder.name)


        return list(modules)



    def is_test_file(self, file: Path):

        parts = [
            part.lower()
            for part in file.parts
        ]


        return (
            "test" in parts
            or
            file.name.endswith("Tests.swift")
        )