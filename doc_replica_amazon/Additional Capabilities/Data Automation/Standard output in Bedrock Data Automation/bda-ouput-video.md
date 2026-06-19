

# Videos
<a name="bda-ouput-video"></a>

BDA offers a set of standard outputs to process and generate insights for videos. Here's a detailed look at each operation type:

## Full Video Summary
<a name="video-summarization"></a>

Full video summary generates an overall summary of the entire video. It distills the key themes, events, and information presented throughout the video into a concise summary. Full video summary is optimized for content with descriptive dialogue such as product overviews, trainings, news casts, talk shows, and documentaries. BDA will attempt to provide a name for each unique speaker based on audio signals (e.g., the speaker introduces themself) or visual signals (e.g., a presentation slide shows a speaker’s name) in the full video summaries and the scene summaries. When a unique speaker’s name is not resolved they will be represented by a unique number (e.g., speaker\_0).

## Chapter Summaries
<a name="video-scene-summarization"></a>

Video chapter summarization provides descriptive summaries for individual scenes within a video. A video chapter is a sequence of shots that form a coherent unit of action or narrative within the video. This feature breaks down the video into meaningful segments based on visual and audible cues, provides timestamps for those segments, and summarizes each. 

## IAB Taxonomy
<a name="video-iab-classification"></a>

The Interactive Advertising Bureau (IAB) classification applies a standard advertising taxonomy to classify video scenes based on visual and audio elements. For Preview, BDA will support 24 top-level (L1) categories and 85 second-level (L2) categories. To download the list of IAB categories supported by BDA, click [here](samples/iab-taxonomy.zip).

## Full Audio Transcript
<a name="full-audio-transcript"></a>

The full audio transcript feature provides a complete text representation of all speech in the audio file. It uses advanced speech recognition technology to accurately transcribe dialogue, narration, and other audio elements. The transcription includes speaker identification, making it easy to navigate and search through the audio content based on the speaker.

## Text in Video
<a name="text-in-video"></a>

This feature detects and extracts text that appears visually in the video. It can identify both static text (like titles or captions) and dynamic text (such as moving text in graphics). Similar to image text detection, it provides bounding box information for each detected text element, allowing for precise localization within video frames.

## Logo Detection
<a name="video-logo-detection"></a>

This feature identifies logos in a video and provides bounding box information, indicating the coordinates of each detected logos within the video frame, and confidence scores. This feature is not enabled by default.

## Content Moderation
<a name="video-content-moderation"></a>

Content moderation detects inappropriate, unwanted, or offensive content in a video. BDA supports 7 moderation categories: Explicit, Non-Explicit Nudity of Intimate parts and Kissing, Swimwear or Underwear, Violence, Drugs & Tobacco, Alcohol, Hate symbols. Explicit text in videos is not flagged.

Bounding boxes and the associated confidence scores can be enabled or disabled for relevant features like text detection, to provide location coordinates and timestamps in the video file. By default, full video summarization, scene summarization, and video text detection are enabled.

**Note**  
 Only one audio track per video is supported. Subtitle file formats (e.g., SRT, VTT, etc.) are not supported. 

## Video Standard Output
<a name="video-standard-output"></a>

The following is an example of a standard output for a video processed through BDA:

```
{
"metadata": {
    "asset_id": "0",
    "semantic_modality": "VIDEO",
    "s3_bucket": "bedrock-data-automation-gamma-assets-us-east-1",
    "s3_key": "demo-assets/Video/MakingTheCut.mp4",
    "format": "QuickTime / MOV",
    "frame_rate": 30,
    "codec": "h264",
    "duration_millis": 378233,
    "frame_width": 852,
    "frame_height": 480
  },
```

This initial section dicusses metadata information regarding the video. This includes the bucket location, format, frame rate and other key pieces of info.

```
"shots": [ ...

    {
      "shot_index": 3,
      "start_timecode_smpte": "00:00:08:19",
      "end_timecode_smpte": "00:00:09:25",
      "start_timestamp_millis": 8633,
      "end_timestamp_millis": 9833,
      "start_frame_index": 259,
      "end_frame_index": 295,
      "duration_smpte": "00:00:01:06",
      "duration_millis": 1200,
      "duration_frames": 36,
      "confidence": 0.9956437242589935,
      "chapter_indices": [
        1
      ]
    },
```

This is an example of a shot element in a response. Shots represent small portions of a video, typically associate with an edit or cut in the video. Shots contain start and end elements, and also a chapter\_indicies element. This element indicates which larger section of the video, called a chapter, the shot is a part of.

```
"chapters": [
    {
      "start_timecode_smpte": "00:00:00:00",
      "end_timecode_smpte": "00:00:08:18",
      "start_timestamp_millis": 0,
      "end_timestamp_millis": 8600,
      "start_frame_index": 0,
      "end_frame_index": 258,
      "duration_millis": 8600,
      "shot_indices": [
        0,
        1,
        2
      ],
      "summary": "At an elegant outdoor venue, a man in a suit and a woman in a patterned dress stand on a raised platform overlooking a reflective pool. The setting is adorned with palm trees and lush greenery, creating a tropical atmosphere. The man initiates the event by asking if they should begin, to which the woman responds affirmatively. As the scene progresses, the focus shifts to a woman wearing a distinctive black and white patterned coat, her hair styled in a bun. She stands alone in a dimly lit room, facing away from the camera. The narrative then moves to a formal setting where a man in a dark suit stands before a curtain backdrop, suggesting he may be about to address an audience or perform. The scene concludes with a view of the entire venue, showcasing its tropical charm with a swimming pool surrounded by palm trees and decorative lighting, indicating it's prepared for a special occasion.",
```

Chapters are larger pieces of a video. Then contain start and end information like shots, and a shot\_indicies element. shot\_indicies tell you which shots are within a chapter. Finally, the summary element, provides a generated summary of the content of the chapter.

```
 "frames": [...
         {
          "timecode_smpte": "00:00:03:15",
          "timestamp_millis": 3500,
          "frame_index": 105,
          "content_moderation": [],
          "text_words": [
            {
              "id": "266db64a-a7dc-463c-b710-7a178a2cc4cc",
              "type": "TEXT_WORD",
              "confidence": 0.99844897,
              "text": "ANDREA",
              "locations": [
                {
                  "bounding_box": {
                    "left": 0.1056338,
                    "top": 0.7363281,
                    "width": 0.19806337,
                    "height": 0.068359375
                  },
                  "polygon": [
                    {
                      "x": 0.1056338,
                      "y": 0.7363281
                    },
                    {
                      "x": 0.30369717,
                      "y": 0.7363281
                    },
                    {
                      "x": 0.30369717,
                      "y": 0.8046875
                    },
                    {
                      "x": 0.1056338,
                      "y": 0.8046875
                    }
                  ]
                }
              ],
              "line_id": "57b760fc-c410-418e-aee3-7c7ba58a71c2"
            },
```

The smallest granularity of a video is a frame, representing a single image within a video. Frames have two notably response elements, content\_moderation and text\_words. The first, content\_moderation provides you with information based on content moderation catagories about the content of the frame if any are detected. The second, text\_words, provides you with a location and information about any text appearing in a video, such as closed captioning.

```
    "statistics": {
    "shot_count": 148,
    "chapter_count": 11,
    "speaker_count": 11
  }
}
```

Finally, statistics provides a breakdown of information about the detection, such as how many shots, speakers, and chapters are in a given video.