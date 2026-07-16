import datetime
import enum
import uuid

from sqlalchemy import JSON, Boolean, DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dronzer.infrastructure.database.base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin


class ClusterRole(str, enum.Enum):
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"
    REPLICA = "REPLICA"
    DISASTER_RECOVERY = "DISASTER_RECOVERY"


class NodeStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    DRAINING = "DRAINING"
    MAINTENANCE = "MAINTENANCE"
    OFFLINE = "OFFLINE"


class ClusterTopology(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Defines a logical Dronzer cluster deployed in a specific geographical region or cloud provider.
    """

    __tablename__ = "clusters"

    name: Mapped[str] = mapped_column(String(255), unique=True)
    region: Mapped[str] = mapped_column(String(100))  # e.g. "us-east-1", "eu-central-1"
    provider: Mapped[str] = mapped_column(String(100))  # e.g. "aws", "gcp", "azure", "bare-metal"

    role: Mapped[ClusterRole] = mapped_column(Enum(ClusterRole), default=ClusterRole.PRIMARY)

    is_maintenance_mode: Mapped[bool] = mapped_column(Boolean, default=False)

    labels: Mapped[dict] = mapped_column(JSON, default=dict)

    nodes: Mapped[list["ClusterNode"]] = relationship("ClusterNode", back_populates="cluster")


class ClusterNode(Base, UUIDMixin, TimestampMixin):
    """
    Represents an individual compute node (e.g., a Kubernetes Pod or Bare Metal VM)
    running the Dronzer Gateway inside a Cluster.
    """

    __tablename__ = "nodes"

    cluster_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("clusters.id", ondelete="CASCADE"), index=True
    )

    hostname: Mapped[str] = mapped_column(String(255))
    ip_address: Mapped[str] = mapped_column(String(50))

    status: Mapped[NodeStatus] = mapped_column(Enum(NodeStatus), default=NodeStatus.ACTIVE)

    last_heartbeat: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )

    capabilities: Mapped[dict] = mapped_column(
        JSON, default=dict
    )  # e.g. {"gpu": true, "memory_gb": 64}
    labels: Mapped[dict] = mapped_column(JSON, default=dict)

    cluster: Mapped["ClusterTopology"] = relationship("ClusterTopology", back_populates="nodes")
