from __future__ import annotations

from typing import TYPE_CHECKING
import numpy

from amulet.api.selection import SelectionGroup
from amulet.api.block import UniversalAirBlock
from amulet.api.data_types import Dimension, OperationReturnType

if TYPE_CHECKING:
    from amulet.api.level import BaseLevel


def delete(
    world: "BaseLevel", dimension: Dimension, selection: SelectionGroup
) -> OperationReturnType:
    air = world.block_palette.get_add_block(UniversalAirBlock)
    air_array = numpy.array(air).astype(numpy.uint32)

    iter_count = len(list(world.get_chunk_slice_box(dimension, selection, False)))
    count = 0

    for chunk, slices, _ in world.get_chunk_slice_box(dimension, selection, False):
        chunk.blocks[slices] = air_array

        if chunk.block_entities:
            for block_entity in list(chunk.block_entities.values()):
                if block_entity.location in selection:
                    del chunk.block_entities[block_entity.location]

        chunk.changed = True
        count += 1
        yield count / iter_count
