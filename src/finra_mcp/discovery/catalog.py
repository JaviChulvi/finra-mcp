"""Local FINRA Query API catalog snapshot helpers."""

from __future__ import annotations

import json
from functools import lru_cache
from importlib import resources
from typing import Any


@lru_cache(maxsize=1)
def load_catalog() -> dict[str, Any]:
    """Load the bundled FINRA Query API catalog snapshot."""
    catalog_path = resources.files("finra_mcp.data").joinpath("dataset_catalog.json")
    return json.loads(catalog_path.read_text(encoding="utf-8"))


def list_groups() -> list[dict[str, Any]]:
    catalog = load_catalog()
    groups = []
    for group in catalog.get("groups", []):
        groups.append(
            {
                "group": group["group"],
                "label": group.get("label", group["group"]),
                "dataset_count": len(group.get("datasets", [])),
                "dataset_name_count": sum(
                    len(dataset.get("variants", [])) for dataset in group["datasets"]
                ),
                "documentation_categories": group.get("documentation_categories", []),
            }
        )
    return groups


def iter_logical_datasets(group: str | None = None):
    for group_entry in load_catalog().get("groups", []):
        if group and group_entry["group"] != group:
            continue
        yield from group_entry.get("datasets", [])


def iter_dataset_names(group: str | None = None):
    for dataset in iter_logical_datasets(group):
        for variant in dataset.get("variants", []):
            yield dataset, variant


def list_datasets(
    group: str | None = None, *, include_variants: bool = True
) -> list[dict[str, Any]]:
    datasets = []
    for dataset in iter_logical_datasets(group):
        item = {
            "group": dataset["group"],
            "dataset": dataset["dataset"],
            "title": dataset["title"],
            "description": dataset.get("description"),
            "documentation_url": dataset.get("documentation_url"),
            "metadata_endpoint": dataset.get("metadata_endpoint_pattern"),
            "data_endpoint": dataset.get("endpoint_pattern"),
            "variant_count": len(dataset.get("variants", [])),
        }
        if include_variants:
            item["variants"] = [
                {
                    "kind": variant["kind"],
                    "name": variant["name"],
                    "data_endpoint": variant["data_endpoint"],
                    "metadata_endpoint": variant["metadata_endpoint"],
                    "field_count": variant.get("field_count", 0),
                    "metadata_available": variant.get("metadata_available", False),
                }
                for variant in dataset.get("variants", [])
            ]
        datasets.append(item)
    return datasets


def find_dataset(group: str, dataset_name: str) -> dict[str, Any] | None:
    for dataset in iter_logical_datasets(group):
        if dataset.get("dataset") == dataset_name:
            return dataset
        for variant in dataset.get("variants", []):
            if variant.get("name") == dataset_name:
                item = dict(dataset)
                item["selected_variant"] = variant
                return item
    return None


def fields_from_catalog(group: str, dataset_name: str) -> list[dict[str, Any]]:
    dataset = find_dataset(group, dataset_name)
    if not dataset:
        return []
    selected = dataset.get("selected_variant")
    if selected:
        return selected.get("fields", [])
    variants = dataset.get("variants", [])
    return variants[0].get("fields", []) if variants else []
