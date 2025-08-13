import arcade
import os
from start_view import StartView

# Configuracion del juego
MAP_WIDTH = 30 * 70
MAP_HEIGHT = 20 * 70
TILE_SIZE = 70

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 980
SCREEN_TITLE = "Pingu Academy"

# Fisica
PLAYER_MOVEMENT_SPEED = 6
GRAVITY = 1
PLAYER_JUMP_SPEED = 20
TILE_SCALING = 0.5

# Rutas
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
IMAGES_DIR = os.path.join(ASSETS_DIR, 'imagenes')
MAPS_DIR = os.path.join(ASSETS_DIR, 'maps')

# Enemigo que dispara balas verticales hacia abajo
class EnemySprite(arcade.Sprite):
    # Inicializa el enemigo con imagen, escala, lista de balas y tiempo entre disparos
    def __init__(self, image_file, scale, bullet_list, time_between_firing):
        super().__init__(image_file, scale=scale)
        self.time_since_last_firing = 0.0
        self.time_between_firing = time_between_firing
        self.bullet_list = bullet_list

    # Actualiza el enemigo cada frame, controlando cuando dispara
    def update(self, delta_time: float = 1 / 60):
        self.time_since_last_firing += delta_time

        if self.time_since_last_firing >= self.time_between_firing:
            self.time_since_last_firing = 0.0

            bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png")
            bullet.center_x = self.center_x
            bullet.angle = 90
            bullet.top = self.bottom
            bullet.change_y = -5
            self.bullet_list.append(bullet)

# Enemigo que dispara balas horizontales hacia la izquierda
class EnemySprite2(arcade.Sprite):
    # Inicializa el segundo tipo de enemigo con configuracion similar al primero
    def __init__(self, image_file, scale, bullet_list, time_between_firing):
        super().__init__(image_file, scale=scale)
        self.time_since_last_firing = 0.0
        self.time_between_firing = time_between_firing
        self.bullet_list = bullet_list

    # Actualiza el enemigo y crea balas horizontales en lugar de verticales
    def update(self, delta_time: float = 1 / 60):
        self.time_since_last_firing += delta_time

        if self.time_since_last_firing >= self.time_between_firing:
            self.time_since_last_firing = 0.0

            bullet = arcade.Sprite("../assets/imagenes/paloma.png", scale=0.5)
            bullet.center_x = self.center_x
            bullet.angle = 0
            bullet.top = self.bottom
            bullet.change_x = -5
            self.bullet_list.append(bullet)

# Pantalla que se muestra cuando el juego termina
class GameOverView(arcade.View):
    # Inicializa la pantalla final con puntuacion y mensaje personalizado
    def __init__(self, final_score: int = 0, message: str = "Fin del juego"):
        super().__init__()
        self.final_score = final_score
        self.message = message
        arcade.set_background_color(arcade.color.DARK_BLUE)

        self.logo = None
        try:
            ruta_logo = os.path.join(IMAGES_DIR, "pinguino.png")
            if os.path.exists(ruta_logo):
                self.logo = arcade.load_texture(ruta_logo)
        except Exception:
            self.logo = None

        self.logo_sprite = arcade.Sprite()
        if self.logo:
            self.logo_sprite.texture = self.logo
        self.logo_list = arcade.SpriteList()

        self.base_y = None
        self.text_y = None
        self._float_dir = 1
        self._float_speed = 1
        self._float_range = 20

    # Configura la posicion inicial de elementos cuando se muestra la vista
    def on_show_view(self):
        w, h = self.window.width, self.window.height
        if self.logo:
            self.logo_sprite.center_x = w // 2
            self.logo_sprite.center_y = h // 2 + 110
            if not self.logo_list:
                self.logo_list.append(self.logo_sprite)
        self.base_y = h // 2 + 40
        self.text_y = self.base_y

    # Dibuja todos los elementos de la pantalla final en cada frame
    def on_draw(self):
        self.clear()
        self.logo_list.draw()
        w, h = self.window.width, self.window.height

        arcade.draw_text(self.message, w/2, self.text_y,
                        arcade.color.BLACK, 40, anchor_x="center", font_name="Arial")

        arcade.draw_text(f"Monedas: {self.final_score}", w/2, h/2 - 20,
                        arcade.color.BLACK, 24, anchor_x="center", font_name="Arial")

        arcade.draw_text("ENTER: Volver al Inicio   |   ESC: Salir",
                        w/2, h/2 - 70, arcade.color.BLACK, 16,
                        anchor_x="center", font_name="Arial")

    # Actualiza la animacion de flotacion del texto principal
    def on_update(self, dt: float):
        self.text_y += self._float_speed * self._float_dir
        if self.text_y > self.base_y + self._float_range:
            self._float_dir = -1
        elif self.text_y < self.base_y - self._float_range:
            self._float_dir = 1

    # Maneja las teclas presionadas para navegar o salir del juego
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            try:
                self.window.show_view(StartView(make_game_view=lambda: GameView()))
            except Exception:
                self.window.show_view(StartView())
        elif key == arcade.key.ESCAPE:
            arcade.exit()

