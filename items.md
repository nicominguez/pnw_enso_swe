# Project improvement items

This file contains the approved changes derived from `active.pdf`, `todo.md`, and `todo_2.md`. Items are ordered by source. Source 2 and source 3 refine or supersede earlier decisions where they differ.

## 1. active.pdf

### Datos del proyecto

- [ ] Keep Nicolás Mínguez Aguirre as the participant.
- [ ] Keep both Kaggle and GitHub dataset links.
- [ ] Keep the group-code field blank.
- [ ] Change the report title to use “bandas de elevación” when the final model is confirmed.
- [ ] Fix typos and capitalization in the project metadata and presentation text.

### Presentación

- [ ] Keep the explanation that SWE is useful for anticipating droughts and floods and depends on many factors.
- [ ] Keep the explanation that ENSO summarizes broad atmosphere-ocean circulation and is external to SWE.
- [ ] Reword the research question as whether the ENSO signal in SWE differs by zone or elevation band.
- [ ] Keep the causal diagram, but present it consistently with the final treatment of zone and elevation.
- [ ] Mention that zone and elevation overlap geographically and that this issue is revisited in the conclusions and alternatives.

### Dataset

- [ ] Keep the SNOTEL and NOAA PSL source descriptions.
- [ ] Keep the 1980/81–2025/26 period and ending-year season notation.
- [ ] Keep season, SWE, elevation, ENSO, and the other relevant variables in the dataset table.
- [ ] Keep zone as categorical and elevation as numeric in DS1 and DS2.
- [ ] Fix LaTeX citation, label, table, and cross-reference problems.
- [ ] Use Spanish LaTeX configuration so captions and table labels render correctly.
- [ ] Replace double-question-mark section syntax with proper Spanish double-question-mark headings.

### Objetivos

- [ ] Replace the objective introduction and pipeline that currently describe ANCOVA with the final ANOVA-or-alternative design.
- [ ] Keep the objective of deciding the temporal unit and controlling temporal autocorrelation in SWE and ENSO.
- [ ] Reword O1 to cover aggregation of numerical variables, while leaving static variables unchanged.
- [ ] Justify keeping zone categorical instead of encoding it through latitude, ocean distance, HUC, or a similar geospatial variable.
- [ ] Keep incomplete-observation and missingness-bias questions in O2.
- [ ] Keep the station quantity and dispersion objective in O2.
- [ ] State that ENSO remains in °C and that SWE is the transformed variable for the analysis.
- [ ] Keep the objective of studying zone–elevation association and elevation bands within zones.
- [ ] State that the ENSO signal will be compared by zone and elevation band, subject to model-validity checks.

### 5.1.1 Unidad temporal

- [ ] Keep December–April station seasons as the temporal unit.
- [ ] State that SWE decorrelation between seasons is expected but not guaranteed or assumed without checking.
- [ ] Keep the explicit limitation that ENSO still shows residual dependence and only 46 seasons provide shared ENSO values.
- [ ] Add an effective-sample-size interpretation where relevant.
- [ ] Remove the repeated explanation of the star used for Niño 3.4/anomaly variables.

### 5.1.2 Agregación

- [ ] Keep the station-season as the unit of analysis and distinguish it from an independent station-season sample.
- [ ] Keep maximum SWE, mean TAVG, sum PRCP, and mean ENSO aggregations.
- [ ] Add a clear table explaining that zone and elevation are station constants and ENSO is a season constant.
- [ ] Keep elevation numeric in DS1/DS2 and do not discretize it until the analysis stage.
- [ ] Explain why zone is not encoded immediately as coordinates, ocean distance, or HUC code.
- [ ] Keep the USDA map, but integrate it into a concise table/layout rather than making it the main narrative.

### 5.2.1 Mediciones incompletas

- [ ] Replace “only SWE and ENSO enter the model” with a correct statement of numeric and categorical variables.
- [ ] Keep removal of station-seasons missing any of the five December–April months.
- [ ] Keep the concise discussion of why neighbor and same-station imputations create pseudo-observations.
- [ ] Keep the Spearman missingness check as a descriptive check, not proof that missingness is ignorable.

### 5.2.2 Cantidad y dispersión

