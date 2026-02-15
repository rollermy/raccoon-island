using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using StardewValley;
using StardewValley.TerrainFeatures;

namespace RaccoonIsland
{
    /// <summary>
    /// A permanent tent using the vanilla Tent Kit sprite (from Cursors_1_6).
    /// Right-click to enter the tent interior.
    /// </summary>
    public class PermanentTent : LargeTerrainFeature
    {
        private readonly string _interiorName;
        private readonly int _entryX;
        private readonly int _entryY;

        public PermanentTent()
            : base(needsTick: false)
        {
        }

        public PermanentTent(Vector2 tileLocation, string interiorName, int entryX, int entryY)
            : base(needsTick: false)
        {
            Tile = tileLocation;
            _interiorName = interiorName;
            _entryX = entryX;
            _entryY = entryY;
        }

        public override Rectangle getBoundingBox()
        {
            Vector2 t = Tile;
            return new Rectangle((int)(t.X - 1f) * 64, (int)(t.Y - 1f) * 64, 192, 128);
        }

        public override bool performUseAction(Vector2 tileLocation)
        {
            if (_interiorName != null)
            {
                Game1.warpFarmer(_interiorName, _entryX, _entryY, false);
                return true;
            }
            return base.performUseAction(tileLocation);
        }

        public override void draw(SpriteBatch spriteBatch)
        {
            Vector2 t = Tile;
            // Back layer: tent interior/shadow (drawn behind player)
            spriteBatch.Draw(Game1.mouseCursors_1_6,
                Game1.GlobalToLocal(t * 64f + new Vector2(-2f, -1f) * 64f),
                new Rectangle(48, 208, 64, 48), Color.White,
                0f, Vector2.Zero, 4f, SpriteEffects.None, 0.0001f);
            // Front layer: tent canvas (drawn at tile depth, above player when behind)
            spriteBatch.Draw(Game1.mouseCursors_1_6,
                Game1.GlobalToLocal(t * 64f + new Vector2(-1f, -3f) * 64f),
                new Rectangle(0, 192, 48, 64), Color.White,
                0f, Vector2.Zero, 4f, SpriteEffects.None, t.Y * 64f / 10000f);
        }
    }
}
