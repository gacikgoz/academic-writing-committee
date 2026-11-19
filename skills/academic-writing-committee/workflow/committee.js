export const meta = {
  name: 'academic-writing-committee',
  description: 'Guideline-driven writing committee: briefs, tiered writers, readers, reviewer and editor committees, iterating until every unit is approved',
  whenToUse: 'Writing or revising a long academic document (book, thesis, paper set, report) that must satisfy a guidelines file, with independent review and editing',
  phases: [
    { title: 'Plan', detail: 'scout units, first reading and developmental briefs' },
    { title: 'Write', detail: 'tiered writers revise their units' },
    { title: 'Read', detail: 'reader personas report confusion, gaps and redundancy' },
    { title: 'Review', detail: 'mechanical checks, reviewer committee and chair decision' },
    { title: 'Edit', detail: 'line and consistency editors polish accepted units, regression check' },
    { title: 'Integrate', detail: 'global checks, integration editor, cross-unit claims review and editor-in-chief' },
    { title: 'Learn', detail: 'retrospective updates lessons, lint rules and roster; commits' },
  ],
}

// ---------------------------------------------------------------------------
// Configuration (all fields arrive through `args`; see committee/config.md)
// ---------------------------------------------------------------------------
const A = args && typeof args === 'object' ? args : {}
if (!A.root || !A.skillDir) throw new Error('args.root and args.skillDir are required (absolute paths)')

const ROOT = A.root
const SKILL = A.skillDir
const STATE = A.stateDir || `${ROOT}/.writing-committee`
const NAME = A.name || 'the document'
const GOAL = A.goal || 'Revise every unit so that it satisfies the guidelines in full.'
// An empty list means the project has no guidelines file: the writing guide and the publication-type section rule.
const GUIDE = Array.isArray(A.guidelines) ? A.guidelines : ['guidelines.md']
const CONTEXT = A.context || []
const WRITING = A.writingSkills || []
const PUBTYPE = A.publicationType || ''
const PUBSECTION = A.publicationSection || ''
const PROFILE_NOTE = A.profileNote || ''
const CHECKS = A.checks || {}
const ASSET_DIR = A.assetDir || ''
const BIB = Array.isArray(A.bibliography) ? A.bibliography : A.bibliography ? [A.bibliography] : []
const READ_FIRST = A.readBeforeBrief !== false  // readers also read the original text before the brief
const PRIOR = A.priorAccepted || []  // [{id, files, tier?}] accepted in earlier runs; judged and reopenable in global rounds
const GLOBAL_FILES = A.globalFiles || []  // prose files of the whole document in reading order
const REFLISTS = Array.isArray(A.referenceList) ? A.referenceList : A.referenceList ? [A.referenceList] : []  // manual reference lists (no bibliography database)
const ONLINE = A.onlineCitations !== false  // global rounds verify references online (Crossref, arXiv, doi.org)
const GLOBAL_ONLY = A.globalOnly === true  // no units to revise: only the global rounds
const LANGUAGE = A.language || 'the language the document is written in'
const LIM = Object.assign({ maxRounds: 5, maxGlobalRounds: 2, waveSize: 6, maxRepairs: 2, maxAgents: 900, laterRoundRounds: 2.5 }, A.limits || {})
const COMMIT = Object.assign({ perWave: true, push: false, branch: '' }, A.commit || {})
const ADAPT = A.adaptRoster !== false
const REVIEW_ONLY = A.reviewOnly === true  // one round of checks, readers, reviewers and chair; no edits
// A shard is one of several workflows that revise disjoint units of the same document at the same
// time (prepare_run.py --shards). Every workflow has its own cap on concurrent agents, so shards are
// how a run gets more agents working at once. A shard runs no global round and keeps its own
// lessons files, which prepare_run.py --record merges into the committee's when the shard ends.
const SHARD = A.shard && Number(A.shard.of) > 1 ? { index: Number(A.shard.index), of: Number(A.shard.of) } : null
const SKIP_GLOBAL = !!SHARD || A.skipGlobal === true
const PLAN_ONLY = A.planOnly === true  // first reading and developmental briefs only; a later run revises
const SFX = SHARD ? `.shard-${SHARD.index}` : ''
const LESSONS = `${STATE}/lessons${SFX}.md`
const LINT = `${STATE}/lint_rules${SFX}.md`
const PROPOSALS = `${STATE}/guideline_proposals${SFX}.md`
const SHARD_NOTE = SHARD ? `This workflow is shard ${SHARD.index} of ${SHARD.of}: other committee workflows are revising other units of this document in the same working tree right now. Their uncommitted files appear in git status and git diff: leave them alone, limit every git command to your own files (for example \`git diff -- <files>\`), and never run a command that resets, cleans, stashes or checks out the working tree.\n` : ''

const MODELS = ['haiku', 'sonnet', 'opus', 'fable']
const EFFORTS = ['low', 'medium', 'high', 'xhigh', 'max']

const R = Object.assign({
  scout: { model: 'sonnet', effort: 'medium' },
  brief: { model: 'opus', effort: 'high' },
  briefCritical: { model: 'fable', effort: 'high' },
  writerTiers: [
    { model: 'sonnet', effort: 'high' },
    { model: 'opus', effort: 'high' },
    { model: 'fable', effort: 'high' },
    { model: 'fable', effort: 'xhigh' },
  ],
  checker: { model: 'haiku', effort: 'low' },
  chair: { model: 'opus', effort: 'high' },
  chairCritical: { model: 'fable', effort: 'high' },
  regression: { model: 'sonnet', effort: 'medium' },
  integration: { model: 'opus', effort: 'high' },
  globalChair: { model: 'fable', effort: 'high' },
  retrospective: { model: 'sonnet', effort: 'high' },
  committer: { model: 'haiku', effort: 'low' },
}, A.roster || {})

// Fallback roster (prepare_run.py always passes the profile's roster; these match the general entries of committee/catalog.json)
const READERS = A.readers || [
  { key: 'newcomer', persona: 'a reader who has the stated prerequisites but meets this topic for the first time; flags every undefined term, skipped step, unexplained symbol, unreadable figure and place where they would ask "what is this?"', model: 'sonnet', effort: 'medium' },
  { key: 'expert', persona: 'a researcher who knows the field well; flags what is imprecise, outdated, shallow or missing (assumptions, guarantees, recent results, failure cases, open problems, key related work) and anything they would skip as already known', model: 'sonnet', effort: 'high' },
]
const REVIEWERS = A.reviewers || [
  { key: 'guidelines', focus: 'compliance with every applicable rule of the guidelines; cite the rule (section and bullet) for each finding', model: 'sonnet', effort: 'medium' },
  { key: 'technical', focus: 'correctness of every definition, claim, derivation, equation, algorithm, number and code fragment; recompute numerical examples with a script; consistent notation, units and dimensions', model: 'opus', effort: 'high', critical: { model: 'fable', effort: 'high' } },
  { key: 'claims', focus: 'calibration and coherence of claims: no overclaiming and no underselling; contributions, numbers, terms and scope identical wherever they recur; conclusions that follow from the evidence', model: 'opus', effort: 'high' },
  { key: 'references', focus: 'every reference is real and correctly described (verify authors, title, venue, year and identifier by search and with the citation checker), and each cited work supports the sentence citing it', model: 'sonnet', effort: 'high' },
  { key: 'presentation', focus: 'figures, tables, equations, lists, headings and layout as rendered; legibility, labels, captions, references to them in the text', model: 'sonnet', effort: 'medium' },
  { key: 'language', focus: 'fluency and coherence: paragraph flow and transitions, repetition, formulaic phrasing, the house rules on dashes, hyphens, conjunction commas, paragraph openings, abbreviations and internal identifiers, chains of and, parallel lists, consistent terms and spelling', model: 'sonnet', effort: 'medium' },
]
const EDITORS = A.editors || [
  { key: 'line', focus: 'prose: clarity, concision, flow between sentences and paragraphs, terminology, capitalization, punctuation, parallel lists; remove filler and repetition without removing substance', model: 'sonnet', effort: 'high' },
  { key: 'consistency', focus: 'notation, terminology and spelling against the shared glossary and the rest of the document; labels, cross-references, captions, table and equation conventions', model: 'sonnet', effort: 'medium' },
]

