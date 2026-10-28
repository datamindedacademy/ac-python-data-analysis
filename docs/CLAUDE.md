# Working on the slides

The deck is `slides.md` (Slidev), with a local theme in `theme/` and extra styles in `style.css`.

## The work

- A question is a question: answer it, and only change slides when that is asked for or agreed on.
- A request gives a goal, not a specification: use your judgement on how to do it well, including what the
  change needs to work (room on the slide, a matching solution). If a suggested route does not work, say so
  instead of quietly doing something else.
- Before reporting, look at a screenshot of every changed slide as a critical reviewer would, and fix what is
  off.
- Leave everything else as it is: do not reword, rename or move what was not mentioned. Flag other problems you
  notice instead of fixing them.
- Do not overcorrect. Fixing one problem must not create another: when you shorten, the slide must stay correct,
  complete in its essentials and clear. Check that every sentence is still true and says what matters, and
  that nothing on the slide is left unexplained (a variable that appears from nowhere, a claim cut in half).

## What a good slide is

- The audience has had about one day of Python. Everything a slide uses is either explained on it or on an
  earlier slide; no cryptic Python, no unexplained arguments.
- Each slide can be read on its own: the data it works on is on the slide.
- The layout follows the content of that slide, not a template.
- Examples and techniques are realistic: what people actually do day to day. Teach current pandas, and be
  opinionated where a newer way is better (for example new DataFrames with `assign` and `pd.col` instead of
  changing them in place).
- On slides the DataFrame is usually just `df`; results get a new name, never `df = df...`.
- No live demos: everything the presenter shows is on the slides. Demos go wrong.
- Clicks (`v-click`) build up a slide in steps: what is not relevant yet (the next function, a follow-up
  like renumbering) comes behind a click. Not to hide an output for the room to guess. Only where a slide
  has clearly separate steps.
- Outputs are what the code really prints, and claims about pandas are checked, not remembered.
- Be brief: one short sentence where a paragraph would fit, and a note on a slide is one line, two at most.
  But the slide still stands on its own: keep what someone reading only the slide needs.
- Little text, in plain, exact language and standard terms. Brief, but never cryptic: write full sentences, not
  shorthand like "In `groupby`: the column name as text." If a point needs that much compressing, it probably
  does not belong on the slide. Not patronizing, no clever or kitschy titles; accent colour and bold
  only where they mean something.
- Content is not traded away for a minor style or layout detail.
- A picture or diagram shows something the slide needs; no decoration that repeats what earlier slides
  already explained.
- Column headers say what the column shows. An input starts with "Input:" ("Input: one row per measurement"); a
  column with code starts with a verb for what it does ("Calculating the mean per station", "Converting to date
  with .dt.normalize()"), not a bare noun ("The mean per station", "One day with .dt.normalize()"). Headers that
  explain or contrast ("How it works", "Naive" / "Time-zone aware") stay as they are. A header fits on one line.
- Parallel statements that contrast two things (`"count"` counts the values that are not missing,
  `"size"` counts the rows) go on a line each, not run together in one paragraph that wraps.
- Docs links are clickable and show their full, clean URL.
- On slides, a docs link is "more info": it can point to a user guide or a general page.
- In the exercises, a docs link is only there when there is something to look up: the syntax or arguments of
  a function the answer could reasonably use (`read_csv` has dozens of arguments). It points to the API
  reference of that function, never to a page that explains a broad concept. When the slides already show
  all the answer needs (`case_when`), there is no link. A function that is not on the slides at all gets a link
  marked "(not in the slides)", but avoid exercises that need one.
- Slides explain concepts; they do not have to match the exercises. Nothing refers to a specific client or
  delivery.
- The transcript (`<!-- ... -->`, Slidev's speaker notes) is what the presenter says while showing the slide,
  word for word. It is not a place for details left off the slide. It is also how the timing of the day is
  estimated.

## Technical

The theme is installed as a copy (`file:./theme`), and the Slidev server does not pick up changes to `theme/`
until it restarts.
