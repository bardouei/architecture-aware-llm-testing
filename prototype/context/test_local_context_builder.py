import tempfile
import unittest
from pathlib import Path

from prototype.context.local_context_builder import collect_local_context


class LocalContextBuilderTests(unittest.TestCase):
    def test_selects_referenced_and_extension_definitions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "Packages/Feature/Sources/Feature/HomeFeature.swift"
            action = root / "Packages/Feature/Sources/Feature/HomeAction.swift"
            dependency = root / "Packages/Feature/Sources/Feature/PostsClient.swift"
            unrelated = root / "Packages/Other/Sources/Other/Noise.swift"
            child = root / "Packages/Child/Sources/Child/ChildFeature.swift"
            entity = root / "Packages/Domain/Sources/Domain/Entity.swift"
            for path in (target, action, dependency, unrelated, child, entity):
                path.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                "struct HomeFeature { let client: PostsClient; let child: ChildFeature }"
            )
            action.write_text("extension HomeFeature { enum Action {} }")
            dependency.write_text("struct PostsClient {}")
            unrelated.write_text("struct Noise {}")
            child.write_text("struct ChildFeature { let entity: Entity }")
            entity.write_text("struct Entity {}")

            evidence = collect_local_context(root, target, "HomeFeature")

        self.assertEqual(
            {item["path"] for item in evidence},
            {
                "Packages/Feature/Sources/Feature/HomeAction.swift",
                "Packages/Feature/Sources/Feature/PostsClient.swift",
                "Packages/Child/Sources/Child/ChildFeature.swift",
                "Packages/Domain/Sources/Domain/Entity.swift",
            },
        )
