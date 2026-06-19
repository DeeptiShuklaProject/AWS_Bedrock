

# Score definitions
<a name="guardrails-use-invoke-guardrail-checks-scores"></a>

## Severity score (for content filters and prompt attack detection)
<a name="guardrails-use-invoke-guardrail-checks-severity-score"></a>

With content filters and prompt attack detection, the API returns a severity score, which is a numeric value in the range [0, 1] that represents the strongest match for the safety check criteria. These scores are discrete with the possible values being 0, 0.2, 0.4, 0.6, 0.8, and 1.0.

A score of 1 (maximum) is the strongest match, indicating the closest match to the definition of the safety check. A score of 0 (minimum) is the weakest match, indicating the content is benign.

The severity score is a property of the content itself, not the certainty of the underlying model about its classification. It answers the question, "How strongly does this content match the criteria for the safety check?" It does not answer, "How sure is the underlying model?" The following table elaborates this definition.


**Severity score meaning by safeguard**  

| Safeguard | Granularity | Meaning of a severity score | 
| --- | --- | --- | 
| Content filter | Per category (HATE, VIOLENCE, INSULTS, SEXUAL, MISCONDUCT) | How strongly does the content match the harmful content for each category? | 
| Prompt attack | Per attack vector (JAILBREAK, PROMPT\_INJECTION, PROMPT\_LEAKAGE) | How strongly does the content match each attack vector? | 

The score by itself doesn't block any content. You use the score as a threshold to control how restrictive your application acts.

## Confidence score (for sensitive information filters)
<a name="guardrails-use-invoke-guardrail-checks-confidence-score"></a>

With sensitive information filters, the API returns a confidence score that indicates how certain the model is that a PII entity is present. This score is relevant to PII detection and reflects the model's confidence about the presence of PII entities that you selected when you invoked the API.