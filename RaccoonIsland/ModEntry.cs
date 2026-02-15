using System;
using System.Collections.Generic;
using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;
using StardewModdingAPI;
using StardewModdingAPI.Events;
using StardewValley;
using StardewValley.Buildings;
using StardewValley.Menus;
using StardewValley.Objects;
using StardewValley.TerrainFeatures;
using xTile;
using xTile.Layers;
using xTile.Tiles;
using SObject = StardewValley.Object;

namespace RaccoonIsland
{
    public class ModEntry : Mod
    {
        private const string LocationName = "RaccoonIsland";
        private Texture2D _statueTexture;
        private Texture2D _raccoonGodTexture;

        private const float CX = 40f, CY = 40f;
        private const float SwimStart = 27f;
        private bool _wasSwimming;

        private readonly Dictionary<string, List<LargeTerrainFeature>> _savedCustomFeatures = new();

        private Vector2 _hoverTile = new Vector2(-1, -1);
        private double _hoverStartTime;
        private string _hoverTreeName;

        private static readonly Dictionary<string, string> TreeNames = new Dictionary<string, string>
        {
            { "1", "Oak Tree" },
            { "2", "Maple Tree" },
            { "3", "Pine Tree" },
            { "6", "Coconut Palm" },
            { "628", "Cherry Tree" },
            { "629", "Apricot Tree" },
            { "630", "Orange Tree" },
            { "631", "Peach Tree" },
            { "632", "Pomegranate Tree" },
            { "633", "Apple Tree" },
        };

        public override void Entry(IModHelper helper)
        {
            helper.Events.GameLoop.GameLaunched += OnGameLaunched;
            helper.Events.GameLoop.SaveLoaded += OnSaveLoaded;
            helper.Events.GameLoop.Saving += OnSaving;
            helper.Events.GameLoop.Saved += OnSaved;
            helper.Events.GameLoop.DayStarted += OnDayStarted;
            helper.Events.Input.ButtonPressed += OnButtonPressed;
            helper.Events.Display.RenderedWorld += OnRenderedWorld;
            helper.Events.GameLoop.UpdateTicked += OnUpdateTicked;
            helper.Events.Display.RenderedHud += OnRenderedHud;
        }

        private void OnGameLaunched(object sender, GameLaunchedEventArgs e)
        {
            Monitor.Log("Raccoon Island mod launched!", LogLevel.Info);
        }

        private void OnButtonPressed(object sender, ButtonPressedEventArgs e)
        {
            if (!Context.IsWorldReady)
                return;

            if (e.Button == SButton.F7)
            {
                var tile = Game1.player.Tile;
                Monitor.Log($"[{Game1.currentLocation.Name}] X:{(int)tile.X} Y:{(int)tile.Y}", LogLevel.Alert);
            }
        }

        private GameLocation GetOrCreateLocation(string name, string asset, bool isOutdoors = true)
        {
            GameLocation loc = Game1.getLocationFromName(name);
            if (loc != null)
                return loc;
            loc = new GameLocation();
            loc.mapPath.Value = Helper.ModContent.GetInternalAssetName($"assets/{asset}").Name;
            loc.name.Value = name;
            loc.isOutdoors.Value = isOutdoors;
            Game1.locations.Add(loc);
            return loc;
        }

        private static bool HasWarpTo(GameLocation location, string targetName)
        {
            foreach (var w in location.warps)
                if (w.TargetName == targetName)
                    return true;
            return false;
        }

