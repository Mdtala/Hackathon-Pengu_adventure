# src/start_view.py
import arcade
import os
import math

# Rutas (mismo criterio que tu main)
BASE_DIR   = os.path.dirname(os.path.dirname(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "imagenes")
RUTA_LOGO  = os.path.join(IMAGES_DIR, "pingus.png")
RUTA_FONT  = os.path.join(BASE_DIR, "PressStart2P-Regular.ttf")

class StartView(arcade.View):
    """
    Pantalla de inicio. No importa GameView para evitar imports circulares.
    Recibe make_game_view: una función que devuelve una instancia de GameView.
    """
    def __init__(self, make_game_view):
        super().__init__()
        self.make_game_view = make_game_view
        arcade.set_background_color(arcade.color.BLACK)

        # Fuente con fallback
        try:
            if os.path.exists(RUTA_FONT):
                arcade.load_font(RUTA_FONT)
                self.font_name = "Press Start 2P"
            else:
                self.font_name = "Arial"
        except Exception:
            self.font_name = "Arial"

        # Logo opcional
        self.logo = None
        try:
            if os.path.exists(RUTA_LOGO):
                self.logo = arcade.load_texture(RUTA_LOGO)
        except Exception:
            self.logo = None

        self.logo_sprite = arcade.Sprite()
        if self.logo:
            self.logo_sprite.texture = self.logo
        self.logo_list = arcade.SpriteList()

        # Animación de texto
        self.base_font_size = 16
        self.scale_time = 0
        self.base_y = None
        self.text_y = None
        self.float_dir = 1
        self.float_speed = 1
        self.float_range = 20

    def on_show_view(self):
        w, h = self.window.width, self.window.height
        if self.logo:
            self.logo_sprite.center_x = w // 2
            self.logo_sprite.center_y = h // 2 + 100
            if not self.logo_list:
                self.logo_list.append(self.logo_sprite)
        self.base_y = h // 2 + 40
        self.text_y = self.base_y

    def on_draw(self):
        self.clear()
        self.logo_list.draw()
        w, h = self.window.width, self.window.height

        arcade.draw_text("PINGU'S ADVENTURE",
                         w/2, self.text_y, arcade.color.BLACK, 30,
                         anchor_x="center", font_name=self.font_name)

        # “respiración” del texto
        scale = 1 + 0.04 * math.sin(self.scale_time)
        size = int(self.base_font_size * scale)

        arcade.draw_text("Presioná ENTER para jugar",
                         w/2, h/2 - 60, arcade.color.BLACK, size,
                         anchor_x="center", font_name=self.font_name)
        arcade.draw_text("ESC para salir",
                         w/2, h/2 - 95, arcade.color.BLACK, 14,
                         anchor_x="center", font_name=self.font_name)

    def on_update(self, dt: float):
        self.text_y += self.float_speed * self.float_dir
        if self.text_y > self.base_y + self.float_range:
            self.float_dir = -1
        elif self.text_y < self.base_y - self.float_range:
            self.float_dir = 1
        self.scale_time += dt * 2

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            game_view = self.make_game_view()  # crea GameView sin importar aquí
            game_view.setup()
            self.window.show_view(game_view)
        elif key == arcade.key.ESCAPE:
            arcade.exit()
