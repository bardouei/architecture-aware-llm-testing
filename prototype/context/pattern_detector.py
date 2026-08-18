class PatternDetector:


    def detect(self, components, files):

        patterns = []


        names = [
            c["name"]
            for c in components
        ]


        if any(
            "ViewModel" in name
            for name in names
        ):
            patterns.append(
                "MVVM"
            )


        if any(
            "UseCase" in name
            for name in names
        ):

            patterns.append(
                "Clean Architecture"
            )


        return patterns