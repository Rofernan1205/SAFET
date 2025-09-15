# alembic/env.py (versión recomendada)
from logging.config import fileConfig
import os
from sqlalchemy import engine_from_config, pool
from alembic import context

from dotenv import load_dotenv
load_dotenv()

# Alembic config
config = context.config

# Si existe DATABASE_URL en .env, lo aplicamos a la config de alembic
db_url = os.getenv("DATABASE_URL")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Importa Base y tus modelos para que target_metadata conozca todo
# Asegúrate que models.models usa exactamente el mismo Base de database.connection
from database.connection import Base
# importa tu módulo de modelos (evitar wildcard import si puedes)
# from models import models as models_module
# opcional: importa clases concretas para evitar efectos colaterales
from models.models import *

target_metadata = Base.metadata

# Opciones comunes para que autogenerate detecte cambios de tipo y defaults
compare_kwargs = {
    "compare_type": True,
    "compare_server_default": True,
}

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        **compare_kwargs
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # Detectar si es sqlite para habilitar render_as_batch
    url = config.get_main_option("sqlalchemy.url") or ""
    is_sqlite = url.startswith("sqlite://")

    with connectable.connect() as connection:
        if is_sqlite:
            # render_as_batch ayuda con ALTER TABLE en sqlite
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                render_as_batch=True,
                **compare_kwargs
            )
        else:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                **compare_kwargs
            )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
