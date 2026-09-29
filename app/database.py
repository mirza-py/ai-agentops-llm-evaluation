from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Boolean,
    Text
)

from sqlalchemy.orm import (
    declarative_base,
    sessionmaker
)


DATABASE_URL = "sqlite:///./agentops.db"


engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()


class EvaluationLog(Base):

    __tablename__ = "evaluation_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    prompt = Column(
        Text,
        nullable=False
    )

    response = Column(
        Text,
        nullable=False
    )

    model = Column(
        String,
        nullable=False
    )

    prompt_version = Column(
        String,
        default="v1"
    )

    latency_seconds = Column(
        Float
    )

    relevance = Column(
        Float
    )

    accuracy = Column(
        Float
    )

    completeness = Column(
        Float
    )

    clarity = Column(
        Float
    )

    quality_score = Column(
        Float
    )

    failure = Column(
        Boolean,
        default=False
    )

    failure_reason = Column(
        Text,
        nullable=True
    )


Base.metadata.create_all(
    bind=engine
)