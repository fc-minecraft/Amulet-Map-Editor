from typing import TYPE_CHECKING

from amulet.api.structure import structure_cache
from amulet.api.data_types import Dimension, OperationReturnType
from amulet.api.selection import SelectionGroup
from .delete import delete
from amulet_map_editor.programs.edit.api.operations import OperationError

if TYPE_CHECKING:
    from amulet.api.level import BaseLevel


def cut(
    world: "BaseLevel", dimension: Dimension, selection: SelectionGroup
) -> OperationReturnType:
    if selection:
        yield 0, "Copying"
        structure = yield from world.extract_structure_iter(selection, dimension)
        structure_cache.add_structure(structure, structure.dimensions[0])
        yield 0, "Deleting"
        yield from delete(
            world,
            dimension,
            selection,
        )
    else:
        raise OperationError(
            "At least one selection is required for the copy operation."
        )