        private void OnSaveLoaded(object sender, SaveLoadedEventArgs e)
        {
            // Load textures
            RaccoonStatue.Sprite = Helper.ModContent.Load<Texture2D>("assets/raccoon_statue.png");
            MineEntrance.Sprite = Helper.ModContent.Load<Texture2D>("assets/mine_entrance.png");
            _statueTexture = RaccoonStatue.Sprite;

            // Get or create island (reuses saved location to preserve placed objects)
            GameLocation island = Game1.getLocationFromName(LocationName);
            bool isNew = island == null;
            if (isNew)
            {
                island = new GameLocation();
                island.mapPath.Value = Helper.ModContent.GetInternalAssetName("assets/RaccoonIsland.tmx").Name;
                island.name.Value = LocationName;
                island.waterColor.Value = new Color(0, 200, 180);
                Game1.locations.Add(island);
                SpawnForestTrees(island);
            }

            // Farm warp (only add once)
            GameLocation farm = Game1.getLocationFromName("Farm");
            if (farm != null && !HasWarpTo(farm, LocationName))
            {
                farm.warps.Add(new Warp(67, 20, LocationName, 40, 66, false));
                Monitor.Log("Added warp to Raccoon Island on the Farm.", LogLevel.Info);
            }

            // Raccoon statue portal at end of dock
            island.largeTerrainFeatures.Add(new RaccoonStatue(new Vector2(40, 72), "Farm", 67, 19));
            if (!HasWarpTo(island, "Farm"))
            {
                island.warps.Add(new Warp(40, 72, "Farm", 67, 19, false));
            }

            // Island warps (only add once)
            if (!HasWarpTo(island, "Beach"))
                island.warps.Add(new Warp(15, 11, "Beach", 40, 19, false));

            // Load tent interiors and place permanent tents
            var tents = new[]
            {
                new { Name = "Tent01", Asset = "TentInterior01", TileX = 51, TileY = 37, ExitX = 51 },
                new { Name = "Tent02", Asset = "TentInterior02", TileX = 48, TileY = 32, ExitX = 48 },
                new { Name = "Tent03", Asset = "TentInterior03", TileX = 43, TileY = 29, ExitX = 43 },
                new { Name = "Tent04", Asset = "TentInterior04", TileX = 36, TileY = 29, ExitX = 36 },
                new { Name = "Tent05", Asset = "TentInterior05", TileX = 32, TileY = 32, ExitX = 32 },
                new { Name = "Tent06", Asset = "TentInterior06", TileX = 29, TileY = 37, ExitX = 29 },
                new { Name = "Tent07", Asset = "TentInterior07", TileX = 29, TileY = 43, ExitX = 29 },
                new { Name = "Tent08", Asset = "TentInterior08", TileX = 32, TileY = 48, ExitX = 32 },
                new { Name = "Tent09", Asset = "TentInterior09", TileX = 36, TileY = 51, ExitX = 36 },
                new { Name = "Tent10", Asset = "TentInterior10", TileX = 43, TileY = 51, ExitX = 43 },
                new { Name = "Tent11", Asset = "TentInterior11", TileX = 48, TileY = 48, ExitX = 48 },
                new { Name = "Tent12", Asset = "TentInterior12", TileX = 51, TileY = 43, ExitX = 51 },
            };

            foreach (var t in tents)
            {
                // Remove any existing location with this name
                GameLocation existing = Game1.getLocationFromName(t.Name);
                if (existing != null)
                    Game1.locations.Remove(existing);

                // Create a new location using the FarmHouse map via the constructor
                GameLocation interior = new GameLocation("Maps/FarmHouse", t.Name);
                interior.isOutdoors.Value = false;
                Game1.locations.Add(interior);

                // Remove the vanilla warp property so it doesn't send to Farm
                if (interior.map != null && interior.map.Properties.ContainsKey("Warp"))
                    interior.map.Properties.Remove("Warp");

                PlaceJunimoHut(interior);

                island.largeTerrainFeatures.Add(
                    new PermanentTent(new Vector2(t.TileX, t.TileY), t.Name, 3, 8));

                interior.warps.Clear();
                interior.warps.Add(new Warp(3, 12, LocationName, t.ExitX, t.TileY + 1, false));
                interior.warps.Add(new Warp(3, 11, LocationName, t.ExitX, t.TileY + 1, false));
            }

            // Raccoon god statue at center of path intersection
            _raccoonGodTexture = Helper.ModContent.Load<Texture2D>("assets/raccoon_god.png");
            island.largeTerrainFeatures.Add(new RaccoonGodStatue(new Vector2(40, 40)));

            // Mine entrance at center of path intersection
            GameLocation mine = GetOrCreateLocation("RaccoonMine", "RaccoonMine.tmx", isOutdoors: false);
            island.largeTerrainFeatures.Add(new MineEntrance(new Vector2(40, 40), "RaccoonMine", 8, 2));
            mine.largeTerrainFeatures.Add(new MineEntrance(new Vector2(8, 1), LocationName, 40, 41));

            // Beach warp (only add once)
            GameLocation beach = Game1.getLocationFromName("Beach");
            if (beach != null && !HasWarpTo(beach, LocationName))
            {
                beach.warps.Add(new Warp(40, 20, LocationName, 15, 11, false));
                Monitor.Log("Added warp to Raccoon Island on the Beach.", LogLevel.Info);
            }

            Monitor.Log("Raccoon Island location added.", LogLevel.Info);
        }