// Model ceiling (configuration `modelCeiling`): no role runs on a model above it, except the roles it names
// (role names as in roster adjustments: chair, globalChair, writerTier:2, reviewer:technical, ...).
const CEIL = !A.modelCeiling ? null
  : typeof A.modelCeiling === 'string' ? { model: A.modelCeiling, except: [] }
  : { model: A.modelCeiling.model, except: A.modelCeiling.except || [] }
const capped = (role, v) => {
  if (!CEIL || !v || !MODELS.includes(CEIL.model) || CEIL.except.includes(role)) return v
  return MODELS.indexOf(v.model) > MODELS.indexOf(CEIL.model) ? { ...v, model: CEIL.model } : v
}
if (CEIL) {
  for (const k of Object.keys(R)) {
    if (k === 'writerTiers') R.writerTiers = R.writerTiers.map((t, i) => capped(`writerTier:${i}`, t))
    else R[k] = capped(k, R[k])
  }
  for (const [kind, xs] of [['reader', READERS], ['reviewer', REVIEWERS], ['editor', EDITORS]]) {
    xs.forEach((x, i) => {
      xs[i] = capped(`${kind}:${x.key}`, x)
      if (x.critical) xs[i].critical = capped(`${kind}:${x.key}`, x.critical)
    })
  }
}

// Run effort (configuration `effort`, prepare_run.py --effort; the user chooses it): every role runs at it,
// except the mechanical checker and the committer, which keep their own effort. The last writer tier runs
// one level higher, so that escalating to it still adds effort when the model stays the same.
const EFFORT = EFFORTS.includes(A.effort) ? A.effort : null
if (EFFORT) {
  const up = EFFORTS[Math.min(EFFORTS.length - 1, EFFORTS.indexOf(EFFORT) + 1)]
  const at = (v, e) => (v ? { ...v, effort: e } : v)
  for (const k of Object.keys(R)) {
    if (k === 'checker' || k === 'committer') continue
    if (k === 'writerTiers') R.writerTiers = R.writerTiers.map((t, i, all) => at(t, all.length > 1 && i === all.length - 1 ? up : EFFORT))
    else R[k] = at(R[k], EFFORT)
  }
  for (const xs of [READERS, REVIEWERS, EDITORS]) {
    xs.forEach((x, i) => {
      xs[i] = at(x, EFFORT)
      if (x.critical) xs[i].critical = at(x.critical, EFFORT)
    })
  }
}

// ---------------------------------------------------------------------------
// Schemas
// ---------------------------------------------------------------------------
const SEV = { type: 'string', enum: ['blocker', 'major', 'minor', 'nit'] }
const FINDING = { type: 'object', properties: {
  id: { type: 'string' }, severity: SEV, location: { type: 'string' }, rule: { type: 'string' },
  problem: { type: 'string' }, fix: { type: 'string' } }, required: ['id', 'severity', 'location', 'problem', 'fix'] }
const FINDINGS = { type: 'array', items: FINDING }
const STRS = { type: 'array', items: { type: 'string' } }

const S_SCOUT = { type: 'object', properties: {
  units: { type: 'array', items: { type: 'object', properties: {
    id: { type: 'string' }, title: { type: 'string' }, files: STRS,
    difficulty: { type: 'string', enum: ['standard', 'hard', 'critical'] }, goal: { type: 'string' } },
    required: ['id', 'files', 'difficulty'] } },
  notes: { type: 'string' } }, required: ['units', 'notes'] }
const S_BRIEF = { type: 'object', properties: {
  difficulty: { type: 'string', enum: ['standard', 'hard', 'critical'] },
  brief_path: { type: 'string' }, summary: { type: 'string' },
  plan: { type: 'array', items: { type: 'object', properties: { item: { type: 'string' }, rule: { type: 'string' } }, required: ['item'] } },
  shared_change_requests: STRS }, required: ['difficulty', 'brief_path', 'summary', 'plan'] }
const S_WRITER = { type: 'object', properties: {
  report_path: { type: 'string' }, summary: { type: 'string' }, files_changed: STRS,
  resolved: STRS, disputed: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, reason: { type: 'string' } }, required: ['id', 'reason'] } },
  self_check_passed: { type: 'boolean' }, shared_change_requests: STRS }, required: ['report_path', 'summary', 'files_changed', 'self_check_passed'] }
const S_CHECK = { type: 'object', properties: {
  passed: { type: 'boolean' }, findings: FINDINGS, summary: { type: 'string' } }, required: ['passed', 'findings', 'summary'] }
const S_READER = { type: 'object', properties: {
  rating: { type: 'integer', minimum: 1, maximum: 5 }, overall: { type: 'string' },
  findings: { type: 'array', items: { type: 'object', properties: {
    severity: SEV, location: { type: 'string' },
    kind: { type: 'string', enum: ['confusion', 'gap', 'redundant', 'too_basic', 'too_advanced', 'flow', 'figure', 'error', 'praise'] },
    problem: { type: 'string' }, suggestion: { type: 'string' } }, required: ['severity', 'location', 'kind', 'problem', 'suggestion'] } } },
  required: ['rating', 'overall', 'findings'] }
const S_REVIEW = { type: 'object', properties: {
  verdict: { type: 'string', enum: ['approve', 'approve_with_minor', 'revise', 'reject'] },
  findings: FINDINGS, strengths: STRS }, required: ['verdict', 'findings'] }
const S_CHAIR = { type: 'object', properties: {
  decision: { type: 'string', enum: ['accept', 'revise'] }, rationale: { type: 'string' },
  actions: { type: 'array', items: { type: 'object', properties: {
    id: { type: 'string' }, severity: SEV, source: { type: 'string' }, location: { type: 'string' }, instruction: { type: 'string' } },
    required: ['id', 'severity', 'source', 'instruction'] } },
  dismissed: STRS,
  dismissed_checks: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, reason: { type: 'string' } }, required: ['id', 'reason'] } },
  repeated_issues: { type: 'boolean' }, escalate: { type: 'boolean' },
  rerun_reviewers: STRS, rerun_readers: STRS, lessons: STRS },
  required: ['decision', 'rationale', 'actions', 'repeated_issues', 'escalate', 'rerun_reviewers', 'rerun_readers', 'lessons'] }
const S_EDITOR = { type: 'object', properties: {
  summary: { type: 'string' }, files_changed: STRS, concerns: FINDINGS }, required: ['summary', 'files_changed', 'concerns'] }
const S_RETRO = { type: 'object', properties: {
  summary: { type: 'string' }, lessons_added: STRS, lint_rules_added: STRS, guideline_proposals: STRS,
  roster_adjustments: { type: 'array', items: { type: 'object', properties: {
    role: { type: 'string' }, model: { type: 'string', enum: MODELS }, effort: { type: 'string', enum: EFFORTS }, reason: { type: 'string' } },
    required: ['role', 'model', 'effort', 'reason'] } } },
  required: ['summary', 'lessons_added', 'lint_rules_added', 'guideline_proposals', 'roster_adjustments'] }
const S_INTEG = { type: 'object', properties: {
  summary: { type: 'string' }, files_changed: STRS, remaining: FINDINGS }, required: ['summary', 'files_changed', 'remaining'] }
const S_GLOBAL = { type: 'object', properties: {
  decision: { type: 'string', enum: ['approve', 'reopen'] }, rationale: { type: 'string' },
  reopen: { type: 'array', items: { type: 'object', properties: { unit: { type: 'string' }, actions: STRS }, required: ['unit', 'actions'] } },
  remaining_issues: STRS }, required: ['decision', 'rationale', 'reopen', 'remaining_issues'] }
