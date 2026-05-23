import { TEMPLATES, QUESTION_TYPES, STAKES } from "./templates.js";
import { estimateCost, DEFAULT_PRICING } from "./token-estimate.js";

const STORAGE_KEY = "palamedes-ui-settings-v1";
const SESSION_KEY = "palamedes-ui-session-v1";

const $ = (id) => document.getElementById(id);

function loadSettings() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
  } catch {
    return {};
  }
}

function saveSettings(s) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(s));
}

function loadSession() {
  try {
    return JSON.parse(sessionStorage.getItem(SESSION_KEY) || "null");
  } catch {
    return null;
  }
}

function saveSession(s) {
  sessionStorage.setItem(SESSION_KEY, JSON.stringify(s));
}

function fillSelect(el, items) {
  el.innerHTML = "";
  for (const item of items) {
    const o = document.createElement("option");
    o.value = item.id;
    o.textContent = item.label;
    el.appendChild(o);
  }
}

function getTemplate(id) {
  return TEMPLATES.find((t) => t.id === id) || TEMPLATES[0];
}

function getFactor(list, id, key) {
  const row = list.find((x) => x.id === id);
  return row ? row[key] : 1;
}

function updateEstimate() {
  const q = $("question").value.trim();
  const template = getTemplate($("template").value);
  const est = estimateCost({
    questionChars: q.length,
    templateOutputTokens: template.outputTokens,
    questionTypeFactor: getFactor(QUESTION_TYPES, $("question-type").value, "inputFactor"),
    stakesFactor: getFactor(STAKES, $("stakes").value, "rigorFactor"),
    inputPricePer1M: Number($("price-in").value) || DEFAULT_PRICING.inputPricePer1M,
    outputPricePer1M: Number($("price-out").value) || DEFAULT_PRICING.outputPricePer1M,
  });
  $("estimate").textContent = `~${est.totalTokens.toLocaleString()} tokens · ~$${est.totalUsd.toFixed(2)} (heuristic)`;
}

async function loadSystemPrompt() {
  const res = await fetch("./prompts/research-system.md");
  if (!res.ok) throw new Error("Missing prompts/research-system.md");
  return res.text();
}

function buildUserPrompt(systemTpl, fields) {
  return systemTpl
    .replaceAll("{{QUESTION_TYPE}}", fields.questionType)
    .replaceAll("{{STAKES}}", fields.stakes)
    .replaceAll("{{TEMPLATE_ID}}", fields.templateId)
    .replaceAll("{{USER_QUESTION}}", fields.question);
}

const DEFAULT_REFINEMENTS = [
  "Which load-bearing claim needs stronger sources?",
  "What is the strongest counterargument or falsifier?",
  "Compare the leading alternative framing.",
  "What evidence would change the recommendation?",
];

function sectionBody(text, name) {
  const re = new RegExp(
    `^#{1,4}\\s*${name}\\s*\\n([\\s\\S]*?)(?=^#{1,4}\\s*(?:SHORT_ANSWER|FULL_REPORT|REFINEMENT_OPTIONS)\\b|$)`,
    "im",
  );
  const m = text.match(re);
  return m ? m[1].trim() : "";
}

function tryParseJsonArray(raw) {
  const start = raw.indexOf("[");
  if (start < 0) return null;
  for (let end = raw.length; end > start; end -= 1) {
    if (raw[end - 1] !== "]") continue;
    try {
      const arr = JSON.parse(raw.slice(start, end));
      if (Array.isArray(arr)) return normalizeRefinements(arr);
    } catch {
      /* try shorter slice */
    }
  }
  return null;
}

