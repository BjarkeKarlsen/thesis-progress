---
name: reviewing-like-the-author
description: Reads a thesis section the way the author does and writes margin comments in their voice, red notes beside each paragraph that ask why a modelling choice was made, where an idea comes from, whether the reader can follow the order and the terms, and what repeats. Use when the author says "comment it like I do", "give me red comments", "review this section like me" or "do the same as my comments" on a chapter, a section or the compiled PDF.
---

# Reviewing like the author

The goal is a set of comments the author could have written, so they can read them, agree or disagree, and then
decide what to rewrite. **This skill only comments. It never edits the
thesis.** Rewriting follows the workflow in the workspace `CLAUDE.md` (discuss,
then a review PDF, then apply).

## How the author reads

The author reads as a first-time reader, front to back, one paragraph at a
time, and asks at every paragraph "does the reader know this yet, and do they
know why?". They comment on almost every paragraph, also the good ones.

The comments come from ten questions. Ask all of them of every paragraph,
figure, table and equation, in reading order.

1. **Why did we model it this way?** Every modelling choice needs its
   reason in the text, right where the choice is made. Missing reasons are
   the most common comment.
   - "Then why does the storage layer never see the order coming in? Again we
     miss a spot to argue for why."
   - "Why did we model so the agent only can carry one item to the
     workstation at a time, but for the put-away it can hold more? We need to
     give a reason for this modelling."
   - "What does the one section a SKU belongs to mean and why did we model it
     this way?" (and the author answers it: without it random storage would
     be as good, so the model loses its meaning)
   - "We should also note why we defined the rules as we did and not using RL
     to learn it for the storage."

2. **Where does the idea come from?** Borrowed or our own? If borrowed, cite
   it where it is used. If our own, say so.
   - "Where do we have the ideas from? Did we just invent them or is it an
     extension of existing ideas?"
   - "Direction to the target. Where does this come from. Oh yeah, from
     Knippenberg. Then we should cite it."
   - "Is this from someone else's definition or idea, as described in
     Background or related works?"
   - "How much can we simplify if we referred to Axsäter?"

3. **Reading order.** Define before use, and show after defining. No forward
   references in the Problem Formulation. Shared things come before the parts
   that differ.
   - "Storage rule forward reference is not allowed."
   - "Should the table come before the image? So we first define it and then
     show how it works."
   - "The crowding feature in the picture is presented here and is forward
     referenced. Follow the reading order."
   - "Does the reader know about release time yet?"
   - "The three controllers share the assignment rule. This lays the
     foundation, so should it not move up?"
   - "Do we get the reader through the storage in the right order or should
     we move some of it around?"
   - "This rule is on the next page. So what rule are we referring to?"

4. **One name per idea, and few names.** Two words for one thing, or one
   symbol that might be another, confuses the reader. Too many new terms at
   once drowns them.
   - "What is the difference between a shelf and a storage vertex? As I
     understand it is the same, but again we confuse the reader."
   - "Here we talk about controllers, however we also use arms. Why is that?"
   - "The pickup vertex, is it a name for the three vertex types? Either say
     it clearly or drop it and name all three."
   - "Here I feel like the reader drowns in terms like shipment."
   - "Earlier we stated assign as a rule, here as a function. There seems to
     be some confusion."

5. **Plain words.** No coding language, no fancy words, no "technical
   language" where a normal sentence works.
   - "What a tally? Use normal words."
   - "Task records is bad wording, feels like coding language."
   - "It is very technical language. Should just be readable."
   - "What is a parcel or package? Is package a cleaner word?"

6. **Symbols earn their place.** Every symbol must be defined before use and
   must be needed. If it is not needed, remove it. Hard maths needs words.
   - "Q_t, where is that defined? And what word would we use if it was just
     in text?"
   - "Why do you use that symbol? Can we remove it?"
   - "Have we yet defined s_t here, or is it just thrown in before the reader
     understands the term?"
   - "The sigma part of t_j is way too hard to understand. Why is it part of
     it and how do we describe it better?"
   - "What do we mean with W_1 Tea? Here I cannot follow it."

7. **No repetition.** Not of the text just above, not of a table in the next
   line, not of a definition from an earlier section.
   - "This is a repetition of the text just above. We need to make sure we
     don't repeat ourselves all the time."
   - "We repeat the table just after the table. Define it once."
   - "We already defined that an agent gets at most one task. Here we repeat
     ourselves again."
   - "Is this just our rule from the agents and collisions section, and a
     repetition here?"