const S_COMMIT = { type: 'object', properties: {
  committed: { type: 'boolean' }, sha: { type: 'string' }, pushed: { type: 'boolean' }, note: { type: 'string' } },
  required: ['committed', 'pushed'] }

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
const pick = (o) => ({ model: MODELS.includes(o.model) ? o.model : undefined, effort: EFFORTS.includes(o.effort) ? o.effort : undefined })
const list = (xs) => xs.map(x => `- ${x}`).join('\n')
const json = (x) => JSON.stringify(x, null, 1)
const unitDir = (u) => `${STATE}/units/${u.id}`
const isCritical = (u) => u.difficulty === 'critical'
const startTier = (d) => (d === 'critical' ? 2 : d === 'hard' ? 1 : 0)
const RANK = { standard: 0, hard: 1, critical: 2 }
const stronger = (a, b) => ((RANK[a] || 0) >= (RANK[b] || 0) ? a : b)
const isHeavy = (f) => f.severity === 'blocker' || f.severity === 'major'
let agentsLaunched = 0
const rosterApplied = []

async function call(prompt, opts) {
  // One retry on a null result (skipped agent or terminal API error).
  for (let attempt = 0; attempt < 2; attempt++) {
    agentsLaunched++
    const r = await agent(prompt, opts)
    if (r) return r
    log(`retrying ${opts.label} after an empty result`)
  }
  return null
}

// Mechanical roles need only the standards and the checkers, not the whole writing guide.
const GUIDE_LIGHT = new Set(['Mechanical Checker', 'Committer'])

function contract(roleTitle, extra) {
  return `You are the ${roleTitle} of an academic writing committee working on ${NAME}.
Project root: ${ROOT} (run every command from there). Committee state directory: ${STATE}.
Goal of this run: ${GOAL}
Before anything else read, in this order:
1. Your role contract: the section "${roleTitle}" in ${SKILL}/committee/roles.md, and the shared rules at the top of that file.
2. The severity scale and gates in ${SKILL}/committee/quality-gates.md.
2a. ${GUIDE_LIGHT.has(roleTitle) ? `The sections "Five Standards Every Text Meets" and "Checkers" of the academic writing guide, ${SKILL}/SKILL.md.` : `The academic writing guide: ${SKILL}/SKILL.md, then the reference files it maps to your role (always ${SKILL}/references/language-mechanics.md and ${SKILL}/references/claims-and-coherence.md; the others as your task needs).`}${PUBTYPE ? ` This document is a ${PUBTYPE}: read ${PUBSECTION ? `the section "${PUBSECTION}"` : 'its section'} in ${SKILL}/references/publication-types.md.${PROFILE_NOTE ? ' ' + PROFILE_NOTE : ''}` : ''}
3. ${GUIDE.length ? `The guidelines, which are the authority for every decision: ${GUIDE.map(g => `${ROOT}/${g}`).join(', ')}.` : 'This project has no guidelines file: the academic writing guide and the publication-type section above are the guidelines, and the authority for every decision.'}
${CONTEXT.length ? `4. Supporting context: ${CONTEXT.map(c => `${ROOT}/${c}`).join(', ')}.\n` : ''}5. Committee lessons learned so far, if present: ${STATE}/lessons.md and ${STATE}/lint_rules.md.${SHARD ? ` Parallel shards keep their own until they end: read ${STATE}/lessons.shard-*.md and ${STATE}/lint_rules.shard-*.md as well.` : ''}
${WRITING.length ? `6. Additional writing references (subordinate to the guidelines): ${WRITING.join(', ')}.\n` : ''}Write in ${LANGUAGE}. Never invent facts, citations, results or dates; mark anything you cannot verify.
Give any command that can take more than two minutes (a full build, online citation verification) the maximum Bash timeout of 10 minutes, or run it in the background and read its output when it ends; never let a default two-minute timeout cut it off.${ONLINE ? '' : `
Online citation verification is switched off for this project (onlineCitations is false): never pass --online to check_citations.py; verify references by web search, and report each one you could not verify as open, never as verified.`}
${SHARD_NOTE}${extra || ''}`
}

const assetDir = (u) => (ASSET_DIR ? ASSET_DIR.replaceAll('{unit}', u.id) : '')

function unitHeader(u) {
  return `UNIT ${u.id}${u.title ? ` — ${u.title}` : ''}
Files you may read freely; files this unit OWNS (only these may be edited by unit roles): ${u.files.join(', ')}
${ASSET_DIR ? `New files this unit creates (figures, figure sources, data) go under ${assetDir(u)}/ and are owned by this unit.\n` : ''}${BIB.length ? `Bibliography: ${BIB.join(', ')}${BIB.some(b => u.files.includes(b)) ? ' (owned by this unit)' : ' (shared: request additions as shared change requests)'}.\n` : ''}Configured difficulty: ${u.difficulty || 'standard'}.
Unit-specific goal: ${u.goal || '(none beyond the run goal)'}
Developmental brief: ${unitDir(u)}/brief.md`
}

const fill = (cmd, u) => cmd.replaceAll('{skill}', SKILL).replaceAll('{bib}', BIB.join(' ')).replaceAll('{files}', u.files.join(' ')).replaceAll('{main}', u.files[0]).replaceAll('{unit}', u.id)
// A unit may override the project's unit check with its own `check` (an empty string runs none).
const unitCheckCmd = (u) => (typeof u.check === 'string' ? (u.check ? fill(u.check, u) : '') : CHECKS.unit ? fill(CHECKS.unit, u) : '')
const PROSE = /\.(tex|texview|md|markdown|txt)$/i
// --skip-missing: a file that a unit has yet to create is skipped with a notice, not a failed run.
const manuscriptCmd = (files) => (files.length ? `python3 ${SKILL}/scripts/check_manuscript.py --skip-missing ${files.join(' ')}` : '')
const onlineOpts = () => ` --online --cache ${STATE}/citations-cache.json`
const citationCmd = (files, online, reflists) => (files.length || (reflists && reflists.length) ? `python3 ${SKILL}/scripts/check_citations.py --skip-missing ${files.join(' ')}${BIB.map(b => ` --bib ${b}`).join('')}${(reflists || []).map(r => ` --reference-list ${r}`).join('')}${online && ONLINE ? onlineOpts() : ''}` : '')
const referenceListCmds = (online) => REFLISTS.map(r => `python3 ${SKILL}/scripts/check_citations.py --reference-list ${r}${online && ONLINE ? onlineOpts() : ''}`)
// Every mechanical check of a unit: the project's command, then the two checkers on the unit's prose files.
// A reference list the unit owns is also parsed as one (duplicates, malformed identifiers, missing fields).
const unitChecks = (u) => [unitCheckCmd(u), manuscriptCmd(u.files.filter(f => PROSE.test(f))),
  citationCmd(u.files.filter(f => PROSE.test(f) && !REFLISTS.includes(f)), false, REFLISTS.filter(r => u.files.includes(r)))].filter(Boolean)
const CHECKER_RULES = `Report the findings of check_manuscript.py and check_citations.py as candidates (set rule to the script's name): a citation key missing from the bibliography, a reference reported NOT_FOUND, and a title METADATA_MISMATCH are blockers; UNVERIFIED and URL_ONLY references are open items for the references lens, which verifies them by search; the rest are minor unless the quality gates or lint_rules.md rate them higher. Online verification (--online) and a full build can take several minutes: give such a command the Bash timeout of 10 minutes, or run it in the background and read its log when it ends; later citation runs read the cache. A file reported as "skipped missing file" is one a unit has yet to create: it is not a failure, unless the unit under check was supposed to create it in this round. Files whose format the scripts do not accept get the same checks by reading. Your catalog is commands and searchable patterns only: recomputing numbers belongs to the technical lens and looking at rendered pages to the presentation lens.`

// Waves: at most LIM.waveSize units, and no two units in a wave share a file.
function makeWaves(units) {
  const waves = []
  for (const u of units) {
    let placed = false
    for (const w of waves) {
      if (w.length >= LIM.waveSize) continue
      const taken = new Set(w.flatMap(x => x.files))
      if (u.files.every(f => !taken.has(f))) { w.push(u); placed = true; break }
    }
    if (!placed) waves.push([u])
  }
  return waves
}

