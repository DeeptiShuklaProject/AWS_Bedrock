

# Audio
<a name="audio-processing"></a>

The Amazon Bedrock Data Automation (BDA) feature offers a set of standard output to process and generate insights for audio files. Here's a detailed look at each operation type:

## Full Audio Summary
<a name="audio-audio-summarization"></a>

Full audio summary generates an overall summary of the entire audio file. It distills the key themes, events, and information presented throughout the audio into a concise summary.

## Full Audio Transcript
<a name="audio-audio-transcript"></a>

The full audio transcript feature provides a complete text representation of all spoken content in the audio. It uses advanced speech recognition technology to accurately transcribe dialogue, narration, and other audio elements. The transcription includes time-stamping, making it easy to navigate and search through audio content based on spoken words.

### Speaker and Channel Labeling
<a name="w2aac32c10c11c13b5b3b7"></a>

For the generated transcript, you can enable channel and/or speaker labeling. This will give each channel or speaker a number, and then indicate within the transcript when a channel is being used and a particular speaker is speaking. This label appears within the response as "spk\_" followed by a unique number for each speaker, up to 30 speakers. The first speaker would be "spk\_0", "spk\_1" and so on. Audio channels are indicated similarly with the first channel labeled as "ch\_0", but can only be labeled up two channels.

## Topic Summary
<a name="audio-topic-summary"></a>

Audio topic summary separates the audio file into sections called topics, and summarizes them to provide key information. These topics are given timestamps to help place them in the audio file as a whole. This feature is not enabled by default.

## Content Moderation
<a name="audio-content-moderation"></a>

Content moderation uses audio and text-based cues to identify and classify voice-based toxic content into seven different categories: 
+ ****Profanity****: Speech that contains words, phrases, or acronyms that are impolite, vulgar, or offensive.
+ ****Hate speech:**** Speech that criticizes, insults, denounces, or dehumanizes a person or group on the basis of an identity (such as race, ethnicity, gender, religion, sexual orientation, ability, and national origin).
+  ****Sexual: ****Speech that indicates sexual interest, activity, or arousal using direct or indirect references to body parts, physical traits, or sex.
+ ****Insults:**** Speech that includes demeaning, humiliating, mocking, insulting, or belittling language. This type of language is also labeled as bullying
+ ****Violence or threat: ****Speech that includes threats seeking to inflict pain, injury, or hostility toward a person or group.
+ ****Graphic:**** Speech that uses visually descriptive and unpleasantly vivid imagery. This type of language is often intentionally verbose to amplify a recipient's discomfort.
+ ****Harassment or abusive:**** Speech intended to affect the psychological well-being of the recipient, including demeaning and objectifying terms. This type of language is also labeled as harassment.

## Audio Standard Output
<a name="audio-standard-output-example"></a>

This section focuses on the different response objects you receive from running the API operation InvokeDataAutomation on an audio file. Below we'll break down each section of the response object and then see a full, populated response for an example document. The first section we'll receive is `metadata`.

```
 "metadata": {
    "asset_id": "0",
    "semantic_modality": "AUDIO",
    "s3_bucket": "bedrock-data-automation-gamma-assets-us-east-1",
    "s3_key": "demo-assets/Audio/AWS_TCA-Call-Recording-2.wav",
    "sample_rate": 8000,
    "bitrate": 256000,
    "number_of_channels": 2,
    "codec": "pcm_s16le",
    "duration_millis": 237560,
    "format": "wav",
    "dominant_asset_language": "EN",
    "generative_output_language": "DEFAULT/EN"
  }
```

This section breaks down information about the file such as its s3 location, bitrate, audio channels, and format. Next we look at `audio_items`.

`dominant_asset_language` indicaties what language is the most present in a piece of audio based on length in seconds. `generative_output_language` indicates which language the response output will be in. When set to "DEFAULT" it will use the dominant language.

```
"audio_items": [
    {
      "item_index": 0,
      "audio_segment_index": 0,
      "content": "Auto",
      "start_timestamp_millis": 9,
      "end_timestamp_millis": 119
    },
    ...
]
```

The items section includes a breakdown of the audio file on a sound by sound basis. Each item is usually about word length. The item\_index indicates the item's place in the audio\_items indicies, and the audio\_segment\_index indicates where it sits in the segements indicies which we'll discuss next.

```
"audio_segments": [
    {
      "start_timestamp_millis": 0,
      "end_timestamp_millis": 1970,
      "segment_index": 0,
      "type": "TRANSCRIPT",
      "text": "Auto sales, Cherry speaking. How can I help you?",
      "speaker": {
        "speaker_label": "spk_0"
      },
      "channel": {
        "channel_label": "ch_0"
      },
      "audio_item_indices": [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11
      ],
      "language": "EN"
    },
    ...
]
```

Here we get a breakdown of the file based on longer spans of time, with each segment equal to roughly a sentence. It tells us which audio items are included in the segment and the text of the segment itself. Next let's look at content moderation.

With speaker and channel labeling enabled, you can see the `speaker_label` and `channel_label` sections which indicate which speaker and channel are present in this segment.

```
"content_moderation": [
      {
        "id": "93068e72-290d-4aad-8717-a2cd0e02b0d0",
        "type": "AUDIO_MODERATION",
        "confidence": 0.0476,
        "start_timestamp_millis": 0,
        "end_timestamp_millis": 1970,
        "moderation_categories": [
          {
            "category": "profanity",
            "confidence": 0.1582
          },
          ...
        ]
      },
      ...
]
```

The content moderation section goes through each individual segment and analyzes it for any of the seven moderation catagories, providing confidence scores for each section. Our next section is topics.

```
"topics": [
    {
      "topic_index": 0,
      "start_timestamp_millis": 0,
      "end_timestamp_millis": 36790,
      "summary": "As follows:\n\nSuzanne, a customer, recently had her Hyundai serviced at the auto sales shop where Carrie works. Suzanne had a 3 p.m. appointment and got her car serviced, which included an oil change and filter changes. However, when Suzanne left the shop, her oil light was still on, which she found concerning. Carrie acknowledged that this sometimes happens, even after a service visit, and assured Suzanne that she would look into the issue further.",
      "transcript": {
        "representation": {
          "text": "Auto sales, Cherry speaking. How can I help you? Yeah, hi Carrie, um, my name is Suzanne. I literally just left your shop. Um, I just went in and got my Hyundai service. Um, it just was, it just needed like filter error changes oil change and all that kind of stuff, um, but. When I left and my oil light is still on and I don't know why. Got it. You just got it serviced here, but when you drove off the light was still on. Is that what happened? Yeah, yeah, yeah, like I literally like I had a 3 p.m. appointment and I just got it, you know, believe it or not, this, this happens."
        }
      },
      "audio_segment_indices": [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10
      ]
    },
    ...
]
```

Topic sections are the next level of granularity from segements. These are groupings of segements are broken down roughly by concepts. Each topic comes with a generated summary of the topic, and the exact test of the topic. Our final part of a response is statistics.

```
 "statistics": {
    "word_count": 749,
    "topic_count": 4
  }
```

This section summarizes the information about the audio file. This includes word count and total topics.