        private void OnSaving(object sender, SavingEventArgs e)
        {
            _savedCustomFeatures.Clear();
            foreach (var location in Game1.locations)
            {
                var custom = new List<LargeTerrainFeature>();
                foreach (var feature in location.largeTerrainFeatures)
                {
                    if (feature is RaccoonStatue || feature is PermanentTent || feature is MineEntrance || feature is RaccoonGodStatue)
                        custom.Add(feature);
                }
                if (custom.Count > 0)
                {
                    _savedCustomFeatures[location.Name] = custom;
                    foreach (var f in custom)
                        location.largeTerrainFeatures.Remove(f);
                }
            }
        }

        private void OnSaved(object sender, SavedEventArgs e)
        {
            foreach (var kvp in _savedCustomFeatures)
            {
                var location = Game1.getLocationFromName(kvp.Key);
                if (location != null)
                {
                    foreach (var feature in kvp.Value)
                        location.largeTerrainFeatures.Add(feature);
                }
            }
            _savedCustomFeatures.Clear();
        }

        private void PlaceJunimoHut(GameLocation location)
        {
            try
            {
                // Place Junimo Hut furniture in top-right corner
                string hutId = null;
                foreach (var kvp in Game1.content.Load<Dictionary<string, string>>("Data\\Furniture"))
                {
                    if (kvp.Value.Contains("Junimo Hut") || kvp.Key.Contains("JunimoHut") || kvp.Key.Contains("Junimo_Hut"))
                    {
                        hutId = kvp.Key;
                        Monitor.Log($"Found Junimo Hut furniture: key={kvp.Key}, value={kvp.Value}", LogLevel.Trace);
                        break;
                    }
                }
                if (hutId != null)
                {
                    Furniture hut = new Furniture(hutId, new Vector2(8, 3));
                    location.furniture.Add(hut);
                    Monitor.Log($"Placed Junimo Hut ({hutId}) in {location.Name}", LogLevel.Trace);
                }
                else
                {
                    Monitor.Log("Could not find Junimo Hut in furniture data", LogLevel.Warn);
                }

                // Place Dark Cat Tree furniture
                Furniture catTree = new Furniture("DarkCatTree", new Vector2(1, 9));
                location.furniture.Add(catTree);

                // Place Long Elixir Table furniture in top-left corner
                string tableId = null;
                foreach (var kvp in Game1.content.Load<Dictionary<string, string>>("Data\\Furniture"))
                {
                    if (kvp.Value.Contains("Long Elixir Table") || kvp.Key.Contains("LongElixirTable") || kvp.Key.Contains("Long_Elixir_Table"))
                    {
                        tableId = kvp.Key;
                        Monitor.Log($"Found Long Elixir Table: key={kvp.Key}, value={kvp.Value}", LogLevel.Trace);
                        break;
                    }
                }
                if (tableId != null)
                {
                    Furniture table = new Furniture(tableId, new Vector2(1, 4));
                    location.furniture.Add(table);
                    Monitor.Log($"Placed Long Elixir Table ({tableId}) in {location.Name}", LogLevel.Trace);
                }
                else
                {
                    Monitor.Log("Could not find Long Elixir Table in furniture data", LogLevel.Warn);
                }

                Monitor.Log($"Placed Junimo Hut, Dark Cat Tree, and Long Elixir Table in {location.Name}", LogLevel.Trace);
            }
            catch (Exception ex)
            {
                Monitor.Log($"Failed to place Junimo Hut in {location.Name}: {ex.Message}", LogLevel.Warn);
            }
        }

        private void SpawnForestTrees(GameLocation island)
        {
            const int width = 80, height = 80;
            const float cx = 40f, cy = 40f;
            const float forestMin = 14f, beachMin = 22f;
            const int spacing = 2; // minimum tiles between trees (keeps fruit trees growing)
            // All tree types in a single pool for equal distribution
            // Wild: oak(1), maple(2), pine(3), coconut palm(6)
            // Fruit: pomegranate(632), apple(633), orange(630), cherry(628), apricot(629)
            string[] allTypes = { "1", "2", "3", "6", "632", "633", "630", "628", "629" };
            int treeCount = 0;
            int typeIndex = 0;

            var occupied = new HashSet<(int, int)>();

            for (int y = 0; y < height; y++)
            {
                for (int x = 0; x < width; x++)
                {
                    float dist = (float)Math.Sqrt((x - cx) * (x - cx) + (y - cy) * (y - cy));
                    if (dist <= forestMin || dist > beachMin)
                        continue;

                    if (x == 39 || x == 40 || y == 39 || y == 40)
                        continue;

                    if (occupied.Contains((x, y)))
                        continue;

                    var tile = new Vector2(x, y);
                    string type = allTypes[typeIndex % allTypes.Length];
                    typeIndex++;

                    int typeNum = int.Parse(type);
                    if (typeNum >= 628)
                    {
                        var ft = new FruitTree(type, 4);
                        ft.GreenHouseTileTree = true;
                        island.terrainFeatures[tile] = ft;
                    }
                    else
                    {
                        island.terrainFeatures[tile] = new Tree(type, Tree.treeStage);
                    }
                    treeCount++;

                    // Reserve surrounding tiles so no tree is placed within spacing distance
                    for (int dy = -spacing; dy <= spacing; dy++)
                        for (int dx = -spacing; dx <= spacing; dx++)
                            occupied.Add((x + dx, y + dy));
                }
            }

            Monitor.Log($"Spawned {treeCount} trees (9 types, equal distribution) on Raccoon Island.", LogLevel.Info);
        }

