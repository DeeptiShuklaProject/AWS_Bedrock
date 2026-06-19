

# Blueprints
<a name="bda-blueprint-info"></a>

Blueprints are artifacts that you can use to configure your file processing business logic. Each blueprint consists of a list of field names that you can extract, the data format in which you want the response for the field to be extracted—such as string, number, or boolean—as well as natural language context for each field that you can use to specify data normalization and validation rules. You can create a blueprint for each class of file that you want to process, such as a W2, pay stub or ID card. Blueprints can be created using the console or the API. Each blueprint that you create is an AWS resource with its own blueprint ID and ARN.

When using a blueprint for extraction, you can use a catalog blueprint or a custom created blueprint. If you already know the kind of file you're looking to extract from, catalog bluprints provide a premade starting place. You can create custom blueprints for files that aren't in the catalog. When creating a blueprint you can use several methods, such as a generated blueprint via the blueprint prompt, manual creation by adding individual fields, or creating the JSON of a blueprint using the JSON Editor. These can be saved to your account and shared.

**Note**  
Audio blueprints cannot be created via Blueprint Prompts.

A blueprint's maximum size is 100,000 characters, JSON formatted. For blueprints that are intended to be used with the [InvokeDataAutomationAsync](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_data-automation-runtime_InvokeDataAutomationAsync.html) API the maximum fields per blueprint is 100. For Blueprints that are intended to be used with the [InvokeDataAutomation](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_data-automation-runtime_InvokeDataAutomation.html) API the maximum fields per blueprint is 15.

**Note**  
When using Blueprints you might find yourself using Prompts, either in fields or for Blueprint creation. Only allow trusted sources to control the prompt input. Amazon Bedrock is not responsible for validating the intent of the blueprint.

## Blueprint walkthrough
<a name="bda-blueprint-walkthrough"></a>

Lets take an example of an ID document such as a passport and walk through a blueprint for this document.

![Sample passport with standard fields, demonstrating layout and data fields that will be extracted.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/bda/passport2.png)


Here is an example blueprint for this ID document that we created on the console.

![Table layout of passport field definitions, with various categories, showing an example blueprint.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/bda/bdapassport.png)


At its core, a blueprint is a data structure that contains fields, which in turn contain the information extracted by BDA custom output. There are two types of fields—explicit and implicit—located in the extraction table. Explicit extractions are used for clearly stated information that can be seen in the document. Implicit extractions are used for information that need to be transformed from how they appear in the document. For example, you can remove the dashes from a social security number, converting from 111-22-3333 to 111223333. Fields contain certain basic components:
+ Field name: This is a name you can provide for each field that you want to extract from the document. You can use the name that you use for the field in your downstream system such as `Place_Birth` or `Place_of_birth`. Field names cannot contain forward slashes (`/`); use underscores or alphanumeric characters instead.
+ Description: This is an input that provides natural language context for each field in the blueprint to describe data normalization or validation rules to be followed. For example, `Date of birth in YYYY-MM-DD format` or `Is the year of birth before 1992?`. You can also use the prompt as a way to iterate on the blueprint and improve the accuracy of BDA’s response. Providing a detailed prompt that describes the field you need helps the underlying models to improve their accuracy. Prompts may be up to 300 characters long.
+ Results: The information extracted by BDA based on the prompt and field name.
+ Type: The data format that you want the response for the field to use. We support string, number, boolean, array of string, and array of numbers.
+ Confidence score: The percentage of certainty that BDA has that your extraction is accurate. Audio and Image blueprints do not return a confidence score.
+ Extraction Types: The type of extraction, either explict or inferred.
+ Page Number: Which page of the document that the result was found on. Audio and Video blueprints do not return a page number.

In addition to simple fields, BDA custom output offers several options for use cases that you might encounter in document extraction: table fields, groups, and custom types. 

**Table Fields**  
When creating a field, you can choose to create a table field instead of a basic field. You can name the field and provide a prompt, as with other fields. You can also provide column fields. These fields have a column name, column description, and column type. When shown in the extraction table, a table field has the column results grouped beneath the table name. Table fields can only have up to 15 subfields.

**Groups**  
A group is a structure that's used to organize several results into a single location within your extraction. When you create a group, you give the group a name and you can create and place fields into that group. This group is marked in your extractions table, and lists below it the fields that are within the group. 

**Custom types**  
You can create a custom type while editing a blueprint in the Blueprint Playground. Any field can be a custom type. This type has a unique name, and prompts the creation of the fields that make up the detection. An example would be creating a custom type called Address, and including in it the fields “zip\_code”, “city\_name”, “street\_name”, and “state”. Then, while processing a document, you could use the custom type in a field “company\_address”. That field then returns all of the information, grouped in rows beneath the custom type. You can have up to 30 custom type fields per blueprint.