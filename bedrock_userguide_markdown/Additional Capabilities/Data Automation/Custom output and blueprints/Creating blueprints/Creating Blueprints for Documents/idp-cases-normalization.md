

# Create Blueprints for Normalization
<a name="idp-cases-normalization"></a>

BDA provides normalization capabilities that allow you to convert and standardize the extracted data according to your specific requirements. These normalization tasks can be categorized into Key Normalization and Value Normalization.

**Key normalization**  
In many cases, document fields can have variations in how they are represented or labeled. For example, the "Social Security Number" field could appear as "SSN," "Tax ID," "TIN," or other similar variations. To address this challenge, BDA offers Key Normalization, which enables you to provide instructions on the variations within your field definitions.

By using key normalization, you can guide BDA to recognize and map different representations of the same field to a standardized key. This feature ensures that data is consistently extracted and organized, regardless of the variations present in the source documents.


| Field | Instruction | Extraction Type | Type | 
| --- | --- | --- | --- | 
| LastName | Last name or Surname of person | Explicit | String | 
| BirthNum | Document Number or file number of the birth certificate | Explicit | String | 
| OtherIncome | Other income, including federal and state gasoline or fuel tax credit or refund | Explicit | Number | 
| BusinessName | Name of the business, contractor or entity filling the W9 | Explicit | String | 
| power factor | Power factor or multiplier used for this usage line item | Explicit | String | 
| BirthPlace | Name of Hospital or institution where the child is born | Explicit | String | 
| Cause of Injury | Cause of injury or occupational disease, including how it is work related | Explicit | String | 

For fields with predefined value sets or enumerations, you can provide the expected values or ranges within the field instruction. We recommend that you include the variations in quotation marks as shown in the examples.


| Field | Instruction | Extraction Type | Type | 
| --- | --- | --- | --- | 
| LICENSE\_CLASS | The single letter class code, one of "A", "B" or "C" | Explicit | String | 
| sex | The sex. One of "M" or "F" | Explicit | String | 
| InformantType | The type of the information. One of "Parent" or "Other" | Explicit | String | 
| INFORMATION COLLECTION CHANNEL | ONE AMONG FOLLOWING: "FACE TO FACE INTERVIEW", "TELEPHONE INTERVIEW", "FAX OR MAIL", "EMAIL OR INTERNET" | Explicit | String | 

**Value normalization**  
Value normalization is a key task in data processing pipelines, where extracted data needs to be transformed into a consistent and standardized format. This process ensures that downstream systems can consume and process the data seamlessly, without encountering compatibility issues or ambiguities.

Using normalization capabilities in BDA, you can standardize formats, convert units of measurement and cast values to specific data types.

For Value Normalization tasks, the Inferred extraction type should be used as the value may not exactly match the raw text or OCR of the document after it is normalized. For example, a date value like "06/25/2022" that requires to be formatted to "YYYY-MM-DD" will be extracted as "2022-06-25" after normalization, thereby not matching the OCR output from the document.

Standardize Formats: You can convert values to predefined formats, such as shortened codes, numbering schemes, or specific date formats. This allows you to ensure consistency in data representation by adhering to industry standards or organizational conventions.


| Field | Instruction | Extraction Type | Type | 
| --- | --- | --- | --- | 
| ssn | The SSN, formatted as XXX-XX-XXX | Inferred | String | 
| STATE | The two letter code of the state | Inferred | String | 
| EXPIRATION\_DATE | The date of expiry in YYYY-MM-DD format | Inferred | String | 
| DATE\_OF\_BIRTH | The date of birth of the driver in YYYY-MM-DD format | Inferred | String | 
| CHECK\_DATE | The date the check has been signed. Reformat to YYYY-MM-DD | Inferred | String | 
| PurchaseDate | Purchase date of vehicle in mm/dd/yy format | Inferred | String | 

You can also convert values to a standard unit of measurement or to a specific data type by handling scenarios like Not applicable.


| Field | Instruction | Extraction Type | Type | 
| --- | --- | --- | --- | 
| WEIGHT | Weight converted to pounds | Inferred | Number | 
| HEIGHT | Height converted to inches | Inferred | Number | 
| nonqualified\_plans\_income | The value in field 11. 0 if N/A. | Inferred | Number | 