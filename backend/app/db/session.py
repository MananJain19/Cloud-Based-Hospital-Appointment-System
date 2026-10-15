database_url = settings.database_url

if database_url.startswith("postgres://"):
    database_url = database_url.replace(
        "postgres://", "postgresql+asyncpg://", 1
    )
elif database_url.startswith("postgresql://"):
    database_url = database_url.replace(
        "postgresql://", "postgresql+asyncpg://", 1
    )

_is_sqlite = database_url.startswith("sqlite")

_connect_args = (
    {"statement_cache_size": 0}
    if database_url.startswith("postgresql+asyncpg://")
    else {}
)

engine = create_async_engine(
    database_url,
    pool_pre_ping=True,
    connect_args=_connect_args,
    **(
        {"poolclass": NullPool}
        if _is_sqlite
        else {"pool_size": 1, "max_overflow": 0}
    ),
)
