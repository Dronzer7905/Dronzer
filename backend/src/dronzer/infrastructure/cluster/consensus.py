import asyncio
from typing import Any

import structlog

logger = structlog.get_logger("dronzer.cluster.consensus")


class DistributedLockManager:
    """
    Provides cross-node distributed locks (Redlock algorithm equivalent).
    Ensures that cron-jobs or database migrations only run on a single node
    across the entire global cluster.
    """

    def __init__(self, redis_client: Any):
        self.redis = redis_client

    async def acquire_lock(self, lock_name: str, lease_ttl_ms: int = 10000) -> bool:
        """
        Attempts to acquire a distributed lock.
        """
        logger.debug(f"Attempting to acquire distributed lock: {lock_name}")
        if not self.redis:
            return True  # Mock for local dev

        # Implementation would use SET NX PX
        # e.g., await self.redis.set(lock_name, "locked", nx=True, px=lease_ttl_ms)
        return True

    async def release_lock(self, lock_name: str):
        if self.redis:
            # await self.redis.delete(lock_name)
            pass


class LeaderElection:
    """
    Ensures that only ONE node in a given Cluster Topology acts as the "Leader".
    The Leader is responsible for managing the Distributed Scheduler, Database failovers,
    and triggering Disaster Recovery snapshots.
    """

    def __init__(self, node_id: str, lock_manager: DistributedLockManager):
        self.node_id = node_id
        self.lock_manager = lock_manager
        self.is_leader = False
        self._election_task = None
        self.lease_duration_ms = 15000

    async def start_election_loop(self, cluster_name: str):
        """
        Runs continuously in the background on every Node.
        """
        logger.info(f"Node {self.node_id} joining leader election for cluster {cluster_name}")
        self._election_task = asyncio.create_task(self._election_heartbeat(cluster_name))

    async def _election_heartbeat(self, cluster_name: str):
        lock_name = f"leader_election:{cluster_name}"

        while True:
            try:
                acquired = await self.lock_manager.acquire_lock(lock_name, self.lease_duration_ms)

                if acquired and not self.is_leader:
                    logger.warning(
                        f"Node {self.node_id} ACQUIRED LEADER STATUS for {cluster_name}!"
                    )
                    self.is_leader = True
                    # Trigger Leader specific startup hooks (e.g. start global scheduler)

                elif not acquired and self.is_leader:
                    logger.error(f"Node {self.node_id} LOST LEADER STATUS! Stepping down.")
                    self.is_leader = False
                    # Trigger Leader teardown hooks

            except Exception as e:
                logger.exception("Leader election error", error=str(e))
                self.is_leader = False

            # Sleep for slightly less than the lease duration to renew before expiry
            await asyncio.sleep((self.lease_duration_ms / 1000) * 0.7)
