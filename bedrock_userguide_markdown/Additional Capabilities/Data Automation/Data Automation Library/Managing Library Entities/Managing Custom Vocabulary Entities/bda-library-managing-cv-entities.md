

# Managing Custom Vocabulary Entities
<a name="bda-library-managing-cv-entities"></a>

This section describes how to add, update, delete, and view custom vocabulary entities/lists within your Data Automation Libraries. Custom vocabulary entities contain domain-specific terms and phrases that improve extraction accuracy for audio and video content in your target languages.

You can manage vocabulary entities through asynchronous ingestion jobs using the AWS Management Console or AWS CLI. Operations include adding new vocabulary using S3 manifest files or inline payloads, monitoring job status and reviewing outputs, updating entities with UPSERT operations (which replace the entire entity), deleting specific entities, and viewing entity lists or detailed phrase information. All modifications are processed through the InvokeDataAutomationLibraryIngestionJob API with different operation types (UPSERT or DELETE).