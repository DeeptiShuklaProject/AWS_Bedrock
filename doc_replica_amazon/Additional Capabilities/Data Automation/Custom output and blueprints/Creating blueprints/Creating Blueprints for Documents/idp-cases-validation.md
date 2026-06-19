

# Create Blueprints for Validation
<a name="idp-cases-validation"></a>

BDA allows you to define validation rules to ensure the accuracy of the extracted data. These validation rules can be incorporated into your blueprints, enabling BDA to perform various checks on the extracted data. BDA allows you to create custom validations tailored to your specific business or industry requirements. Below are some examples of validations to illustrate the range of this capability.

**Numeric validations**  
Numeric validations are used to check whether the extracted numeric data falls within a specified range of values or meets certain criteria. These validations can be applied to fields such as amounts, quantities, or any other numerical data.


| Field | Instruction | Extraction Type | Type | 
| --- | --- | --- | --- | 
| BalanceGreaterCheck | Is previous balance greater than $1000? | Inferred | Boolean | 
| Is Gross Profit equal to difference between Sales and COGS? | Validation question | Inferred | Boolean | 
| is\_gross\_pay\_valid | Is the YTD gross pay the largest dollar amount value on the paystub? | Inferred | Boolean | 

**Date/Time validations**  
Date/time validations are used to check whether the extracted date or time data falls within a specific range or meets certain criteria. These validations can be applied to fields such as due dates, expiration dates, or any other date/time-related data.


| Field | Instruction | Extraction Type | Type | 
| --- | --- | --- | --- | 
| was\_injury\_reported\_after\_1\_month | Was the injury reported to the employer more than 1 month after the injury date? | Inferred | Boolean | 
| is\_overdue | Is the statement overdue? Has the balance due date expired? | Inferred | Boolean | 
| is\_delivery\_date\_valid | Is the delivery date within the next 30 days? | Inferred | Boolean | 

**String/Format validations**  
String/format validations are used to check whether the extracted data adheres to a specific format or matches predefined patterns. These validations can be applied to fields such as names, addresses, or any other textual data that requires format validation.


| Field | Instruction | Extraction Type | Type | 
| --- | --- | --- | --- | 
| routing\_number\_valid | True if the bank routing number has 9 digits | Inferred | Boolean | 
| Is\_NumMeterIDsListed | Are there more than 5 meter IDs listed on the bill? | Inferred | Boolean | 

With BDA's custom validation capabilities, you can create complex validation rules that combine multiple conditions, calculations, or logical operations to ensure the extracted data meets your desired criteria. These validations can involve cross-field checks, calculations, or any other custom logic specific to your business processes or regulatory requirements.

By incorporating these validation rules into your blueprints, BDA can automatically validate the extracted data, ensuring its accuracy and compliance with your specific requirements. This capability enables you to make trigger human reviews where validations have failed.