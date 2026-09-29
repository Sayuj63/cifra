# CompLens Design System

## 1. Principle

CompLens should look like a professional scientific product, not an admin dashboard.

Keywords:

- precise
- quiet
- analytical
- editorial
- premium
- technical
- trustworthy

---

# 2. Color tokens

```css
--bg: #FAFAF8;
--surface: #FFFFFF;
--surface-muted: #F6F5F2;

--text: #171717;
--text-secondary: #676762;
--text-tertiary: #92918B;

--border: #E8E6E1;
--border-strong: #D9D6CF;

--orange: #FF5A1F;
--orange-hover: #E94A12;
--orange-soft: #FFF1EA;
--orange-tint: #FFF8F4;

--positive: #1F7A55;
--warning: #A66A00;
--negative: #B5473A;
```

Do not add alternate brand colors without a reason.

---

# 3. Typography

Recommended:

Primary:
- Geist or Inter

Monospace:
- Geist Mono or IBM Plex Mono

Scale:

- Display: 48 / 52
- H1: 32 / 38
- H2: 24 / 30
- H3: 18 / 24
- Body: 15 / 23
- Small: 13 / 19
- Label: 12 / 16

Use monospaced numerals selectively for metrics, versions, and technical metadata.

---

# 4. Radius

- buttons: 7px
- inputs: 7px
- cards: 10px
- large containers: 12px max
- pill: 999px only for semantic status/tag elements

Never make every container pill-shaped.

---

# 5. Spacing

Base spacing scale:

- 4
- 8
- 12
- 16
- 24
- 32
- 48
- 64
- 96

---

# 6. Shadows

Default:
no shadow.

Use subtle shadow only for:
- floating popover
- dropdown
- dialog
- elevated contextual menu

Main page hierarchy should rely on:
- spacing
- typography
- borders
- background contrast

---

# 7. Orange semantics

Orange means one of:

- primary action
- active state
- selected model
- current chart point
- important analytical annotation
- focus indicator

Orange must not be scattered decoratively.

---

# 8. Navigation

Use a slim top navigation.

Suggested:

```text
CompLens    Estimate  Explore  Model Lab  Explain  Fairness  Methodology
```

Do not use a permanent sidebar unless a later information architecture genuinely requires one.

---

# 9. Landing page

Hero copy:

**Salary estimates, with evidence.**

Supporting copy:

> CompLens benchmarks candidate compensation using validated regression models and exposes the uncertainty and reasoning behind every estimate.

Actions:

- Estimate compensation
- Explore the model

Below hero, show real model metadata once available.

Do not show fake metrics while artifacts are unavailable.

---

# 10. Estimate screen

Desktop layout:

Left 40%:
candidate inputs.

Right 60%:
prediction/result canvas.

Before prediction:
show explanatory empty state.

After prediction:
show:

- point estimate
- 90% interval
- salary range visualization
- model/version
- local explanation
- caveat

Prediction result should feel like a research output, not a KPI card.

---

# 11. Explore screen

Use narrative sections rather than tiled dashboard cards.

Core sequence:

1. Salary vs Experience
2. Linear vs Polynomial
3. Salary by Role
4. Salary by Industry
5. Salary by City
6. Missingness/Data Quality

Each section should answer a question.

---

# 12. Model Lab

Use a high-quality table as the primary object.

Columns:

- Model
- CV R²
- CV RMSE
- CV MAE
- fold variability
- train/CV gap
- status

The champion can receive a restrained orange indicator.

Charts should supplement the table, not replace it.

---

# 13. Explain page

Sections:

- global importance
- experience response curve
- local prediction explanation
- counterfactual explorer

Avoid excessive card nesting.

---

# 14. Fairness page

Sections:

- what is being evaluated
- error by city
- interval coverage by city
- city counterfactual
- city ablation
- limitations

Clearly state the difference between subgroup diagnostics and proof of fairness.

---

# 15. Charts

Requirements:

- label axes
- show units
- use neutral tones
- reserve orange for focus/primary series
- avoid rainbow palettes
- no 3D charts
- no unnecessary legends
- tooltips should show exact values
- responsive layout
- keyboard-accessible where possible

---

# 16. Motion

Use motion only to clarify:

- result reveal
- tab/panel state
- chart focus
- dropdown/popover transitions

Duration:
120–250ms.

Avoid:
- looping animation
- parallax
- bouncing
- glowing
- floating blobs

---

# 17. Responsive behavior

Must support:

- 1440px desktop
- 1280px laptop
- 1024px tablet landscape
- 768px tablet
- 390px mobile

Mobile navigation can collapse.

Prediction form/result should stack.

Tables may use controlled horizontal scroll.

---

# 18. Empty/error/loading states

Every API-backed page must implement:

- loading
- empty
- error
- success

Never render fake model values while waiting.
