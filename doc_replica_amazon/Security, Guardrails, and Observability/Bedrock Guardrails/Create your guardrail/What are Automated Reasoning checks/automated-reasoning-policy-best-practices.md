

# Automated Reasoning policy best practices
<a name="automated-reasoning-policy-best-practices"></a>

This page consolidates best practices for creating and maintaining Automated Reasoning policies. Read this before creating your first policy and refer back to it when debugging issues. For the conceptual foundations behind these practices, see [Automated Reasoning checks concepts](automated-reasoning-checks-concepts.md). For step-by-step creation instructions, see [Create your Automated Reasoning policy](create-automated-reasoning-policy.md).

## Start simple and iterate
<a name="bp-start-simple"></a>

The most common mistake when creating an Automated Reasoning policy is trying to capture an entire complex document in a single pass. Instead, start with a focused subset of your rules and build incrementally.

1. Pick a single, well-defined section of your source document (for example, parental leave eligibility from an HR handbook).

1. Create a policy from that section and review the extracted rules and variables.

1. Write tests that cover the key scenarios for that section.

1. Fix any issues before adding more content.

1. Use iterative policy building to merge additional sections one at a time. For more information, see [Iterative policy building](create-automated-reasoning-policy.md#iterative-policy-building).

This approach has two advantages: it makes issues easier to isolate (you know which section introduced a problem), and it keeps the policy manageable during development. A policy with 10 well-tested rules is more useful than one with 100 untested rules.

## Pre-process documents with an LLM
<a name="bp-preprocess-with-llm"></a>

For documents that are lengthy, contain narrative prose, or mix rules with non-rule content (such as legal disclaimers or organizational background), run the document through an LLM before uploading it to Automated Reasoning checks. Ask the LLM to extract the content as explicit if-then rules. This preprocessing step significantly improves the quality of the extracted policy because Automated Reasoning checks works best with clear, declarative statements rather than unstructured text.

When writing your preprocessing prompt, include the following instructions for the LLM:
+ Extract rules in if-then format with clear conditions and consequences.
+ Preserve all conditions, logical operators (AND, OR, NOT), quantifiers ("at least", "at most"), and exception clauses ("unless", "except when").
+ Add sanity rules for common-sense constraints — such as "account balance cannot be negative" or "credit score must be between 300 and 850" — which translate into boundary rules in your policy (see [Validate ranges for numerical values](#bp-validate-ranges)).

**Important**  
Always review the LLM's output against your original document before using it as source text. LLMs can hallucinate rules not present in the source, misinterpret conditions, or drop important exceptions. The preprocessing step is a starting point — not a substitute for human review.

For detailed prompt templates and a step-by-step preprocessing workflow, see [(Optional) Use an LLM to rewrite documents as logical rules](create-automated-reasoning-policy.md#preprocess-with-llm).

## Use implications (=>) to structure rules
<a name="bp-use-implications"></a>

The if-then format (using the `=>` implication operator) is the single most important rule-writing pattern. Every rule that expresses a conditional relationship should use this format.


| Good: Implication | Bad: Bare assertion | 
| --- | --- | 
| (=> (and isFullTime (> tenureMonths 12)) eligibleForParentalLeave) | eligibleForParentalLeave | 
| (=> (> loanAmount 500000) requiresCosigner) | requiresCosigner | 

Bare assertions (rules without an if-then structure) create axioms — statements that are always true. The assertion `eligibleForParentalLeave` tells Automated Reasoning checks that parental leave eligibility is always true, regardless of any conditions. Any input that says the user is *not* eligible would return `IMPOSSIBLE` because it contradicts this axiom.

Bare assertions are appropriate only for boundary conditions that should always hold, such as:

```
;; Account balance can never be negative
(>= accountBalance 0)

;; Interest rate is always between 0 and 1
(and (>= interestRate 0) (<= interestRate 1))
```

If you find bare assertions in your extracted policy, rewrite them as conditionals or delete them. For more information on reviewing your extracted policy, see [Review the extracted policy](create-automated-reasoning-policy.md#review-extracted-policy).

## Write comprehensive variable descriptions
<a name="bp-variable-descriptions"></a>

Variable descriptions are the primary factor in translation accuracy. When Automated Reasoning checks translate natural language into formal logic, it uses variable descriptions to determine which variables correspond to concepts mentioned in the text. Vague or incomplete descriptions are the number one cause of `TRANSLATION_AMBIGUOUS` results.

A good variable description should answer four questions:

1. **What does this variable represent?** Explain the concept in plain language.

1. **What unit or format does it use?** Specify units (months, dollars, percentage as decimal) and any conversion rules.

1. **How might users refer to this concept?** Include synonyms, alternative phrasings, and common ways users express this concept in everyday language.

1. **What are the boundary conditions?** Describe edge cases, default values, and what the variable means when set to specific values.

**Example: Before and after**


| Vague (causes translation failures) | Detailed (translates reliably) | 
| --- | --- | 
| tenureMonths: "How long the employee has worked." | tenureMonths: "The number of complete months the employee has been continuously employed. When users mention years of service, convert to months (for example, 2 years = 24 months). Set to 0 for new hires who have not yet completed their first month." | 
| isFullTime: "Full-time status." | isFullTime: "Whether the employee works full-time (true) or part-time (false). Set to true when users mention being 'full-time', working 'full hours', or working 40\+ hours per week. Set to false when users mention being 'part-time', working 'reduced hours', or working fewer than 40 hours per week." | 
| interestRate: "The interest rate." | interestRate: "The annual interest rate expressed as a decimal value, where 0.05 means 5% and 0.15 means 15%. When users mention a percentage like '5%', convert to the decimal form (0.05)." | 

## Use booleans for non-exclusive states
<a name="bp-booleans-non-exclusive"></a>

When modeling states that can co-exist, use separate boolean variables instead of a single enum. A person can be both a veteran and a teacher. Using an enum `customerType = {VETERAN, TEACHER}` forces a choice between them, creating a logical contradiction when both apply.


| Good: Separate booleans | Bad: Enum for non-exclusive states | 
| --- | --- | 
| `isVeteran` (BOOL): "Whether the customer is a military veteran."<br />`isTeacher` (BOOL): "Whether the customer is a teacher." | `customerType` (enum: VETERAN, TEACHER, STUDENT): "The type of customer."<br />Problem: A customer who is both a veteran and a teacher cannot be represented. | 

Reserve enums for truly mutually exclusive categories where only one value can apply at a time, such as `leaveType = {PARENTAL, MEDICAL, BEREAVEMENT}` (an employee can only request one type of leave at a time). For more information on custom types, see [Custom types (enums)](automated-reasoning-checks-concepts.md#ar-concept-custom-types).

## Specify units and formats in variable descriptions
<a name="bp-units-formats"></a>

Ambiguity about units is a common source of translation errors. If a user says "I've worked here for 2 years" and your variable is `tenureMonths`, the translation needs to know to convert years to months. If your variable description doesn't specify the unit, the translation may assign `tenureMonths = 2` instead of `tenureMonths = 24`.

Always specify:
+ The unit of measurement (months, days, dollars, percentage).
+ The format (decimal vs. percentage, date format, currency).
+ Conversion rules for common alternative expressions (for example, "2 years = 24 months").

**Examples:**
+ `loanAmount`: "The total loan amount in US dollars. When users mention amounts in thousands (for example, '500K'), convert to the full number (500000)."
+ `submissionDate`: "The number of days after the due date that the submission was made. A value of 0 means the submission was on time. Positive values indicate late submissions."

## Validate ranges for numerical values
<a name="bp-validate-ranges"></a>

For numerical variables, add boundary rules that constrain the valid range. This prevents logically impossible scenarios and helps Automated Reasoning checks produce more meaningful results.

```
;; Account balance cannot be negative
(>= accountBalance 0)

;; Interest rate must be between 0 and 1 (0% to 100%)
(and (>= interestRate 0) (<= interestRate 1))

;; Credit score ranges from 300 to 850
(and (>= creditScore 300) (<= creditScore 850))

;; Tenure in months cannot be negative
(>= tenureMonths 0)
```

Without these boundary rules, Automated Reasoning checks might consider scenarios with negative account balances or credit scores above 1000, which are meaningless in your domain. Boundary rules are one of the few cases where bare assertions (rules not in if-then format) are appropriate.

## Use intermediate variables for abstraction
<a name="bp-intermediate-variables"></a>

When multiple rules share a common condition, extract that condition into an intermediate boolean variable. This simplifies your rules and makes the policy easier to maintain.

**Example: Membership tiers**

Instead of repeating the membership condition in every benefit rule:

```
;; Without intermediate variable (repetitive)
(=> (and (> purchaseTotal 1000) (> accountAge 12)) eligibleForFreeShipping)
(=> (and (> purchaseTotal 1000) (> accountAge 12)) eligibleForPrioritySupport)
(=> (and (> purchaseTotal 1000) (> accountAge 12)) eligibleForEarlyAccess)
```

Define an intermediate variable and reference it:

```
;; With intermediate variable (cleaner)
(=> (and (> purchaseTotal 1000) (> accountAge 12)) isPremiumMember)
(=> isPremiumMember eligibleForFreeShipping)
(=> isPremiumMember eligibleForPrioritySupport)
(=> isPremiumMember eligibleForEarlyAccess)
```

This pattern makes it easier to update the membership criteria later — you only need to change one rule instead of three.

## Use enums for categorization
<a name="bp-enums-categorization"></a>

When a variable represents a category with a fixed set of mutually exclusive values, use a custom type (enum) instead of multiple booleans or a string. Enums constrain the possible values and make rules clearer.


| Good: Enum | Avoid: Multiple booleans for exclusive states | 
| --- | --- | 
| Type: `LeaveType = {PARENTAL, MEDICAL, BEREAVEMENT, PERSONAL}`<br />Variable: `leaveType` (LeaveType)<br />Rule: `(=> (= leaveType PARENTAL) (>= leaveDays 60))` | `isParentalLeave` (BOOL)<br />`isMedicalLeave` (BOOL)<br />`isBereavementLeave` (BOOL)<br />Problem: Nothing prevents multiple booleans from being true simultaneously. | 

**Tip**  
Include an `OTHER` or `NONE` value in your enum if it's possible for the input to not match any of the defined categories. This prevents translation issues when the input doesn't fit neatly into one of the defined values.

## Keep logic declarative, not procedural
<a name="bp-declarative-logic"></a>

Automated Reasoning policies describe *what is true*, not *how to compute it*. Avoid writing rules that look like code with sequential steps or precedence logic.


| Good: Declarative | Avoid: Procedural thinking | 
| --- | --- | 
| "If the employee is full-time and has more than 12 months of tenure, then they are eligible for parental leave."<br />This states a fact about the relationship between conditions and outcomes. | "First check if the employee is full-time. If yes, then check tenure. If tenure is greater than 12 months, set eligibility to true."<br />This describes a procedure, not a logical relationship. | 

Similarly, avoid encoding precedence or priority between rules. In formal logic, all rules apply simultaneously. If you need to express that one condition overrides another, encode it explicitly in the rule conditions:

```
;; GOOD: Explicit exception handling
;; General rule: full-time employees with 12+ months get parental leave
(=> (and isFullTime (> tenureMonths 12) (not isOnProbation))
    eligibleForParentalLeave)

;; BAD: Trying to encode precedence
;; "Rule 1 takes priority over Rule 2" — this concept doesn't exist
;; in formal logic. Instead, combine the conditions into a single rule.
```

## Naming conventions
<a name="bp-naming-conventions"></a>

Consistent naming makes policies easier to read, maintain, and debug. Follow these conventions:
+ **Boolean variables:** Use the `is` or `has` prefix. For example: `isFullTime`, `hasDirectDeposit`, `isEligibleForLeave`.
+ **Numerical variables:** Include the unit in the name. For example: `tenureMonths`, `loanAmountUSD`, `creditScore`.
+ **Enum types:** Use PascalCase for type names and UPPER\_SNAKE\_CASE for values. For example: `LeaveType = {PARENTAL, MEDICAL, BEREAVEMENT}`.
+ **Variables:** Use camelCase. For example: `tenureMonths`, `isFullTime`, `leaveType`.

Avoid abbreviations that might be ambiguous. Use `tenureMonths` instead of `tenMo`, and `isFullTime` instead of `ft`. Clear names help both human reviewers and the translation process.

## Common anti-patterns
<a name="bp-anti-patterns"></a>

The following patterns frequently cause issues in Automated Reasoning policies. If you encounter unexpected test results, check whether your policy contains any of these anti-patterns.

### Axioms instead of implications
<a name="bp-anti-axioms"></a>

As described in [Use implications (=>) to structure rules](#bp-use-implications), bare assertions create axioms that are always true. This is the most common anti-pattern and the most damaging — it makes entire categories of inputs return `IMPOSSIBLE`.

**Symptom:** Tests that should return `VALID` or `INVALID` return `IMPOSSIBLE` instead.

**Fix:** Find bare assertions in your rules and rewrite them as implications, or delete them if they don't represent boundary conditions.

### Overlapping variables
<a name="bp-anti-overlapping-variables"></a>

Having two variables that represent the same or similar concepts (for example, `tenureMonths` and `monthsOfService`) confuses the translation process. Automated Reasoning checks can't determine which variable to use for a given concept, leading to inconsistent translations and `TRANSLATION_AMBIGUOUS` results.

**Symptom:** Tests return `TRANSLATION_AMBIGUOUS` even with clear, unambiguous input text.

**Fix:** Merge overlapping variables into a single variable with a comprehensive description. Update all rules that reference the deleted variable.

### Overly complex policies
<a name="bp-anti-overly-complex"></a>

Policies with too many variables, deeply nested conditions, or non-linear arithmetic can exceed processing limits and return `TOO_COMPLEX` results.

**Symptom:** Tests return `TOO_COMPLEX` or time out.

**Fix:** Simplify the policy. Remove unused variables, break complex rules into simpler ones using intermediate variables, and avoid non-linear arithmetic (exponents, irrational numbers). If your domain is genuinely complex, consider splitting it into multiple focused policies.

### Contradictory rules
<a name="bp-anti-contradictory-rules"></a>

Rules that contradict each other make it impossible for Automated Reasoning checks to reach a conclusion. For example, one rule says full-time employees are eligible for leave, while another says employees in their first year are not eligible — without specifying what happens to full-time employees in their first year.

**Symptom:** Tests return `IMPOSSIBLE` for inputs that involve the conflicting rules.

**Fix:** Check the quality report for conflicting rules. Resolve conflicts by merging the rules into a single rule with explicit conditions, or by deleting one of the conflicting rules. For more information, see [Review the extracted policy](create-automated-reasoning-policy.md#review-extracted-policy).

### Unused variables
<a name="bp-anti-unused-variables"></a>

Variables that aren't referenced by any rules add noise to the translation process. The translation may assign values to unused variables, wasting processing capacity and potentially causing `TRANSLATION_AMBIGUOUS` results when the unused variable competes with a similar active variable.

**Symptom:** Unexpected `TRANSLATION_AMBIGUOUS` results, or translations that assign values to variables that don't affect any rules.

**Fix:** Delete unused variables. In the console, look for warning indicators next to variables. Via the API, check the quality report from `GetAutomatedReasoningPolicyBuildWorkflowResultAssets` with `--asset-type QUALITY_REPORT`.

### Missing enum values
<a name="bp-anti-missing-enum-values"></a>

If your enum doesn't include a value for every possible category that users might mention, the translation may fail or produce unexpected results when the input doesn't match any defined value.

**Symptom:** Tests return `TRANSLATION_AMBIGUOUS` or `NO_TRANSLATIONS` when the input mentions a category not in the enum.

**Fix:** Add an `OTHER` or `NONE` value to your enum to handle inputs that don't match the defined categories. Update the enum value descriptions to clarify when each value applies.