# Sprite del jugador con animaciones basadas en archivos PNG individuales
class AnimatedPlayer(arcade.Sprite):
    # Inicializa el jugador con sistema de animaciones y estados de movimiento
    def __init__(self, scale=1.0):
        super().__init__(scale=scale)
        self.animations = {}
        self.current_animation = "idle_right"
        self.animation_frame = 0
        self.animation_timer = 0.0
        self.animation_speed = 0.3

        self.facing_direction = 1
        self.is_moving = False
        self.is_jumping = False

        self.load_animations()
        self.set_animation("idle_right")
        if "idle_right" in self.animations and self.animations["idle_right"]:
            self.texture = self.animations["idle_right"][0]

    # Carga todas las texturas de animacion desde archivos PNG
    def load_animations(self):
        animation_files = [
            ("idle_right", "idle-right.png"),
            ("idle_left", "idle-left.png"),
            ("walk_right", "walking-right1.png"),
            ("walk_right", "walking-right2.png"),
            ("walk_left", "walking-left1.png"),
            ("walk_left", "walking-left2.png"),
            ("jump_right", "jump-right.png"),
            ("jump_left", "jump-left.png"),
        ]
        
        for anim_name in ["idle_right", "idle_left", "walk_right", "walk_left", "jump_right", "jump_left"]:
            self.animations[anim_name] = []
            
        for anim_name, filename in animation_files:
            file_path = os.path.join(IMAGES_DIR, filename)
            try:
                if os.path.exists(file_path):
                    texture = arcade.load_texture(file_path)
                    self.animations[anim_name].append(texture)
            except Exception:
                pass

        loaded_any = any(len(frames) > 0 for frames in self.animations.values())
        if not loaded_any:
            fallback = arcade.Texture.create_filled("player_fallback", (50, 50), arcade.color.BLUE)
            for anim_name in self.animations.keys():
                if not self.animations[anim_name]:
                    self.animations[anim_name] = [fallback]

    # Cambia la animacion actual del jugador
    def set_animation(self, animation_name):
        if animation_name in self.animations:
            textures = self.animations[animation_name]
            if textures:
                self.current_animation = animation_name
                self.animation_frame = 0
                self.animation_timer = 0.0
                self.texture = textures[0]

    # Actualiza los frames de la animacion basado en el tiempo transcurrido
    def update_animation(self, delta_time):
        if self.current_animation not in self.animations:
            return
        current_textures = self.animations[self.current_animation]
        if len(current_textures) <= 1:
            return
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0.0
            self.animation_frame = (self.animation_frame + 1) % len(current_textures)
            self.texture = current_textures[self.animation_frame]

    # Determina que animacion mostrar basado en el estado de movimiento del jugador
    def update_movement_state(self):
        if self.change_x > 0:
            self.facing_direction = 1
        elif self.change_x < 0:
            self.facing_direction = -1
        self.is_moving = abs(self.change_x) > 0.1
        self.is_jumping = abs(self.change_y) > 0.5
        
        if self.is_jumping:
            new_animation = "jump_right" if self.facing_direction == 1 else "jump_left"
        elif self.is_moving:
            new_animation = "walk_right" if self.facing_direction == 1 else "walk_left"
        else:
            new_animation = "idle_right" if self.facing_direction == 1 else "idle_left"
            
        if new_animation != self.current_animation:
            self.set_animation(new_animation)