        private void OnDayStarted(object sender, DayStartedEventArgs e)
        {
            GameLocation island = Game1.getLocationFromName(LocationName);
            if (island == null)
                return;
            SpawnBeachForageables(island);
            SpawnTownForageables(island);
        }

        private void SpawnTownForageables(GameLocation island)
        {
            var rng = new Random((int)Game1.uniqueIDForThisGame + Game1.Date.TotalDays + 777);
            int count = rng.Next(4, 9);

            // Mixed pool: spring, summer, fall, desert, and ginger island forageables
            string[] pool =
            {
                // Spring
                "16",  // Wild Horseradish
                "18",  // Daffodil
                "20",  // Leek
                "22",  // Dandelion
                // Summer
                "396", // Spice Berry
                "398", // Grape
                "402", // Sweet Pea
                "259", // Fiddlehead Fern
                // Fall
                "281", // Common Mushroom
                "406", // Wild Plum
                "408", // Hazelnut
                "410", // Blackberry
                // Desert
                "88",  // Coconut
                "90",  // Cactus Fruit
                // Ginger Island
                "829", // Ginger
                "851", // Magma Cap
            };

            var townTiles = new List<Vector2>();
            for (int y = 0; y < 80; y++)
            {
                for (int x = 0; x < 80; x++)
                {
                    float dist = (float)Math.Sqrt((x - CX) * (x - CX) + (y - CY) * (y - CY));
                    if (dist > 5f && dist <= 12f && x != 39 && x != 40 && y != 39 && y != 40)
                        townTiles.Add(new Vector2(x, y));
                }
            }

            int spawned = 0;
            int attempts = 0;
            while (spawned < count && attempts < 200)
            {
                attempts++;
                var tile = townTiles[rng.Next(townTiles.Count)];
                if (island.objects.ContainsKey(tile) || island.terrainFeatures.ContainsKey(tile))
                    continue;

                string itemId = pool[rng.Next(pool.Length)];
                var obj = new SObject(itemId, 1);
                obj.IsSpawnedObject = true;
                island.objects.Add(tile, obj);
                spawned++;
            }

            Monitor.Log($"Spawned {spawned} town forageables on Raccoon Island.", LogLevel.Trace);
        }

        private void SpawnBeachForageables(GameLocation island)
        {
            var rng = new Random((int)Game1.uniqueIDForThisGame + Game1.Date.TotalDays);
            int count = rng.Next(3, 7);
            string season = Game1.currentSeason;

            // Beach forageables by season (item ID, cumulative weight)
            (string id, int weight)[] table;
            switch (season)
            {
                case "summer":
                    table = new[] { ("372", 43), ("719", 57), ("723", 71), ("718", 76), ("394", 100) };
                    break;
                case "winter":
                    table = new[] { ("392", 48), ("372", 72), ("719", 84), ("723", 96), ("718", 100) };
                    break;
                default: // spring, fall
                    table = new[] { ("372", 56), ("719", 75), ("723", 94), ("718", 100) };
                    break;
            }

            var beachTiles = new List<Vector2>();
            for (int y = 0; y < 80; y++)
            {
                for (int x = 0; x < 80; x++)
                {
                    float dist = (float)Math.Sqrt((x - CX) * (x - CX) + (y - CY) * (y - CY));
                    if (dist > 22f && dist <= 27f)
                        beachTiles.Add(new Vector2(x, y));
                }
            }

            int spawned = 0;
            int attempts = 0;
            while (spawned < count && attempts < 200)
            {
                attempts++;
                var tile = beachTiles[rng.Next(beachTiles.Count)];
                if (island.objects.ContainsKey(tile) || island.terrainFeatures.ContainsKey(tile))
                    continue;

                int roll = rng.Next(100);
                string itemId = table[table.Length - 1].id;
                foreach (var entry in table)
                {
                    if (roll < entry.weight)
                    {
                        itemId = entry.id;
                        break;
                    }
                }

                var obj = new SObject(itemId, 1);
                obj.IsSpawnedObject = true;
                island.objects.Add(tile, obj);
                spawned++;
            }

            Monitor.Log($"Spawned {spawned} beach forageables on Raccoon Island.", LogLevel.Trace);
        }

