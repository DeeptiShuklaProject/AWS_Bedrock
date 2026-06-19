

# Automated Reasoning checks concepts
<a name="automated-reasoning-checks-concepts"></a>

This page describes the building blocks of Automated Reasoning checks. Understanding these concepts will help you create effective policies, interpret test results, and debug issues. For a high-level overview of what Automated Reasoning checks do and when to use them, see [Rules](#ar-concept-rules).

## Policies
<a name="ar-concept-policies"></a>

An Automated Reasoning *policy* is a resource in your AWS account that contains a set of formal logic rules, a schema of variables, and optional custom types. The policy encodes the business rules, regulations, or guidelines that you want to validate LLM responses against.

Policies are created from source documents — such as HR handbooks, compliance manuals, or product specifications — that describe the rules in natural language. When you create a policy, Automated Reasoning checks extract the rules and variables from your document and translates them into formal logic that can be mathematically verified.

The relationship between policies, guardrails, and your application is as follows:

```
Source Document ──► Automated Reasoning Policy ──► Guardrail ──► Your Application
  (natural          (rules + variables +           (references     (calls guardrail
   language)         custom types)                  a policy        APIs to validate
                                                    version)        LLM responses)
```

Key characteristics of policies:
+ Each policy is identified by an Amazon Resource Name (ARN) and exists in a specific AWS Region.
+ Policies have a `DRAFT` version (called "Working Draft" in the console) that you edit during development, and numbered immutable versions that you create for deployment.
+ A guardrail can reference the DRAFT policy or a specific numbered version. Using a numbered version means you can update the `DRAFT` without affecting your deployed guardrail.
+ Each policy should focus on a specific domain (for example, HR benefits, loan eligibility, product return rules) rather than trying to cover multiple unrelated areas.

For step-by-step instructions on creating a policy, see [Create your Automated Reasoning policy](create-automated-reasoning-policy.md).

## Fidelity report
<a name="ar-concept-fidelity-report"></a>

A *fidelity report* measures how accurately an extracted policy represents the source documents it was generated from. The report is automatically generated when you create a policy from a source document, and provides two key scores along with detailed grounding information that links every rule and variable back to specific statements in your source content.

The fidelity report is designed to help non-technical subject matter experts explore and validate a policy without needing to understand formal logic. In the console, the **Source Document** tab displays the fidelity report as a table of numbered atomic statements extracted from your document, showing which rules and variables each statement grounds. You can filter by specific rules or variables and search for content within the statements.

The fidelity report includes two scores, each ranging from 0.0 to 1.0:
+ **Coverage score** — Indicates how well the policy covers the statements in the source documents. A higher score means more of the source content is represented in the policy.
+ **Accuracy score** — Indicates how faithfully the policy rules represent the source material. A higher score means the extracted rules more closely match the intent of the original document.

Beyond the aggregate scores, the fidelity report provides detailed grounding for each rule and variable in the policy:
+ **Rule reports** — For each rule, the report identifies the specific statements from the source documents that support it (grounding statements), explains how those statements justify the rule (grounding justifications), and provides an individual accuracy score with a justification.
+ **Variable reports** — For each variable, the report identifies the source statements that support the variable definition, explains the justification, and provides an individual accuracy score.
+ **Document sources** — The source documents are broken down into atomic statements — individual, indivisible facts extracted from the text. The document content is annotated with line numbers so you can trace each rule and variable back to the exact location in the original document.

## Rules
<a name="ar-concept-rules"></a>

Rules are the core of an Automated Reasoning policy. Each rule is a formal logic expression that captures a relationship between variables. Rules are expressed using a subset of [SMT-LIB](https://smtlib.cs.uiowa.edu/) syntax, a standard format for formal logic that Automated Reasoning checks use for mathematical verification. See [KMS permissions for Automated Reasoning policies](create-automated-reasoning-policy.md#automated-reasoning-policy-kms-permissions)

Most rules should follow an *if-then* (implicative) format. This means rules should have a condition (the "if" part) and a conclusion (the "then" part), connected by the implication operator `=>`.

**Well-formed rules (if-then format):**

```
;; If the employee is full-time AND has worked for more than 12 months,
;; then they are eligible for parental leave.
(=> (and isFullTime (> tenureMonths 12)) eligibleForParentalLeave)

;; If the loan amount is greater than 500,000, then a co-signer is required.
(=> (> loanAmount 500000) requiresCosigner)
```

**Bare assertions (rules without an if-then structure) create axioms — statements that are always true.** This is useful to check boundary conditions such as account balances having positive values, but can also make certain conditions logically impossible and lead to unexpected `IMPOSSIBLE` results during validation. For example, the bare assertion `(= eligibleForParentalLeave true)` means Automated Reasoning checks treat it as a fact that the user is eligible for parent leave. Any input that mentions not being eligible would produce a validation result of `IMPOSSIBLE` because it contradicts this axiom.

```
;; GOOD: Useful to check impossible conditions such as 
;; negative account balance
(>= accountBalance 0)

;; BAD: This asserts eligibility as always true, regardless of conditions.
eligibleForParentalLeave
```

Rules support the following logic operators:


| Operator | Meaning | Example | 
| --- | --- | --- | 
| => | Implication (if-then) | (=> isFullTime eligibleForBenefits) | 
| and | Logical AND | (and isFullTime (> tenure 12)) | 
| or | Logical OR | (or isVeteran isTeacher) | 
| not | Logical NOT | (not isTerminated) | 
| = | Equality | (= employmentType FULL\_TIME) | 
| >, <, >=, <= | Comparison | (>= creditScore 700) | 

For best practices on writing effective rules, see [Automated Reasoning policy best practices](automated-reasoning-policy-best-practices.md).

## Variables
<a name="ar-concept-variables"></a>

Variables represent the concepts in your domain that Automated Reasoning checks use to translate natural language into formal logic and to evaluate rules. Each variable has a name, a type, and a description.

Automated Reasoning checks support the following variable types:


| Type | Description | Example | 
| --- | --- | --- | 
| BOOL | True or false value | isFullTime — Whether the employee works full-time | 
| INT | Whole number | tenureMonths — Number of months the employee has worked | 
| NUMBER | Decimal number | interestRate — Annual interest rate as a decimal (0.05 means 5%) | 
| Custom type (enum) | One value from a defined set | leaveType — One of: PARENTAL, MEDICAL, BEREAVEMENT, PERSONAL | 

**Warning**  
Model your domain using only the variable types in the preceding table. Avoid designing a policy that depends on unsupported data — such as raw strings or free-form text — or that requires the translation step to compute or interpret a value. Aim to minimize the complexity of the translation.  
Automated Reasoning checks are designed to interpret natural language, and are not applicable to all forms of verification. For instance, validating that a password meets a set of requirements is better handled by deterministic, rule-based code, since it depends on evaluating the raw value character by character rather than reasoning over natural language.

**Note**  
Within a policy definition, variable names, custom type names, and the values defined within custom types all share a single namespace. Every one of these names must be unique across all three categories. You cannot use the same name for a variable and a type, and the same value cannot appear in more than one custom type. For example, if a `LeaveType` type defines an `OTHER` value, no other type (such as `Severity`) can also define `OTHER`, and no variable can be named `OTHER`. When you need a similar value in more than one type, prefix it with the type name to keep each name unique while preserving its meaning — for example, `LeaveType_OTHER` and `Severity_OTHER`.

### The critical role of variable descriptions
<a name="ar-concept-variable-descriptions"></a>

Variable descriptions are the single most important factor in translation accuracy. When Automated Reasoning checks translate natural language into formal logic, it uses variable descriptions to determine which variables correspond to concepts mentioned in the text. Vague or incomplete descriptions lead to `TRANSLATION_AMBIGUOUS` results or incorrect variable assignments.

**Example: How descriptions affect translation**

Consider a user asking: "I've been working here for 2 years. Am I eligible for parental leave?"


| Vague description (likely to fail) | Detailed description (likely to succeed) | 
| --- | --- | 
| tenureMonths: "How long the employee has worked." | tenureMonths: "The number of complete months the employee has been continuously employed. When users mention years of service, convert to months (for example, 2 years = 24 months). Set to 0 for new hires." | 

With the vague description, Automated Reasoning checks may not know to convert "2 years" to 24 months, or may not assign the variable at all. With the detailed description, the translation is unambiguous.

Good variable descriptions should:
+ Explain what the variable represents in plain language.
+ Specify the unit and format (for example, "in months", "as a decimal where 0.15 means 15%").
+ Include non-obvious synonyms and alternative phrasings that users might use (for example, "Set to true when users mention being 'full-time' or working full hours").
+ Describe boundary conditions (for example, "Set to 0 for new hires").

## Custom types (enums)
<a name="ar-concept-custom-types"></a>

Custom types define a set of named values that a variable can take. They are equivalent to enumerations (enums) in programming languages. Use custom types when a variable represents a category with a fixed set of possible values.

**Examples:**


| Type name | Possible values | Use case | 
| --- | --- | --- | 
| LeaveType | PARENTAL, MEDICAL, BEREAVEMENT, PERSONAL | Categorize the type of leave an employee is requesting | 
| Severity | CRITICAL, MAJOR, MINOR | Classify the severity of an issue or incident | 

**When to use enums vs. booleans:**
+ Use enums when the values are *mutually exclusive* — a variable can only be one value at a time. For example, `leaveType` can be PARENTAL or MEDICAL, but not both simultaneously.
+ Use separate boolean variables when states can *co-exist*. For example, a person can be both a veteran and a teacher. Using an enum `customerType = {VETERAN, TEACHER}` would force a choice between them, creating a logical contradiction when both apply. Instead, use two booleans: `isVeteran` and `isTeacher`.

**Tip**  
If it's possible for a variable not to have any value from the enum, include an `OTHER` or `NONE` value. This prevents translation issues when the input doesn't match any of the defined values.

## Translation: from natural language to formal logic
<a name="ar-concept-translation"></a>

Translation is the process by which Automated Reasoning checks convert natural language (user questions and LLM responses) into formal logic expressions that can be mathematically verified against your policy rules. Understanding this process is key to debugging issues and creating effective policies.

Automated Reasoning checks validate content in two distinct steps:

1. **Translate** — Automated Reasoning checks use foundation models (LLMs) to translate the natural language input into formal logic. This step maps concepts in the text to your policy's variables and expresses the relationships as logical statements. Because this step uses LLMs, it may *contain errors*. Automated Reasoning checks uses multiple LLMs to translate the input text then uses the semantic equivalence of the redundant translations to set a confidence score. The quality of the translation depends on how well your variable descriptions match the language used in the input.

1. **Validate** — Automated Reasoning checks use mathematical techniques (through SMT solvers) to check whether the translated logic is consistent with your policy rules. This step *is mathematically sound* — if the translation is correct, the validation result will be consistent.

**Important**  
This two-step distinction is critical for debugging. If you are certain the rules in the policy are correct, when a test fails or returns unexpected results, the issue is mist likely in step 1 (translation), not step 2 (validation). The mathematical validation is sound and if the translation correctly captures the meaning of the input, the validation result will be correct. Focus your debugging efforts on improving variable descriptions and ensuring the translation assigns the right variables with the right values.

**Example: Translation in action**

Given a policy with variables `isFullTime` (BOOL), `tenureMonths` (INT), and `eligibleForParentalLeave` (BOOL), and the input:
+ **Question:** "I'm a full-time employee and I've been here for 18 months. Can I take parental leave?"
+ **Answer:** "Yes, you are eligible for parental leave."

Step 1 (translate) produces:

```
Premises: isFullTime = true, tenureMonths = 18
Claims: eligibleForParentalLeave = true
```

Step 2 (validate) checks these assignments against the policy rule `(=> (and isFullTime (> tenureMonths 12)) eligibleForParentalLeave)` and confirms the claim is `VALID`.

To improve translation accuracy:
+ Write detailed variable descriptions that cover how users refer to concepts in everyday language.
+ Remove duplicate or near-duplicate variables that could confuse the translation (for example, `tenureMonths` and `monthsOfService`).
+ Delete unused variables that aren't referenced by any rules — they add noise to the translation process.
+ Use question-and-answer tests to validate translation accuracy with realistic user inputs. For more information, see [Test an Automated Reasoning policy](test-automated-reasoning-policy.md).

## Findings and validation results
<a name="ar-concept-findings"></a>

When Automated Reasoning checks validate content, it produces a set of *findings*. Each finding represents a factual claim extracted from the input, along with the validation result, the variable assignments used, and the policy rules that support the conclusion. The overall (aggregated) result is determined by sorting findings in order of severity and selecting the worst result. The severity order from worst to best is: `TRANSLATION_AMBIGUOUS`, `IMPOSSIBLE`, `INVALID`, `SATISFIABLE`, `VALID`.

### Structure of a finding
<a name="ar-concept-findings-structure"></a>

The result type determines which fields are present in the finding. See the [Validation results reference](#ar-concept-validation-results) section for an in-depth description of each finding type. However, most finding types share a common `translation` object that contains the following components:

`premises`  
Context, assumptions, or conditions extracted from the input that affect how a claim should be evaluated. In question-and-answer formats, the premise is often the question itself. Answers can also contain premises that establish constraints. For example, in "I'm a full-time employee with 18 months of service," the premises are `isFullTime = true` and `tenureMonths = 18`.

`claims`  
Factual statements that Automated Reasoning checks evaluate for accuracy. In a question-and-answer format, the claim is typically the answer. For example, in "Yes, you are eligible for parental leave," the claim is `eligibleForParentalLeave = true`.

`confidence`  
A score from 0.0 to 1.0 representing how certain Automated Reasoning checks is about the translation from natural language to formal logic. Higher scores indicate greater certainty. A confidence of 1.0 means all translation models agreed on the same interpretation.

`untranslatedPremises`  
References to portions of the original input text that correspond to premises but could not be translated into formal logic. These highlight parts of the input that Automated Reasoning recognized as relevant but couldn't map to policy variables.

`untranslatedClaims`  
References to portions of the original input text that correspond to claims but could not be translated into formal logic. A `VALID` result only covers the translated claims — untranslated claims are not validated.

### Validation results reference
<a name="ar-concept-validation-results"></a>

Each finding is exactly one of the following types. The type determines the meaning of the result, the fields available in the finding, and the recommended action for your application. All finding types that include a `translation` field also include a `logicWarning` field that is present when the translation contains logical issues independent of the policy rules (for example, statements that are always true or always false).


| Result | Finding fields | Recommended action | 
| --- | --- | --- | 
| VALID | `translation` — The translated premises, claims, confidence score, and any untranslated references.<br />`supportingRules` — The policy rules that prove the claims are correct. Each rule includes its identifier and the policy version ARN.<br />`claimsTrueScenario` — A scenario (set of variable assignments) demonstrating how the claims are logically true. | Serve the response to the user. Log supportingRules and claimsTrueScenario for audit purposes — they provide mathematically verifiable proof of validity. Check untranslatedPremises and untranslatedClaims for parts of the input that were not validated. | 
| INVALID | `translation` — The translated premises, claims, confidence score, and any untranslated references.<br />`contradictingRules` — The policy rules that the claims violate. Each rule includes its identifier and the policy version ARN. | Do not serve the response. Use translation (to see what was claimed) and contradictingRules (to see which rules were violated) to rewrite the response or block it. In a rewriting loop, pass the contradicting rules and incorrect claims to the LLM to generate a corrected response. | 
| SATISFIABLE | `translation` — The translated premises, claims, confidence score, and any untranslated references.<br />`claimsTrueScenario` — A scenario demonstrating how the claims could be logically true.<br />`claimsFalseScenario` — A scenario demonstrating how the claims could be logically false under different conditions. | Compare claimsTrueScenario and claimsFalseScenario to identify the missing conditions. Rewrite the response to include the additional information needed to make it VALID, ask the user for clarification about the missing conditions, or serve the response with a caveat that it may be incomplete. | 
| IMPOSSIBLE | `translation` — The translated premises, claims, confidence score, and any untranslated references. Inspect the premises to identify contradictions.<br />`contradictingRules` — The policy rules that conflict with the premises or with each other. If populated, the contradiction may be in the policy itself. | Check whether the input contains contradictory statements (for example, "I'm full-time and also part-time"). If the input is valid, the contradiction is likely in your policy — check contradictingRules and review the quality report. See [Troubleshoot and refine your Automated Reasoning policy](address-failed-automated-reasoning-tests.md). | 
| TRANSLATION\_AMBIGUOUS | Does not contain a `translation` object. Instead provides:<br />`options` — The competing logical interpretations (up to 2). Each option contains its own `translations` with premises, claims, and confidence. Compare options to see where models disagreed.<br />`differenceScenarios` — Scenarios (up to 2) that illustrate how the different interpretations differ in meaning, with variable assignments highlighting the practical impact of the ambiguity. | Inspect options to understand the disagreement. Improve variable descriptions to reduce ambiguity, merge or remove overlapping variables, or ask the user for clarification. You can also adjust the confidence threshold — see [Confidence thresholds](#ar-concept-confidence-thresholds). | 
| TOO\_COMPLEX | Does not contain a `translation`, rules, or scenarios. The input exceeded processing capacity due to volume or complexity. | Shorten the input by breaking it into smaller pieces, or simplify policy by reducing the number of variables, and avoid complex arithmetic (for example, exponents or irrational numbers). You can split your policy into smaller, more focused policies. | 
| NO\_TRANSLATIONS | Does not contain a `translation`, rules, or scenarios. May appear alongside other findings if only part of the input could be translated. | A NO\_TRANSLATIONS finding is included in the output whenever one of the other findings includes untranslated premises or claims. Look through the other findings to see which portions of the input were not translated. If the content should be relevant, add variables to your policy to capture the missing concepts. If the content is off-topic, consider using topic policies to filter it before it reaches Automated Reasoning checks. | 

**Note**  
A `VALID` result covers only the parts of the input captured through policy variables in the translated premises and claims. Statements that fall outside the scope of your policy's variables are not validated. For example, "I can submit my homework late because I have a fake doctor's note" might be deemed valid if the policy has no variable to capture whether the doctor's note is fake. Automated Reasoning checks will likely include "fake doctor's note" as an untranslated premise in its finding. Treat untranslated content and `NO_TRANSLATIONS` findings as a warning signal.

## Confidence thresholds
<a name="ar-concept-confidence-thresholds"></a>

Automated Reasoning checks use multiple foundation models to translate natural language into formal logic. Each model produces its own translation independently. The *confidence score* represents the level of agreement among these translations — specifically, the percentage of models that produced semantically equivalent interpretations.

The *confidence threshold* is a value you set (from 0.0 to 1.0) that determines the minimum level of agreement required for a translation to be considered reliable enough to validate. It controls the trade-off between coverage and accuracy:
+ **Higher threshold** (for example, 0.9): Requires strong agreement among translation models. Produces fewer findings but with higher accuracy. More inputs will be flagged as `TRANSLATION_AMBIGUOUS`.
+ **Lower threshold** (for example, 0.5): Accepts translations with less agreement. Produces more findings but with a higher risk of incorrect translations. Fewer inputs will be flagged as `TRANSLATION_AMBIGUOUS`.

**How the threshold works:**

1. Multiple foundation models each translate the input independently.

1. Translations that are supported by a percentage of models equal to or above the threshold become high-confidence findings with a definitive result (`VALID`, `INVALID`, etc.).

1. If one or more translations fall below the threshold, Automated Reasoning checks surface an additional `TRANSLATION_AMBIGUOUS` finding. This finding includes details about the disagreements between the models, which you can use to improve your variable descriptions or ask the user for clarification.

**Tip**  
Start with the default threshold and adjust based on your testing results. If you see too many `TRANSLATION_AMBIGUOUS` results for inputs that should be unambiguous, focus on improving your variable descriptions rather than lowering the threshold. Lowering the threshold may reduce `TRANSLATION_AMBIGUOUS` results but increases the risk of incorrect validations.