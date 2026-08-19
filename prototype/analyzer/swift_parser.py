import re
from pathlib import Path



class SwiftParser:


    IGNORE_TYPES = {
        "String",
        "Int",
        "Double",
        "Bool",
        "Float",
        "Date",
        "URL",
        "UUID",
        "Any",
        "ObservableObject"
    }



    def __init__(self, files, project_root=None):

        self.files = files
        self.project_root = Path(project_root).resolve() if project_root else None



    def parse(self):

        result = {

            "components": [],

            "protocols": []

        }


        for file in self.files:


            path = Path(file)


            if not path.exists():
                continue



            content = path.read_text()



            protocols = self.extract_protocols(
                content
            )


            result["protocols"].extend(
                protocols
            )



            types = self.extract_types(
                content,
                self.display_path(path)
            )


            result["components"].extend(
                types
            )



        return result



    def extract_protocols(self, content):

        pattern = r"protocol\s+(\w+)"

        return re.findall(
            pattern,
            content
        )

    def display_path(self, path):

        if self.project_root:

            try:

                return str(path.resolve().relative_to(self.project_root))

            except ValueError:

                pass

        return str(path)

    def extract_types(
        self,
        content,
        filename
    ):

        components = []


        type_pattern = (
            r"(?:final\s+)?(class|struct|actor)\s+(\w+)"
            r"(?:\s*:\s*([\w,\s]+))?"
        )


        types = re.findall(
            type_pattern,
            content
        )


        for type_kind, type_name, inheritance in types:


            implements = []


            if inheritance:

                inherited_types = [
                    item.strip()
                    for item in inheritance.split(",")
                ]


                # Framework types that are not architecture interfaces
                ignored = {
                    "ObservableObject",
                    "View",
                    "NSObject"
                }


                implements = [
                    item
                    for item in inherited_types
                    if item not in ignored
                ]



            dependencies = (
                self.extract_dependencies(
                    content,
                    type_name
                )
            )



            components.append({

                "name": type_name,

                "type": type_kind,

                "file": filename,

                "implements": implements,

                "dependencies": dependencies

            })


        return components


    def extract_dependencies(
        self,
        content,
        class_name
    ):

        dependencies = []


        # property injection
        property_pattern = (
            r"let\s+\w+\s*:\s*(\w+)"
        )


        matches = re.findall(
            property_pattern,
            content
        )


        dependencies.extend(
            matches
        )

        # The Composable Architecture dependency-key injection.
        dependencies.extend(
            re.findall(r"@Dependency\(\\\.(\w+)\)", content)
        )

        # TCA reducer composition and destination references. Only names that
        # resolve to parsed components are traversed by the context selector.
        dependencies.extend(
            name
            for name in re.findall(r"\b([A-Z]\w*Feature)\b", content)
            if name != class_name
        )


        # init parameters
        init_pattern = (
            r"init\s*\((.*?)\)"
        )


        init_matches = re.findall(
            init_pattern,
            content,
            re.DOTALL
        )


        for init in init_matches:


            params = re.findall(
                r":\s*(\w+)",
                init
            )


            dependencies.extend(
                params
            )



        dependencies = [

            dep

            for dep in dependencies

            if dep not in self.IGNORE_TYPES

        ]



        return list(
            set(dependencies)
        )
