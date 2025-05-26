# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from ..Config import Config
from ..core.logger import logging

LOGS = logging.getLogger(__name__)

# Initialize BASE at module level
BASE = declarative_base()
SESSION = None

def start() -> scoped_session:
    """Initialize database connection and return scoped session"""
    if not Config.DB_URI:
        raise ValueError("DB_URI not configured in Config!")
    
    # Fix postgres:// to postgresql:// if needed
    database_url = (
        Config.DB_URI.replace("postgres://", "postgresql://")
        if Config.DB_URI.startswith("postgres://")
        else Config.DB_URI
    )
    
    try:
        engine = create_engine(database_url)
        BASE.metadata.bind = engine
        BASE.metadata.create_all(engine)
        return scoped_session(
            sessionmaker(bind=engine, autoflush=False)
        )
    except Exception as e:
        LOGS.error("Failed to initialize database: %s", str(e))
        raise

# Initialize database connection
try:
    SESSION = start()
except Exception as e:
    LOGS.error("Database initialization failed: %s", str(e))
    # You may want to set SESSION to None or raise depending on your needs
    SESSION = None
    raise  # Remove this if you want the bot to run without DB
