

# Creating Blueprints for Extraction
<a name="idp-cases-extraction"></a>

BDA allows you to define the specific data fields you want to extract from your documents when creating a blueprint. This acts as a set of instructions that guide BDA on what information to look for and how to interpret it.

**Defining fields**  
To get started, you can create a property for each field that requires extraction, such as employee\_id or product\_name. For each field, you need to provide a description, data type, and inference type.

To define a field for extraction, you need to specify the following parameters:
+ Field Name: Provides a human-readable explanation of what the field represents. This description helps in understanding the context and purpose of the field, aiding in the accurate extraction of data.
+ Instruction: Provides a natural language explanation of what the field represents. This description helps in understanding the context and purpose of the field, aiding in the accurate extraction of data.
+ Type: Specifies the data type of the field's value. BDA supports the following data types:
  + string: For text-based values
  + number: For numerical values
  + boolean: For true/false values
  + array: For fields that can have multiple values of the same type (e.g., an array of strings or an array of numbers)
+ Inference Type: Instructs BDA on how to handle the extraction of the field's value. The supported inference types are:
  + Explicit: BDA should extract the value directly from the document.
  + Inferred: BDA should infer the value based on the information present in the document.

Here's an example of a field definition with all the parameters:

------
#### [ Console ]

![Console showing field configuration with Type set to String and Extraction type set to Explicit.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/bda/bdaadd.png)


------
#### [ API ]

```
"product_name":{
   "type":"string",
   "inferenceType":"Explicit",
   "description":"The short name of the product without any extra details"
}
```

------

In this example:
+ The type is set to string, indicating that the value of the product\_name field should be text-based.
+ The inferenceType is set to Explicit, instructing BDA to extract the value directly from the document without any transformation or validation.
+ The instruction provides additional context, clarifying that the field should contain the short name of the product without any extra details.

By specifying these parameters for each field, you provide BDA with the necessary information to accurately extract and interpret the desired data from your documents.


| Field | Instruction | Extraction Type | Type | 
| --- | --- | --- | --- | 
| ApplicantsName | Full Name of the Applicant | Explicit | string | 
| DateOfBirth | Date of birth of employee | Explicit | string | 
| Sales | Gross receipts or sales | Explicit | number | 
| Statement\_starting\_balance | Balance at beginning of period | Explicit | number | 

**Multi-Valued Fields**  
In cases where a field may contain multiple values, you can define arrays or tables.

**List of Fields**  
For fields that contain a list of values, you can define an array data type. 

In this example, "OtherExpenses" is defined as an array of strings, allowing BDA to extract multiple expense items for that field.

------
#### [ Console ]

![Console showing field configuration with Type set to Array of String and Extraction type set to Explicit.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/bda/bdaarray.png)


------
#### [ API ]

```
"OtherExpenses":{
   "type":"array",
   "inferenceType":"Explicit",
   "description":"Other business expenses not included in fields 8-26 or field 30",
   "items":{
      "type":"string"
   }
}
```

------

**Tables**  
If your document contains tabular data, you can define a table structure within the schema.

In this example, "SERVICES\_TABLE" is defined as a Table type, with column fields such as product name, description, quantity, unit price and amount.

------
#### [ Console ]

![Console showing field configuration with Type set to Table, Extraction type set to Explicit, and column-specific fields.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/bda/bdatable.png)


------
#### [ API ]

```
"definitions":{
   "LINEITEM":{
      "properties":{
         "quantity":{
            "type":"number",
            "inferenceType":"Explicit"
         },
         "unit price":{
            "type":"number",
            "inferenceType":"Explicit"
         },
         "amount":{
            "type":"number",
            "inferenceType":"Explicit",
            "description":"Unit Price * Quantity"
         },
         "product name":{
            "type":"string",
            "inferenceType":"Explicit",
            "description":"The short name of the product without any extra details"
         },
         "product description":{
            "type":"string",
            "inferenceType":"Explicit",
            "description":"The full item list description text"
         }
      }
   }
},
"properties":{
   "SERVICES_TABLE":{
      "type":"array",
      "description":"Line items table listing all the items / services charged in the invoice including quantity, price, amount, product / service name and description.",
      "items":{
         "$ref":"#/definitions/LINEITEM"
      }
   },
   "...
        ..."
]
```

------

By defining comprehensive schemas with appropriate field descriptions, data types, and inference types, you can ensure that BDA accurately extracts the desired information from your documents, regardless of variations in formatting or representation.