8. **What are we trying to tell the reader?** A paragraph must have a clear
   point. A sentence alone must not float.
   - "Here we say the lines of an order share release time and workstation,
     but what are we trying to state to the reader with this?"
   - "This section does not make any sense whatsoever. What are we trying to
     tell the reader?"
   - "Does this make sense as a lone line of text? No, it should be combined
     with something else."
   - "Is the two-agents-in-neighbouring-zones example good to have here? Does
     it help the reader?"

9. **Figures.** Each figure must be concrete, show only what has been
   defined, and match the text. The author dislikes figures and wording that
   "feel AI".
   - "The image feels AI. Why does it have V and W in it? We do not explain
     them. We need to be very concrete about images."
   - "Should the text go beside the image, and split it into 3 images?"
   - "Picking uses up stock again, should maybe have a figure." (ask for a
     figure where a rule is hard to follow, such as the pickup rule)
   - "Why t_j^released and then released? It feels AI." (a symbol followed by
     the same word in prose)
   - "We can write the figure text more clearly."

10. **Is it true, and is it the whole story?** Check claims against the code
    (`slap-mapd-coupling`) and against the model the author now has.
    Challenge the method itself. Name what is out of scope and what belongs
    in the Discussion.
    - "A line takes its units from the shelf nearest its workstation? Is that
      true, or have we changed that model?"
    - "If they select one at a time, is it still centralised? What can we
      criticise about this way of doing it?"
    - "Why have we not done what Token Passing does and let another agent
      complete it?"
    - "Congestion-aware storage only looks at tasks standing still, not at
      tasks taking a detour. We need to reason for this and add it to the
      Discussion."
    - "We could easily have done Knippenberg's delivery time. But we need to
      say it is out of scope."
    - "The decentralised controller is not defined as the others are. Does
      this leave the reader wondering? Argue why or why not."

Also note structure ("split fixed, demand and congestion so it is easier to
find what belongs to what", "does this belong here or later?") and practical
faults (broken links between sections in the PDF).

## The voice

- First person plural for the thesis ("we", "our"), "I" for the reader's
  own view ("I feel like", "I cannot follow it", "as I understand it").
- Mostly questions. Often a question, then the likely answer, then what to
  do ("So it takes from the first shelf and then the next closest? Then we
  should provide an image for this rule.").
- Short, informal, direct. No hedging, no politeness padding.
- Quote or name the exact phrase or symbol being commented on.
- Praise what works, briefly: "Fine pickup time text.", "Section-based is
  really easy to understand. Good.", "I like how we explain it afterwards."
- Add "Be critical" where the comment is a hunch, not a sure fault. When
  writing such a comment, also give your own view on whether the hunch holds.

Write the comments in correct English with UK spelling. Keep the thesis prose rules in mind when suggesting
directions (no dashes, no colons joining clauses), but the comments themselves
are notes, not prose.

## Procedure

1. **Scope.** Find what to review: a chapter, a section label, or a page
   range of the compiled PDF. Pull `thesis/` first. Read the `.tex` of that
   part, the compiled PDF pages (for figures, tables and the order the
   reader meets them), and the `[Axx]` entries in
   `thesis-progress/decisions/GAPS.md` it carries, so you do not ask for a
   reason the author already decided and logged.
2. **Read what came before.** List the symbols, terms and ideas the reader
   already has when the section starts. This is what questions 3, 4 and 6
   are checked against. `thesis/Appendices/A.Notation.tex` says what each
   symbol means.
3. **Go paragraph by paragraph**, in reading order, with the ten questions.
   One comment per paragraph, figure, table or display equation that needs
   one, plus short praise where it reads well. Merge points about the same
   paragraph into one comment. For question 10, check the claim in
   `slap-mapd-coupling` before writing the comment and say what the code
   does.
4. **Be critical of yourself.** Drop a comment if the answer is already in
   the text above it, or if GAPS.md settles it. Keep comments that a first
   reader would really stumble on.
5. **Output.**
   - An annotated copy of the PDF, red notes in a wide right margin next to
     the paragraph they are about, written to the scratchpad. Write the
     comments to a JSON list of `{"page", "quote", "comment"}` (page is the
     1-based PDF page, quote a short exact phrase from that paragraph), then
     run
     `uv run -q --with pymupdf python -I <this skill>/scripts/annotate.py IN.pdf notes.json OUT.pdf`.
     Fix any "quote not found" by choosing a shorter or different phrase.
     Look at one or two pages with `pdftoppm` to check the placement.
   - In chat, a short list grouped by the ten questions, most important
     first, with the page and the phrase. End with the two or three changes
     that would help the reader most.
6. **Stop.** Do not rewrite anything. If the author wants changes, discuss
   them first, then follow the review PDF workflow in `CLAUDE.md`.
