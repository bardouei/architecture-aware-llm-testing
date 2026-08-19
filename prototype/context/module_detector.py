from pathlib import Path


class ModuleDetector:

    def __init__(self):
        pass


    def detect(
        self,
        file_path: str
    ) -> str:

        """
        Detect module name from file path.

        Examples:

        Feature/Login/LoginViewModel.swift
            ->
        Feature/Login


        Domain/LoginUseCase.swift
            ->
        Domain


        Data/UserRepository.swift
            ->
        Data

        """


        path = Path(file_path)


        parts = list(path.parts)



        # Find architecture folders

        if "Feature" in parts:

            index = parts.index(
                "Feature"
            )

            module_parts = parts[
                index:
            ]

            return "/".join(
                module_parts[:-1]
            )



        if "Domain" in parts:

            return "Domain"



        if "Data" in parts:

            return "Data"



        if "Core" in parts:

            return "Core"



        # fallback

        return "Unknown"



    def detect_components(
        self,
        components
    ):

        """
        Add module information
        to architecture components.
        """


        enriched = []


        for component in components:


            file_path = component.get(
                "file",
                ""
            )


            component["module"] = (
                self.detect(
                    file_path
                )
            )


            enriched.append(
                component
            )


        return enriched