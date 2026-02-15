using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using StardewValley;
using StardewValley.TerrainFeatures;

namespace RaccoonIsland
{
    public class RaccoonGodStatue : LargeTerrainFeature
    {
        public RaccoonGodStatue()
            : base(needsTick: false)
        {
        }

        public RaccoonGodStatue(Vector2 tileLocation)
            : base(needsTick: false)
        {
            Tile = tileLocation;
        }

        public override Rectangle getBoundingBox()
        {
            Vector2 t = Tile;
            return new Rectangle((int)(t.X - 1) * 64, (int)(t.Y - 4) * 64, 192, 320);
        }

        public override void draw(SpriteBatch spriteBatch)
        {
        }
    }
}
