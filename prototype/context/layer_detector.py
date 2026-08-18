from pathlib import Path


class LayerDetector:


    def detect(self, file_path):

        path = file_path.lower()


        if "viewmodel" in path:
            return "Presentation"


        if "feature" in path:
            return "Presentation"


        if "domain" in path:
            return "Domain"


        if "usecase" in path:
            return "Domain"


        if "repository" in path:
            return "Data"


        if "data" in path:
            return "Data"


        return "Unknown"