function perUnitEstimate() {
  if (REVIEW_ONLY) return 3 + READERS.length + REVIEWERS.length
  if (PLAN_ONLY) return 1 + (READ_FIRST ? READERS.length : 0)
  const first = 3 + READERS.length + REVIEWERS.length
  const later = 5
  return 1 + (READ_FIRST ? READERS.length : 0) + first + Math.max(0, LIM.laterRoundRounds - 1) * later + EDITORS.length + 1
}

function applyRoster(adjustments) {
  if (!ADAPT) return
  for (const a of adjustments || []) {
    const v = capped(String(a.role), { model: a.model, effort: a.effort })
    if (!MODELS.includes(v.model) || !EFFORTS.includes(v.effort)) continue
    const [kind, key] = String(a.role).split(':')
    const target = kind === 'reader' ? READERS.find(x => x.key === key)
      : kind === 'reviewer' ? REVIEWERS.find(x => x.key === key)
      : kind === 'editor' ? EDITORS.find(x => x.key === key)
      : kind === 'writerTier' ? R.writerTiers[Number(key)] : null
    if (target) Object.assign(target, v)
    else if (R[kind] && !Array.isArray(R[kind])) R[kind] = v
    else continue
    rosterApplied.push({ role: a.role, model: v.model, effort: v.effort, reason: a.reason })
    log(`roster: ${a.role} -> ${v.model}/${v.effort} (${a.reason})`)
  }
}

// ---------------------------------------------------------------------------
// Unit pipeline: first reading -> brief -> (write -> check -> read -> review -> chair)* -> edit -> regression
// ---------------------------------------------------------------------------
async function processUnit(u, initialActions, fromTier) {
  try {
    return await processUnitInner(u, initialActions, fromTier)
  } catch (e) {
    log(`${u.id}: failed with ${e && e.message ? e.message : e}`)
    return { id: u.id, files: u.files, status: 'failed', rounds: 0, tier: null, tier_index: fromTier || u.tier || null, open_actions: [`orchestration error: ${e && e.message ? e.message : e}`], next_actions: initialActions || [], lessons: [] }
  }
}

// Readers in parallel; each writes <dir>/reader-<key>.md. Returns the structured feedback.
async function runReaders(u, set, dir, tag, what) {
  return (await parallel(set.map(r => () => call(`${contract('Reader')}
${unitHeader(u)}
${what} You read as ${r.persona}.
Read the unit as a reader would: the rendered output if the unit check produced one, otherwise the source. Report what helped and every place you were confused, lost, bored, or found an error, with exact locations. Write your feedback to ${dir}/reader-${r.key}.md. Do not edit any other file: the report file is the one file you write, and writing it is part of your task (your structured return does not replace it).`,
    { label: `read:${u.id}:${r.key}:${tag}`, phase: 'Read', schema: S_READER, ...pick(r) }).then(x => x ? { key: r.key, ...x } : null)))).filter(Boolean)
}

const readerNote = (dir) => (dir ? `Reader feedback: ${dir}/reader-*.md. Address every confusion and gap it reports (or explain in your report why not), and keep what readers said helped.` : '')

const passes = {}  // a unit reopened in this run writes its reports to pass-<n>/, keeping the first pass's

