# Figures and Tables

How to decide what deserves a display, build it honestly, caption it, and tie it to the text. Venue rules on formats, sizes, counts, and caption placement override this file.

## Contents

1. Prose, Table, or Figure
2. Planning the Exhibits
3. Tables
4. Figures
5. Captions and Text References
6. Honesty and Image Integrity
7. Accessibility and Alt Text
8. Flow Diagrams
9. Figures in Teaching Texts
10. Presentation Pass on Rendered Pages
11. Provenance and Final Review

## Prose, Table, or Figure

| Use | When |
|---|---|
| Prose | A few values that the argument needs directly |
| Table | Exact values matter, or the reader compares along several dimensions |
| Figure | The point is a pattern: trend, distribution, relationship, sequence, structure, or spatial layout |

- A display earns its place when it carries verified content more clearly than a paragraph could. There is no correct number of displays per page.
- Do not present the same data three times. The text states what the display shows and what follows from it; it does not read the table aloud.
- Every display has one message. If you cannot state it in a sentence, split or redesign the display.

## Planning the Exhibits

Plan displays before drafting; they are the frame of an empirical paper and many readers see nothing else.

- An empirical paper usually needs three: a figure of the model, design, or pipeline; a self-contained table or figure of the main results; and a table that makes robustness checks visible instead of burying them in prose.
- A questionnaire-based empirical paper typically adds measurement tables (items and loadings, validity) and a table for mediation or moderation. A computing paper typically adds an overview figure of the approach, a main results table, an ablation table with a column for the change from the full system, and a sensitivity plot.
- Use the same labels in displays as in the text: variable names, group names, abbreviations, and order.
- Design displays so that another person could reuse them to explain the work.

## Tables

- [ ] Title or caption states the population, time point, analysis set, and what the numbers are.
- [ ] Column and row headers carry units; abbreviations are defined in a note.
- [ ] Denominators are shown; percentages can be recomputed from the counts given.
- [ ] Missing, zero, not measured, not applicable, and below the detection limit are distinguished.
- [ ] Precision matches the measurement; decimals are aligned and consistent within a column.
- [ ] Uncertainty and test quantities are named (SD, SE, 95% CI, p), never left to a symbol.
- [ ] Values agree with the abstract, the text, the figures, and the supplement.
- [ ] Layout is quiet: horizontal rules at top, under the header, and at the bottom; no vertical rules; no shading that carries meaning alone.
- [ ] Comparisons run down columns, which the eye scans more easily than rows; rows are in a meaningful order, not alphabetical by default.
- [ ] In results tables, the direction of "better" is marked for each metric, and any highlighting of the best value follows a stated rule (for example, best within one standard error).
- [ ] The table is live text, not an image, wherever the venue allows.

## Figures

- [ ] Axes are labeled with quantity and unit; scales, transformations, and reference lines are explicit.
- [ ] A truncated or nonlinear axis is visible and justified. Bar charts start at zero.
- [ ] Individual observations or the distribution are shown when a summary would hide the structure (small samples, skew, clusters).
- [ ] Error bars and bands are defined in the caption (SD, SE, CI, range), and group sizes are given.
- [ ] Every encoding (color, shape, line style, size) is explained in a legend or by direct labels. Direct labels beat a distant legend.
- [ ] Groups are distinguishable without color: vary shape, line style, or labels as well, and use a palette that survives color-vision deficiency and grayscale printing.
- [ ] Text in the figure is legible at final size, about the size of the caption text and no smaller than the venue allows.
- [ ] Panels that should be compared share axes; panels are lettered and each is described.
- [ ] No decoration: no 3D effects, no unneeded gridlines, no dual axes that imply a relation.
- [ ] Images carry scale bars and orientation where relevant; the choice of a "representative" image is explained.
- [ ] The file is vector for line art and of sufficient resolution for images, in the format the venue asks for.
- [ ] No significance stars, trend lines, or fitted curves appear unless they come from an analysis described in the methods.

## Captions and Text References

- A caption lets the display stand alone: what is shown, what each panel and encoding means, the population and sample size, units, what the uncertainty measure is, and the method needed to read it. One sentence may state the takeaway if the venue allows interpretive captions.
- **Placement differs by style.** Engineering and computing styles commonly put table captions above and figure captions below; APA puts the number and title above both. Follow the venue.
- Number displays in order of first mention, separately by type. Mention every display in the text before it appears, and place it near that mention.
- Refer by number ("Table 2 shows"), never by position ("the table below"), because layout moves.
- Make the reference do work: "Error falls with sample size (Figure 3)" tells the reader what to look for; "see Figure 3" does not.
- In a supplement or appendix, number with a prefix (Figure S1, Table A2) and refer to those from the main text too.

