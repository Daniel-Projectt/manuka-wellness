# Manuka — Salud Preventiva

Sitio web de una página para **Manuka** ([@manukard](https://www.instagram.com/manukard/)), centro de salud preventiva y bienestar integral en Santo Domingo, República Dominicana.

**Demo:** https://daniel-projectt.github.io/manuka-wellness/

## Identidad

Todo salió de la marca real, no de una plantilla:

| Token | Valor | De dónde salió |
|---|---|---|
| Crema | `#F5EBDD` | Las paredes y el mural botánico |
| Navy | `#22394E` | Las puertas del centro |
| Oro | `#C79A2E` | El sello del logo |
| Caoba | `#6A3C2D` | El disco del logo |

- **Tipografía:** Marcellus (capitales romanas, como el wordmark del logo) + Karla.
- **Logo:** el real, tomado del perfil de Instagram.
- **Sin fotos, a propósito.** Las únicas imágenes del espacio que existen públicas
  son frames borrosos de un reel; montar el sitio sobre eso lo hacía ver barato.
  En su lugar la página es una **lámina de herbario** — que es literalmente lo que
  cuelga de sus paredes: flores prensadas enmarcadas. Los especímenes (`assets/fern.svg`, `flor.svg`, `hoja.svg`)
  están generados con `scripts/botanicals.py` y se usan como máscara CSS, así que se colorean
  desde el CSS y pesan 8 KB o menos cada uno.

## Stack

HTML + CSS + JS puro, sin dependencias ni build. Todo el sitio pesa ~100 KB.

- `index.html` — una página, secciones ancladas
- `css/style.css` — identidad visual completa
- `js/main.js` — nav, menú móvil, revelado al scroll, CTA fija de móvil
- `scripts/botanicals.py` — dibuja los tres especímenes (helecho, aciano, hoja ancha)
- `assets/` — logo, favicons, láminas botánicas

El contenido es visible por defecto: el revelado al scroll solo se activa si el JS
arranca, y hay un respaldo de 3 s. Si el JS falla, la página se lee igual.

## Datos usados (verificados en su Instagram, 16-jul-2026)

- Tagline: *"Más que un centro de bienestar, somos parte de tu estilo de vida."* · *"Sana tu cuerpo"*
- Teléfonos: **809.373.2805** · **829.655.0075**
- Terapias: sueroterapia, ozonoterapia, exosomas, autohemoterapia, colónicos y enemas, detox iónico, sauna, drenaje linfático, masaje terapéutico, reflexología podal

## Pendiente de confirmar con el dueño

- [ ] **Fotos originales en alta.** Las actuales son frames de un reel (720px, con algo de blur). Con las originales el sitio sube un nivel.
- [ ] **Cuál de los dos números es el de WhatsApp.** Ahora mismo el CTA usa el 829.655.0075 (el que tiene 📲 en la bio); el 809.373.2805 va como teléfono.
- [ ] **Dirección.** Calle Max Henríquez Ureña 63 salió de un directorio, no de su Instagram — confirmar.
- [ ] **Horario de atención** (no lo publican).
- [ ] Descripciones de cada terapia — las actuales son un resumen corto y prudente, sin prometer resultados médicos.
- [ ] Equipo / médicos que quieran mostrar.