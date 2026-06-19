

# Using the Bedrock Data Automation Console
<a name="bda-blueprints-console"></a>

In Amazon Bedrock Data Automation (BDA), two major artifacts are used when processing information. Projects, which store output configurations, and Blueprints which let you customize the output format and extraction logic for your unstructured content. 

This section will discuss creating Projects and Blueprints in the BDA Console. For more information on how projects work in within BDA, see [Bedrock Data Automation projects](bda-projects.md). To learn more about Blueprints in BDA, see [How to create blueprints for custom outputs](bda-idp.md#how-to-create-blueprints).

## Projects in the BDA Console
<a name="projects-in-bda-console"></a>

In the BDA Console, you can create and manage projects. Projects allow you to control which standard outputs are retrieved when running an inference operation, and control how custom outputs are handled during inference.

Create a project by:

1. Navigate to the Amazon Bedrock service. From there, select "Data Automation" from the sidebar menu.

1. Select "Create project".

1. Give the project a name and then select "Create project" again.

1. This will take you to the Project Details page where you can see which standard outputs are enabled by your project. You can then control custom outputs by selecting the "Custom output" tab and then selecting the "Create blueprint" option. Additionally, you can add an existing Blueprint to the Project.

## Creating Blueprints in the BDA Console
<a name="accessing-bda-console"></a>

Alternatively, you can select "Data Automation" from the sidebar menu and navigate directly to Custom output setup. In the BDA dashboard, locate and choose the "Custom output setup" tab. This will take you to the Blueprints management page.

## Initiating Blueprint Creation
<a name="initiating-blueprint-creation"></a>

1. Choose the "Create Blueprint" button to start the process of creating a new Blueprint.

1. Select either "Upload from computer" or "Import from S3", and provide a file that's representative of the files you want to process.

1. Enter a Blueprint prompt for blueprint generation. When entering a prompt, you can specify any fields you would expect to find in your uploaded document. You can also specify data normalizations or validations.

1. Select "Generate blueprint".

1. Give the blueprint a name and choose "Create blueprint".

1. In the Custom blueprints section you can select the "Create blueprint" button.

1. Your blueprint will be created, and you will be able to see the extractions that have been identified based on your provided prompt.

## Previewing the Blueprint
<a name="previewing-the-blueprint"></a>

Use the preview feature to test your Blueprint with sample data. This allows you to verify that the extraction and formatting are working as expected.

Select "save and exit blueprint prompt" to save your blueprint as a resource.

## Managing Blueprints
<a name="managing-blueprints"></a>

After creation, you can manage your Blueprints from the Blueprints dashboard. Options include:
+ Editing existing Blueprints
+ Duplicating Blueprints
+ Deleting Blueprints
+ Viewing Blueprint version history

You can also add a blueprint to a project by selecting the "Add to project" dropdown menu and selecting a project you have created.

## Using Your Blueprint
<a name="using-your-blueprint"></a>

Once created, you can use your Blueprint in BDA projects or directly in API calls to process your unstructured content. To use a Blueprint:
+ When making API calls, include the Blueprint ARN in your request parameters. See the section on calling the API for more info.
+ When making an API call, include the ARN of the Project containing the Blueprint. See the section on calling the API for more info.

## Processing Documents with Console
<a name="processing-documents-with-console"></a>

The BDA Console also allows you to easily test and preview the insights that BDA can extract from your unstructured content. These tests can only be performed one document at a time. To process multiple documents, see using the API. You can upload sample documents, images, videos, or audio files, and the Console will display the default insights that BDA can generate, as well as the option to apply any Custom Blueprints you have created.

You can test a blueprint you have created and applied to a project by going to the Projects section of Data Automation and then selecting a project.

Once you are on the project details page, select "Test". On the Test page you will be able to select a file and choose to process the file with either standard output or a blueprint you have created.