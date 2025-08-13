# src/game_over_view.py
import arcade
import os

BASE_DIR   = os.path.dirname(os.path.dirname(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "imagenes")
RUTA_LOGO  = os.path.join(IMAGES_DIR, "pinguino.png")   # cambialo si el archivo se llama distinto
RUTA_FONT  = os.path.join(BASE_DIR, "PressStart2P-Regular.ttf")

class GameOverView(arcade.View):
    """
    Pantalla final. No importa GameView/StartView para evitar imports circulares.
    Usa callbacks/factories para reiniciar o volver al menú.
    """
    def __init__(self, final_score: int = 0, message: str = "Fin del juego",
                make_game_view=None, make_start_view=None):
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_BLUE)
        self.final_score = final_score
        self.message = message
        self.make_game_view = make_game_view
        self.make_start_view = make_start_view

        try:
            if os.path.exists(RUTA_FONT):
                arcade.load_font(RUTA_FONT)
                self.font_name = "Press Start 2P"
            else:
                self.font_name = "Arial"
        except Exception:
            self.font_name = "Arial"

        self.logo = arcade.load_texture(RUTA_LOGO) if os.path.exists(RUTA_LOGO) else None
        self.logo_sprite = arcade.Sprite()
        if self.logo:
            self.logo_sprite.texture = self.logo
        self.logo_list = arcade.SpriteList()

        self.base_y = None
        self.text_y = None
        self.float_dir = 1
        self.float_speed = 1
        self.float_range = 20

    def on_show_view(self):
        w, h = self.window.width, self.window.height
        if self.logo:
            self.logo_sprite.center_x = w // 2
            self.logo_sprite.center_y = h // 2 + 110
            if not self.logo_list:
                self.logo_list.append(self.logo_sprite)
        self.base_y = h // 2 + 40
        self.text_y = self.base_y

    def on_draw(self):
        self.clear()
        self.logo_list.draw()
        w, h = self.window.width, self.window.height

        arcade.draw_text(self.message, w/2, self.text_y,
                        arcade.color.BLUE_GREEN, 40, anchor_x="center", font_name=self.font_name)
        arcade.draw_text(f"Monedas: {self.final_score}", w/2, h/2 - 20,
                        arcade.color.WHITE, 24, anchor_x="center", font_name=self.font_name)
        arcade.draw_text("ENTER: Reiniciar  |  I: Inicio  |  ESC: Salir",
                        w/2, h/2 - 70, arcade.color.LIGHT_GRAY, 16, anchor_x="center", font_name=self.font_name)

    def on_update(self, dt: float):
        self.text_y += self.float_speed * self.float_dir
        if self.text_y > self.base_y + self.float_range:
            self.float_dir = -1
        elif self.text_y < self.base_y - self.float_range:
            self.float_dir = 1

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER and self.make_game_view:
            game = self.make_game_view()
            game.setup()
            self.window.show_view(game)
        elif key == arcade.key.I and self.make_start_view:
            self.window.show_view(self.make_start_view())
        elif key == arcade.key.ESCAPE:
            arcade.exit()
