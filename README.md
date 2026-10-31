# Harvest Moon: Friends of Mineral Town (GBA) — Ecosistema de Decompilación, Ingeniería Inversa y ROM Hacking

Este repositorio unifica los proyectos clave de decompilación, análisis de bytecode y herramientas gráficas de modificación para **Harvest Moon: Friends of Mineral Town (USA)** de Game Boy Advance (`HARVESTMOGBAA4NE`), **excluyendo cualquier archivo ROM propietario (`.gba`)**.

> **¿Eres principiante? Lee la [Guía para principiantes](./GUIA_PRINCIPIANTES.md).**

---

## Estructura del Repositorio y Genealogía Técnica

| Carpeta | Proyecto Base | Lenguaje | Propósito dentro del Ecosistema |
| :--- | :--- | :--- | :--- |
| **[`StanHash_fomt/`](./StanHash_fomt)** | [StanHash/fomt](https://github.com/StanHash/fomt) | C++ (`agbcp`) / C (`agbcc`) / ASM | **Decompilación 1:1 (*matching*)**: Recompila una ROM 100% idéntica byte por byte (`SHA1: a2fc3574f0a65a4fcf7682fb274b9d7eebdef963`) a partir de las clases originales en C++ (`Farmer`, `Bachelorette`, `Field`, `Barn`, `Coop`, `Animal`, `ScriptEngine`). |
| **[`StanHash_mary/`](./StanHash_mary)** | [StanHash/mary](https://github.com/StanHash/mary) | Rust | **Compilador y Descompilador de Scripts original**: Primer motor capaz de traducir el bytecode de eventos de la máquina virtual de pila (`0x0F89D4`) a código estructurado de alto nivel (`if/else`, `switch`, `do/while`) usando la librería [`lib_fomt.txt`](./StanHash_mary/goodies/lib_fomt.txt). |
| **[`HM-Studio/`](./HM-Studio)** | [andrey-moura/HM-Studio](https://github.com/andrey-moura/HM-Studio) | C++ (`wxWidgets`) | **Precursor de edición GUI**: Primer entorno visual para editar ítems, cartas, fuentes, guardados y descomprimir gráficos de FoMT/MFoMT. |
| **[`FIO-DECOMP-HMFOMT/`](./FIO-DECOMP-HMFOMT)** | [Denisovich728/FIO-DECOMP-HMFOMT](https://github.com/Denisovich728/FIO-DECOMP-HMFOMT) | Pseudo-C (Ghidra) / JSON / Markdown | **Base de Datos de Referencia y Documentación**: Contiene **30,001 cadenas de texto** ([`strings.h`](./FIO-DECOMP-HMFOMT/include/text/strings.h)), los **1,328 eventos descompilados** ([`assets/events/`](./FIO-DECOMP-HMFOMT/assets/events)), catálogos JSON de retratos/sprites/animaciones y documentación arquitectónica en [`docs/`](./FIO-DECOMP-HMFOMT/docs). |
| **[`FOMT_Studio/`](./FOMT_Studio)** | [Denisovich728/FOMT_Studio](https://github.com/Denisovich728/FOMT_Studio) | Python 3 (`PyQt6`) | **Suite Todo-en-Uno de Ingeniería Inversa y Modding (v3.7.1)**: Integra y expande los hallazgos de `mary`, `HM-Studio`, `StanHash/fomt` y `u/MelodyCrystel` en una interfaz gráfica completa. |

---

## Arquitectura de `FOMT_Studio` (v3.7.1 "Listen The World")

`FOMT_Studio` recoge las bases de `StanHash/mary`, `StanHash/fomt` y `HM-Studio` y construye sobre ellas cinco subsistemas principales:

1. **Decompilador de Patrones Nativos THUMB (`NativeProcDecompiler`)**:
   - Ubicado en [`FOMT_Studio/Nucleos_Positronicos/Nucleo_de_Rutinas_AI/native_proc_viewer.py`](./FOMT_Studio/Nucleos_Positronicos/Nucleo_de_Rutinas_AI/native_proc_viewer.py).
   - Analiza las **328 rutinas nativas en código máquina ARM/THUMB** de la *Dispatch Table* (`0x03F900`), detectando invocaciones de retratos (`Set_Portrait`), lectura/escritura de *flags*, entrega de ítems y llamadas internas del motor (`Register_Shipment`, `Init_Shop_UI`, `Play_SE`).
2. **Arquitectura de Datos `Cilixes` (`SuperLibrary`)**:
   - Ubicada en [`FOMT_Studio/Banco_de_Datos/super_lib.py`](./FOMT_Studio/Banco_de_Datos/super_lib.py) y [`FOMT_Studio/Banco_de_Datos/Cilixes/`](./FOMT_Studio/Banco_de_Datos/Cilixes).
   - Identifica quirúrgicamente la ROM mediante los 16 bytes del header (`0xA0-0xAF`) para dar soporte simultáneo a **FoMT** y **MFoMT** mediante tablas CSV dinámicas (`Fomt_Lib.csv`, `Fomt_Mapas.csv`, `Fomt_Portraits.csv`, `Fomt_Flags.csv`).
3. **Motor de Scripts `SlipSpace Engine v3`**:
   - Ubicado en [`FOMT_Studio/Nucleos_Positronicos/Nucleo_de_Scripts/SlipSpace_Script_Engine/`](./FOMT_Studio/Nucleos_Positronicos/Nucleo_de_Scripts/SlipSpace_Script_Engine).
   - Port a Python y evolución de `StanHash/mary` con **decoración semántica bidireccional**: traduce IDs numéricos a nombres legibles de personajes, objetos, retratos, emotes y códigos de control (`\BRK`, `\WAIT_CLICK`), y al recompilar resuelve los nombres a binario optimizando instrucciones `PUSH8`/`PUSH16`.
4. **Gestión Gráfica (`LZ77` + `ArcanoMarvelous`) y Audio (`Sappy` / `MIDI`)**:
   - Descompresión dual: BIOS GBA estándar (`0x10` LZ77) y compresión RLE/LZ propietaria de Marvelous (`0x70` en [`arcano_marvelous_unpacker.py`](./FOMT_Studio/Banco_de_Datos/Utilidades/arcano_marvelous_unpacker.py)).
   - Renderizador completo de los **66 mapas** ([`fomt_mapdata.py`](./FOMT_Studio/Nucleos_Positronicos/Nucleo_de_Mapas/fomt_mapdata.py)), **184 retratos** (`Melody Portrait Engine`), **91 bancos de sprites** y compilador nativo de **MIDI a Sappy** ([`midi_compiler.py`](./FOMT_Studio/Nucleos_Positronicos/Nucleo_de_Sonido/midi_compiler.py)).
5. **Ingeniería de Memoria y Repunteo (`MemoryManager`)**:
   - Ubicado en [`FOMT_Studio/Banco_de_Datos/gestor_memoria.py`](./FOMT_Studio/Banco_de_Datos/gestor_memoria.py).
   - Sobrescribe *In-Place (1:1)* si el recurso modificado cabe en su bloque original, o busca espacio libre (`0x75C254+`), fuerza **alineación estricta a 4 bytes** (`(offset + 3) & ~3`), recicla el banco antiguo y actualiza los punteros GBA Little Endian (`offset | 0x08000000`).

---

## Galería Visual Extraída con la Suite

### Mapas Completos Descomprimidos (`BG3` + `BG2` + `BG1`)
![Mapa 0: La Granja](./docs/imagenes/fomt_map_farm.png)
![Mapa 2: Plaza Rosa (Rose Square)](./docs/imagenes/fomt_map_rose_square.png)

### Retratos (`Melody Portrait Engine`) y Sprites (`4bpp BGR555`)
![Galería de Retratos](./docs/imagenes/fomt_portraits_gallery.png)
![Hojas de Sprites](./docs/imagenes/fomt_sprites_showcase.png)

### Módulos Interactivos de `FOMT_Studio`
| IDE de Scripts (`SlipSpace v3`) | Visor de Mapas (`Titán`) |
| :---: | :---: |
| ![IDE SlipSpace](./docs/imagenes/fomt_studio_script_ide.png) | ![Visor de Mapas](./docs/imagenes/fomt_studio_map_titan.png) |

| Explorador de Sprites y Fuentes (`¡Instalar Ñ!`) | Motor de Audio (`Sappy / MIDI`) |
| :---: | :---: |
| ![Sprites UI](./docs/imagenes/fomt_studio_sprites_ui.png) | ![Audio Sappy](./docs/imagenes/fomt_studio_audio_sappy.png) |

| Editor Masivo de Ítems y Herramientas | Rutinas Diarias de NPCs y Pathfinding `A*` |
| :---: | :---: |
| ![Items UI](./docs/imagenes/fomt_studio_items_ui.png) | ![Rutinas IA](./docs/imagenes/fomt_studio_npc_routines.png) |

---

## Requisitos y Uso (Trae tu propia ROM)

> [!IMPORTANT]
> Este repositorio **no incluye ninguna ROM**. Para utilizar las herramientas o compilar el código debes colocar tu copia legal de **`Harvest Moon - Friends of Mineral Town (USA).gba`** (`8,388,608 bytes`, `SHA1: A2FC3574F0A65A4FCF7682FB274B9D7EEBDEF963`).

### 1. Ejecutar `FOMT_Studio` (Windows)
```powershell
cd FOMT_Studio
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\python main.py
```
O ejecuta directamente [`Iniciar_FoMT_Studio.bat`](./Iniciar_FoMT_Studio.bat) desde la raíz.

### 2. Compilar la ROM 1:1 en `StanHash_fomt` (Linux / WSL2)
1. Instala `binutils-arm-none-eabi` y compila la rama `cp` de [`notyourav/agbcc`](https://github.com/notyourav/agbcc) dentro de `StanHash_fomt/tools/agbcc/`.
2. Copia tu ROM original como `StanHash_fomt/baserom.gba`.
3. Ejecuta:
```bash
cd StanHash_fomt
make compare -j4
# Resultado esperado: fomt.gba: OK
```

---

## Créditos
- **StanHash**: Creador de [fomt](https://github.com/StanHash/fomt) y [mary](https://github.com/StanHash/mary).
- **Andrey Moura (Moonslate)**: Creador de [HM-Studio](https://github.com/andrey-moura/HM-Studio).
- **u/MelodyCrystel**: Offsets y paletas maestras de sprites y retratos.
- **Denisovich728**: Creador de [FOMT_Studio](https://github.com/Denisovich728/FOMT_Studio) y [FIO-DECOMP-HMFOMT](https://github.com/Denisovich728/FIO-DECOMP-HMFOMT).