async function processUnitInner(u, initialActions, fromTier) {
  const res = { id: u.id, files: u.files, status: 'open', rounds: 0, tier: null, tier_index: null, open_actions: [], next_actions: [], lessons: [] }

  if (REVIEW_ONLY) return reviewUnit(u)
  const pass = (passes[u.id] = (passes[u.id] || 0) + 1)
  const base = pass > 1 ? `${unitDir(u)}/pass-${pass}` : unitDir(u)
  let difficulty = u.difficulty || 'standard'
  let readerDir = null  // latest directory that holds reader feedback
  // Plan: readers on the current text, then the developmental brief (both skipped when the unit resumes with
  // explicit actions, or when a plan-only run has already written its brief)
  if (!initialActions && u.briefed && !PLAN_ONLY) {
    if (u.readersR0) readerDir = `${unitDir(u)}/r0`
  } else if (!initialActions) {
    if (READ_FIRST && READERS.length) {
      const r0 = `${unitDir(u)}/r0`
      const pre = await runReaders(u, READERS, r0, 'r0', 'Before revision: read the current text.')
      if (pre.length) readerDir = r0
    }
    const brief = await call(`${contract('Developmental Editor')}
${unitHeader(u)}
${readerNote(readerDir)}
Write the developmental brief for this unit to ${unitDir(u)}/brief.md: what to keep, cut, restructure, deepen and add (content, figures, examples, questions) so that the unit meets every applicable guideline, with each plan item tied to a guideline rule. Rate the difficulty: standard (prose and structure), hard (mathematics, derivations, new figures, research-level content) or critical (the unit sets conventions others depend on, or is unusually large and difficult). The configured difficulty is a floor: rate higher when the unit needs it, never lower. List any change that needs a file this unit does not own as a shared change request.`,
      { label: `brief:${u.id}`, phase: 'Plan', schema: S_BRIEF, ...pick(isCritical(u) ? R.briefCritical : R.brief) })
    if (!brief) { res.status = 'failed'; res.open_actions = ['developmental brief could not be produced']; return res }
    difficulty = stronger(difficulty, brief.difficulty)
    u.difficulty = difficulty
    if (PLAN_ONLY) { res.status = 'briefed'; res.difficulty = difficulty; res.readers_r0 = !!readerDir; return res }
  }
  if (PLAN_ONLY) { res.status = 'briefed'; res.difficulty = difficulty; res.readers_r0 = !!u.readersR0; return res }
  let tier = Math.min(R.writerTiers.length - 1, Math.max(startTier(difficulty), u.tier || 0, fromTier || 0))
  const critical = difficulty === 'critical'
  let actions = initialActions || []
  let readerKeys = READERS.map(r => r.key)
  let reviewerKeys = REVIEWERS.map(r => r.key)
  const ALWAYS = ['claims', 'language'].filter(k => REVIEWERS.some(r => r.key === k))  // prose can drift in any revision
  let accepted = false

  for (let round = 1; round <= LIM.maxRounds && !accepted; round++) {
    res.rounds = round
    const rdir = `${base}/r${round}`
    const W = R.writerTiers[Math.min(tier, R.writerTiers.length - 1)]
    res.tier = `${W.model}/${W.effort}`
    res.tier_index = tier

    const wr = await call(`${contract('Writer')}
${unitHeader(u)}
Round ${round}. ${actions.length ? `Resolve every action below (or dispute it with evidence):\n${json(actions)}` : 'Carry out the developmental brief in full.'}
${readerNote(readerDir)}${round > 1 ? `\nThe previous round's chair decision and reviews: ${base}/r${round - 1}/chair.md and review-*.md.` : ''}
Revise the owned files directly; edit, do not rewrite from scratch; keep all substantive content unless the brief or an action says otherwise. Before you finish, run these checks and fix what they report:
${list(unitChecks(u).map(c => `\`${c}\``))}
Write your change report to ${rdir}/writer.md.`,
      { label: `write:${u.id}:r${round}`, phase: 'Write', schema: S_WRITER, ...pick(W) })
    if (!wr) { res.status = 'failed'; res.open_actions = ['writer produced no result']; res.next_actions = actions; return res }

    const chk = await call(`${contract('Mechanical Checker')}
${unitHeader(u)}
Round ${round}. Run, from the project root:
${list(unitChecks(u).map(c => `\`${c}\``))}
Then apply every rule in ${STATE}/lint_rules.md${SHARD ? ` and ${STATE}/lint_rules.shard-*.md` : ''} (if present) and the command and pattern checks of the quality gates' Mechanical Check Catalog to the owned files. ${CHECKER_RULES} ${CHECKS.notes ? `Notes on the commands: ${fill(CHECKS.notes, u)}` : ''}
Report each finding with an id and its exact location. Write your report to ${rdir}/checks.md. Do not edit any other file: the report file is the one file you write, and writing it is part of your task (your structured return does not replace it).`,
      { label: `check:${u.id}:r${round}`, phase: 'Review', schema: S_CHECK, ...pick(R.checker) })

    const readerSet = READERS.filter(r => readerKeys.includes(r.key))
    const readers = readerSet.length ? await runReaders(u, readerSet, rdir, `r${round}`, `Round ${round}: read the revised text (the checks are in ${rdir}/checks.md).`) : []
    if (readers.length) readerDir = rdir

    const reviewerSet = REVIEWERS.filter(r => reviewerKeys.includes(r.key))
    const reviews = (await parallel(reviewerSet.map(v => () => call(`${contract('Reviewer')}
${unitHeader(u)}
Round ${round}. Your lens: ${v.focus}.
The writer's report is ${rdir}/writer.md; the mechanical checks are in ${rdir}/checks.md.${readerDir ? ` Reader feedback (from ${readerDir === rdir ? 'this round' : 'the latest round that had readers'}) is in ${readerDir}/reader-*.md: weigh it, and confirm or reject each point in your lens with a reason.` : ''} ${actions.length ? `Verify that these actions were resolved: ${json(actions)}.` : ''}
Review the current state of the owned files (use git diff to see this round's changes) through your lens only. Return a verdict and findings with severity, exact location, the guideline rule and a concrete fix. Write your review to ${rdir}/review-${v.key}.md. Do not edit any other file: the report file is the one file you write, and writing it is part of your task (your structured return does not replace it).`,
      { label: `review:${u.id}:${v.key}:r${round}`, phase: 'Review', schema: S_REVIEW, ...pick(critical && v.critical ? v.critical : v) }).then(x => x ? { key: v.key, ...x } : null)))).filter(Boolean)

    const chair = await call(`${contract('Committee Chair')}
${unitHeader(u)}
Round ${round} of at most ${LIM.maxRounds}. Writer tier this round: ${res.tier}.
Writer result: ${json(wr)}
Mechanical checks: ${json(chk)}
Reader feedback: ${json(readers)}${readerDir && readerDir !== rdir ? ` (no readers this round; the latest feedback is in ${readerDir}/reader-*.md)` : ''}
Reviews: ${json(reviews)}
Previous actions: ${json(actions)}
Consolidate: merge duplicates, settle conflicts between reviewers and readers using the guidelines, verify each blocker or major finding yourself against the files before keeping it, dismiss false positives with a reason, and judge any writer dispute. The mechanical checks can contain false positives: list each checker finding you dismiss in dismissed_checks with its id and the reason; a build error, an undefined reference or lost content that you can confirm is never dismissed. Decide "accept" only if no blocker or major action remains open and every undismissed check finding is minor or less; minor and nit actions go to the editors. If you accept, copy the owned files to ${base}/accepted/ (same relative paths) as the regression snapshot. Say which reviewers and readers must look again next round (only those whose concerns remain), whether issues are repeating, and whether the writer should be escalated to a stronger tier. Record transferable lessons (patterns other units should avoid). Write your decision to ${rdir}/chair.md.`,
      { label: `chair:${u.id}:r${round}`, phase: 'Review', schema: S_CHAIR, ...pick(critical ? R.chairCritical : R.chair) })
    if (!chair) { res.status = 'failed'; res.open_actions = ['chair produced no decision']; res.next_actions = actions; return res }

    res.lessons.push(...(chair.lessons || []))
    const heavy = (chair.actions || []).filter(isHeavy)
    const dismissedChecks = new Set((chair.dismissed_checks || []).map(d => d.id))
    const openChecks = chk ? (chk.findings || []).filter(f => isHeavy(f) && !dismissedChecks.has(f.id)) : []
    const checksOk = chk ? openChecks.length === 0 : false
    if (chair.decision === 'accept' && heavy.length === 0 && checksOk) {
      accepted = true
      actions = (chair.actions || []).filter(a => a.severity === 'minor' || a.severity === 'nit')
    } else {
      const checkActions = chk
        ? openChecks.map((f, i) => ({ id: `check-r${round}-${i + 1}`, severity: f.severity, source: 'checker', location: f.location, instruction: `${f.problem} Fix: ${f.fix}` }))
        : [{ id: `check-r${round}`, severity: 'major', source: 'checker', instruction: 'The mechanical checker returned no result: run the checks listed above yourself and fix what they report.' }]
      const chairActions = chair.actions || []
      // An accepting chair's list holds only minor items, so failed checks must be added to it explicitly.
      actions = chair.decision === 'accept' || chairActions.length === 0 ? chairActions.concat(checksOk ? [] : checkActions) : chairActions
      if (actions.length === 0) actions = [{ id: `chair-r${round}`, severity: 'major', source: 'chair', instruction: `Resolve the blocker and major findings in ${rdir}/chair.md.` }]
      readerKeys = (chair.rerun_readers || []).filter(k => READERS.some(r => r.key === k))
      reviewerKeys = [...new Set([...(chair.rerun_reviewers || []).filter(k => REVIEWERS.some(r => r.key === k)), ...ALWAYS])]
      if (reviewerKeys.length === 0 && REVIEWERS.length) reviewerKeys = [REVIEWERS[0].key]
      if (round < LIM.maxRounds && (chair.escalate || (chair.repeated_issues && round >= 2))) {
        if (tier < R.writerTiers.length - 1) { tier++; log(`${u.id}: writer escalated to ${R.writerTiers[tier].model}/${R.writerTiers[tier].effort}`) }
      }
    }
  }

  if (!accepted) { res.status = 'unresolved'; res.open_actions = actions.map(a => `${a.severity}: ${a.instruction}`); res.next_actions = actions; return res }

  // Editor committee (sequential: they edit the same files)
  for (const e of EDITORS) {
    await call(`${contract('Editor')}
${unitHeader(u)}
Your focus: ${e.focus}.
The unit has been accepted by the review committee. Edit the owned files directly to finish it. Also resolve these minor items from the committee: ${json(actions)}.
Do not change meaning, claim strength, mathematics, numbers, labels or cross-reference targets, and never add a new claim, reason, example or fact (you may only reword, reorder, cut repetition and fix form); if you believe a substantive change is needed, including a claim that is overstated or undersold, report it as a concern instead. Write your edit report to ${base}/editor-${e.key}.md.`,
      { label: `edit:${u.id}:${e.key}`, phase: 'Edit', schema: S_EDITOR, ...pick(e) })
  }

  // Regression check, with bounded repairs by the writer
  for (let repair = 0; repair <= LIM.maxRepairs; repair++) {
    const reg = await call(`${contract('Regression Checker')}
${unitHeader(u)}
The editors have just edited this accepted unit (reports: ${base}/editor-*.md). Run:
${list(unitChecks(u).map(c => `\`${c}\``))}
Compare the files with the chair's accepted snapshot in ${base}/accepted/ (fall back to git diff if it is missing) and report any changed meaning, broken mathematics or numbers, lost content, broken references or new mechanical failures. Any claim, reason or fact that is new or changed since the snapshot is at least a major finding unless it says exactly what the accepted text said. Write your report to ${base}/regression-${repair}.md. Do not edit any other file: the report file is the one file you write, and writing it is part of your task (your structured return does not replace it).`,
      { label: `regress:${u.id}:${repair}`, phase: 'Edit', schema: S_CHECK, ...pick(R.regression) })
    // Only blocker and major findings fail the check; a failed check with no such finding is
    // made explicit, so a unit never ends unresolved with an empty action list.
    const bad = !reg ? [{ severity: 'major', problem: 'no regression result' }]
      : (reg.findings || []).filter(isHeavy).concat(!reg.passed && !(reg.findings || []).length
        ? [{ severity: 'major', problem: `the regression check failed without listing findings: ${reg.summary || 'no summary'}`, fix: `rerun the checks and compare with ${base}/accepted/` }] : [])
    if (bad.length === 0) { res.status = 'accepted'; break }
    if (repair === LIM.maxRepairs) {
      res.status = 'unresolved'
      res.open_actions = bad.map(f => `${f.severity}: ${f.problem}`)
      res.next_actions = bad.map((f, i) => ({ id: `regression-${i + 1}`, severity: f.severity, source: 'regression', location: f.location, instruction: `${f.problem}${f.fix ? ' Fix: ' + f.fix : ''}` }))
      break
    }
    await call(`${contract('Writer')}
${unitHeader(u)}
Repair the regressions found after editing: ${json(bad)}. Keep the editors' improvements where they are correct. Write a short report to ${base}/repair-${repair}.md.`,
      { label: `repair:${u.id}:${repair}`, phase: 'Edit', schema: S_WRITER, ...pick(R.writerTiers[Math.min(tier, R.writerTiers.length - 1)]) })
  }
  return res
}

