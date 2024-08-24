import pygame
import json
PATH = 'data/maps/'


NEIGHBOR_OFFSETS = [(0, 0), (0, 1), (0, -1), (1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1)]
PHYSICS_TILES = {'zavod_0'}
AUTOTILING_TILES = {'zavod_0'}
AUTO_TILING = {
    tuple(sorted([(1, 0), (0, 1)])): 0,
    tuple(sorted([(-1, 0), (0, 1), (1, 0)])): 1,
    tuple(sorted([(-1, 0), (0, 1)])): 2,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(1, 0), (0, 1), (-1, 0), (0, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (-1, 0)])): 7,
    tuple(sorted([(-1, 0), (0, -1)])): 8,
    tuple(sorted([(1, 0)])): 9,
    tuple(sorted([(-1, 0)])): 10,
    tuple(sorted([(0, 1)])): 11,
    tuple(sorted([(0, -1)])): 12,
    tuple(sorted([(1, 0), (-1, 0)])): 13,
    tuple(sorted([(0, -1), (0, 1)])): 14,
}

AUTO_TILING = [
    {tuple(sorted([(1, 0)])): 9,
    tuple(sorted([(-1, 0)])): 10,
    tuple(sorted([(0, 1)])): 11,
    tuple(sorted([(0, -1)])): 12},
    {tuple(sorted([(1, 0), (-1, 0)])): 13,
    tuple(sorted([(0, -1), (0, 1)])): 14,
    tuple(sorted([(-1, 0), (0, -1)])): 8,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(-1, 0), (0, 1)])): 2,
    tuple(sorted([(1, 0), (0, 1)])): 0},
    {tuple(sorted([(1, 0), (0, -1), (-1, 0)])): 7,
     tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 5,
     tuple(sorted([(1, 0), (0, -1), (0, 1)])): 3,
     tuple(sorted([(-1, 0), (0, 1), (1, 0)])): 1},
    {tuple(sorted([(1, 0), (0, 1), (-1, 0), (0, -1)])): 4}
]

class Tilemap:
    def __init__(self, game, tile_size=32) -> None:
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

    def extract(self, id_pair, keep=False):
        mathces = []
        delete = []

        for tile in self.offgrid_tiles.copy():
            if (tile['type'], tile['vatiant']) in id_pair:
                mathces.append(tile.copy())
                if not keep:
                    delete.append(tile)
        
        for tile in delete:
            self.offgrid_tiles.remove(tile)
        
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if (tile['type'], tile['variant']) in id_pair:
                mathces.append(tile.copy())
                mathces[-1]['pos'] = mathces[-1]['pos'].copy()
                mathces[-1]['pos'][0] *= self.tile_size
                mathces[-1]['pos'][1] *= self.tile_size
                if not keep:
                    delete.append(loc)
        
        for loc in delete:
            del self.tilemap[loc]

        return mathces
    
    def tiles_around(self, pos):
        tiles = []
        tile_loc = [int(pos[0] // self.tile_size), int(pos[1] // self.tile_size)]
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles

    def physics_tiles_around(self, pos):
        tiles = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                tiles.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return tiles
    
    def auto_tiling(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            tile_type = tile['type']
            tiling = set()

            if tile_type in AUTOTILING_TILES:

                for offset in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    check_loc = str(tile['pos'][0] + offset[0]) + ';' + str(tile['pos'][1] + offset[1])
                    if check_loc in self.tilemap:
                        if self.tilemap[check_loc]['type'] == tile_type:
                            tiling.add(offset)
                
                if tiling:
                    tile['variant'] = AUTO_TILING[len(tiling) - 1][tuple(sorted(tiling))]
                else:
                    tile['variant'] = 15

    def render(self, surf, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
        
        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))

    def load(self, path):
        f = open(path, 'r')
        map_data =json.load(f)
        f.close()

        self.tile_size = map_data['tile_size']
        self.tilemap = map_data['tilemap']
        self.offgrid_tiles = map_data['offgrid']