- [ ] Split the Stampede Pass discussion into the general Niña-versus-Niño pattern and the substantial within-phase variability.
- [ ] Keep the statement that SWE decreases over time and that factors outside ENSO should remain a limitation or control issue.
- [ ] Keep the station filter of at least 30 of 46 complete seasons.
- [ ] Explain that this filter addresses both quantity and coverage across ENSO phases.
- [ ] Add a counts-flow table for the station, zone, and row filters.
- [ ] Move or remove the introductory sentence before the graphs so the graphs are easier to read.

### 5.3.1 SWE y ENSO

- [ ] Use `log(1 + SWE)` only as the proposed SWE transformation, and explain it in terms of scale, zeros, and interpretation.
- [ ] Keep ENSO in its original °C scale.
- [ ] Do not per-station-standardize SWE.
- [ ] Rewrite the section around the research implications of the transformation instead of Python implementation details.
- [ ] Discuss the possibility of a zero-aware or other model in the conclusion/alternatives if standard assumptions fail.
- [ ] Verify whether AWDB reports SWE in mm or inches before defining the `+1` shift and back-transformation.

### 5.3.2 Zona y elevación

- [ ] Replace relative elevation terciles with globally fixed or otherwise justified elevation bands unless a later validation requires another definition.
- [ ] Explain the binning criterion and how stations are distributed across bins.
- [ ] Use a contingency-table or chi-squared approach that is appropriate for categorical zone and elevation bands.
- [ ] Quantify zone–elevation association and explain how it affects separation of effects.
- [ ] State the information lost by discretizing elevation and the interpretation of fixed bands.
- [ ] Add a zone-by-elevation contingency table or heatmap with station counts.

### 5.3.3 Modelo

- [ ] Remove unsupported claims that a three-way ANOVA has been validated.
- [ ] Test independence, normality, homoscedasticity, cell coverage, and design rank before fitting or interpreting ANOVA.
- [ ] If independence, normality, or equal variance fail, do not present ANOVA as the inferential result.
- [ ] State the ANOVA formulas and nested models only as a clearly labeled what-if or method-checking section.
- [ ] Rename nested models R0/R1/R2 and reserve M for a multiplicative contrast.
- [ ] Explain treatment and sum-to-zero intercept interpretation only if the ANOVA validation permits it.
- [ ] Explain the n=46 limitation and shared-season structure in the results and limitations.
- [ ] Add a concise, tested coverage table only if the selected model uses zone/band/phase cells.

### 5.3.4 and Conclusión

- [ ] Remove the standalone 5.3.4 complexity appendix and merge the relevant transformation and model discussions into concise sections.
- [ ] Rewrite the conclusion with three paragraphs: summary, challenges/issues, and alternatives or out-of-scope complexity.
- [ ] Keep 46 seasons, residual temporal correlation, zone–elevation association, discretization, and ANOVA validity as limitations.
- [ ] Name ANCOVA, nonparametric tests, season-block resampling, mixed models, and spatial/temporal surfaces as alternatives.
- [ ] Do not implement or deeply derive alternatives because this is primarily a data-preparation project.

## 2. todo.md

### Fixed choices

- [ ] Retain ENSO phases of Niño, Niña, and Neutral for a phase-based what-if model; otherwise preserve continuous ENSO.
- [ ] Retain ±0.5 °C as the default phase threshold and ±0.4/±0.75 as sensitivity thresholds.
- [ ] Keep Neutral as the reference phase for contrasts.
- [ ] Use zone and elevation bands as separate factors rather than constructing elevation bands as nested subcategories within zones.
- [ ] Keep zones with at least six stations only as a coverage safeguard with at least two stations per elevation band.
- [ ] Rename nested model labels R0/R1/R2 and keep log1p as the initial SWE transformation.

### Data-preparation reasoning

- [ ] Keep the Niña/Niño asymmetry rationale for a categorical ENSO factor.
- [ ] Keep the caveat that 46 ENSO seasons are shared and not 10,021 independent ENSO observations.
- [ ] Keep zone categorical and do not use coordinates or proximity for the main categorical comparison.
- [ ] Keep discretization as a deliberate simplification, but remove elaborate cost/mitigation tables.

### Model and diagnostics