// Review-only mode: one independent assessment of the current text, with no edits.
async function reviewUnit(u) {
  const res = { id: u.id, files: u.files, status: 'reviewed', rounds: 1, tier: null, tier_index: null, open_actions: [], next_actions: [], lessons: [] }
  const rdir = `${unitDir(u)}/review`
  const chk = await call(`${contract('Mechanical Checker')}
${unitHeader(u)}
Review-only run. Run, from the project root:
${list(unitChecks(u).map(c => `\`${c}\``))}
${CHECKER_RULES} Report findings with exact locations. Write your report to ${rdir}/checks.md. Do not edit any other file: the report file is the one file you write, and writing it is part of your task (your structured return does not replace it).`,
    { label: `check:${u.id}:review`, phase: 'Review', schema: S_CHECK, ...pick(R.checker) })
  const readers = await runReaders(u, READERS, rdir, 'review', 'Review-only run.')
  const reviews = (await parallel(REVIEWERS.map(v => () => call(`${contract('Reviewer')}
${unitHeader(u)}
Review-only run. Your lens: ${v.focus}. Reader feedback is in ${rdir}/reader-*.md and the checks in ${rdir}/checks.md. Review the current files through your lens only and write your review to ${rdir}/review-${v.key}.md. Do not edit any other file: the report file is the one file you write, and writing it is part of your task (your structured return does not replace it).`,
    { label: `review:${u.id}:${v.key}:review`, phase: 'Review', schema: S_REVIEW, ...pick(isCritical(u) && v.critical ? v.critical : v) }).then(x => x ? { key: v.key, ...x } : null)))).filter(Boolean)
  const chair = await call(`${contract('Committee Chair')}
${unitHeader(u)}
Review-only run: consolidate, do not decide acceptance of edits. Checks: ${json(chk)}. Reader feedback: ${json(readers)}. Reviews: ${json(reviews)}.
Verify every blocker and major finding yourself, dismiss false positives with a reason, merge duplicates, and write a prioritized revision report to ${rdir}/report.md: an overall assessment (as a program committee or editor would give it, with the main strengths and the decisive weaknesses), then every action ordered by severity with its location and a concrete fix. Set decision to "accept" only if nothing blocker or major remains.`,
    { label: `chair:${u.id}:review`, phase: 'Review', schema: S_CHAIR, ...pick(isCritical(u) ? R.chairCritical : R.chair) })
  if (chair) {
    res.open_actions = (chair.actions || []).map(a => `${a.severity}: ${a.instruction}`)
    res.status = chair.decision === 'accept' ? 'reviewed-ready' : 'reviewed-needs-work'
    res.report = `${rdir}/report.md`
  } else { res.status = 'failed'; res.open_actions = ['chair produced no report'] }
  return res
}

// ---------------------------------------------------------------------------
// Retrospective and commits
// ---------------------------------------------------------------------------
async function retrospective(label, results) {
  const r = await call(`${contract('Retrospective Analyst')}
This is the retrospective after ${label}. Unit outcomes: ${json(results.map(x => ({ id: x.id, status: x.status, rounds: x.rounds, tier: x.tier, open: x.open_actions, lessons: x.lessons })))}.
Read the chair, reviewer and reader reports under ${STATE}/units/ for these units. Update ${LESSONS} (recurring problems turned into short, concrete preventive instructions for writers, reviewers and editors; merge with existing lessons, keep it under 150 lines), ${LINT} (mechanical patterns a checker can grep for, with the guideline rule each enforces) and ${PROPOSALS} (amendments or clarifications for the human owner; never edit the guidelines yourself).${SHARD ? ` These three are this shard's own files (create them if they are missing, each with a one-line heading): first read ${STATE}/lessons.md, ${STATE}/lint_rules.md, ${STATE}/guideline_proposals.md and the other shards' files (${STATE}/*.shard-*.md), add only what they lack, and never edit any of those, because each shard's files are merged into the committee's when the shard ends.` : ''} Propose roster adjustments only where the evidence is clear (e.g. a reviewer lens that keeps missing issues needs a stronger model; a role that never finds anything can use a cheaper one); they persist into later runs. Roles: scout, brief, briefCritical, chair, chairCritical, checker, regression, integration, globalChair, retrospective, committer, writerTier:<0-${R.writerTiers.length - 1}>, reader:<key>, reviewer:<key>, editor:<key>.`,
    { label: `retro:${label}`, phase: 'Learn', schema: S_RETRO, ...pick(R.retrospective) })
  if (r) applyRoster(r.roster_adjustments)
  return r
}

async function commit(label, results, sharedFiles) {
  if (!COMMIT.perWave) return null
  const units = results.map(x => ({ id: x.id, status: x.status, files: ASSET_DIR ? x.files.concat([`${assetDir(x)}/`]) : x.files }))
  const shared = (sharedFiles || []).filter(Boolean)
  const push = COMMIT.branch ? `git push -u origin HEAD:${COMMIT.branch}` : 'git push -u origin HEAD'
  if (SHARD) {
    // Other shards stage and commit in the same repository: name every path, so that a commit never
    // takes a file another committer has staged, and wait when the index is locked.
    return call(`${contract('Committer')}
Commit the work of ${label}. Run \`git status --short\`. The paths of this commit are the owned files of these units (a path ending in / means every file under that directory, including new ones): ${json(units)}. Everything else in git status belongs to the parallel shards: never stage or commit it. Stage with \`git add -- <paths>\` (leave out paths that do not exist), then commit with \`git commit -m <message> -- <the same paths>\`, which commits exactly those paths even when another committer has staged files of its own. The first line of the message is "${NAME}: ${label}" and its body lists each unit with its status. If git reports that index.lock exists, another committer is at work: wait five seconds and try again, up to ten times, and never delete the lock file. Never amend, never rebase, never force-push. ${COMMIT.push ? `Then push with \`${push}\`; a parallel shard may push at the same moment, so on any failure wait a few seconds and push again, up to 6 times.` : 'Do not push.'}`,
      { label: `commit:${label}`, phase: 'Learn', schema: S_COMMIT, ...pick(R.committer) })
  }
  return call(`${contract('Committer')}
Commit the work of ${label}. Run \`git status --short\`; stage the owned files of these units (a path ending in / means every file under that directory, including new ones) and any committee state files that are not git-ignored: ${json(units)}.${shared.length ? ` Also stage these files that the Integration Editor changed: ${shared.join(', ')}.` : ''} Never stage unrelated files, never amend, never rebase, never force-push. Commit with a message whose first line is "${NAME}: ${label}" and whose body lists each unit with its status. ${COMMIT.push ? `Then push with \`${push}\` (retry up to 4 times with backoff on network errors).` : 'Do not push.'}`,
    { label: `commit:${label}`, phase: 'Learn', schema: S_COMMIT, ...pick(R.committer) })
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
const stages = GLOBAL_ONLY ? [] : Array.isArray(A.stages) ? A.stages : [{ id: 'main', units: A.units || [], scope: A.scope }]
if (!GLOBAL_ONLY && !stages.some(st => (st.units && st.units.length) || st.scope)) {
  log('nothing to do: no stage has units or a scope')
  return { status: 'complete', accepted: [], unresolved: [], deferred: [], rounds: {}, global: null, agents_launched: 0 }
}

phase('Plan')
const knownUnits = () => PRIOR.map(p => ({ id: p.id, files: p.files })).concat(stages.flatMap(s => (s.units || []).map(u => ({ id: u.id, files: u.files }))))
for (const st of stages) {
  if ((st.units && st.units.length) || !st.scope) { st.units = st.units || []; continue }
  const known = knownUnits()
  const sc = await call(`${contract('Scout')}
