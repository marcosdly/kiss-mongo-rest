"""Utility variables/functions/classes related to IO operations,
like path resolution."""

from os import path
from dataclasses import dataclass

@dataclass(init=False, frozen=True)
class StaticPaths:
    CONFIG: str = path.abspath(path.join(path.dirname(__file__), "..", "config"))

@dataclass(init=False, frozen=True)
class ConfigFiles:
    HYPERCORN: str = path.join(StaticPaths.CONFIG, "hypercorn.toml")