# Vista principal del juego que maneja toda la logica del gameplay
class GameView(arcade.View):
    # Inicializa todas las variables del juego y configura el estado inicial
    def __init__(self):
        super().__init__()
        self.player_sprite = None
        self.player_list = None
        self.wall_list = None
        self.ground_list = None
        self.coin_list = None
        self.scene = None

        self.physics_engine = None
        self.tile_map = None

        self.camera = None
        self.gui_camera = None

        self.coins_collected = 0
        self.total_coins = 0
        self.game_completed = False
        self._game_over_shown = False

        self.coin_counter_text = None
        self.victory_title_text = None
        self.victory_subtitle_text = None

        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.gameover_sound = arcade.load_sound(":resources:sounds/gameover1.wav")

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    # Configura todos los elementos del juego: mapa, jugador, enemigos, monedas, fisica
    def setup(self):
        self.camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

        map_path = os.path.join(MAPS_DIR, "level1.tmx")
        self.tile_map = arcade.load_tilemap(map_path, 1.0)

        self.player_list = arcade.SpriteList()
        self.wall_list = self.tile_map.sprite_lists.get("Walls", arcade.SpriteList())
        self.ground_list = self.tile_map.sprite_lists.get("Ground", arcade.SpriteList())
        self.coin_list = arcade.SpriteList()

        self.scene = arcade.Scene()
        self.scene.add_sprite_list("Espinas", use_spatial_hash=True)
        self.scene.add_sprite_list("Balas")

        coordinate_list = [(1360, 410), (1430, 410), (1650, 555), (1710, 555)]
        for coordinate in coordinate_list:
            espinas = arcade.Sprite(
                ":resources:images/tiles/boxCrate_double.png", scale=TILE_SCALING
            )
            espinas.position = coordinate
            espinas.alpha = 0
            self.scene.add_sprite("Espinas", espinas)

        self.create_player()

        enemy = EnemySprite(
            ":resources:images/space_shooter/playerShip1_green.png",
            scale=0.5,
            bullet_list=self.scene["Balas"],
            time_between_firing=3.0,
        )
        enemy.center_x = 1000
        enemy.center_y = 750 - enemy.height
        enemy.angle = 180
        self.scene.add_sprite("Balas", enemy)

        enemy2 = EnemySprite2(
            ":resources:images/space_shooter/playerShip1_green.png",
            scale=0.5,
            bullet_list=self.scene["Balas"],
            time_between_firing=3.0,
        )
        enemy2.center_x = 2300
        enemy2.center_y = 940 - enemy.height
        enemy2.angle = 180
        self.scene.add_sprite("Balas", enemy2)

        self.create_coins_from_objects()

        collision_list = arcade.SpriteList()
        for wall in self.wall_list:
            collision_list.append(wall)
        for ground in self.ground_list:
            collision_list.append(ground)
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=collision_list
        )

    # Crea y posiciona el sprite del jugador en el mapa
    def create_player(self):
        player_layer = self.tile_map.sprite_lists.get("Player")
        if player_layer and len(player_layer) > 0:
            map_player = player_layer[0]
            self.player_sprite = AnimatedPlayer(scale=1.0)
            self.player_sprite.center_x = map_player.center_x
            self.player_sprite.center_y = map_player.center_y + TILE_SIZE
            map_player.remove_from_sprite_lists()
        else:
            self.player_sprite = AnimatedPlayer(scale=1.0)
            self.player_sprite.center_x = 300
            self.player_sprite.center_y = 400
        self.player_list.append(self.player_sprite)

    # Busca objetos tipo moneda en el mapa y crea sprites de monedas
    def create_coins_from_objects(self):
        if not hasattr(self.tile_map, 'object_lists') or "Objects" not in self.tile_map.object_lists:
            return
        coins_created = 0
        for obj in self.tile_map.object_lists["Objects"]:
            if hasattr(obj, 'name') and obj.name == "coin":
                coin = self.create_coin_sprite(obj)
                if coin:
                    self.coin_list.append(coin)
                    coins_created += 1
        self.total_coins = coins_created
        self.setup_text_objects()

    # Crea un sprite de moneda individual basado en un objeto del mapa
    def create_coin_sprite(self, obj):
        try:
            coin = arcade.Sprite(":resources:images/items/coinGold.png", 0.5)
            x, y = self.extract_coordinates_from_shape(obj)
            coin.center_x = x
            coin.center_y = y
            return coin
        except Exception:
            coin = arcade.SpriteSolidColor(24, 24, arcade.color.GOLD)
            coin.center_x = 500
            coin.center_y = 400
            return coin

    # Extrae las coordenadas de posicion de un objeto del mapa
    def extract_coordinates_from_shape(self, obj):
        try:
            if hasattr(obj, 'shape') and obj.shape:
                points = obj.shape
                x_coords = [p[0] for p in points]
                y_coords = [p[1] for p in points]
                return (min(x_coords) + max(x_coords)) / 2, (min(y_coords) + max(y_coords)) / 2
            elif hasattr(obj, 'center_x'):
                return obj.center_x, obj.center_y
            elif hasattr(obj, 'x'):
                return obj.x, obj.y
            else:
                return 500, 400
        except Exception:
            return 500, 400

    # Inicializa los objetos de texto para mostrar informacion en pantalla
    def setup_text_objects(self):
        self.coin_counter_text = arcade.Text(
            f"Monedas: {self.coins_collected}/{self.total_coins}",
            SCREEN_WIDTH - 200, SCREEN_HEIGHT - 40,
            arcade.color.BLACK, 24, font_name="Arial", anchor_x="center"
        )
        self.victory_title_text = arcade.Text(
            "FELICITACIONES!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20,
            arcade.color.BLACK, 36, font_name="Arial", anchor_x="center"
        )
        self.victory_subtitle_text = arcade.Text(
            "Recolectaste todas las monedas!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20,
            arcade.color.BLACK, 20, font_name="Arial", anchor_x="center"
        )

    # Actualiza el texto del contador de monedas con los valores actuales
    def update_coin_counter_text(self):
        self.coin_counter_text.text = f"Monedas: {self.coins_collected}/{self.total_coins}"

    # Dibuja todos los elementos del juego en cada frame
    def on_draw(self):
        self.clear()
        self.camera.use()
        for layer_name, sprite_list in self.tile_map.sprite_lists.items():
            if layer_name != "Player":
                sprite_list.draw()
        
        self.scene.draw()
        self.player_list.draw()
        self.coin_list.draw()
        
        self.gui_camera.use()
        self.coin_counter_text.draw()
        if self.game_completed:
            self.draw_victory_message()

    # Dibuja el mensaje de victoria cuando el juego se completa
    def draw_victory_message(self):
        arcade.draw_lrbt_rectangle_filled(
            SCREEN_WIDTH // 2 - 200, SCREEN_WIDTH // 2 + 200,
            SCREEN_HEIGHT // 2 - 100, SCREEN_HEIGHT // 2 + 100,
            (0, 0, 0, 150)
        )
        self.victory_title_text.draw()
        self.victory_subtitle_text.draw()

    # Maneja las teclas presionadas para controlar el movimiento del jugador
    def on_key_press(self, key, modifiers):
        if self.game_completed:
            return
        if key in (arcade.key.UP, arcade.key.W, arcade.key.SPACE):
            if self.physics_engine.can_jump():
                arcade.play_sound(self.jump_sound)
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key in (arcade.key.LEFT, arcade.key.A):
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    # Maneja cuando se sueltan las teclas para detener el movimiento horizontal
    def on_key_release(self, key, modifiers):
        if self.game_completed:
            return
        if key in (arcade.key.LEFT, arcade.key.A):
            self.player_sprite.change_x = 0
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player_sprite.change_x = 0

    # Actualiza toda la logica del juego en cada frame
    def on_update(self, delta_time):
        if self.game_completed:
            if not hasattr(self, "_game_over_shown") or not self._game_over_shown:
                self._game_over_shown = True
                self.window.show_view(GameOverView(
                    final_score=self.coins_collected,
                    message="FELICITACIONES! Completaste el nivel"
                ))
            return

        self.physics_engine.update()
        if hasattr(self.player_sprite, 'update_animation'):
            self.player_sprite.update_animation(delta_time)
        if hasattr(self.player_sprite, 'update_movement_state'):
            self.player_sprite.update_movement_state()
        self.check_coin_collisions()

        if self.player_sprite.center_x < 0:
            self.player_sprite.center_x = 0
        elif self.player_sprite.center_x > MAP_WIDTH:
            self.player_sprite.center_x = MAP_WIDTH
            
        if arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Balas"]
        ):
            self.coins_collected = 0
            self.total_coins = 0
            arcade.play_sound(self.gameover_sound)
            self.update_coin_counter_text()
            self.setup()
        
        self.scene["Balas"].update(delta_time)

        if arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Espinas"]
        ):
            self.coins_collected = 0
            self.total_coins = 0
            arcade.play_sound(self.gameover_sound)
            self.update_coin_counter_text()
            self.setup()

        if self.player_sprite.center_y < -100:
            self.player_sprite.center_x = 300
            self.player_sprite.center_y = 400
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
            arcade.play_sound(self.gameover_sound)

        self.update_camera()

    # Detecta y maneja las colisiones entre el jugador y las monedas
    def check_coin_collisions(self):
        coins_hit = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        for coin in coins_hit:
            if coin in self.coin_list:
                coin.remove_from_sprite_lists()
                self.coins_collected += 1
                arcade.play_sound(self.collect_coin_sound)
                self.update_coin_counter_text()
                if self.coins_collected >= self.total_coins and self.total_coins > 0:
                    self.game_completed = True

    # Actualiza la posicion de la camara para seguir al jugador
    def update_camera(self):
        target_x = self.player_sprite.center_x
        target_y = self.player_sprite.center_y
        min_x = SCREEN_WIDTH / 2
        max_x = MAP_WIDTH - SCREEN_WIDTH / 2
        min_y = SCREEN_HEIGHT / 2
        max_y = MAP_HEIGHT - SCREEN_HEIGHT / 2
        target_x = max(min_x, min(target_x, max_x))
        target_y = max(min_y, min(target_y, max_y))
        self.camera.position = (target_x, target_y)

# Funcion principal que inicia el juego
def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.show_view(StartView(make_game_view=lambda: GameView()))
    arcade.run()

if __name__ == "__main__":
    main()