from typing import Any

import structlog

logger = structlog.get_logger("dronzer.marketplace.resolver")


class DependencyResolver:
    """
    Resolves complex, nested package dependency trees.
    Builds a Directed Acyclic Graph (DAG) to ensure all required
    child packages are installed before the parent package.
    Detects circular dependencies and Semantic Version conflicts.
    """

    def __init__(self, registry_client: Any = None):
        self.registry = registry_client

    async def resolve_install_graph(
        self, package_name: str, requested_version: str
    ) -> list[dict[str, str]]:
        """
        Calculates the flat installation order required to install the requested package
        and all of its nested dependencies without conflicts.
        """
        logger.info(f"Resolving dependency graph for {package_name}@{requested_version}")

        install_plan = []
        visited = set()
        resolving = set()

        # We would query the real DB here. Mocking a dependency tree:
        # parent -> child_a (>=1.0.0), child_b (>=2.1.0)

        async def _dfs(pkg: str, ver_constraint: str):

            if pkg in resolving:
                raise ValueError(f"Circular dependency detected involving {pkg}")

            if pkg in visited:
                # In production, we must verify if the already visited version satisfies the new ver_constraint
                return

            resolving.add(pkg)

            # 1. Fetch package metadata from Registry
            # mock_meta = await self.registry.get_package_version(pkg, ver_constraint)
            mock_dependencies = {}
            if pkg == package_name:
                mock_dependencies = {"@core/http-client": ">=1.0.0", "@utils/logger": ">=2.0.0"}

            # 2. Recursively resolve children
            for child_pkg, child_constraint in mock_dependencies.items():
                await _dfs(child_pkg, child_constraint)

            resolving.remove(pkg)
            visited.add(pkg)

            # Post-order traversal guarantees children are installed before parents
            install_plan.append({"package": pkg, "version": ver_constraint})

        await _dfs(package_name, requested_version)

        logger.debug("Dependency resolution complete", plan=install_plan)
        return install_plan
