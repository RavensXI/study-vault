# Geography Image Generation Progress

**Approach**: Each of 40 lessons gets up to THREE images:
1. **Hero image** — real photo from Wikimedia Commons (CC-BY-SA or public domain), placed between `lesson-header` and `a11y-toolbar`
2. **Matplotlib diagram** — tile-based infographic using FancyBboxPatch, placed after first `key-fact` div
3. **Gemini textbook diagram** (selected lessons only) — scientific/educational illustration in textbook style, placed before `exam-tip` div. Model: `gemini-2.0-flash-preview-image-generation`. Prompt pattern: "Create a clear, simple textbook-style educational diagram..."

**Palettes**:
- Paper 1 (indigo): `#312e81 #3730a3 #4338ca #4f46e5 #6366f1 #818cf8`, shadow `#c7d2fe`, title `#1e1b4b`
- Paper 2 (red): `#7f1d1d #991b1b #b91c1c #dc2626 #ef4444 #f87171`, shadow `#fecaca`, title `#450a0a`

**Gemini API key**: `AIzaSyCW-APQx2QDUIMfjJQdwt3Z4RRMDYqyEuo`

**Hero image HTML pattern**:
```html
<figure class="lesson-hero-image">
  <img src="lesson-NN-hero.jpg" alt="Description" style="object-position: center XX%;">
  <figcaption>Description. Photo: Author / Wikimedia Commons (License)</figcaption>
</figure>
```

**Diagram HTML pattern** (matplotlib):
```html
<figure class="diagram">
  <img src="diagram_name.jpg" alt="Description">
</figure>
```

**Diagram HTML pattern** (Gemini concept):
```html
<figure class="diagram">
  <img src="diagram_name_concept.jpg" alt="Description">
</figure>
```

**Scripts**:
- `download_geo_heroes.py` — downloads all 40 hero images from Wikimedia Commons
- `generate_geo_diagrams_all.py` — generates all 40 matplotlib diagrams
- `generate_geo_gemini_diagrams.py` — generates Gemini textbook diagrams for selected lessons
- `insert_geo_images.py` — updates all 40 lesson HTML files with hero + diagram elements

## Status

### Paper 1 (Physical Geography) — indigo palette
| # | Topic | Hero | MPL Diagram | Gemini Diagram | HTML |
|---|-------|------|-------------|----------------|------|
| 01 | Natural Hazards & Plate Tectonics | DONE (Litli-Hrútur eruption, 29%) | DONE (4 tiles: types) | skip | DONE |
| 02 | Plate Boundaries & Earthquakes | TODO | TODO (3 tiles: boundary types) | YES (plate boundary cross-sections) | TODO |
| 03 | Earthquake Responses & Risk | TODO | TODO (3 tiles: predict/protect/plan) | skip | TODO |
| 04 | Volcanic Hazards & Case Studies | TODO | TODO (VS tiles: Pinatubo vs Eyjafjallajökull) | skip | TODO |
| 05 | Tropical Storms: Formation | TODO | TODO (4 tiles: formation conditions) | YES (tropical storm cross-section) | TODO |
| 06 | Typhoon Haiyan | TODO | TODO (VS tiles: effects vs responses) | skip | TODO |
| 07 | Extreme Weather & Climate Change | TODO | TODO (tiles: UK weather extremes) | skip | TODO |
| 08 | Climate Change: Evidence & Response | TODO | TODO (VS tiles: mitigation vs adaptation) | YES (greenhouse effect diagram) | TODO |
| 09 | Ecosystems & Nutrient Cycling | TODO | TODO (4 tiles: ecosystem components) | YES (nutrient cycle diagram) | TODO |
| 10 | Tropical Rainforests | TODO | TODO (4 tiles: rainforest layers) | YES (rainforest layers cross-section) | TODO |
| 11 | Deforestation & Management | TODO | TODO (tiles: causes of deforestation) | skip | TODO |
| 12 | Hot Deserts: Adaptations | TODO | TODO (tiles: plant + animal adaptations) | skip | TODO |
| 13 | Desertification | TODO | TODO (cycle: causes → effects → feedback) | YES (desertification process) | TODO |
| 14 | Waves & Coastal Erosion | TODO | TODO (VS tiles: constructive vs destructive) | YES (wave types cross-section) | TODO |
| 15 | Coastal Landforms: Erosion | TODO | TODO (flow: crack→cave→arch→stack→stump) | YES (headland erosion sequence) | TODO |
| 16 | Coastal Management | TODO | TODO (VS tiles: hard vs soft engineering) | skip | TODO |
| 17 | River Landscapes & Processes | TODO | TODO (3 tiles: upper/middle/lower course) | YES (river long profile) | TODO |
| 18 | River Landforms | TODO | TODO (tiles: key landforms) | YES (oxbow lake formation) | TODO |
| 19 | Flooding & Hydrographs | TODO | TODO (tiles: flood causes) | YES (storm hydrograph) | TODO |
| 20 | Flood Management | TODO | TODO (VS tiles: hard vs soft engineering) | skip | TODO |

### Paper 2 (Human Geography) — red palette
| # | Topic | Hero | MPL Diagram | Gemini Diagram | HTML |
|---|-------|------|-------------|----------------|------|
| 01 | Urbanisation & the DTM | TODO | TODO (tiles: push/pull factors) | YES (DTM 5-stage diagram) | TODO |
| 02 | Rio: Location & Importance | TODO | TODO (tiles: why Rio matters) | skip | TODO |
| 03 | Rio: Challenges | TODO | TODO (3 tiles: social/economic/environmental) | skip | TODO |
| 04 | Rio: Improvements | TODO | TODO (tiles: improvement strategies) | skip | TODO |
| 05 | Liverpool: Location & Importance | TODO | TODO (tiles: why Liverpool matters) | skip | TODO |
| 06 | Liverpool: Decline & Deprivation | TODO | TODO (tiles: causes of decline) | skip | TODO |
| 07 | Liverpool: Greening | TODO | TODO (tiles: green initiatives) | skip | TODO |
| 08 | Liverpool: Regeneration | TODO | TODO (tiles: regeneration projects) | skip | TODO |
| 09 | DTM & Population Growth | TODO | TODO (5 tiles: DTM stages) | YES (DTM line chart) | TODO |
| 10 | Uneven Development | TODO | TODO (tiles: causes of uneven development) | skip | TODO |
| 11 | Closing the Gap | TODO | TODO (tiles: strategies) | skip | TODO |
| 12 | India: Location & Context | TODO | TODO (tiles: key facts) | skip | TODO |
| 13 | India: Economy & TNCs | TODO | TODO (tiles: economic sectors) | skip | TODO |
| 14 | India: Growth & Environment | TODO | TODO (VS: growth vs environmental cost) | skip | TODO |
| 15 | Changing UK Economy | TODO | TODO (VS: primary/secondary → tertiary/quaternary) | skip | TODO |
| 16 | Post-Industrial UK | TODO | TODO (tiles: science parks, business parks) | skip | TODO |
| 17 | North-South Divide | TODO | TODO (VS: North vs South) | skip | TODO |
| 18 | Resource Management | TODO | TODO (3 tiles: food/water/energy) | skip | TODO |
| 19 | Fracking & Energy Security | TODO | TODO (VS: for vs against fracking) | skip | TODO |
| 20 | Sustainable Energy | TODO | TODO (tiles: renewable sources) | skip | TODO |
