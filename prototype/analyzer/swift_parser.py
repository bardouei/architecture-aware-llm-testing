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



    def __init__(self, files):

        self.files = files



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



            classes = self.extract_classes(
                content,
                path.name
            )


            result["components"].extend(
                classes
            )



        return result



    def extract_protocols(self, content):

        pattern = r"protocol\s+(\w+)"

        return re.findall(
            pattern,
            content
        )

    def extract_classes(
        self,
        content,
        filename
    ):

        components = []


        class_pattern = (
            r"(?:final\s+)?class\s+(\w+)(?:\s*:\s*([\w,\s]+))?"
        )


        classes = re.findall(
            class_pattern,
            content
        )


        for class_name, inheritance in classes:


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
                    class_name
                )
            )



            components.append({

                "name": class_name,

                "type": "class",

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