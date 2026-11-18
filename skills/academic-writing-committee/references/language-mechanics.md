# Language Mechanics

Punctuation and word-level mechanics that make academic prose clean and fluent: hyphens and dashes, coordination with *and*, repetition, flow, generic wording, and the small conventions (abbreviations, numbers, capitals, quotation marks, lists, spelling) that readers notice only when they are wrong. Sentence and paragraph style is in `style.md`; numbers, units, and statistics in `mathematics-and-notation.md`; claim strength in `claims-and-coherence.md`. The rules below follow common American practice (largely *The Chicago Manual of Style*). A venue's style guide, a publisher's house style, or a project's style sheet overrides them; where practice varies, the text says so.

## Contents

1. Hyphens, En Dashes, and Em Dashes
2. Typing the Characters
3. Coordination with *And*
4. Avoiding Repetition
5. Fluency and Coherence
6. Words That Make Text Read as Generic
7. Abbreviations, Numbers, Capitals, Quotation Marks, Lists, and Spelling
8. Checklist
9. What the Manuscript Checker Detects

## Hyphens, En Dashes, and Em Dashes

Three different marks with three different jobs. Using one for another is a typesetting error that copyeditors fix and reviewers notice.

| Mark | Character | Job | Example |
|---|---|---|---|
| Hyphen | - | Joins words into one unit; splits words at line ends | a two-stage procedure |
| En dash | – | Ranges; relations between two equal terms; joins an open compound to another word | pp. 112–118; encoder–decoder |
| Em dash | — | Sets off an interruption or an amplification | The bound is tight—up to a constant—for all *n*. |
| Minus sign | − | Subtraction and negative numbers | −0.4, *x* − *y* |

### Hyphens in Compound Modifiers

**What to do.** Hyphenate a compound that modifies a following noun when the hyphen prevents a misreading or is standard. Leave it open after the noun.

| Before the noun (hyphenated) | After the noun (open) |
|---|---|
| a well-known result | the result is well known |
| a long-term study | effects over the long term |
| a high-dimensional space | the space is high dimensional |
| a data-driven method | the method is driven by data |
| a two-sided test | the test is two sided |

- **No hyphen after an *-ly* adverb:** "a highly accurate model," not "highly-accurate."
- **No hyphen with *very*, *most*, *less*, *least* in most cases:** "a less common case."
- **Number plus unit as a modifier:** hyphenate a spelled-out unit ("a three-layer network," "a 10-minute session"), but not a unit symbol ("a 3 mm gap," "a 5 kg load").
- **Fractions as modifiers** are hyphenated ("a two-thirds majority"); as nouns, many styles leave them open ("two thirds of the sample"). Check the house style.
- **Permanent compounds** follow the dictionary: *decision making* as a noun, *decision-making* as a modifier in many dictionaries. Look the word up once and record the choice.
- **Avoid long hyphenated stacks.** "A state-of-the-art-inspired, easy-to-deploy, low-latency approach" is a noun stack with hyphens; rewrite it as a clause.

**How to check.** Search for each compound modifier you use often in both forms ("long term" and "long-term") and confirm that the form follows the position.

### Prefixes

- Most common prefixes close up in American usage: *nonlinear, preprocessing, multiclass, subgroup, reanalysis, coauthor, postdoctoral*.
- Hyphenate before a capital letter or a numeral (*non-Euclidean, pre-2020*), with *self-* (*self-attention, self-supervised*), and where the closed form misleads or means something else (*re-create* versus *recreate*, *re-sign* versus *resign*).
- Fields differ on some terms (*pretraining* and *pre-training*, *multimodal* and *multi-modal*). Follow the venue or the field's dominant usage, then keep one form everywhere, including figure labels and tables.

### Suspended Hyphens

When two compounds share a final element, keep the hyphen on the first and a space after it:

- "first- and second-order methods," "short- and long-term effects," "4- and 8-bit quantization."

Do not suspend if it makes the phrase hard to parse; write both compounds in full instead.

### En Dashes

