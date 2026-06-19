

# Disabling modalities and routing file types
<a name="bda-routing-enablement"></a>

By default, projects in BDA process supported file types, by sorting them to different semantic modalities. When creating or editing your project, you can modify what modalities will be processed, and which file types will be sent to which modalities. In this section, we will go through enabling and disabling different modalities, routing files to specific modalities, and the default routing procedure for BDA.

## Disabling modality processing
<a name="bda-modality-enablement"></a>

When you create a project, you might have a use case in mind that doesn't include processing all kinds of files. For example, you may want to only process documents and audio files. If that is the case, you don't want BDA to send a JPEG to be processed as an image or an MP4 to be processed as a video. Modality enablement allows you to turn off certain modalities in a project, curating responses from BDA's processing.

**Disabling modalities with the BDA Console**  
When using the BDA console, modality enablement is handled by a checklist, where you can simply select or deselect each modality while editing or creating your Project. These options are located under the Advanced settings tab. At least one Modality must be selected for a project.

![Modality enablement section with checkboxes for Document, Image, Video, and Audio modalities.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/bda/modalityenableconsole.png)


**Disabling modalities with the BDA API**  
When using the BDA API, modality enablement is handled by the `overrideConfiguration` request element, located in the `CreateDataAutomation` operation. Each modality has an associate section where you can declare the modality `ENABLED` or `DISABLED`. Below is an example of the `overrideConfiguration` element with only document and audio modalities enabled. The `modalityProcessing` flag defaults to `ENABLED`.

```
"overrideConfiguration" : {
    "document": {
        "splitter": {
            "state": ENABLED
        },
        "modalityProcessing": {
            "state": ENABLED
        },
    },
    "image": {
        "modalityProcessing": {
            "state": DISABLED
        }
    },
    "video": {
        "modalityProcessing": {
            "state": DISABLED 
        }
    },
    "audio": {
        "modalityProcessing": {
            "state": ENABLED
        }
    },
    ...
}
```

The ellipsies at the end of this section indicates the removal of the `modalityRouting` element, which we will discuss more in the next section.

## Routing files to certain processing types
<a name="bda-modality-routing"></a>

Certain file types are capable of being routed to different modalities, based on a variety of factors. With modality routing you can set certain file types to route to certain modality processing manually. JPEGs and PNGs can be routed to either document or image processing. MP4s and MOVs can be routed to either video or audio processing.

**Routing with the BDA Console**  
While in the Advanced settings tab when creating or editing a blueprint, you can choose to add a new manual modality routing. This lets you select one of the 4 available file types and then which processing modality they will be routed to. Below is a screenshot of the console, with a manual modality routing that sends PNG files to the document processing modality.

**Note**  
Settings for JPEG files apply to both ".jpeg" and ".jpg" files. Settings for MP4 settings apply to both ".mp4" ".m4v" files.

![Console drop-down menus for file type and modality destination, selected as PNG and Document.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/bda/manualrouting.png)


**Routing with the BDA API**  
Similar to modality enablement, modality routing is handled via the `overrideConfiguration` request element. Below is an example of the `modalityRouting` portion of `overrideConfiguration`. This example assumes all modalities are enabled, and routes JPEG and PNG files to the document modality, and MP4 and MOV files to the audio modality.

```
...
   "modalityRouting": {
        "jpeg": DOCUMENT, 
        "png": DOCUMENT,  
        "mp4": AUDIO,     
        "mov": AUDIO      
    }
}
```

The ellipsies at the beginning of the example indicate the removal of the rest of the `overrideConfiguration`, which is discussed more in the section on modality enablement and the document splitter functionality.

## Standard routing for the InvokeDataAutomationAsync API
<a name="bda-standard-routing-async"></a>

Without setting up your own routing procedures, BDA uses a standard set of procedures based on file type to determine what modality BDA will route to. The default procedures are listed in the table below.

PNGs and JPEGs list Semantic Classifer as a default behavior. This means that BDA will look at indicators of whether or not a submitted file is an image or a document using internal models and perform routing automatically.


| File Types | Default Routing Behavior | 
| --- | --- | 
| PNG | Semantic Classifer; Either Image or Document | 
| JPEG | Semantic Classifer; Either Image or Document | 
| PDF, TIFF | Document | 
| MP4, MOV | Video | 
| AMR, FLAC, M4A, MP3, OGG, WEBM, WAV | Audio | 

## Standard routing for the InvokeDataAutomation API
<a name="bda-standard-routing-sync"></a>

The [InvokeDataAutomation](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_data-automation-runtime_InvokeDataAutomation.html) API will also look at indicators of whether or not a submitted PNG or JPEG file is an image or a document using internal models and perform routing automatically. The default procedures are listed in the table below.

PNGs and JPEGs list Semantic Classifier as a default behavior. This means that BDA will look at indicators of whether or not a submitted file is an image or a document using internal models and perform routing automatically. PDF and TIFF files will be routed to Documents modality for processing. InvokeDataAutomation API does not currently support Audio and Video files.


| File Types | Default Routing Behavior | 
| --- | --- | 
| PNG | Semantic Classifer; Either Image or Document | 
| JPEG | Semantic Classifer; Either Image or Document | 
| PDF, TIFF | Document | 