function parseRefinementOptions(text) {
  const block = sectionBody(text, "REFINEMENT_OPTIONS");
  const searchIn = block || text.slice(Math.max(0, text.length - 2500));

  const fenced = searchIn.match(/```(?:json)?\s*(\[[\s\S]*\])\s*```/i);
  if (fenced) {
    try {
      const arr = JSON.parse(fenced[1]);
      if (Array.isArray(arr)) return normalizeRefinements(arr);
    } catch {
      /* fall through */
    }
  }

  const fromJson = tryParseJsonArray(searchIn);
  if (fromJson?.length) return fromJson;

  const lines = (block || searchIn)
    .split("\n")
    .map((l) => l.replace(/^[\s>*-]+|^\d+\.\s*/, "").trim())
    .filter((l) => l.length > 8 && !l.startsWith("{") && !l.startsWith("["));
  if (lines.length) return normalizeRefinements(lines);

  return DEFAULT_REFINEMENTS;
}

function normalizeRefinements(items) {
  return items
    .map((item) => (typeof item === "string" ? item : item?.prompt || item?.label || String(item)))
    .map((s) => s.trim())
    .filter(Boolean)
    .slice(0, 6);
}

function parseSections(text) {
  let shortAnswer = sectionBody(text, "SHORT_ANSWER");
  let fullReport = sectionBody(text, "FULL_REPORT");
  if (!shortAnswer && !fullReport) {
    const refIdx = text.search(/^#{1,4}\s*REFINEMENT_OPTIONS\s*$/im);
    const body = refIdx >= 0 ? text.slice(0, refIdx) : text;
    const parts = body.split(/\n(?=#{1,3}\s)/);
    if (parts.length >= 2) {
      shortAnswer = parts[0].replace(/^#+\s*\w+\s*/m, "").trim();
      fullReport = parts.slice(1).join("\n").trim();
    } else {
      shortAnswer = body.trim().slice(0, 1200);
      fullReport = body.trim();
    }
  }
  const refinements = parseRefinementOptions(text);
  return {
    shortAnswer: (shortAnswer || text).trim().slice(0, 8000),
    fullReport: (fullReport || text).trim(),
    refinements,
  };
}

function renderRefinements(options, onPick) {
  const host = $("refinements");
  host.innerHTML = "";
  host.classList.remove("hint-empty");
  const list = options.length ? options : DEFAULT_REFINEMENTS;
  for (const opt of list) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "chip";
    btn.textContent = opt;
    btn.addEventListener("click", () => onPick(opt));
    host.appendChild(btn);
  }
}

function downloadText(filename, content) {
  const blob = new Blob([content], { type: "text/markdown;charset=utf-8" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = filename;
  a.click();
  URL.revokeObjectURL(a.href);
}

async function callLlm(messages, settings) {
  const base = settings.apiBase.replace(/\/$/, "");
  const res = await fetch(`${base}/chat/completions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${settings.apiKey}`,
    },
    body: JSON.stringify({
      model: settings.model,
      messages,
      temperature: 0.4,
    }),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`${res.status}: ${err.slice(0, 400)}`);
  }
  const data = await res.json();
  return data.choices?.[0]?.message?.content ?? "";
}

async function runResearch(isRefinement, refinementText) {
  const stored = loadSettings();
  const settings = {
    apiBase: $("api-base").value.trim() || stored.apiBase || "https://api.openai.com/v1",
    model: $("model").value.trim() || stored.model || "gpt-4o-mini",
    apiKey: $("api-key").value.trim() || stored.apiKey || "",
  };
  if (!settings.apiKey) {
    $("status").textContent = "Add an API key (stored only in this browser's localStorage).";
    return;
  }
  saveSettings({
    apiBase: settings.apiBase,
    model: settings.model,
    priceIn: $("price-in").value,
    priceOut: $("price-out").value,
  });

  const question = $("question").value.trim();
  if (!question && !isRefinement) {
    $("status").textContent = "Enter a research question.";
    return;
  }

  $("run").disabled = true;
  $("status").textContent = "Running…";

  try {
    const systemTpl = await loadSystemPrompt();
    const fields = {
      questionType: $("question-type").selectedOptions[0].textContent,
      stakes: $("stakes").value,
      templateId: $("template").value,
      question: isRefinement
        ? `${loadSession()?.question || question}\n\nFollow-up: ${refinementText}`
        : question,
    };
    const userContent = buildUserPrompt(systemTpl, fields);
    let messages = loadSession()?.messages || [];
    if (!isRefinement || !messages.length) {
      messages = [
        {
          role: "system",
          content:
            "You are palamedes. Use exact markdown headings ### SHORT_ANSWER, ### FULL_REPORT, ### REFINEMENT_OPTIONS. Under REFINEMENT_OPTIONS output only a JSON array of 4 strings.",
        },
        { role: "user", content: userContent },
      ];
    } else {
      messages = [...messages, { role: "user", content: refinementText }];
    }

    const raw = await callLlm(messages, settings);
    messages = [...messages, { role: "assistant", content: raw }];
    const parsed = parseSections(raw);

    $("short-answer").textContent = parsed.shortAnswer;
    $("full-report").textContent = parsed.fullReport;
    renderRefinements(parsed.refinements, (opt) => runResearch(true, opt));

    const session = {
      question,
      templateId: fields.templateId,
      messages,
      lastRaw: raw,
      updatedAt: new Date().toISOString(),
    };
    saveSession(session);

    $("download-md").onclick = () =>
      downloadText(`palamedes-${fields.templateId}.md`, parsed.fullReport);
    $("download-short").onclick = () =>
      downloadText(`palamedes-short.md`, parsed.shortAnswer);

    $("status").textContent = "Done.";
  } catch (e) {
    $("status").textContent = String(e.message || e);
  } finally {
    $("run").disabled = false;
  }
}

function init() {
  fillSelect($("template"), TEMPLATES);
  fillSelect($("question-type"), QUESTION_TYPES);
  fillSelect($("stakes"), STAKES);
  $("template").value = "full-report";
  $("question-type").value = "empirical";
  $("stakes").value = "L2";

  const s = loadSettings();
  if (s.apiBase) $("api-base").value = s.apiBase;
  if (s.model) $("model").value = s.model;
  if (s.priceIn) $("price-in").value = s.priceIn;
  if (s.priceOut) $("price-out").value = s.priceOut;

  ["question", "template", "question-type", "stakes", "price-in", "price-out"].forEach((id) => {
    $(id).addEventListener("input", updateEstimate);
    $(id).addEventListener("change", updateEstimate);
  });

  $("save-key").addEventListener("click", () => {
    const key = $("api-key").value.trim();
    if (!key) {
      $("status").textContent = "Key empty.";
      return;
    }
    const s2 = { ...loadSettings(), apiKey: key };
    saveSettings(s2);
    $("api-key").value = "";
    $("status").textContent = "API key saved to localStorage (this device only).";
  });

  $("clear-key").addEventListener("click", () => {
    const s2 = loadSettings();
    delete s2.apiKey;
    saveSettings(s2);
    $("status").textContent = "API key cleared from localStorage.";
  });

  $("run").addEventListener("click", () => runResearch(false));
  $("reset-session").addEventListener("click", () => {
    sessionStorage.removeItem(SESSION_KEY);
    $("short-answer").textContent = "";
    $("full-report").textContent = "";
    $("refinements").innerHTML = "";
    $("status").textContent = "Session cleared.";
  });

  const s3 = loadSettings();
  if (s3.apiKey) $("status").textContent = "API key on file (localStorage). Enter a new key to rotate.";

  const session = loadSession();
  if (session?.lastRaw) {
    const parsed = parseSections(session.lastRaw);
    $("short-answer").textContent = parsed.shortAnswer;
    $("full-report").textContent = parsed.fullReport;
    renderRefinements(parsed.refinements, (opt) => runResearch(true, opt));
    if (session.question) $("question").value = session.question;
  } else {
    renderRefinements(DEFAULT_REFINEMENTS, (opt) => {
      if (!$("question").value.trim()) {
        $("status").textContent = "Enter a question first, or run research.";
        return;
      }
      runResearch(true, opt);
    });
  }

  updateEstimate();
}

init();