**Ranges.** Use an en dash, without spaces, for ranges of numbers, dates, pages, sections, and similar sequences: "1998–2004," "pp. 45–67," "Sections 3–5," "ages 18–25."

- Do not mix the dash with words. Write "from 2019 to 2023" or "2019–2023," never "from 2019–2023." Write "between 5 and 10," never "between 5–10."
- In running prose, "to" is often clearer than a dash, and it is required when a value is negative: "−5 to 3," not "−5–3." `mathematics-and-notation.md` recommends words for ranges in prose; keep the dash for tables, citations, and page numbers.
- Repeat the unit or symbol as the field requires ("10%–20%" or "10–20%"); choose one form.

**Relations between two equal terms.** Use an en dash where the two terms stand side by side as equals and *to*, *versus*, or *and* could replace it: "encoder–decoder architecture," "input–output pairs," "teacher–student training," "price–performance trade-off," "the US–EU agreement."

**Eponymous pairs.** A result named after two or more people takes en dashes between the names: "Kullback–Leibler divergence," "Cauchy–Schwarz inequality," "Navier–Stokes equations," "Bose–Einstein statistics." A hyphen means a single person with a double-barreled name: "the Lennard-Jones potential" honors one person. Writing "Kullback-Leibler" with a hyphen tells the reader it is one name.

**Open compounds (optional, house-dependent).** Chicago joins a prefix or suffix to an open compound with an en dash: "post–World War II," "a machine learning–based method." Many journals use a hyphen instead. The safest fix is to recast: "a method based on machine learning."

**How to check.** Search for `[0-9]-[0-9]` and for "from ... –" and "between ... –" patterns; search the bibliography and text for each eponymous name and confirm that the dash is the same everywhere.

### The Minus Sign

A minus is not a hyphen. In mathematics, tables, and negative values, use the true minus (U+2212) or math mode in LaTeX. A hyphen looks too short, may break across a line ("−" at the end of one line and "0.4" on the next), and is read incorrectly by screen readers and by text search.

- Before: "the coefficient was -0.31" (hyphen). After: "the coefficient was −0.31" or `$-0.31$`.
- Keep a space around a binary minus ("*x* − *y*") and none after a unary minus ("−3").

### Em Dashes

**What to do.** Use an em dash, or a pair of them, for a sharp interruption or for an amplification that commas cannot carry. Use it rarely: a reasonable prior is at most one pair in a paragraph, and many paragraphs with none.

- **Interruption:** "The estimator is unbiased—provided the clusters are balanced—and consistent."
- **Amplification at the end:** "Only one component changed—the tokenizer."

**What not to do.**

- Do not use the em dash as an all-purpose connector between clauses. This habit is frequent in formulaic and machine-generated prose, and it hides the logical relation. Choose the mark that states the relation.
- Do not use spaced hyphens (" - ") or double hyphens ("--") as dashes in the final text.

| Habitual dash | Repair |
|---|---|
| "We fine-tune the model—this improves recall." | "Fine-tuning the model improves recall." |
| "The method is simple—and it scales." | "The method is simple, and its cost grows linearly with the number of nodes." (state what *scales* means) |
| "Three factors matter—data, compute, and tuning." | "Three factors matter: data, compute, and tuning." |
| "The effect vanished—suggesting a confound." | "The effect vanished, which suggests a confound." |

- Use a **colon** to introduce a list, an explanation, or an example; **commas** for light parentheticals; **parentheses** for asides the reader can skip; a **semicolon** between closely related independent clauses; a **period** when the second clause stands on its own.
- **Spacing.** American and Chicago style set the em dash closed (no spaces). Many British publishers and some journals use a spaced en dash ( – ) instead. Follow the house style and use one form throughout.

**How to check.** Count em dashes per page; if several paragraphs contain more than one pair, replace most with commas, colons, parentheses, or separate sentences. Search for " - " and "--" in the rendered output.

## Typing the Characters

