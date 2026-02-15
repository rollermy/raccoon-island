# Raccoon Island — Stardew Valley Mod

## Build

```sh
cd RaccoonIsland
export PATH="/opt/homebrew/opt/dotnet@6/bin:$PATH"
export DOTNET_ROOT="/opt/homebrew/opt/dotnet@6/libexec"
dotnet build
```

Build auto-deploys to `~/Library/Application Support/Steam/steamapps/common/Stardew Valley/Contents/MacOS/Mods/RaccoonIsland`.

## Map Generation

```sh
cd RaccoonIsland
python3 generate_map.py
```

Regenerates `assets/RaccoonIsland.tmx` (60x60 concentric island layout).

## Game Locations

The mod creates these custom locations:

- **RaccoonIsland** — main outdoor island (60x60 concentric ring layout)
- **TentNW** — interior for northwest tent
- **TentNE** — interior for northeast tent

[//]: # (### Warpshttps://stardewvalleywiki.com/Long_Elixir_Table)

- Farm (67,20) → RaccoonIsland (30,56)
- RaccoonIsland (28-31, 59) → Farm (67,19)
- Beach (40,20) → RaccoonIsland (5,1)
- RaccoonIsland (5,1) → Beach (40,19)
- RaccoonIsland (24,24) → TentNW interior
- RaccoonIsland (35,24) → TentNE interior

###Island Zones (distancem from center 30,30)

- Town center (dist ≤ 14): grass, paths, plaza, buildings
- Forest ring (14 < dist ≤ 22): trees (TerrainFeature objects)
- Beach ring (22 < dist ≤ 27): sandy beach
- Swimming zone (27 < dist ≤ 32): walkable ocean, player swims
- Deep ocean (dist > 32): blocked by Buildings layer