# Plan: Build `items.md` from the uploaded documents

## Problem
The project has scattered proposed improvements in `active.pdf`, `todo.md`, and `todo_2.md`. The repository may differ from those proposals, and some alternatives are better or worse than the current implementation. This session must determine, sentence by sentence, which version to retain.

## Approach
1. Iterate the sources in this exact order: `active.pdf`, `todo.md`, then `todo_2.md`.
2. For `active.pdf`, compare each substantive sentence or bullet with the current repository and ask the user to choose the version to keep.
3. Move through `todo.md` and `todo_2.md` only after all decisions in the preceding source are resolved.
4. Add only user-approved repository changes to `items.md`, using concrete, tiny, implementation-ready items.
5. Preserve decisions for later implementation; do not modify project files or create code during this planning task.

## Decision output
`items.md` will contain approved changes grouped by source and section, with file-level scope and a clear completion criterion where useful.
# Plan: Assign `items.md` to the paper sections

## Problem

`items.md` contains approved improvements, but each item is not yet organized by the paper's final section hierarchy. The implementation plan must reconcile the checklist with the following structure:

- §1 Datos del proyecto
- §2 Presentación
- §3 Dataset
- §4 Objetivos
- §4.1 Qué puntos existen
- §4.2 Qué puntos sirven
- §4.3 Cómo usamos los puntos
- §5 Desarrollo
- §5.1 Qué puntos existen
- §5.1.1 Unidad temporal
- §5.1.2 Agregación
- §5.2 Qué puntos sirven
- §5.2.1 Mediciones incompletas
- §5.2.2 Cantidad y dispersión de puntos por estación
- §5.3 Cómo usamos los puntos
- §5.3.1 Transformaciones
- §5.3.2 Modelo
- §6 Conclusión
- §7 Referencias

## Cross-source decisions resolved

- Elevation is represented by fixed global elevation bands in §5.3.1/§5.3.2, not relative terciles within each zone.
- Zone and elevation remain separate factors in the main paper framing. Their overlap is checked numerically with a contingency table and discussed descriptively.
- ENSO remains continuous in the main analysis. ENSO phases ±0.5 °C are retained only as a what-if categorical exercise.
- ANOVA is not presented as an accepted inferential result until independence, normality, homoscedasticity, coverage, rank, and n=46 limitations are checked. Its failure is summarized in §6.
- The standalone §5.3.4 is removed. Its relevant caveats and alternatives are distributed across §5.3.1, §5.3.2, and §6.

## Section assignment

### §1 Datos del proyecto

- Keep Nicolás Mínguez Aguirre and both Kaggle/GitHub links.
- Keep the group code blank.
- Update the title to use “bandas de elevación” only in the final wording.
- Correct metadata, capitalization, and typographical issues.

### §2 Presentación

- Retain the SWE usefulness/rationale and the ENSO external-predictor rationale.
- Reword the research question to compare the ENSO signal in SWE by zone and elevation band.
- Keep the ENSO/TAVG/PRCP-to-SWE causal diagram.
- Mention zone–elevation overlap briefly and state that it is revisited in the analysis and conclusion.
- Keep the section below 150 words and fix Spanish/LaTeX rendering.

### §3 Dataset

- Describe SNOTEL and NOAA PSL and the 1980/81–2025/26 period.
- Correct the variable table: station and season variables, numeric variables, and categorical zone/elevation variables.
- Define zone as categorical and elevation as numeric in DS1/DS2.
- Retain the table, caption, labels, and references in valid Spanish LaTeX.
- Keep every `*` explanation concentrated in one table/caption.

### §4 Objetivos

- Remove the ANCOVA description and replace it with the final method-validity framing.
- Replace the O1 pipeline with aggregation and temporal-unit decisions.
- Replace the O2 bullets with incomplete-observation and station coverage decisions.
- Replace O3 with three concise questions: SWE transformation; zone/elevation association and fixed bands; valid analysis and alternatives.
- Keep the introductory objective text under 50 words and each O1/O2/O3 bullet under the specified limits.

#### §4.1 Qué puntos existen

- Decide the December–April seasonal unit and temporal autocorrelation treatment.
- Decide aggregation of SWE, ENSO, TAVG, and PRCP.
- State that zone remains categorical and elevation is initially retained numerically.
- List ENSO discretization only as a what-if sensitivity, not the main representation.

#### §4.2 Qué puntos sirven

- Decide incomplete SWE/ENSO handling and missingness bias.
- Decide the minimum station coverage and how many complete seasons are required.
- Keep the station-season row and station/zone filter decisions.

#### §4.3 Cómo usamos los puntos

- Decide the SWE transformation and whether ENSO needs any scale/phase treatment.
- Study zone–elevation association and fixed elevation bands.
- State that the final model is only used if its assumptions and design checks pass.

