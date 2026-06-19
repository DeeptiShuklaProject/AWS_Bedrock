

# Custom output and blueprints
<a name="bda-custom-output-idp"></a>

When using Amazon Bedrock Data Automation (BDA) you can further fine tune your extractions using custom output configuration. Custom outputs are configured with artifacts called blueprints. Blueprints are a list of instructions for how to extract information from your file, allowing for transformation and adjustment of output. For more information and a detailed walkthrough of a blueprint, see [Blueprints](bda-blueprint-info.md).

Custom output configuration also works alongside projects. When you pass a file to a BDA and reference a project with configured blueprint(s), BDA will process the file using the appropriate blueprint. This works for up to 40 document blueprints, one image blueprint, one audio blueprint, and/or one video blueprint. When working with multiple blueprints, BDA attempts to send documents to the blueprint that best matches the expected layout. For more information about projects and custom output, see [Bedrock Data Automation projects](bda-projects.md).

**Note**  
All files processed by custom output must follow the file restrictions for BDA. For more information on file restrictions see BDA Prerequisites.