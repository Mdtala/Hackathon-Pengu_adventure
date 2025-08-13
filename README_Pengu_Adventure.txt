README — Pengu Adventure

¿De qué trata el juego?
--------------------
Sos un pingüino. Tu misión es juntar 5 monedas en un mapa de plataformas. Si las juntás todas, ganás. Si caés al vacío volves al respawn, si tocás una trampa, perdés tu progreso.

Controles
---------
- Izquierda/Derecha: mover al pingüino
- Barra espaciadora: saltar

Objetivo
--------
Juntar 5 monedas lo más rápido posible sin caer ni tocar trampas.

Cómo instalar (rápido)
----------------------
1) Tener Python 3.10+ instalado.
2) Crear y activar entorno virtual (opcional, recomendado):
   Linux/macOS:
       python3 -m venv venv
       source venv/bin/activate
3) Instalar dependencias:
       pip install arcade

Cómo ejecutar
-------------
- Desde la carpeta del proyecto, corre:
      python -m src.main
  o directamente:
      python src/main.py

Estructura básica (ejemplo)
---------------------------
- src/
  - main.py            → arranque del juego (crea ventana y muestra StartView/GameView)
  - start_view.py      → menú inicial
  - game_over_view.py  → pantalla de fin
- assets/
  - imagenes/          → sprites y fondos
  - sounds/            → sonidos
  - maps/              → nivel en .tmx (Tiled)