### §5 Desarrollo

- Keep data-preparation work as the central narrative.
- Remove Python/library implementation commentary.
- Keep all figures, tables, and calculations tied to a final report section.

#### §5.1.1 Unidad temporal

- Explain monthly autocorrelation and retain December–April seasons.
- State that SWE independence between seasons is expected but not guaranteed.
- Keep the ENSO two-season residual dependence caveat and the n=46 shared-season limitation.
- Remove the duplicate star/footnote explanation.
- Retain the autocorrelation table and representative Stampede Pass figure.

#### §5.1.2 Agregación

- Keep maximum SWE, mean TAVG, sum PRCP, and mean ENSO.
- Add a variable-role table covering:
  - SWE, ENSO, TAVG, PRCP;
  - zone and elevation;
  - station, season, and station-season unit;
  - numerical versus categorical role.
- Explain that elevation remains numeric until §5.3.1/§5.3.2.
- Explain why zone is not encoded through coordinates, distance, or HUC.
- Keep the USDA map only if space and the report structure support it.

### §5.2 Qué puntos sirven

- Carry only quality-control decisions and station coverage evidence.

#### §5.2.1 Mediciones incompletas

- Replace the old claim that only SWE/ENSO enter the model.
- Explain incomplete SWE removal, imputation concerns, and the Spearman missingness check.
- State that Spearman is descriptive and does not prove missingness is ignorable.

#### §5.2.2 Cantidad y dispersión

- Move the Stampede Pass sentence after or beside the figure.
- Separate the general Niña-versus-Niño pattern from substantial overlap/variability.
- Keep the out-of-ENSO time trend as a limitation or control issue.
- Keep the at-least-30-seasons station filter.
- Add the station/zone/row counts-flow table.

### §5.3 Cómo usamos los puntos

- Present transformations and fixed categorical factors, then discuss model validity.
- Do not present unsupported ANCOVA or ANOVA inference.

#### §5.3.1 Transformaciones

- Verify whether AWDB returns SWE in mm or inches.
- Explain the log1p SWE transformation and its implications for zeros and scale.
- Keep ENSO continuous in °C.
- Keep elevation numeric until fixed global bands are introduced.
- State fixed global elevation-band cutoffs and station distribution.
- Retain TAVG/PRCP only as context or out-of-model variables, not as model assumptions.
- Include the Niña/Niño/Neutral ±0.5 °C phase coding only as a clearly labeled what-if sensitivity.
- Add one concise variable/transformation/rationale table.
- Remove detailed Python/library implementation language.

#### §5.3.2 Modelo

- Use zone and fixed elevation bands as separate categorical factors in the what-if design.
- Explain the contingency table for zone–elevation association and replace η² with an appropriate categorical association check.
- Run ANOVA validity checks:
  - independence or dependence structure;
  - residual normality;
  - homoscedasticity;
  - complete cell coverage;
  - design rank;
  - n=46 interpretability.
- If any key assumption fails, stop inferential ANOVA and state this explicitly.
- If the what-if ANOVA is described at all, rename nested models R0/R1/R2 and reserve M for multipliers.
- Explain intercept/contrast coding only after validation.
- Remove row-level Shapiro–Wilk, Breusch–Pagan, Wald, and station-clustered inference claims.
- Keep nonparametric, ANCOVA, season-block, mixed-model, and spatial/temporal alternatives as future directions rather than fitted results.

### §6 Conclusión

- Write exactly three paragraphs:
  1. summary of data preparation and final decisions;
  2. principal limitations and ANOVA failure;
  3. alternative methods and explanation that full complexity is outside scope.
- Include n=46, shared ENSO seasons, residual correlation, zone/elevation overlap, discretization, missingness, and assumption failure.
- Name ANCOVA, nonparametric tests, season blocks/resampling, mixed models, and spatial/temporal surfaces.

### §7 Referencias

- Retain only references used by the final report.
- Add references for any method named in §5.3.2 or §6.
- Remove references used only for obsolete ANCOVA/Wald/clustered-model claims.

## Implementation cleanup

- Remove unused ANCOVA, centered-elevation, two-stage, and row-level model text.
- Rebuild tables and figures from the final DS1/DS2/DS3 pipeline.
- Keep `ds1.csv`, `ds2.csv`, and `ds3.csv` at `data/`; place intermediates under `data/o1/`, `data/o2/`, and `data/o3/`.
- Remove obsolete code, CSV, graph, and text artifacts.
- Keep Spanish/English README claims aligned with the final report.
- Apply the section word limits: Presentation ≤150 words, Dataset ≤100 words, O1/O2/O3 ≤80 words, Development ≈2000 words, Conclusion ≈500 words.
