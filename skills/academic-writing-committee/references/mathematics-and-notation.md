# Mathematics, Notation, and Numbers

Notation, equations, formal statements, algorithms, the reporting of numbers, and statistical reporting, for authors and for reviewers checking the statistics of a manuscript.

## Contents

1. Notation
2. Equations in Prose
3. Definitions, Theorems, and Proofs
4. Algorithms
5. Numbers and Units
6. Statistical Reporting
7. Final Checks

## Notation

- **One symbol, one meaning; one meaning, one symbol.** Never reuse a symbol for a second quantity, and never give one quantity two symbols. This rule is the mathematical form of the one-term rule.
- **Define every symbol at first use,** in words, in the sentence where it appears: "Let *n* denote the number of training examples." Redefine at the start of a chapter if readers may enter there.
- **Keep a notation table** from the first day of drafting (symbol, meaning, where introduced). Publish it in a thesis, a book, or any paper with more than about a dozen symbols.
- **Define symbols as macros** in LaTeX or as named styles elsewhere, so that a change is made once and typography stays uniform.
- **Follow the field's conventions** unless there is a reason not to: for example, vectors and matrices in a consistent bold or uppercase style, sets in calligraphic or blackboard type, random variables uppercase with realizations lowercase, estimates marked with a hat. State the conventions once.
- **Choose mnemonic symbols** and avoid collisions with the field's standard uses. Avoid decorated stacks (a tilde over a hat over a subscripted symbol); name a new quantity instead.
- **Subscripts and superscripts.** Use roman type for labels (*x* with subscript "max") and italic for indices. Do not let a superscript be read as a power when it is an index.
- Use words for words: write "for all" and "there exists" in running text, and keep logical symbols for displayed formal statements.

## Equations in Prose

- **An equation is part of a sentence.** Punctuate it: a comma or period after a displayed equation where the sentence requires one. Read the passage aloud, equation included, to check that it parses.
- **Say what the equation is before or as you show it,** and say what it means after: which term does what, what happens in a limiting case, why the reader should care.
- **Display** equations that are important, long, or referred to later; keep short expressions inline. Number the displayed equations you refer to (or all of them, if the venue does), and refer by number: "Equation (4)" or "(4)," as the venue prefers.
- **Do not start a sentence with a symbol,** and separate two formulas with words: "For *n* > 2, the bound holds," not "*n* > 2, *f*(*n*) holds."
- **Derivations.** Show every step the intended reader could not supply in a line of mental work, and justify each step in words ("by the triangle inequality," "substituting (3)"). Align multi-line derivations on the relation sign. In a research paper, long routine algebra goes to an appendix; in a textbook, it usually stays, because the steps are the lesson.
- **State assumptions and domains** with the result, not pages earlier: the range of each variable, regularity conditions, and when the expression is undefined.
- Keep "where" lists after an equation short. If more than three symbols need defining there, define them before the equation.

## Definitions, Theorems, and Proofs

- **Definitions** are exact and minimal. Italicize the term being defined, say what kind of object it is, and follow with an example and a non-example.
- **Motivate before stating.** One or two sentences on what question the definition or theorem answers. After a formal statement, restate it in plain words.
- **Theorem statements are self-contained:** all hypotheses appear in the statement, quantifiers are explicit and in the right order, and the conclusion is separated from the hypotheses. Label a result by what it establishes (complexity, correctness, convergence, a bound) and use the label consistently.
- **Proofs.** Begin by naming the strategy (induction on *n*, contradiction, construction). Mark where each hypothesis is used; a hypothesis never used is a sign of an error or a stronger theorem. End clearly. In a paper, give a proof sketch in the body that conveys why the result is true and put the full proof in an appendix; in a textbook, give the full proof when it teaches a technique and a reference when it does not.
- Use *lemma*, *proposition*, *theorem*, and *corollary* consistently by weight, and number them in one sequence so that readers can find them.
- **State a formal problem** as *Given* (inputs and assumptions), *Goal* (what to compute, prove, or optimize), and *Constraints*.
- Claim a result as proved only if the proof is in the document or cited. Otherwise call it a conjecture, a heuristic argument, or an empirical observation.

## Algorithms

Present an algorithm at three levels: the idea in a sentence or two, a small example or diagram, and pseudocode.

- Pseudocode lists inputs, outputs, and parameters first; uses the paper's notation; numbers its lines if the text refers to them; and is independent of any programming language.
- State what is guaranteed (correctness, complexity in time and space, convergence) and under which assumptions, and distinguish proved guarantees from observed behavior.
- Report what a reader needs to reimplement it: initialization, stopping rule, tie-breaking, hyperparameters and how they were chosen, random seeds.

## Numbers and Units

Every reported number has a full description somewhere in the document: what it measures, its unit and scale, the numerator and denominator where there is one, the population or analysis set and its size, the time point, and its uncertainty.

- **Units.** Use SI units and standard symbols, with a space between number and unit ("5 kg," "20 °C") and no period after the symbol. Give the unit in table headers and on axes. State currency and price year for money.
- **Precision.** Report as many digits as the measurement and the sample justify, and no more: usually two or three significant digits for estimates, and the same number of decimals within a column. A percentage of a sample under 100 rarely deserves a decimal.
- **Percent and percentage points.** A rise from 10% to 15% is 5 percentage points and 50 percent. Say which.
- **Give the count with the proportion:** "71% (212 of 300)."
- **Distinguish** zero, missing, not measured, not applicable, and below the detection limit.
- **Ranges and intervals.** Write "from 3 to 7" or "3 to 7," and avoid a dash where negative numbers are possible.
- **Consistency.** The same quantity carries the same value, unit, and rounding in the abstract, text, tables, figures, and supplement. Re-check after every substantive edit; a late change to one number is a frequent source of mismatch.
- **Trace every denominator.** Counts at each stage (eligible, enrolled, assigned, followed, analyzed) must reconcile, and each outcome needs its own denominator when data are missing.