Stage "${st.id}": ${st.goal || GOAL}
Scope: ${st.scope}
Divide the scope into units of work that can be revised independently: each unit owns a disjoint set of files (a chapter or section file plus files that only it uses). Give each a stable id (letters, digits and dashes), its files (paths relative to the project root), a difficulty (standard, hard, critical) and a one-line goal. Order units so prerequisites come first. Do not edit any file.${known.length ? `
These units already exist (accepted in earlier runs or planned in this run): never propose them again, never reuse their ids, and never give a new unit their files: ${json(known)}` : ''}`,
    { label: `scout:${st.id}`, phase: 'Plan', schema: S_SCOUT, ...pick(R.scout) })
  const taken = new Set(known.map(k => k.id))
  st.units = (sc ? sc.units : []).filter(u => {
    if (taken.has(u.id)) { log(`stage ${st.id}: scouted unit ${u.id} already exists; dropped`); return false }
    taken.add(u.id)
    u.scouted = true  // recorded in the ledger, so that the next run resumes it instead of scouting again
    return true
  })
  log(`stage ${st.id}: ${st.units.length} units scouted`)
}

const perUnit = perUnitEstimate()
const capacity = Math.max(1, Math.floor((LIM.maxAgents - 12) / perUnit))
const all = stages.flatMap(s => s.units.map(u => ({ ...u, stage: s.id })))
const runnable = all.slice(0, capacity)
const deferred = all.slice(capacity).map(u => u.id)
if (deferred.length) log(`agent budget: ~${perUnit} agents per unit, so ${runnable.length} units run now and ${deferred.length} are deferred to the next run: ${deferred.join(', ')}`)

const results = []
const waveRetros = []
for (const st of stages) {
  const units = runnable.filter(u => u.stage === st.id)
  if (!units.length) continue
  const waves = makeWaves(units)
  for (let i = 0; i < waves.length; i++) {
    if (budget.total && budget.remaining() < 60000) { log('token budget nearly spent; stopping before the next wave'); deferred.push(...waves.slice(i).flat().map(u => u.id)); break }
    const label = `${st.id} wave ${i + 1}/${waves.length}`
    log(`${label}: ${waves[i].map(u => u.id).join(', ')}`)
    // A unit carried over from an earlier run resumes from its open actions (prepare_run.py passes them as `actions`).
    const wave = (await parallel(waves[i].map(u => () => processUnit(u, u.actions && u.actions.length ? u.actions : null, u.tier)))).filter(Boolean)
    results.push(...wave)
    if (REVIEW_ONLY || PLAN_ONLY) continue
    const retro = await retrospective(label, wave)
    if (retro) waveRetros.push(retro)
    await commit(label, wave)
  }
}

if (PLAN_ONLY) {
  // Briefs are written; nothing in the document changed. prepare_run.py --record marks the units as briefed,
  // and the run that revises them starts at the writer.
  log(`plan-only run finished: ${results.map(r => `${r.id}=${r.status}`).join(', ')}`)
  return { status: 'planned',
    briefed: results.filter(r => r.status === 'briefed').map(r => ({ id: r.id, difficulty: r.difficulty, readers_r0: r.readers_r0, files: r.files })),
    failed: results.filter(r => r.status !== 'briefed').map(r => ({ id: r.id, open: r.open_actions })),
    deferred, shard: SHARD, agents_launched: agentsLaunched }
}

if (REVIEW_ONLY) {
  log(`review-only run finished: ${results.map(r => `${r.id}=${r.status}`).join(', ')}`)
  return { status: 'reviewed', reports: results.map(r => ({ id: r.id, status: r.status, report: r.report, open: r.open_actions })), deferred, agents_launched: agentsLaunched }
}

if (SKIP_GLOBAL) {
  // The global rounds edit shared files, so they run alone, in the run that follows the shards.
  const missing = runnable.filter(u => !results.some(r => r.id === u.id)).map(u => ({ id: u.id, status: 'not_run', open: ['unit was not processed (stopped early or lost)'], actions: [], tier_index: u.tier === undefined ? null : u.tier }))
  const done = results.filter(r => r.status === 'accepted').length
  log(`${SHARD ? `shard ${SHARD.index}/${SHARD.of}` : 'run without global rounds'} finished: accepted ${done}/${runnable.length}; deferred ${deferred.length}; agents launched ~${agentsLaunched}; ${SHARD ? 'the global rounds run after every shard has ended' : 'the global rounds run in a later run'}`)
  return {
    status: deferred.length ? 'continue' : 'incomplete',
    shard: SHARD,
    accepted: results.filter(r => r.status === 'accepted').map(r => r.id),
    unresolved: results.filter(r => r.status !== 'accepted').map(r => ({ id: r.id, status: r.status, open: r.open_actions, actions: r.next_actions || [], tier_index: r.tier_index })).concat(missing),
    deferred,
    rounds: Object.fromEntries(results.map(r => [r.id, { rounds: r.rounds, tier: r.tier, tier_index: r.tier_index, files: r.files }])),
    scouted: all.filter(u => u.scouted).map(u => ({ id: u.id, stage: u.stage, files: u.files, goal: u.goal || '', difficulty: u.difficulty || 'standard' })),
    global: null,
    global_checks_passed: false,
    global_pending: true,
    remaining_issues: ['the global rounds have not run on these units yet'],
    roster_adjustments: rosterApplied,
    lessons: waveRetros.flatMap(r => r.lessons_added || []),
    guideline_proposals: waveRetros.flatMap(r => r.guideline_proposals || []),
    agents_launched: agentsLaunched,
  }
}

// Integration: global checks, integration editor, cross-unit claims review, editor-in-chief; may reopen units
const docUnits = () => PRIOR.filter(p => !results.some(r => r.id === p.id)).map(p => ({ id: p.id, status: 'accepted (earlier run)', files: p.files }))
  .concat(results.map(x => ({ id: x.id, status: x.status, files: x.files, open: x.open_actions })))
// The configured reading order first, then prose files of earlier and scouted units it lacks.
const proseFiles = [...new Set(GLOBAL_FILES.concat(PRIOR.concat(runnable).flatMap(u => u.files)).filter(f => PROSE.test(f)))]
const globalCmds = (CHECKS.global || []).map(c => fill(c, { id: 'global', files: proseFiles.length ? proseFiles : [''] }))
  .concat([manuscriptCmd(proseFiles), citationCmd(proseFiles.filter(f => !REFLISTS.includes(f)), true)].filter(Boolean), referenceListCmds(true))
const globalCheckPrompt = (g, gdir, again) => `${contract('Mechanical Checker')}
Global round ${g}${again ? ', after the Integration Editor' : ''}. Run every global check, from the project root, on the whole document (the prose files are listed in reading order, so repetition across units is visible):
${list(globalCmds.map(c => `\`${c}\``))}
${CHECKER_RULES} Report all failures with locations, and which unit owns each location. Write the report to ${gdir}/checks${again ? '-after' : ''}.md. Do not edit any other file: the report file is the one file you write, and writing it is part of your task (your structured return does not replace it).`
const globalOk = (c) => !!c && !(c.findings || []).some(isHeavy)

let globalDecision = null
let lastGlobalCheck = null
const remainingIssues = []
let pendingReopen = []
// Complete only when every unit of this run is accepted, including earlier units the editor-in-chief reopened.
const complete = () => deferred.length === 0 && runnable.every(u => results.some(r => r.id === u.id && r.status === 'accepted'))
  && results.every(r => r.status === 'accepted')
for (let g = 1; g <= LIM.maxGlobalRounds; g++) {
  phase('Integrate')
  const gdir = `${STATE}/global/round-${g}`
  const gchk = await call(globalCheckPrompt(g, gdir, false), { label: `global-check:${g}`, phase: 'Integrate', schema: S_CHECK, ...pick(R.checker) })
  lastGlobalCheck = gchk
  const integ = await call(`${contract('Integration Editor')}