## Honesty and Image Integrity

- A display shows the data that the methods describe. Do not select, crop, rescale, or smooth so as to create an impression the full data would not give.
- Adjust an image only in ways the venue permits, apply the adjustment to the whole image, and disclose it. Never remove, add, move, or duplicate features. Mark splices between lanes or panels.
- Keep the original, unprocessed files and a record of every processing step.
- Do not rebuild data from a screenshot of someone else's published figure, and do not reuse a published figure without the permission its license requires.
- Do not generate or alter research images with generative AI tools and present them as data. Most publishers restrict AI-generated figures of any kind; check the current policy before using one even for a schematic.
- When reviewing, describe a suspected duplication or manipulation neutrally and by location, and send it to the editor only (procedure: `review-and-revision.md`, Suspected Integrity Problem).

## Accessibility and Alt Text

- Alt text names the type of display and its purpose, then the main pattern: the axes, the groups, the direction of the effect, and the uncertainty needed to read it.
- It does not repeat the caption, list every data point, or add a conclusion that the figure does not show.
- Write alt text against the final figure and revise it when the figure changes.
- Check contrast, reading order, label size, and independence from color by eye. Automated accessibility checks do not establish that a figure is correct or readable.
- Provide the underlying numbers (a table or data file) for important figures where the venue allows.

## Flow Diagrams

For participant flow in trials and record flow in systematic reviews, use the current official template of the applicable reporting guideline. Fill it only from verified counts, and reconcile every branch with the methods, the results, and the tables: the numbers entering each box must equal the numbers leaving the previous one, minus stated exclusions.

## Figures in Teaching Texts

- A teaching figure shows one idea. Build a complicated picture in stages across several figures instead of presenting the final state at once.
- Use the notation and colors of the text, and keep the same visual convention for the same concept throughout the book.
- Refer to the figure at the point in the explanation where the reader should look, and say what to notice.
- Prefer a worked diagram of a small, concrete instance to an abstract schematic.
- Write the caption so that a student reviewing only the figures recovers the main point.

## Presentation Pass on Rendered Pages

The source never shows what the reader sees. After every substantial revision, build the document, render its pages as images, and look at each page at reading size. Fix what the pass finds in the source, rebuild, and look again.

- [ ] **Referred to and explained.** Every figure and table is mentioned in the text before it appears, and the text says what it shows and what to notice: "Latency falls as the reserve grows, until about 10% of the slots (Figure 4)" (illustrative), not "see Figure 4."
- [ ] **Captions say what to notice.** Each caption names what is shown and the one thing the reader should see; it does not narrate how the display was produced (that goes to the record below).
- [ ] **Near the first mention.** Each float sits on the page of its first mention or the next one. A float that drifts to the end of the section or chapter is moved in the source (placement options, a shorter display, or a different position of the float in the text).
- [ ] **No large blank areas.** No page is half empty because a float did not fit; no column ends early above a full-width display. Shrink, split, or move the display, or shorten the text around it.
- [ ] **Nothing cluttered.** No display tries to show everything: at most the series and columns the point needs, labels legible at print size, no decorative grid, no repeated legend. A table that repeats numbers the text already lists, or the text that reads out every cell of a table, is cut back to one of the two.
- [ ] **Text and displays agree.** The numbers, names, and order in the text match the display they refer to.

The **presentation** reviewer does this pass in every round that changes displays or layout, and the writer does it before handing a unit over (`committee/roles.md`).

## Provenance and Final Review

Keep a short record for each display: identifier and version, source data, the script or manual steps that produced it, who made and who checked it, date, population and units, and license or permission status. The record stays with the evidence and the availability statement; captions and running text describe what the display shows, not how it was made.

Before submission:

- [ ] Every display is mentioned in the text, and every mention points to an existing display.
- [ ] Numbers in displays match the text, the abstract, and each other.
- [ ] Captions are complete and consistent in form.
- [ ] Each figure was regenerated from the final data and code.
- [ ] Symbols, units, and labels survived format conversion; nothing is clipped at final size.
- [ ] Permissions and attributions for reused material are in place.

`scripts/check_manuscript.py` reports labeled figures and tables that the text never references, and references to labels that do not exist.
