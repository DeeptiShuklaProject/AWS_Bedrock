

# Standard output in Bedrock Data Automation
<a name="bda-standard-output"></a>

Standard output is the default way of interacting with Amazon Bedrock Data Automation (BDA). If you pass a document to the BDA API with no established blueprint or project it returns the default standard output for that file type. Standard output can be modified using projects, which store configuration information for each data type. You can have one standard output configuration per data type for each project. BDA always provides a standard output response even if it's alongside a custom output response.

Each data type has different standard output options. Some of these options are part of the default Bedrock Data Automation response, while some exist only as toggles for working with the data type in a project. The following sections go over each data type's unique response options, noting which are defaults and which are optional.