- [ ] Include an ANOVA formula only if a validity gate confirms the model is usable.
- [ ] Explain why Type II sums of squares are used if retained.
- [ ] Explain treatment-coding intercepts only after ANOVA validation.
- [ ] Add residual QQ plots, residual-versus-fitted plots, and variance checks by band.
- [ ] Test normality and equal variance with plots and appropriate numerical checks.
- [ ] Remove old row-level Shapiro–Wilk, Breusch–Pagan, Wald, and station-clustered inference claims.
- [ ] Remove station-clustered Wald tests from the main inference.

### Complexity and future work

- [ ] Keep only the n=46 shared-season limitation in the complexity discussion.
- [ ] Mention ANCOVA as a future continuous-covariate alternative.
- [ ] Mention station and season block/mixed models as future alternatives.
- [ ] Mention spatial or spatio-temporal surfaces briefly.
- [ ] Remove appendix code and detailed R/lme4/mgcv formulations.

### Implementation phases

- [ ] Remove any archival, old-code archive, or tag requirement.
- [ ] Keep the reframing of title, question, objectives, pipeline, and method names.
- [ ] Remove unsupported ANCOVA and centered-elevation statements.
- [ ] Keep the station filter and counts-flow table.
- [ ] Keep the zone coverage filter and zone-by-band coverage table.
- [ ] Keep verification of the SWE unit before defining the log1p transformation.
- [ ] Keep a focused comparison of SWE transformations with a table of variable/transformation/rationale.
- [ ] Remove ENSO phase factor work from the main analysis if ANOVA is not valid; continuous ENSO remains available.
- [ ] Add a hard validity gate; if ANOVA is invalid, use the conclusion to point to alternatives rather than fit the model anyway.
- [ ] Remove old tables and figures that depend on row-level ANCOVA or Wald inference.
- [ ] Rebuild and consistency-check the report; remove every number that came from unsupported row-level inference.
- [ ] Ensure no text elsewhere repeats obsolete ANCOVA, centered-elevation, or two-stage-slope claims.

### Repository cleanup

- [ ] Remove unused text, code, CSVs, and graphs.
- [ ] Keep `ds1.csv`, `ds2.csv`, and `ds3.csv` at the `data/` level.
- [ ] Organize intermediate outputs under `data/o1/`, `data/o2/`, and `data/o3/`.
- [ ] Keep the Spanish and English READMEs only if they accurately describe the final project.
- [ ] Remove obsolete row-level output and analysis paths.

### Report limits

- [ ] Keep the requested word/page limits for Presentación, Dataset, Objetivos, Desarrollo, and Conclusiones.
- [ ] Keep Desarrollo around 2000 words and Conclusiones around 500 words.

## 3. todo_2.md

- [ ] Keep the report focused on data preparation, not Python libraries or code mechanics.
- [ ] Mention the two-stage framing of elevation and zone in the conclusion as a future/interpretive alternative.
- [ ] Keep the project’s primary factor presentation without implying that zone bands are hierarchical constructions.
- [ ] Fix citations, cross-references, labels, graph references, table references, and Spanish packages.
- [ ] Remove the repeated `*` explanation in 5.1.1.
- [ ] Keep zone categorical and elevation numeric in DS1/DS2.
- [ ] Explain why zone is not encoded directly and mention latitude, ocean distance, and HUC as rejected or future encodings.
- [ ] Replace the 5.1.2 layout plan with a table above the map/text that classifies numerical and categorical variables.
- [ ] Move the Stampede Pass opening sentence after or beside the graph in an easier-to-read position.
- [ ] Rewrite 5.3.1 to discuss transformation consequences rather than implementation or library details.
- [ ] Use globally fixed or otherwise justified elevation bands rather than zone-relative terciles.
- [ ] Add a contingency table for zone/elevation association and the relevant numerical table.
- [ ] Rename nested models R0/R1/R2 and avoid reuse of M.
- [ ] Keep a coverage check only if a model is retained; otherwise mention it briefly after ANOVA fails validation.
- [ ] Keep n=46 and the effective-replicate limitation in 5.3.3 and the conclusion.
- [ ] Keep the revised complexity discussion as alternatives, sample correlation, discretization, and ANOVA failure.
- [ ] Keep the strong three-paragraph conclusion:
  1. overview of the completed data-preparation work;
  2. principal challenges and limitations;
  3. possible alternatives and why the full statistical complexity is outside scope.