Global round ${g}. Units of the document: ${json(docUnits())}.
Global checks: ${json(gchk)}. Shared change requests are in the writer reports and briefs under ${STATE}/units/.
Make the document consistent as a whole: apply justified shared change requests to shared files (files no unit owns), reconcile terminology, notation and cross-references between units, remove duplicated explanations by keeping the best one and pointing to it, and fix global check failures in shared files. For problems inside a unit's files, report them instead of editing. List every file you changed in files_changed. Write your report to ${gdir}/integration.md.`,
    { label: `integrate:${g}`, phase: 'Integrate', schema: S_INTEG, ...pick(R.integration) })
  const integFiles = integ ? integ.files_changed || [] : []
  if (integFiles.length) {
    // The integrated document is what must pass, so the checks always run again after the Integration Editor.
    lastGlobalCheck = await call(globalCheckPrompt(g, gdir, true), { label: `global-check:${g}b`, phase: 'Integrate', schema: S_CHECK, ...pick(R.checker) })
    await commit(`integration round ${g}`, [], integFiles)
  }
  const units = docUnits()
  if (units.length > 1) {
    const lens = REVIEWERS.find(r => r.key === 'claims') || capped('reviewer:claims', { model: 'opus', effort: EFFORT || 'high' })
    await call(`${contract('Reviewer')}
Global round ${g}: the cross-unit claims review. Your lens: the claims lens of roles.md, applied to the whole document. Units, in reading order: ${json(units.map(x => ({ id: x.id, files: x.files })))}.
Build the cross-unit contribution map and the claim-evidence matrix of ${SKILL}/references/claims-and-coherence.md over the abstract, the introduction, each unit's opening and summary or conclusion, the discussion and the final conclusion. Every contribution, key number, term and scope statement must agree wherever it recurs, each claim must trace to evidence in some unit, the conclusion must add nothing new, and nothing may be overclaimed or undersold. Report each mismatch with both locations and the unit that should change. Write your review to ${gdir}/claims.md. Do not edit any other file: the report file is the one file you write, and writing it is part of your task (your structured return does not replace it).`,
      { label: `review:global:claims:g${g}`, phase: 'Integrate', schema: S_REVIEW, ...pick(lens) })
  }
  globalDecision = await call(`${contract('Editor-in-Chief')}
Global round ${g} of at most ${LIM.maxGlobalRounds}. Units of the document: ${json(units.map(x => ({ id: x.id, status: x.status, open: x.open })))}. Deferred to a later run: ${json(deferred)}.
Read ${gdir}/checks.md${integFiles.length ? `, ${gdir}/checks-after.md (the checks after the Integration Editor's changes, which decide whether the global checks pass)` : ''}, ${gdir}/integration.md${units.length > 1 ? ` and the cross-unit claims review ${gdir}/claims.md` : ''}, sample the accepted units, and judge the work against the run goal and the guidelines as a whole: coherence, cumulative order, contributions and numbers that agree across units, consistent quality and voice, and the global checks. Approve only if the processed scope is ready and the global checks pass. Otherwise reopen the specific units that need more work (any unit listed above, including units accepted in earlier runs), each with concrete actions. Write your verdict to ${gdir}/verdict.md.`,
    { label: `chief:${g}`, phase: 'Integrate', schema: S_GLOBAL, ...pick(R.globalChair) })
  if (!globalDecision) { remainingIssues.push('the editor-in-chief returned no verdict; the global round must run again'); break }
  remainingIssues.push(...(globalDecision.remaining_issues || []))
  if (globalDecision.decision === 'approve' || !(globalDecision.reopen || []).length) break
  const byId = new Map(PRIOR.map(u => [u.id, { ...u, stage: 'prior' }]).concat(runnable.map(u => [u.id, u])))
  const reopened = globalDecision.reopen.filter(x => byId.has(x.unit))
  const unknown = globalDecision.reopen.filter(x => !byId.has(x.unit))
  if (unknown.length) {
    log(`editor-in-chief named unknown unit(s): ${unknown.map(x => x.unit).join(', ')}`)
    remainingIssues.push(...unknown.map(x => `editor-in-chief asked to reopen "${x.unit}", which is not a unit of this document: ${x.actions.join('; ')}`))
  }
  if (!reopened.length) break
  const chiefActions = (x) => x.actions.map((t, i) => ({ id: `chief-${g}-${i + 1}`, severity: 'major', source: 'editor-in-chief', instruction: t }))
  if (g === LIM.maxGlobalRounds) { pendingReopen = reopened.map(x => ({ unit: x.unit, actions: chiefActions(x) })); break }
  log(`editor-in-chief reopened ${reopened.length} unit(s): ${reopened.map(x => x.unit).join(', ')}`)
  for (const wave of makeWaves(reopened.map(x => byId.get(x.unit)))) {
    const redo = (await parallel(wave.map(u => {
      const prev = results.find(r => r.id === u.id)
      const fromTier = prev && prev.tier_index !== null && prev.tier_index !== undefined ? prev.tier_index : u.tier
      return () => processUnit(u, chiefActions(reopened.find(x => x.unit === u.id)), fromTier)
    }))).filter(Boolean)
    for (const r of redo) { const k = results.findIndex(x => x.id === r.id); if (k >= 0) results[k] = r; else results.push(r) }
    await retrospective(`reopen round ${g}`, redo)
    await commit(`reopen round ${g}`, redo)
  }
}

// Units the editor-in-chief reopened in the last global round carry its actions into the next run.
for (const x of pendingReopen) {
  const k = results.findIndex(r => r.id === x.unit)
  const p = PRIOR.find(q => q.id === x.unit)
  const base = k >= 0 ? results[k] : { id: x.unit, files: p ? p.files : [], rounds: 0, tier: null, tier_index: p && p.tier !== undefined ? p.tier : null, lessons: [] }
  const r = { ...base, status: 'reopened', open_actions: x.actions.map(a => `major: ${a.instruction}`), next_actions: x.actions }
  if (k >= 0) results[k] = r; else results.push(r)
  log(`${x.unit}: reopened by the editor-in-chief in the last global round; its actions carry over to the next run`)
}

const final = await retrospective('run end', results)
await commit('run end', results)
const globalChecksPassed = globalOk(lastGlobalCheck)
const approved = !!globalDecision && globalDecision.decision === 'approve' && pendingReopen.length === 0
const status = complete() && approved && globalChecksPassed ? 'complete' : deferred.length ? 'continue' : 'incomplete'
const missing = runnable.filter(u => !results.some(r => r.id === u.id)).map(u => ({ id: u.id, status: 'not_run', open: ['unit was not processed (stopped early or lost)'], actions: [], tier_index: u.tier === undefined ? null : u.tier }))
const processedIds = new Set(runnable.map(u => u.id).concat(results.map(r => r.id)))
log(`status: ${status}; accepted ${results.filter(r => r.status === 'accepted').length}/${processedIds.size}; deferred ${deferred.length}; global checks ${globalChecksPassed ? 'passed' : 'not passed'}; agents launched ~${agentsLaunched}`)
return {
  status,
  accepted: results.filter(r => r.status === 'accepted').map(r => r.id),
  unresolved: results.filter(r => r.status !== 'accepted').map(r => ({ id: r.id, status: r.status, open: r.open_actions, actions: r.next_actions || [], tier_index: r.tier_index })).concat(missing),
  deferred,
  rounds: Object.fromEntries(results.map(r => [r.id, { rounds: r.rounds, tier: r.tier, tier_index: r.tier_index, files: r.files }])),
  // Units the Scout created (run, deferred or not run): recorded so that later runs resume them instead of scouting again.
  scouted: all.filter(u => u.scouted).map(u => ({ id: u.id, stage: u.stage, files: u.files, goal: u.goal || '', difficulty: u.difficulty || 'standard' })),
  global: globalDecision,
  global_checks_passed: globalChecksPassed,
  global_pending: !approved || !globalChecksPassed,
  remaining_issues: remainingIssues,
  roster_adjustments: rosterApplied,
  lessons: final ? final.lessons_added : [],
  guideline_proposals: final ? final.guideline_proposals : [],
  agents_launched: agentsLaunched,
}
