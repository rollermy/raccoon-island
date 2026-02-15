using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using StardewValley;
using StardewValley.TerrainFeatures;

namespace RaccoonIsland
{
    public class MineEntrance : LargeTerrainFeature
    {
        public static Texture2D Sprite;

        private readonly string _targetLocation;
        private readonly int _targetX;
        private readonly int _targetY;

        public MineEntrance()
            : base(needsTick: false)
        {
        }

        public MineEntrance(Vector2 tileLocation, string targetLocation, int targetX, int targetY)
            : base(needsTick: false)
        {
            Tile = tileLocation;
            _targetLocation = targetLocation;
            _targetX = targetX;
            _targetY = targetY;
        }

        public override Rectangle getBoundingBox()
        {
            return Rectangle.Empty;
        }

        public override bool performUseAction(Vector2 tileLocation)
        {
            if (_targetLocation != null)
            {
                Game1.warpFarmer(_targetLocation, _targetX, _targetY, false);
                return true;
            }
            return base.performUseAction(tileLocation);
        }

        public override void draw(SpriteBatch spriteBatch)
        {
            if (Sprite == null)
                return;

            Vector2 t = Tile;
            spriteBatch.Draw(Sprite,
                Game1.GlobalToLocal(t * 64f),
                new Rectangle(0, 0, 16, 16), Color.White,
                0f, Vector2.Zero, Game1.pixelZoom,
                SpriteEffects.None, t.Y * 64f / 10000f);
        }
    }
}
