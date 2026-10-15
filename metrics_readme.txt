================================================================================
MACHINE TRANSLATION EVALUATION METHODOLOGY: POLISH -> GYGY
================================================================================

1. RESEARCH PROBLEM AND GYGY LANGUAGE CHARACTERISTICS
--------------------------------------------------------------------------------
The gygy language is a constructed language (conlang) featuring a strongly 
agglutinative and oligosynthetic typology[cite: 105], built upon a closed inventory 
of monosyllabic morphemes (where each syllable encodes 8 bits of semantic and 
phonetic information)[cite: 101, 103, 104]. The grammar of gygy is governed by:
- A rigid AOSPV word order (Adverbial - Object - Subject - Predicative - Verb)[cite: 106],
- The "head-final" compounding principle: modifiers strictly precede the core root[cite: 106],
- No traditional lexical categories (nouns, verbs, adjectives); the lexicon is 
  split strictly into conceptual roots (nomina) and structural markers (functiones)[cite: 105],
- Agglutination of lexical roots, tense markers (e.g., -dua, -da)[cite: 111], mood affixes 
  (-li, -fi)[cite: 135, 145], and syntactic boundary clitics (-k, -s, -r, -n, -p) into single 
  orthographic tokens[cite: 105, 106, 112].

Due to these linguistic constraints, evaluating machine translation quality 
(Polish -> gygy) necessitates a balanced suite of complementary automated metrics.


2. VALIDATION DATASET (GOLDEN DATASET)
--------------------------------------------------------------------------------
Model evaluation is conducted on an isolated test set (test_golden.jsonl) that is 
strictly disjoint from the training data to guarantee Data Leakage Prevention. 
The golden dataset comprises 196 reference pairs stratified into 6 distinct categories:
1) podrecznik_gramatyka - Canonical grammar examples from the textbook (covering 
   AOSPV word order[cite: 106], subordinate relative clauses with "ki ... rp"[cite: 137], relative 
   pronoun "hi"[cite: 137], participial clauses "-f", "-rup", "-pyp"[cite: 142, 153], passive voice[cite: 155], 
   reflexivity[cite: 146], and causative constructions[cite: 157]),
2) modlitwa_panska - Translation of the Lord's Prayer[cite: 138],
3) psalm_137 - Poetic translation of Psalm 137,
4) prolog_jana - Philosophical and theological translation of the Prologue to the 
   Gospel of John (John 1:1-14)[cite: 185, 186],
5) te_deum - Translation of the Latin hymn "Te Deum laudamus"[cite: 186, 187],
6) izajasz_11 - Prophetic translation of Isaiah 11:1-5.


3. EVALUATION METRICS
--------------------------------------------------------------------------------
Translation performance is benchmarked using three quantitative metrics computed 
via the industry-standard SacreBLEU scientific library:

A) chrF2 (Character n-gram F-score) — PRIMARY METRIC (Scale: 0 - 100)
   The chrF2 metric computes the coverage of character n-grams (substrings 
   spanning 1 to 6 characters) between the model-generated hypothesis and the gold 
   reference, balancing Precision and Recall via a harmonic mean (beta = 2, giving 
   higher weight to recall).

   Why is chrF2 the primary metric for gygy?
   In polysynthetic and agglutinative languages, a single orthographic word 
   corresponds to an entire phrase or clause in Polish (e.g., "kuokuokuak" = 
   great-grandfather [subject][cite: 110, 111], "luoduoduar" = finished dying [past tense predicate][cite: 111]). 
   If a model correctly predicts the lexical root and syntactic boundaries but makes 
   a single morpheme substitution, word-level metrics assign a zero score. The chrF2 
   metric operates at the sub-word / sub-morphemic level, rewarding the model 
   proportionally for correct structural clitics and core roots.

B) BLEU (Bilingual Evaluation Understudy) — AUXILIARY METRIC (Scale: 0 - 100)
   The classical benchmark in machine translation, measuring word-level n-gram 
   precision (1-gram to 4-gram over whitespace-delimited tokens) penalized by a 
   Brevity Penalty. In this project, BLEU verifies the model's competence in 
   assembling multi-token syntactic clauses (e.g., bracketed "ki ... rp" subordinates[cite: 137] 
   and coordinating conjunctions "ci", "pi", "xi"[cite: 140]).

C) Exact Match (EM) — STRICT SYNTACTIC MATCH (Scale: 0% - 100%)
   The proportion of sentences that are 100% character-for-character identical to 
   the reference translation (after lowercasing and stripping trailing punctuation). 
   It provides an empirical measure of absolute grammar and lexical fidelity.


4. EXPERIMENTAL SETUP (BASELINE VS. FINE-TUNING)
--------------------------------------------------------------------------------
The project evaluates two architectural paradigms:
1. Baseline (In-Context Learning / Few-Shot + Lexicon):
   A frozen foundational LLM receives the full morpheme catalog (morphemes.json)[cite: 107], 
   AOSPV grammatical axioms[cite: 106], and few-shot exemplars within its system prompt, 
   without updating network weights.
2. Fine-Tuned Model (QLoRA + System Prompt):
   The model is fine-tuned (Supervised Fine-Tuning) using low-rank adapters (LoRA) 
   on a synthetic corpus constructed deterministically according to gygy formal grammar.

Comparing the resulting chrF2, BLEU, and Exact Match metrics across both stages 
quantitatively demonstrates the performance gain unlocked by parameter-efficient 
fine-tuning on formal synthetic conlang structures.
================================================================================