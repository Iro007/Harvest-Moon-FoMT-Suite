# Guía para principiantes: usar FoMT Studio

Con esta herramienta puedes ver y editar **Harvest Moon: Friends of Mineral Town (GBA)**: diálogos, mapas, retratos, sprites, música, ítems y horarios de los personajes.

> [!IMPORTANT]
> El repositorio **no incluye el juego**. Necesitas tu propio archivo del juego, `Harvest Moon - Friends of Mineral Town (USA).gba`. Solo funciona con la versión **USA**.

---

## Paso 1: Descargar

1. Entra a https://github.com/Iro007/Harvest-Moon-FoMT-Suite
2. Pulsa el botón verde **Code**, luego **Download ZIP**.
3. Haz clic derecho en el ZIP descargado y elige **Extraer todo**.
4. Mueve la carpeta a un lugar simple, por ejemplo `C:\HarvestMoon`.
   - Evita carpetas dentro de "Descargas" o rutas muy largas.

## Paso 2: Instalar Python (solo una vez)

1. Entra a https://www.python.org/downloads/ y descarga Python 3.11 o superior.
2. Abre el instalador y **marca la casilla "Add python.exe to PATH"**. Está abajo de la primera pantalla.
3. Pulsa **Install Now**.

> Si ya tienes Python instalado, salta este paso.

## Paso 3: Abrir el programa

1. Dentro de la carpeta, haz doble clic en **`Iniciar_FoMT_Studio.bat`**.
2. **La primera vez** se abre una ventana negra que instala todo sola. Tarda entre 2 y 5 minutos y necesita internet. **No la cierres.**
3. Cuando termine, se abre FoMT Studio. Las siguientes veces abre directo.

> Si Windows muestra "Windows protegió su PC", pulsa **Más información** y luego **Ejecutar de todas formas**.

## Paso 4: Cargar el juego

1. En FoMT Studio, abre el menú de archivo y elige **Abrir ROM**.
2. Selecciona tu archivo `Harvest Moon - Friends of Mineral Town (USA).gba`.
3. Espera a que termine de cargar.

> [!WARNING]
> **Haz una copia de seguridad de tu ROM antes de editar.** Copia el archivo `.gba` y guárdalo aparte. Si algo sale mal, vuelves a la copia.

---

## ¿Qué puedo hacer?

| Módulo | Para qué sirve |
| :--- | :--- |
| **Scripts / Eventos** | Leer y cambiar diálogos y cutscenes (hay 1,328 eventos). |
| **Mapas** | Ver los 66 mapas del juego y editar tiles. |
| **Retratos y sprites** | Ver y editar las caras y los dibujos de los personajes. |
| **Audio** | Escuchar las 144 pistas, exportarlas a MIDI o meter música propia. |
| **Ítems** | Cambiar precios y datos de objetos y herramientas. |
| **Rutinas de NPC** | Cambiar dónde está cada aldeano a cada hora. |
| **Parches rápidos** | Mejoras con un clic (ver abajo). |

### Parches rápidos recomendados (menú "Parches Rápidos")
- **¡Instalar Ñ!**: añade la Ñ y las tildes (á é í ó ú) al juego. Sirve para traducirlo al español.
- **Cultivos caminables**: puedes caminar sobre los cultivos.
- **Escaleras visibles en las minas**: evita quedarte atascado.
- **Piedra de teletransporte desde el año 1**.

## Paso 5: Guardar y jugar

1. Guarda los cambios desde FoMT Studio.
2. Abre el archivo `.gba` modificado con un emulador, por ejemplo **mGBA** (https://mgba.io) o **VisualBoyAdvance**.
3. También puedes probarlo en una consola real con un cartucho flash.

---

## Si algo falla

| Problema | Solución |
| :--- | :--- |
| *"Windows no puede encontrar .venv\Scripts\pythonw.exe"* | Estás usando una versión vieja del `.bat`. Descarga el ZIP de nuevo. El nuevo instala todo solo. |
| *"No se encontró Python"* | Haz el Paso 2 y marca **Add python.exe to PATH**. Luego abre el `.bat` otra vez. |
| La instalación se queda parada o da error | Revisa tu internet y vuelve a abrir el `.bat`. Si falla, borra la carpeta `FOMT_Studio\.venv` y reintenta. |
| El programa dice que la ROM no es válida | Usa la versión **USA**. Los archivos comprimidos (`.zip`) no sirven: extrae el `.gba`. |
| El juego no abre en el emulador tras editar | Vuelve a tu copia de seguridad y repite los cambios de a uno. |

---

## Para jugadores avanzados
La carpeta `StanHash_fomt` permite recompilar el juego desde el código C++. Necesita Linux o WSL2 y conocimientos técnicos. Está explicada en el [README](./README.md).
