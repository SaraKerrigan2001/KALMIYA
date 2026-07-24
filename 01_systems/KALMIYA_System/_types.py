"""
KALMIYA Custom Types

Define TypeAlias centralizados para reutilización en toda la aplicación.
Esto mantiene consistencia de tipos y facilita cambios globales.
"""

from typing import TypeAlias

# Device/Network types
DeviceDict: TypeAlias = dict[str, str | int]
"""Device info dict with ip, mac, hostname, port."""

SecurityScan: TypeAlias = list[DeviceDict]
"""List of scanned devices."""

NetworkInfo: TypeAlias = dict[str, str | int | list]
"""Network information dict."""

# Data types
ThoughtRecord: TypeAlias = dict[str, str]
"""Neural thought record with timestamp and content."""

CommandLog: TypeAlias = dict[str, str]
"""Command history with timestamp, command, response."""

UserMemory: TypeAlias = dict[str, str]
"""User memory key-value pairs."""

# Response types
AIResponse: TypeAlias = dict[str, str | int | bool]
"""Response from AI engine with content, tokens, etc."""

ConversationEntry: TypeAlias = dict[str, str]
"""Single message in conversation history."""

# Configuration types
ConfigDict: TypeAlias = dict[str, str | int | bool]
"""Configuration settings."""

# Generic types
JsonData: TypeAlias = dict[str, any] | list[any]
"""JSON-serializable data."""

CallbackFn: TypeAlias = callable[[str], None]
"""Generic callback function."""
