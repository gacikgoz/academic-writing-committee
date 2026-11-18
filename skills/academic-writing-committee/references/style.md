# Prose Style

Sentence- and paragraph-level guidance for any academic document. A venue's style guide or a project's own guidelines override anything here. The numbers in this file (sentence lengths, paragraph sizes) are rough priors, not targets.

## Contents

1. Write for a Defined Reader
2. Sentences
3. Words
4. Calibrated Claims
5. Paragraphs
6. Transitions and Signposting
7. Voice, Person, and Tense
8. Lists, Headings, and Emphasis
9. Before-and-After Repairs
10. Grammar and Usage Traps

## Write for a Defined Reader

- Default reader: a capable graduate student from an adjacent field. Specialists should find the text precise enough to cite; the adjacent reader should be able to follow it without a dictionary.
- Test a passage by asking what that reader knows at this point in the document. Anything used but not yet introduced is a defect, however familiar it is to you.
- For international readers, avoid idioms ("ballpark figure" becomes "approximate value"), prefer common words, state things explicitly instead of relying on shared context, use SI units, and explain examples that depend on one country's institutions.
- Describe people with the terms their community prefers and the venue accepts (person-first or identity-first), and keep participants' own descriptions where that matters.

## Sentences

- **Agent and action.** Put who or what acts in the subject and what it does in the verb. "The model overfits small samples" beats "Overfitting is exhibited by the model in the case of small samples."
- **One idea per sentence.** Put the main point in the main clause, and put new or important information at the end, where readers expect the stress.
- **Old before new.** Open a sentence with something the reader already has, then add to it (`language-mechanics.md`, Fluency and Coherence).
- **Vary length.** Short sentences carry emphasis; medium ones explain; long ones (more than about 30 words) are for lists and tightly bound qualifications, and should be rare. If you run out of breath reading a sentence aloud, split it.
- **Parallel form.** Items in a series, a comparison, or a list take the same grammatical shape (`language-mechanics.md`, Coordination with *And*).
- **Attach modifiers to what they modify.** "To improve accuracy, more data were collected" has no one improving anything; write "To improve accuracy, we collected more data."

### Active and Passive

Prefer the active voice because it names the actor and is shorter. Use the passive on purpose, not by default.

| Use the passive when | Example |
|---|---|
| The actor is unknown or irrelevant | "The manuscripts were copied in the twelfth century." |
| The procedure is standard and the object is the topic | "Participants were randomly assigned to two groups." |
| It keeps the paragraph's topic in subject position | "This estimator is biased when clusters are few." |

Remove empty passives that hide both actor and point: "It was found that X" becomes "We found X" or just "X"; "It can be seen that" becomes "Figure 2 shows that."

## Words

### Prefer the Plain Word

Choose the shorter, more common word when it is equally precise: use, show, help, about, before, enough. Do not swap *show* for *demonstrate* or *use* for *employ*; that raises the register without adding meaning. Replace a weak verb only when a more specific one says more: "is different from" can become "exceeds," and "has an effect on" can become "slows."

| Wordy | Concise |
|---|---|
| due to the fact that | because |
| in order to | to |
| at this point in time | now |
| a majority of | most |
| in the event that | if |
| has the ability to, is able to | can |
| with regard to | about |
| prior to, subsequent to | before, after |
| take into consideration | consider |

| Nominalization | Verb |
|---|---|
| perform an analysis of | analyze |
| make an assumption | assume |
| reach a conclusion | conclude |
| give an explanation of | explain |
| conduct an investigation into | investigate |
| the utilization of | using |

Nouns such as *analysis* or *implementation* are fine as names of things ("the statistical analysis," "our implementation"). The problem is the buried verb, not the noun.

Trim redundant pairs: past history, end result, completely eliminate, close proximity, future plans.

### Replace Vague Words with Measured Ones

| Vague | Specific (illustrative values) |
|---|---|
| fast | 3.2 ms per query |
| many participants | 212 of 300 participants (71%) |
| recently | since 2021 |
| improves accuracy | raises accuracy from 87% to 94% |
| performs well | exceeds 90% accuracy on 7 of 9 datasets |
| several studies | three studies (with their citations) |

Reserve *significant* for statistical significance and report the statistic with it (see `mathematics-and-notation.md`). Otherwise write *large* or *substantial* and give the size, then say why it matters (`claims-and-coherence.md`). Spell out a number that begins a sentence, or recast the sentence.

### Terms, Acronyms, and Jargon

- **One term, one meaning.** Once a concept has a name, use exactly that name everywhere; the rule and its checks are in `language-mechanics.md`, Avoiding Repetition.
- Define each technical term and expand each acronym where it first appears, then use the short form consistently. Redefine in an abstract, and again in a chapter of a long work if readers may enter there.
- Introduce a new concept with a one-sentence definition, a statement of what it is not (how it differs from its nearest neighbor), and one example.
- Cut buzzwords and stacked noun phrases ("a novel synergistic optimization paradigm"). Cut quotation marks used for distancing; if a word is wrong, replace it.

## Calibrated Claims

