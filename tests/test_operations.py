import unittest
import numpy
from amulet.api.selection import SelectionGroup, SelectionBox
from amulet.api.level import World
from amulet_map_editor.programs.edit.plugins.operations.stock_plugins.internal_operations.copy import copy
from amulet_map_editor.programs.edit.plugins.operations.stock_plugins.internal_operations.cut import cut
from amulet_map_editor.programs.edit.plugins.operations.stock_plugins.internal_operations.delete import delete
from amulet.api.structure import structure_cache

from amulet.api.wrapper import WorldFormatWrapper

class MockWorld(World):
    def __init__(self, tempdir):
        self._level_wrapper = MockLevelWrapper()
        super().__init__(tempdir, self._level_wrapper)
        from amulet.api.block import Block
        self.block_palette.get_add_block(Block("minecraft", "air"))

    def get_chunk_slice_box(self, dimension, selection, create=True):
        for cx, cz in selection.chunk_locations():
            yield self.get_chunk(cx, cz, dimension), (slice(0, 16), slice(0, 16), slice(0, 16)), selection

    def extract_structure_iter(self, selection, dimension):
        yield 0.5
        return MockStructure()

    def get_chunk(self, cx, cz, dimension):
        return MockChunk(cx, cz)

class MockChunk:
    def __init__(self, cx, cz):
        self.coordinates = (cx, cz)
        self.blocks = numpy.zeros((16, 16, 16))
        self.block_entities = {}
        self.changed = False

class MockLevelWrapper(WorldFormatWrapper):
    def __init__(self):
        pass

    @property
    def level_name(self) -> str:
        return "mock"

    def open(self):
        pass

    def close(self):
        pass

    def save(self, wrapper: "WorldFormatWrapper", path: str):
        pass

    def _close(self):
        pass

    def _create(self, path: str, *args, **kwargs):
        pass

    def _delete_chunk(self, cx: int, cz: int, dimension: str):
        pass

    def _get_raw_chunk_data(self, cx: int, cz: int, dimension: str) -> bytes:
        return b""

    def _get_raw_player_data(self, player_id: str) -> bytes:
        return b""

    def _load_player(self, player_id: str):
        pass

    def _open(self, path: str, *args, **kwargs):
        pass

    def _put_raw_chunk_data(self, cx: int, cz: int, data: bytes, dimension: str):
        pass

    def _save(self):
        pass

    def all_chunk_coords(self, dimension: str):
        return []

    def all_player_ids(self):
        return []

    @property
    def dimensions(self) -> list[str]:
        return ["overworld"]

    @property
    def game_version_string(self) -> str:
        return "mock"

    def has_chunk(self, cx: int, cz: int, dimension: str) -> bool:
        return True

    def has_player(self, player_id: str) -> bool:
        return False

    @property
    def is_valid(self) -> bool:
        return True

    @property
    def last_played(self) -> int:
        return 0

    def unload(self):
        pass

    @property
    def valid_formats(self) -> dict[str, str]:
        return {}

from amulet.api.level import BaseLevel

class MockStructure(BaseLevel):
    def __init__(self):
        self._dimensions = ["overworld"]

    @property
    def dimensions(self):
        return self._dimensions

    def _get_obj_doc(self, doc_name: str) -> dict:
        return {}

    def has_chunk(self, cx: int, cz: int, dimension: str) -> bool:
        return False

    def _put_raw_chunk_data(self, cx: int, cz: int, data: bytes, dimension: str):
        pass

    def _get_raw_chunk_data(self, cx: int, cz: int, dimension: str) -> bytes:
        return b""

class OperationTest(unittest.TestCase):
    def setUp(self):
        self.world = MockWorld("temp")
        self.dimension = "overworld"
        self.selection = SelectionGroup([SelectionBox((0,0,0), (16,16,16))])

    def test_copy(self):
        from amulet_map_editor.programs.edit.api.operations import OperationSilentAbort

        op = copy(self.world, self.dimension, self.selection)
        with self.assertRaises(OperationSilentAbort):
            while True:
                next(op)
        self.assertIsNotNone(structure_cache.get_structure())

    def test_cut(self):
        op = cut(self.world, self.dimension, self.selection)
        with self.assertRaises(StopIteration):
            while True:
                next(op)
        self.assertIsNotNone(structure_cache.get_structure())

    def test_delete(self):
        op = delete(self.world, self.dimension, self.selection)
        with self.assertRaises(StopIteration):
            while True:
                next(op)

if __name__ == '__main__':
    unittest.main()
