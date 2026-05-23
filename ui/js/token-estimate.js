/**
 * Heuristic USD estimate — not a quote from the provider.
 * @param {{ questionChars: number, templateOutputTokens: number, questionTypeFactor: number, stakesFactor: number, inputPricePer1M: number, outputPricePer1M: number }} p
 */
export function estimateCost(p) {
  const inputTokens = Math.ceil((p.questionChars + 2800) / 4 * p.questionTypeFactor * p.stakesFactor);
  const outputTokens = Math.ceil(p.templateOutputTokens * p.stakesFactor);
  const inputUsd = (inputTokens / 1_000_000) * p.inputPricePer1M;
  const outputUsd = (outputTokens / 1_000_000) * p.outputPricePer1M;
  return {
    inputTokens,
    outputTokens,
    totalUsd: inputUsd + outputUsd,
    totalTokens: inputTokens + outputTokens,
  };
}

export const DEFAULT_PRICING = {
  inputPricePer1M: 3.0,
  outputPricePer1M: 15.0,
};