        private void OnUpdateTicked(object sender, UpdateTickedEventArgs e)
        {
            if (!Context.IsWorldReady)
                return;

            if (Game1.currentLocation?.Name != LocationName)
            {
                if (_wasSwimming)
                {
                    Game1.player.swimming.Value = false;
                    _wasSwimming = false;
                }
                _hoverTreeName = null;
                return;
            }

            var player = Game1.player;
            float px = player.Position.X / 64f;
            float py = player.Position.Y / 64f;
            float dist = (float)Math.Sqrt((px - CX) * (px - CX) + (py - CY) * (py - CY));
            bool onDock = (int)px >= 39 && (int)px <= 40 && (int)py >= 65 && (int)py <= 70;
            bool shouldSwim = dist > SwimStart && !onDock;

            if (shouldSwim && !_wasSwimming)
            {
                player.swimming.Value = true;
                _wasSwimming = true;
            }
            else if (!shouldSwim && _wasSwimming)
            {
                player.swimming.Value = false;
                _wasSwimming = false;
            }

            var cursorTile = Game1.currentCursorTile;

            if (cursorTile != _hoverTile)
            {
                _hoverTile = cursorTile;
                _hoverStartTime = Game1.currentGameTime.TotalGameTime.TotalSeconds;
                _hoverTreeName = null;
                return;
            }

            if (_hoverTreeName != null)
                return;

            double elapsed = Game1.currentGameTime.TotalGameTime.TotalSeconds - _hoverStartTime;
            if (elapsed < 3.0)
                return;

            var location = Game1.currentLocation;
            if (location.terrainFeatures.TryGetValue(cursorTile, out var feature))
            {
                if (feature is Tree tree && TreeNames.TryGetValue(tree.treeType.Value, out string name))
                    _hoverTreeName = name;
                else if (feature is FruitTree fruitTree && TreeNames.TryGetValue(fruitTree.treeId.Value, out string fruitName))
                    _hoverTreeName = fruitName;
            }
        }

        private void OnRenderedHud(object sender, RenderedHudEventArgs e)
        {
            if (_hoverTreeName == null)
                return;

            IClickableMenu.drawHoverText(e.SpriteBatch, _hoverTreeName, Game1.smallFont);
        }

        private void OnRenderedWorld(object sender, RenderedWorldEventArgs e)
        {
            if (!Context.IsWorldReady)
                return;

            if (Game1.currentLocation.Name == "Beach" && _statueTexture != null)
                DrawStatue(e.SpriteBatch, tileX: 40, tileY: 20);

            if (Game1.currentLocation.Name == "Farm" && _statueTexture != null)
                DrawStatue(e.SpriteBatch, tileX: 67, tileY: 20);

            if (Game1.currentLocation.Name == LocationName)
            {
                if (_raccoonGodTexture != null)
                    DrawRaccoonGod(e.SpriteBatch, tileX: 40, tileY: 40);
                if (_statueTexture != null)
                    DrawStatue(e.SpriteBatch, tileX: 40, tileY: 72);
            }
        }

        private void DrawStatue(SpriteBatch spriteBatch, int tileX, int tileY)
        {
            Vector2 worldPos = new Vector2(tileX * 64f, (tileY - 1) * 64f);
            Vector2 screenPos = Game1.GlobalToLocal(Game1.viewport, worldPos);
            float layerDepth = (tileY * 64f + 32f) / 10000f;

            spriteBatch.Draw(_statueTexture, screenPos,
                new Rectangle(0, 0, 16, 32), Color.White,
                0f, Vector2.Zero, Game1.pixelZoom,
                SpriteEffects.None, layerDepth);
        }

        private void DrawRaccoonGod(SpriteBatch spriteBatch, int tileX, int tileY)
        {
            Vector2 worldPos = new Vector2((tileX - 1) * 64f, (tileY - 4) * 64f);
            Vector2 screenPos = Game1.GlobalToLocal(Game1.viewport, worldPos);
            float layerDepth = (tileY + 1) * 64f / 10000f;

            spriteBatch.Draw(_raccoonGodTexture, screenPos,
                new Rectangle(0, 0, 48, 80), Color.White,
                0f, Vector2.Zero, 4f,
                SpriteEffects.None, layerDepth);
        }
    }
}
