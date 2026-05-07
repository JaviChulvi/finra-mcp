"""Metadata helpers for FINRA Query API datasets."""

from __future__ import annotations

from typing import Any


def normalize_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    """Return a compact, MCP-friendly metadata summary."""
    fields = metadata.get("fields") or []
    return {
        "dataset_group": metadata.get("datasetGroup") or metadata.get("group"),
        "dataset_name": metadata.get("datasetName") or metadata.get("name"),
        "description": metadata.get("description"),
        "partition_fields": metadata.get("partitionFields") or [],
        "primary_id_field": metadata.get("primaryIdField")
        or metadata.get("primaryKeyField")
        or metadata.get("primaryKey"),
        "fields": fields,
        "field_count": len(fields),
        "supports": {key: value for key, value in metadata.items() if key.startswith("supports")},
        "raw": metadata,
    }


def field_names(metadata: dict[str, Any]) -> list[str]:
    fields = metadata.get("fields") or []
    return [field["name"] for field in fields if isinstance(field, dict) and field.get("name")]
