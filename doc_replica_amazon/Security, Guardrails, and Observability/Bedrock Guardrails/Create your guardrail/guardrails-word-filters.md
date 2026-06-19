

# Remove a specific list of words and phrases from conversations with word filters
<a name="guardrails-word-filters"></a>

Amazon Bedrock Guardrails has word filters that you can use to block words and phrases (exact match) in input prompts and model responses. You can use following word filters to block profanity, offensive, or inappropriate content, or content with competitor or product names.
+ **Profanity filter** – Turn on to block profane words. The list of profanities is based on conventional definitions of profanity and it's continually updated.
+ **Custom word filter **– Add custom words and phrases using the AWS Management Console of up to three words to a list. You can add up to 10,000 items to the custom word filter.

  You have the following options for adding words and phrases using the Amazon Bedrock AWS Management Console:
  + Add manually in the text editor.
  + Upload a .txt or .csv file.
  + Upload an object from an Amazon S3 bucket.
**Note**  
You can only upload documents and objects using the AWS Management Console. API and SDK operations only support text, and do not include the upload of documents and objects.

## Configure word policy for your guardrail
<a name="guardrails-word-policy-configure"></a>

You can configure word policies for your guardrail by using the AWS Management Console or Amazon Bedrock API.

------
#### [ Console ]

1. Sign in to the AWS Management Console with an IAM identity that has permissions to use the Amazon Bedrock console. Then, open the Amazon Bedrock console at [https://console.aws.amazon.com/bedrock](https://console.aws.amazon.com/bedrock).

1. From the left navigation pane, choose **Guardrails**, and then choose **Create guardrail**.

1. For **Provide guardrail details** page, do the following:

   1. In the **Guardrail details** section, provide a **Name** and optional **Description** for the guardrail.

   1. For **Messaging for blocked prompts**, enter a message that displays when your guardrail is applied. Select the **Apply the same blocked message for responses** checkbox to use the same message when your guardrail is applied on the response.

   1. (Optional) To enable [cross-Region inference](guardrails-cross-region.md) for your guardrail, expand **Cross-Region inference**, and then select **Enable cross-Region inference for your guardrail**. Choose a guardrail profile that defines the destination AWS Regions where guardrail inference requests can be routed.

   1. (Optional) By default, your guardrail is encrypted with an AWS managed key. To use your own customer-managed KMS key, expand **KMS key selection** and select the **Customize encryption settings (advanced)** checkbox.

      You can select an existing AWS KMS key or select **Create an AWS KMS key** to create a new one.

   1. (Optional) To add tags to your guardrail, expand **Tags**, and then, select **Add new tag** for each tag you define.

      For more information, see [Tagging Amazon Bedrock resources](tagging.md).

   1. Choose **Next**.

1. On the **Add word filters** page, do the following:

   1. Select **Filter profanity** to block profanity in prompts and responses. The list of profanity is based on conventional definitions and is continually updated.

   1. For **Add custom words and phrases**, select how to add words and phrases for your guardrail to block. If you upload a file of words, each line in the file should contain one word or a phrase of up to three words. Don't include a header. You have the following options:  
****    
[See the AWS documentation website for more details](http://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-word-filters.html)

   1. Edit the words and phrases for the guardrail to block in the **View and edit words and phrases** section. You have the following options:
      + If you uploaded a word list from a local file or Amazon S3 object, this section will populate with your word list. To filter for items with errors, select **Show errors**.
      + To add an item to the word list, select **Add word or phrase**. Enter a word or a phrase of up to three words in the box and press **Enter** or select the checkmark icon to confirm the item.
      + To edit an item, select the edit icon (![Edit icon represented by a pencil symbol.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/edit.png)) next to the item.
      + To delete an item from the word list, select the trash can icon (![Trash can icon representing a delete action.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/trash.png)) or, if you're editing an item, select the delete icon (![Close or cancel icon represented by an "X" symbol.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/close.png)) next to the item.
      + To delete items that contain errors, select **Delete all** and then select **Delete all rows with error**.
      + To delete all items, select **Delete all** and then select **Delete all rows**.
      + To search for an item, enter an expression in the search bar.
      + To show only items with errors, select the dropdown menu labeled **Show all** and select **Show errors only**.
      + To configure the size of each page in the table or the column display in the table, select the settings icon (![Gear icon representing settings or configuration options.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/icons/settings.png)). Set your preferences and then select **Confirm**.
      + By default, this section displays the **Table** editor. To switch to a text editor in which you can enter a word or phrase in each line, select **Text editor**. The **Text editor** provides the following features:
        + You can copy a word list from another text editor and paste it into this editor.
        + A red X icon appears next to items containing errors and a list of errors appears at the following the editor.

   1. Choose **Next** to configure other policies as needed or **Skip to Review and create** to finish creating your guardrail.

   1. Review the settings for your guardrail.

      1. Select **Edit** in any section you want to make changes to.

      1. When you're done configuring policies, select **Create** to create the guardrail.

------
#### [ API ]

To create a guardrail with word policies, send a [CreateGuardrail](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_CreateGuardrail.html) request. The request format is as follows:

```
POST /guardrails HTTP/1.1
Content-type: application/json

{
    "blockedInputMessaging": "string",
    "blockedOutputsMessaging": "string",
    "wordPolicyConfig": {
        "managedWordListsConfig": [
            {
                "inputAction": "BLOCK | NONE",
                "inputEnabled": true,
                "outputAction": "BLOCK | NONE",
                "outputEnabled": true,
                "type": "PROFANITY"
            },
        ],
        "wordsConfig": [{
            "text": "string",
            "inputAction": "BLOCK | NONE",
            "inputEnabled": true,
            "outputAction": "BLOCK | NONE",
            "outputEnabled": true
        }]
    },
    "description": "string",
    "kmsKeyId": "string",
    "name": "string",
    "tags": [{
        "key": "string",
        "value": "string"
    }],
    "crossRegionConfig": {
        "guardrailProfileIdentifier": "string"
    }
}
```
+ Specify a `name` and `description` for the guardrail.
+ Specify messages for when the guardrail successfully blocks a prompt or a model response in the `blockedInputMessaging` and `blockedOutputsMessaging` fields.
+ Configure word policies in the `wordPolicyConfig` object:
  + Use `managedWordListsConfig` to configure a predefined list of profane words.
  + Use `wordsConfig` array to specify custom words and phrases to filter:
    + Specify the words and phrases to filter in the `text` field.
    + (Optional) Specify the action to take when the word is detected in prompts using `inputAction` or responses using `outputAction`. Choose `BLOCK` to block content and replace with blocked messaging, or `NONE` to take no action but return detection information.
    + (Optional) Use `inputEnabled` and `outputEnabled` to control whether guardrail evaluation is enabled for inputs and outputs.
+ (Optional) Attach any tags to the guardrail. For more information, see [Tagging Amazon Bedrock resources](tagging.md).
+ (Optional) For security, include the ARN of a KMS key in the `kmsKeyId` field.
+ (Optional) To enable [cross-Region inference](guardrails-cross-region.md), specify a guardrail profile in the `crossRegionConfig` object.

The response format is as follows:

```
HTTP/1.1 202
Content-type: application/json

{
    "createdAt": "string",
    "guardrailArn": "string",
    "guardrailId": "string",
    "version": "string"
}
```

------