Hedge once, on the uncertain element, and not at all where the evidence is firm; a language edit must never change claim strength. Verbs, scope, and the calibration ladder are in `claims-and-coherence.md`, which governs claim strength.

## Paragraphs

- A paragraph makes one point. State it in the first sentence, support it with evidence or reasoning, and end by drawing the consequence or handing over to the next paragraph.
- **Ladder test:** copy the first sentence of every paragraph into a list. The list should read as a coherent summary of the section. If it does not, the topic sentences or the order are wrong.
- Typical length is four to eight sentences. A page without a paragraph break, or a run of one-sentence paragraphs, both signal a structural problem.
- Tell the reader what was found, then how: "We found X" before "We ran Y."
- Explain, do not only report. Where you state an effect or a design choice, add the *because* clause: the mechanism or the reason.

## Transitions and Signposting

Choose a connective by the logical relation, and check that the relation really holds (`language-mechanics.md`, Fluency and Coherence).

- The strongest transition is content: end a paragraph on the gap, consequence, or objection that the next paragraph takes up. "Having established A, we can ask B" works; "Next, we discuss B" only announces.
- Between sections, close with what has been established and open with what it makes possible. Between chapters of a long work, open with a short bridge: what the previous chapter gave, what this one must do, why in this order.
- Keep signposting short. One roadmap per document or chapter is enough; delete sentences that only describe the text ("In this section we will talk about ...").

## Voice, Person, and Tense

- First person is accepted in most venues: "we" for the authors, "I" for a single author in the humanities. Check the venue's samples. "This paper argues" and "the study found" are conventional and acceptable; they are the one exception to the rule on human verbs at the end of this file. Avoid giving objects intentions ("the experiment wants to show").
- In textbooks and lecture notes, "we" meaning author and reader together is conventional ("we now compute"); do not switch between "we," "you," and "one" within a passage.

| Function | Tense | Example |
|---|---|---|
| Established knowledge, definitions, general truths | Present | "Gradient descent converges under these conditions." |
| What this document contains or shows | Present | "Section 3 presents ...," "Figure 1 shows ..." |
| What you did (methods) | Past | "We sampled 400 households." |
| What you found (results) | Past | "Accuracy rose by 4 points." |
| What your findings mean | Present | "These results indicate ..." |
| What a specific earlier study did or found | Past | "Lee (2021) measured ..." |
| A line of work continuing to now | Present perfect | "Attention mechanisms have become standard." |

Fields differ: humanities writing discusses texts in the present tense, and computer science describes algorithms in the present. Hold one convention within each function.

## Lists, Headings, and Emphasis

- Use a list for discrete, parallel items (steps, criteria, materials). Use prose for reasoning, because a list drops the connections between items.
- Make headings informative ("Clipping Bounds the Update Norm" tells more than "Analysis"), keep the hierarchy consistent and no deeper than three levels, and avoid a section with a single subsection.
- Emphasize rarely. Italics for a term being defined, bold only where the format expects it. Never let color or weight be the only carrier of meaning.

## Before-and-After Repairs

All values are illustrative. Repairs for generic phrasing, throat-clearing, and term drift are in `language-mechanics.md`; repairs for overclaims, stacked hedges, and vague attribution are in `claims-and-coherence.md`.

| Problem | Before | After |
|---|---|---|
| Empty passive | "It was found that there was a difference between the groups." | "The treated group scored 4.1 points higher (95% CI 1.2 to 7.0)." |
| Buried verb | "We performed an evaluation of the classifier." | "We evaluated the classifier." |
| Vague claim | "The method performs significantly better." | "The method reduces median latency from 48 ms to 31 ms." |
| Unclear pronoun | "The encoder feeds the decoder. It is then frozen." | "The encoder feeds the decoder. The encoder is then frozen." |
| Announcement | "In this section, we will discuss the limitations." | "Two limitations bound these conclusions." |
| Missing mechanism | "Users with a strong identity explored more features." | "Users with a strong identity explored more features, because new features let them extend a tool they regard as their own." |
| Apologetic ending | "Although this study has limitations, more research is needed." | "The effect holds for first-year courses; whether it survives in self-paced courses is the next test." |
| Noun stack | "patient outcome data quality improvement process" | "the process for improving the quality of data on patient outcomes" |

## Grammar and Usage Traps

- **Pronoun without a clear antecedent.** After naming two things, repeat the noun. Give *this* a noun: "this assumption," not a bare "this."
- **Comma splice.** Two independent clauses need a period, a semicolon, or a conjunction.
- **Agreement with a distant subject.** "The set of parameters *is* fixed"; "each of the methods *has* a cost." Treat *data* as plural or singular according to the venue, consistently.
- **Misplaced *only*.** "We tested only three datasets" limits the datasets; "we only tested three datasets" could limit the testing.
- **Incomplete comparison.** "Faster" needs "than what," measured how.
- ***That* and *which*.** In American usage, *that* introduces a restrictive clause and *which* (after a comma) a nonrestrictive one.
- ***Respectively*.** Use it only when two lists really run in parallel, and keep both short.
- **Anthropomorphism and overreach of the subject.** Data show; authors argue; models predict. Models do not "believe" and figures do not "prove."
