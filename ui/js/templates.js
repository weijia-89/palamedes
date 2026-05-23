/** @typedef {{ id: string, label: string, description: string, outputTokens: number }} PalamedesTemplate */

/** @type {PalamedesTemplate[]} */
export const TEMPLATES = [
  {
    id: "full-report",
    label: "Full report",
    description: "Long-form markdown with claim ledger and falsifiers.",
    outputTokens: 4500,
  },
  {
    id: "landscape-one-pager",
    label: "Landscape one-pager",
    description: "Dense skim sheet for printing or sharing.",
    outputTokens: 2200,
  },
  {
    id: "executive-brief",
    label: "Executive brief",
    description: "Recommendation-focused memo.",
    outputTokens: 1800,
  },
  {
    id: "study-guide-site",
    label: "Study guide site",
    description: "Multi-day exam-prep corpus with pedagogy appendix outline.",
    outputTokens: 7500,
  },
];

/** @type {{ id: string, label: string, inputFactor: number }[]} */
export const QUESTION_TYPES = [
  { id: "empirical", label: "Empirical (does X cause Y?)", inputFactor: 1.0 },
  { id: "conceptual", label: "Conceptual (what is X?)", inputFactor: 0.85 },
  { id: "predictive", label: "Predictive (what will happen?)", inputFactor: 1.05 },
  { id: "comparative", label: "Comparative (X vs Y)", inputFactor: 1.1 },
  { id: "investigative", label: "Investigative (why did X?)", inputFactor: 1.15 },
  { id: "synthetic", label: "Literature synthesis", inputFactor: 1.25 },
];

/** @type {{ id: string, label: string, rigorFactor: number }[]} */
export const STAKES = [
  { id: "L0", label: "L0 — exploratory", rigorFactor: 0.75 },
  { id: "L1", label: "L1 — informational", rigorFactor: 0.9 },
  { id: "L2", label: "L2 — advisory", rigorFactor: 1.0 },
  { id: "L3", label: "L3 — decision-driving", rigorFactor: 1.15 },
  { id: "L4", label: "L4 — irreversible", rigorFactor: 1.3 },
];
