

# Create Blueprints for Transformation
<a name="idp-cases-transformation"></a>

BDA allow you to split, and restructure data fields according to your specific requirements. This capability enables you to transform the extracted data into a format that better aligns with your downstream systems or analytical needs. 

In many cases, documents may contain fields that combine multiple pieces of information into a single field. BDA enables you to split these fields into separate, individual fields for easier data manipulation and analysis. For example, if a document contains a person's name as a single field, you can split it into separate fields for first name, middle name, last name, and suffix.

For Transformation tasks, the extraction type can be defined as Explicit or Inferred, depending on if the value requires to be normalized. 


| Field | Instruction | Extraction Type | Type | 
| --- | --- | --- | --- | 
| FIRST\_NAME | The first name | Explicit | String | 
| MIDDLE\_NAME | The middle name or initial | Explicit | String | 
| LAST\_NAME | The last name of the driver | Explicit | String | 
| SUFFIX | The suffix, such as PhD, MSc. etc | Explicit | String | 

Another example is with address blocks that could appear as a single field


| Field | Instruction | Extraction Type | Type | 
| --- | --- | --- | --- | 
| Street | What is the street address | Explicit | String | 
| City | What is the city | Explicit | String | 
| State | What is the state? | Explicit | String | 
| ZipCode | What is the address zip code? | Explicit | String | 

You can define these fields as completely individual fields, or create a Custom Type. Custom Types are re that you can reuse for different fields. In the example below, we create a custom type “NameInfo” that we use for “EmployeeName” and “ManagerName”.

![Console showing how to add custom type details. It also shows the sub-properties added to the custom type.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/bda/bdacustomtype.png)