| Mark | LaTeX | Unicode / Markdown | Word processors |
|---|---|---|---|
| Hyphen | `-` | U+002D, the ordinary key | ordinary key |
| En dash | `--` | U+2013 (–) | Windows: Ctrl + numeric-keypad minus, or Alt+0150; macOS: Option + hyphen |
| Em dash | `---` | U+2014 (—) | Windows: Ctrl + Alt + numeric-keypad minus, or Alt+0151; macOS: Option + Shift + hyphen |
| Minus | `$-$` (math mode) | U+2212 (−) | Insert Symbol, or an equation editor |
| Nonbreaking hyphen | `\nobreakdash-` (amsmath) or an `\mbox{}` | U+2011 | Word: Ctrl + Shift + hyphen |

- **LaTeX.** `--` and `---` become dashes in text mode only. Inside math, `-` is already a minus. Write `Kullback--Leibler`, `pp.~45--67`, and `$-0.3$`. Keep a tie (`~`) before references ("Figure~\ref{fig:loss}") so the number does not start a line.
- **Markdown.** Plain Markdown does not convert hyphens. Some processors do (Pandoc's `smart` extension turns `--` into an en dash and `---` into an em dash); others, including many web renderers, leave them as typed. Either type the Unicode characters or confirm what your toolchain does by inspecting the rendered output.
- **Word processors.** AutoCorrect may turn "--" into a dash depending on settings and context, sometimes the wrong dash. Inspect the result rather than trusting it.
- **Bibliographies.** BibTeX and CSL pass page ranges and names through. Write `pages = {45--67}` and use `--` in eponymous names inside titles.

## Coordination with *And*

**Chains.** A sentence that links three or more clauses with *and* hides which step matters and how they relate. Split it, subordinate it, or turn it into a list.

- Before: "We collected the data and cleaned it and trained the model and it performed well."
- After: "After cleaning the data, we trained the model, which reached 91% accuracy on the held-out set." (values illustrative)

**"And also," "and additionally," "as well as also."** Redundant. Use one: "and," "also," or "as well as."

**Serial comma.** Use the comma before the final conjunction in a list of three or more ("data, code, and models"), as Chicago and most American styles do. Some venues and British styles omit it. Choose one and apply it everywhere, adding it in any case where omission creates ambiguity ("we thank our advisors, Ana and Ben" can read as an appositive).

**"And/or."** Avoid it. Write "A or B or both," "A, B, or both," or just "or" when inclusion is obvious. In formal definitions, say "inclusive or" once if it matters.

**Starting a sentence with *And* or *But*.** Grammatical, and occasionally useful for emphasis. In academic prose a sentence-initial *But* is more acceptable than *And*; use either rarely, and never as a habit at the start of paragraphs.

**Both ... and, either ... or, not only ... but also.** The two parts must be grammatically parallel and placed directly before the elements they join.

- Before: "The method both reduces latency and memory."
- After: "The method reduces both latency and memory."
- Before: "We not only evaluated on images but also text."
- After: "We evaluated not only on images but also on text." Better, often: "We evaluated on images and text." *Not only ... but also* adds emphasis; used repeatedly, it reads as a formula.

**Parallelism.** Items joined by *and* or *or*, and items in a list, share a grammatical form: "to collect, to clean, and to analyze" or "collecting, cleaning, and analyzing," not a mix. Comparisons follow the same rule: "more accurate than the baseline and cheaper to train," not "more accurate than the baseline and its training cost is lower."

**How to check.** Search for " and " and look for sentences containing three or more; search for "and also," "and/or," and sentences that begin with "And."

## Avoiding Repetition

**Repeated words in nearby sentences.** The same content word three or more times in a short span, or twice in one sentence, (outside fixed technical terms) makes the text feel padded. Replace the ordinary word, use a pronoun with a clear antecedent, or combine the sentences.

- Before: "This approach is an important approach because it addresses an important gap."
- After: "This approach matters because it fills a gap that the two dominant methods leave open."

**Repeated sentence openings.** Several consecutive sentences starting with "The model," "We," "This," or "In addition" produce a drumbeat. Vary the openings by putting known information first (given-new order, below), subordinating, or merging.

- Before: "We train on A. We evaluate on B. We compare with C. We find D."
- After: "We train on A and evaluate on B. Against the strongest baseline, C, the method reduces error by 12% (illustrative)."

**Stacked additive transitions.** "Moreover ... Furthermore ... Additionally ... In addition" in successive sentences signals a list disguised as prose and says nothing about the relation. Most of these words can be deleted; when they cannot, the paragraph usually needs a real connective (because, however, therefore) or a list.

- Before: "Moreover, the method is fast. Furthermore, it is accurate. Additionally, it is simple."
- After: "The method is fast (3 ms per query), accurate (94% on the benchmark), and simple to implement (about 40 lines)." (values illustrative)

**Restating the same point in several sections.** The abstract, introduction, and conclusion should agree, but each does a different job (`claims-and-coherence.md`). Inside the body, say a thing once in full, then refer back ("the clipping argument in Section 3.2") rather than re-explaining it. In textbooks, deliberate recaps at chapter ends are pedagogy, not repetition; keep them short and new in wording.

**Elegant variation versus fixed terms.** Vary *ordinary* words; never vary *technical* terms. A reader assumes that "feature," "attribute," and "variable," or "accuracy" and "performance," name different things. Once a term is defined, it stays fixed in text, tables, figures, captions, and the abstract. Keep a term list (the consistency editor checks the text against it).

| Vary freely | Keep fixed |
|---|---|
| show, indicate, reveal (for ordinary reporting) | defined terms, model and dataset names |
| large, substantial, sizable | metric names (F1, recall, BLEU) |
| method, approach (only before either becomes a defined term) | notation, units, abbreviations |

**How to check.** Read each paragraph and mark content words that occur three or more times; list the first word of each sentence on a page and look for runs; search for the additive transitions and count them per page.

## Fluency and Coherence

**Given-new order.** Start a sentence with something the reader already has (a term from the previous sentence, a pronoun with a clear antecedent) and end with the new information. This links sentences without transition words.

- Before: "A 12% error reduction is achieved by dropout. Regularization methods were compared in Section 4."
- After: "Section 4 compares regularization methods. Of these, dropout reduces error the most, by 12%."

**Topic sentences.** The first sentence of a paragraph states its point; the rest supports it. The ladder test in `style.md` checks this.

**Transitions that state the relation.** Pick the connective for the logical relation and confirm the relation holds: *because* and *therefore* claim causation or inference; *however* claims contrast; *for example* claims an instance. "Additionally" between a claim and its counterexample is wrong, not merely weak.

**Paragraph unity.** One point per paragraph. If a paragraph needs two topic sentences, split it. If two adjacent paragraphs make the same point, merge them.

**Sentence-length variety.** Mix short and medium sentences; keep long ones for tightly bound qualifications. A page of uniform medium-length sentences reads as mechanical even when each is correct.

**Signposting in moderation.** One roadmap per paper or chapter, and short bridges between sections. Delete sentences that only announce ("In this section, we will discuss..."); replace them with the claim the section makes.

**How to check.** Read the passage aloud. Wherever you add a word to make it flow, the written text needs that word. Then read only the first sentence of each paragraph in order.

## Words That Make Text Read as Generic

Some words and frames appear so often in boilerplate, promotional text, and unedited machine output that readers discount the sentences that carry them. None is forbidden; each is a prompt to say something specific instead. The test: delete the phrase, and if nothing is lost, leave it deleted; if something is lost, write that thing directly.

| Generic | Write instead |
|---|---|
| "In today's rapidly evolving landscape ..." / "In recent years, X has gained significant attention." | The specific problem and why it matters now, with a fact. |
| delve into, dive into, explore (as filler) | study, measure, analyze, prove, or the actual action |
| plays a crucial / pivotal / vital role | the specific effect: "accounts for 40% of latency" |
| leverage, harness, utilize | use |
| robust, comprehensive, holistic, seamless (unqualified) | name the perturbation, the coverage, or the property |
| novel, groundbreaking, cutting-edge, paradigm shift | say what is new and against what (`claims-and-coherence.md`) |
| a testament to, underscores, highlights the importance of | state the conclusion and its evidence |
| sheds light on, paves the way for, unlocks the potential of | what the result lets someone do |
| tapestry, landscape, realm, journey, intricate interplay | the literal subject |
| "It is worth noting that ..." / "It is important to note that ..." | state the point |
| "X is not just Y; it is Z." | "X does Y and Z," with the evidence for Z |
| "In conclusion," / "Overall," / "In summary," before every closing sentence | a closing sentence that adds the consequence |

Structural habits that read as generic:

- **Reflexive triplets.** Three adjectives or three parallel clauses in every other sentence ("fast, scalable, and robust"). Keep the items you can support; two specific claims beat three vague ones.
- **Summary sentence at the end of every paragraph** that restates the topic sentence. End on the consequence or the handoff instead.
- **Bold-lead bullet lists** where an argument belongs. Reasoning needs connected prose.
- **Bare "This"** opening a sentence ("This shows..."). Give it a noun: "This bound shows...".
- **Uniform paragraph shape** (claim, three supports, summary) repeated throughout.

**How to check.** Search the draft for the left column of the table. For each hit, try deleting the phrase, then try the specific replacement. Integrity questions about AI use and disclosure are in `integrity-and-ai.md`.

## Abbreviations, Numbers, Capitals, Quotation Marks, Lists, and Spelling

### Abbreviations and Acronyms

- Define each acronym at first use in the abstract and again in the body: "large language model (LLM)." In long works, redefine at the start of each chapter where readers may enter.
- Do not define acronyms you use only once or twice; write the words. Do not define the same acronym twice in one section.
- Plurals take *s* without an apostrophe: "LLMs," "GPUs," "the 1990s."
- Choose *a* or *an* by sound: "an MLP," "an SVM," "a UNet."
- Latin abbreviations: in American usage, "e.g.," and "i.e.," take periods and a following comma, and many styles keep them inside parentheses; in running text prefer "for example" and "that is." "Et al." has a period after *al.* "Etc." does not belong after "for example" or "such as."
- Venues often fix abbreviations for "Figure," "Equation," and "Section" (for example, "Fig." in some engineering styles). Follow the venue and be consistent.

### Numbers and Units

Rules for precision, units, percentages, and uncertainty are in `mathematics-and-notation.md`. Two additional mechanics:

- **Words or numerals.** Styles differ: Chicago's general rule spells out whole numbers through one hundred; APA and most scientific styles use numerals from 10 up and for any number with a unit. Check the venue and apply one rule. Always use numerals with units, percentages, and statistics, and never begin a sentence with a numeral.
- **Thousands and decimals.** Use the separators the venue specifies (comma, thin space, or none for four-digit numbers); keep a leading zero before decimals unless the style omits it for quantities that cannot exceed 1.

### Capitalization

- Capitalize a numbered element: "Figure 3," "Table 2," "Section 4," "Theorem 1," "Equation (5)." Lowercase the generic noun: "the next figure," "the theorem above."
- Keep names of methods, models, datasets, and software exactly as their creators write them, and verify the spelling against the original source.
- Do not capitalize ordinary technical terms for emphasis ("Machine Learning," "Gradient Descent") unless they are proper names.
- Headings follow the venue: title case (Chicago) or sentence case (many journals). Apply one rule to every heading, and one rule to every table column header and figure title; the two rules may differ. This guide uses Chicago title case for headings and sentence case for table column headers.

### Quotation Marks

- American style uses double quotation marks, with single marks for a quotation inside a quotation. Periods and commas go inside the closing mark; colons and semicolons go outside; question marks go inside only if they belong to the quotation. British style differs. In computing, some styles place punctuation outside quotation marks around literal strings to avoid changing the string; state the convention and use code formatting for literals where possible.
- Avoid scare quotes. If a word is wrong, replace it; if it is a term being introduced, italicize it once at its definition.
- In LaTeX, type opening quotes as two backticks and closing quotes as two apostrophes, or use `\enquote{}` from the csquotes package. Straight quotes typed as `"` render incorrectly.

### Lists

- Introduce a vertical list with a complete sentence ending in a colon, or with a heading.
- Items are grammatically parallel. If items are full sentences, capitalize them and end each with a period. If they are fragments, follow the house style (often lowercase, no final punctuation) and apply it to every list.
- Run-in lists use the serial comma and, if numbered, parenthesized numerals: "(1) data, (2) code, and (3) models." Use semicolons between items when items contain commas.

### Spelling Consistency

- Choose American or British spelling to match the venue or project and apply it everywhere, including figure labels and supplementary material: *modeling* or *modelling*, *analyze* or *analyse*, *behavior* or *behaviour*. Some publishers use *-ize* with British spelling (Oxford spelling); follow the house style.
- Fix one form for variant compounds: *dataset* or *data set*, *trade-off* or *tradeoff*, *email* or *e-mail*, *fine-tune* or *finetune*. Record the choices in the project's style sheet.
- Run a spell checker set to the chosen variant, and search for the other variant's common forms.

## Checklist

- [ ] Compound modifiers are hyphenated before the noun and open after it; no hyphens after *-ly* adverbs.
- [ ] Prefixed terms use one form throughout (*pretraining* or *pre-training*).
- [ ] Ranges use an en dash (or "to") and never "from ... –" or "between ... –"; negative ranges use "to."
- [ ] Eponymous pairs and relations between equal terms use en dashes (Kullback–Leibler, encoder–decoder).
- [ ] Negative numbers and subtraction use a true minus or math mode.
- [ ] Em dashes are rare and purposeful; no spaced hyphens or double hyphens in the rendered output.
- [ ] No chains of *and*; no "and also" or "and/or"; serial comma applied consistently.
- [ ] Paired constructions (both ... and, not only ... but also) are parallel.
- [ ] No content word repeated three or more times in a short span (or twice in one sentence); no runs of identical sentence openings.
- [ ] No stacked additive transitions; every connective states a relation that holds.
- [ ] Technical terms, names, and abbreviations are fixed; only ordinary words vary.
- [ ] First sentences of paragraphs read as a coherent summary.
- [ ] Generic phrases from the table above are replaced by specific statements.
- [ ] Acronyms defined once at first use (and in the abstract); unused acronyms removed.
- [ ] Numbers, capitals, quotation marks, list punctuation, and spelling follow one convention.

## What the Manuscript Checker Detects

`scripts/check_manuscript.py` is a read-only lint for Markdown, LaTeX (`.tex` and `.texview`), and plain text. Before the prose rules run, it masks mathematics, code, citations, cross-references, URLs, comments, quoted passages, and italic mentions of words (a list such as *may, might, could*, or a single *and*). Quoted examples and other people's words are therefore not checked as the author's prose. Each finding has a line number, a rule id, and a severity: an error for clearly broken text, a warning for a mechanical error or a claim that needs evidence, a note for a stylistic pattern. `--list-rules` prints every rule id. `--disable` switches rules off, `--no-style` switches off the style rules, and `--allow-terms` names fixed terms that may repeat or keep their hyphen. It detects:

- **Hyphens and dashes.** Warnings: a hyphen in a numeric range in prose (`12-15`, `2019-2023`, `0.1-0.5`), but not in dates such as `2024-05-01` or numbering such as `Figure 3-2`; a dash range after `from` or `between`; a spaced hyphen used as a dash; `--` or `---` typed in the prose of a Markdown or text file. Also warnings: an eponymous pair joined by a hyphen, from a list of 64 (`Kullback-Leibler`, `Karush-Kuhn-Tucker`); a hyphen after an adverb in `-ly` (`widely-used`, but not `family-wise`, `early-stopping`, or a proper noun such as `Plotly-based`); the same word twice in a row (but not `in in-context`). Notes: a spaced em dash; a spaced en dash between words used as a break (` -- ` in LaTeX, ` – ` elsewhere), which American style closes up as an em dash; more than two em dashes in one paragraph; a hyphen typed as a minus sign before a number. Two equal terms joined by a hyphen, from a list of 35 (`encoder-decoder`, `input-output`), are notes, because many venues accept the hyphen.
- **Coordination.** A sentence with three coordinating `and` is a note; one with four or more is a warning. An `and` in parentheses, at the end of a serial list, after `between` or `both`, or in a pair of words that closes a phrase is not counted. Notes: `and also`, `and/or`, an ampersand in running prose, and a sentence that begins with `And`.
- **Repetition (notes).** Three or more consecutive sentences that start with the same word, after `The`, `A`, or `An` (prepositions are skipped). Additive transitions (`Moreover`, `Furthermore`, `Additionally`, `In addition`, `Also`, `Besides`) opening two of any three consecutive sentences. A content word of five or more letters used three times within 40 words. A phrase of three or more words repeated close together (within about 300 words) in the same paragraph. Words in headings, and words that recur throughout a file (at least 8 times and 2 per 1,000 words), count as the document's fixed terms: they are not reported as repeated words, nor are phrases that begin and end with them.
- **Wording (notes).** Wordy phrases with plainer equivalents (`in order to`, `due to the fact that`). A subset of the stock generic phrases of the table above (`delve into`, `plays a crucial role`, `paving the way`, `in the realm of`, `tapestry`, `showcase`, `seamless`, `multifaceted`, `holistic`); the rest of the table is for the reader to catch. Empty openers (`it is important to note that`, `it can be seen that`). By default a sentence over 40 words is a note and one over 60 words a warning; masked mathematics does not count.
- **Claims (see `claims-and-coherence.md`).** Warnings: overstatement words (`undoubtedly`, `obviously`, `definitely`, `guarantees`, `clearly shows`) unless negated, with `guarantees` and `universally` left alone in mathematical text and in technical phrases such as `guarantees convergence` or `universally consistent`; `prove` with an empirical subject (`our experiments prove`), or in text that is not mathematical, but not in a theorem, a proof, an exercise instruction, a negation, a sentence with mathematics, or a sentence that points to a section or appendix (`In Section 4 we prove`); `state of the art`, `outperforms all`, or `best-performing` with no citation, cross-reference, or number in the sentence (but not `the best-performing configuration` chosen on one's own validation runs). Also warnings: priority and gap claims in a claim frame (`the first to`, `is the first study`, `we show for the first time`, `to our knowledge ... first`, `unprecedented`, `has never been studied`, `little is known`), but not ordinal enumeration (`the first method ..., the second`) or `saw it for the first time`; absence claims stated as findings (`no effect`, `no difference`, `did not differ`, `not significantly different`, `not associated with`, and `were equivalent` about groups or conditions), but not in mathematical text; unsupported attribution (`several studies have shown`, or a sentence that opens `Studies show`, without a citation); `significant` or `significantly` with no statistic (a comparison with a number, a percentage, an interval, or a named statistic) in the same or the next sentence; causal wording (`causes`, `leads to`, `increases the risk of`), with `--observational`. Notes: certainty words applied to results (`clearly outperforms`; a noun subject with `always` or `never`, such as `the method always converges`; `we solve`); hype words (`novel`, `groundbreaking`, `revolutionary`); underselling (`is merely`, `merely a`, `just a`, `only slightly`, `somewhat`, `a bit`, `we attempt to`); stacked hedges (two hedges in one clause, or three in one sentence).
- **Housekeeping.** Placeholders and to-do markers (including `???`, `[citation]`, `[refs]`, and those in `\title` or `\author` in the LaTeX preamble, but not code in `\verb`, `\texttt`, or an indented code block), and a run in which no file has prose, are errors; a file without prose beside files that have it (a table-only companion file), and a LaTeX file that only includes other files, are notes. Possible personal identifiers, labeled figures and tables never referred to, and references to labels that do not exist are warnings. Notes: a Markdown mention of a figure or table that no caption line matches, and acronyms never expanded or used before their expansion.

Every finding is a prompt for judgment, not a verdict. Fixed technical terms legitimately repeat, a causal verb is right for a randomized experiment, and an em dash can be the best mark in a sentence. A clean report does not mean the prose is fluent; the language reviewer and line editor still read the text.
