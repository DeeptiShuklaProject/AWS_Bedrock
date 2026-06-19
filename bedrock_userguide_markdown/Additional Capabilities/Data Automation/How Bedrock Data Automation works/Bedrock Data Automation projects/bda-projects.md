

# Bedrock Data Automation projects
<a name="bda-projects"></a>

One way to process files using Amazon Bedrock data automation (BDA) is to create a project. A project is a grouping of both standard and custom output configurations. Standard outputs are required in projects, but custom outputs are optional. When you call the `InvokeDataAutomationAsync` API with a project ARN, the file is automatically processed using the configuration settings defined in that project. Output is then generated based on the project's configuration.

A project can be given a stage, either `LIVE` or `DEVELOPMENT`. Each stage is a unique and mutable version of the project. This means you can edit or test with the `DEVELOPMENT` stage, and process customer requests using the `LIVE` stage. `DEVELOPMENT` projects can't be accessed in the console, and must be changed and invoked through the API.

A project allows you to use a single resource for multiple file types. For example, an audio file sent to BDA using project name ABC will be processed using project ABC’s audio standard output configuration. A document sent to BDA using project name ABC will be processed using project ABC’s document standard output configuration.

Projects grant you greater flexibility when setting up standard outputs. Each standard output has its own set of configurable options, such as transcripts or summaries, and projects allow you to change those options to better suit your use case. You can also configure a project with Blueprints for documents, audio, and images to define custom output. A project configured to generate custom output will also generate standard output automatically.

The following sections will go through a few examples of using projects.

## Using Projects with Standard Output
<a name="bda-standard-example"></a>

Let's consider a use case in which you're only interested in extracting transcript summaries of your full audio and video files. By default, when you send audio and video files to BDA, you receive the transcript summaries along with full transcripts, scene level summaries, detected text, and other information. For this use case, you don't want to spend the extra time and resources to collect information you don't need. For this use case, you can configure a standard output project to enable only the summary feature for audio and video files.

To do this using the API or the console, create a project and modify the standard output settings for audio and video. For video, enable **Full Video Summary** but ensure that other extractions (e.g., Full Audio Transcript, Scene Summaries, Content Moderation, etc.) are disabled. Repeat this configuration for audio. After you configure the project to generate only summaries, save the project and note the project's Amazon Resource Names (ARN). This ARN can be used for the `InvokeDataAutomationAsync` operation to process your files at scale. By passing an audio or video file to the BDA and specifying this project ARN, you will receive an output of only the summaries for each of the files. Note, in this example there was no configuration performed for documents or images. This means that if you pass an image or document to BDA using that project ARN, you will receive the default standard output for those files.

## Using projects with custom output and standard output
<a name="bda-mixed-example"></a>

For this use case, let's assume that you want to generate standard output summaries for documents and audio files, and to also extract custom fields from your documents. After you create a project, configure the standard output for audio to enable **Full audio summary** and ensure that other extractions are not enabled. Repeat this standard output configuration for documents. You can then configure custom output for documents by adding a new blueprint or a preexisting blueprint from the BDA global catalog. Documents passed to BDA using this project ARN will generate the standard output full document summaries and the blueprint output for defined custom fields. Audio files passed to BDA using this project ARN will generate full summaries.

When processing documents, you might want to use multiple blueprints for different kinds of documents that are passed to your project. A project can have up to 40 document blueprints attached. BDA automatically matches your documents to the appropriate blueprint that's configured in your project, and generates custom output using that blueprint. Additionally, you might want to pass documents in bulk. If you pass a file that contains multiple documents, you can choose to split the document when creating your project. If you choose to do this, BDA scans the file and splits it into individual documents based on context. Those individual documents are then matched to the correct blueprint for processing.

Currently, images only support a single blueprint definition per project. Image file types JPG and PNG might be treated as images or as scanned documents based on their contents. We recommend that you create a custom blueprint for images when you process custom output for documents so BDA provides the desired output for image files that contain text.

Audio files also only support a single blueprint definition per project.