## Statistical Reporting

### Estimates and Uncertainty

- Report the effect estimate with its unit and a measure of uncertainty (usually a 95% confidence or credible interval), not a p-value alone. State what the interval is.
- Give exact p-values where p-values are used ("p = 0.03," not "p < 0.05"), with the test, its assumptions, and the sample size. Follow the venue's rules for leading zeros and for italic statistics symbols.
- Name the test or model fully enough to reproduce it: inputs, model form, covariates, how uncertainty was computed, software and version.
- Say whether "±" means standard deviation, standard error, or an interval, every time.
- For binary outcomes, give counts and denominators per group, and both absolute and relative effects where the field's guideline asks for them. Keep risk difference, risk ratio, and odds ratio distinct; do not convert one into another in prose, and do not infer an absolute effect without the baseline risk.
- For machine-learning results, report the mean and spread over several seeds or folds, state what varied, and compare with baselines under the same budget.

### What a P-Value Does Not Say

Following the American Statistical Association's 2016 statement: a p-value indicates how incompatible the data are with a specified model; it is not the probability that the hypothesis is true or that the result arose by chance; a threshold alone should not drive a conclusion; it does not measure the size or importance of an effect; and it is interpretable only when all analyses run are reported.

- "Significant" in one group and "not significant" in another does not show that the groups differ. Test the interaction.
- **Absence of evidence.** A nonsignificant result does not establish "no effect" or equivalence. Report the estimate with its interval, and say which effect sizes they rule out; claim equivalence or noninferiority only with a prespecified margin and a matching analysis.
- Do not compute "observed" or post hoc power to explain a null result; it restates the p-value. The interval carries the information.
- Statistical significance is not practical, clinical, or scientific importance. Interpret the size.

### Design and Analysis Must Match

- **Unit of analysis.** Repeated measurements, technical replicates, and members of a cluster are not independent observations. Define the unit, and use an analysis that reflects pairing, nesting, or clustering.
- **Label each analysis** as confirmatory (specified before seeing the relevant data), exploratory (chosen or changed afterwards), or descriptive, and use the same label in methods, results, and discussion. Never present a post hoc analysis as planned.
- **Multiplicity.** State the family of comparisons and how it was handled (a hierarchy of tests, control of family-wise error or false discovery rate, or transparent exploratory labeling). No single correction is right for every case.
- **Missing data.** Report how much is missing, by group and variable, the assumed mechanism, the method used, and a sensitivity analysis.
- **Causal claims from observational data:**
  - State the target contrast (which exposure levels, in which population, over what time).
  - Choose the adjustment set by subject-matter reasoning, ideally shown in a causal diagram, not by screening variables against the outcome.
  - Do not adjust for colliders or for variables affected by the exposure (post-treatment variables).
  - Discuss unmeasured confounding and its likely direction; a sensitivity analysis helps.
- **Prediction models:**
  - Keep training, tuning, and evaluation data separate, and fit preprocessing and feature selection inside resampling, so that no information leaks from the test data.
  - Report calibration as well as discrimination, with uncertainty.
  - Distinguish internal from external validation, and say how the external data differ.
  - Tune baselines with the same effort and budget as the proposed model.

### Statistical Review Checklist

For authors before submission and for reviewers:

- [ ] The target quantity (estimand) and the unit of analysis are stated, and the analysis matches them.
- [ ] Denominators reconcile from eligible to analyzed, per group and per outcome.
- [ ] Missing data are quantified and handled by a stated method, with a sensitivity analysis.
- [ ] Each analysis is labeled confirmatory, exploratory, or descriptive; prespecified analyses match the protocol or registration.
- [ ] The family of comparisons and its multiplicity handling are stated.
- [ ] Every effect has an estimate, an interval, and a sample size; "±" is defined.
- [ ] Model assumptions are stated and checked where the conclusion depends on them.
- [ ] The sample size is justified by the target effect and variability, or the precision achieved is reported.
- [ ] Code and data are available, or the restriction is explained.

### Rules of Thumb to Avoid

Fixed heuristics mislead writers and reviewers alike: "n below 30 is too small," "three replicates suffice," "always apply Bonferroni," "test normality first," "a nonsignificant baseline test proves randomization worked," "a nonsignificant test shows data are missing completely at random." Adequacy depends on the target effect, the variability, the design, and the decision at stake. Give the reasoning for the choice that was made: a sample-size justification states the target effect and the assumed variability, not a convention.

## Final Checks

- [ ] Every symbol is defined at first use and matches the notation table; no symbol has two meanings.
- [ ] Every numbered equation that is referred to exists, and references point to the right one.
- [ ] Each theorem's hypotheses are stated and each is used in the proof.
- [ ] Units appear on every number, axis, and table column that needs one.
- [ ] Percentages recompute from the counts. (Agreement across the whole document is in the Author's Final Audit, `review-and-revision.md`.)
- [ ] No "no effect" claim rests on nonsignificance alone; the rest of the statistics is in the checklist above.
- [ ] Symbols, subscripts, superscripts, and special characters survived conversion to the submission format; check the rendered output, not the source.
