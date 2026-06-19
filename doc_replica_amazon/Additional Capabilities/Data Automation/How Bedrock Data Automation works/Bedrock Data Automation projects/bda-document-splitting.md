

# Splitting documents while using projects
<a name="bda-document-splitting"></a>

Amazon Bedrock Data Automation (BDA) supports splitting documents when using the Amazon Bedrock API. When enabled, splitting allows BDA to take a PDF containing multiple logical documents and split it into separate documents for processing. 

Once splitting is complete, each segment of the split document is processed independently. This means an input document can contain different document types. For example, if you have a PDF containing 3 bank statements and one W2, splitting would attempt to divide it into 4 separate documents that would be processed individually.

BDA automatic splitting supports files with up to 3000 pages, and supports individual documents of up to 20 pages each.

The option to split documents is off by default, but can be toggled on when using the API. Below is an example of creating a project with the splitter enabled. The ellipsies represent additional blueprints provided to the project.

```
   response = client.create_data_automation_project(
    projectName={{project_name}},
    projectDescription="{{Provide a project description}}",
    projectStage='LIVE',
    standardOutputConfiguration=output_config,
    customOutputConfiguration={
    'blueprints': [
        {
        'blueprintArn': {{Blueprint ARN}},
        'blueprintStage': 'LIVE'
        },
        ...
        ]
        },
         overrideConfiguration={'document': {'splitter': {'state': 'ENABLED'}}}
)
```

The part that enables the splitting process is the overrideConfiguration line. This line sets up the splitter and allows you to pass multiple documents within the same file.

Documents are split by the semantic boundaries in the document. 

Document splitting happens independently of applying blueprints, and documents that are split will be matched to the closest blueprint. For more information on how BDA matches blueprints see [Understanding blueprint matching](#bda-blueprint-matching).

## Understanding blueprint matching
<a name="bda-blueprint-matching"></a>

Blueprint matching is based on the following elements:
+  Blueprint name 
+  Blueprint description 
+  Blueprint fields 

When processing documents, you can provide multiple blueprints to match against. This allows processing different document types with appropriate blueprints. You can provide multiple blueprint IDs when invoking the data automation API, and BDA will attempt to match each document to the best fitting blueprint. This allows processing mixed document types in a single batch. This is useful when documents are expected to be of different types (e.g. bank statements, invoices, passports).

If you need separate blueprints because document formats are very different or require specialized prompts, creating one blueprint per document type can help with matching. For more information on creating useful blueprints, see [Best practices for creating blueprints](#bda-blueprint-best-practices).

## Best practices for creating blueprints
<a name="bda-blueprint-best-practices"></a>

 Follow the following best practices to get the most out of your blueprints: 
+ Be explicit and detailed in blueprint names and descriptions to aid matching 
+ Providing multiple relevant blueprints allows BDA to select the best match. Create separate blueprints for significantly different document formats 
+ Consider creating specialized blueprints for every vendor/document source, if you need maximum accuracy
+ Do not include two blueprints of the same type in a project (e.g. two W2 blueprints). Information from the document itself and the blueprint is used to process documents, and including multiple blueprints of the same type in a project will lead to worse performance. 

By using document splitting and multiple blueprint matching, BDA can more flexibly handle varied document sets while applying the most appropriate extraction logic to each document.