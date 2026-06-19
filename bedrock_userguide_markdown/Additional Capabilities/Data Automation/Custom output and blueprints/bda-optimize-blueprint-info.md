

# Optimize your blueprints with ground truth
<a name="bda-optimize-blueprint-info"></a>

You can improve blueprint accuracy by providing example content assets with the correct expected results. Blueprint instruction optimization uses your examples to refine the natural language instructions in your blueprint fields, which improves your inference **Results** accuracy.

Blueprint instruction optimization works best when you need to extract specific values that appear directly in your documents, such as invoice numbers, contract amounts, or tax form fields. We recommend providing 3 to 10 example assets that represent the documents you process in production, especially ones where you have encountered accuracy challenges.

**How blueprint instruction optimization works**  
Blueprint instruction optimization analyzes the differences between your expected results and the initial inference results. The service iteratively refines the natural language instructions for each field of your blueprint until the instructions produce more accurate results across your example assets. This process completes in minutes without requiring any model training or fine-tuning.

When you start your optimization process, you provide your example assets and the corresponding ground truth data—the correct values you expect to extract for each field. Blueprint instruction optimization compares these values against inference results and adjusts the field descriptions to improve accuracy. After optimization completes, you receive accuracy metrics that show the accuracy improvement, including exact match rates and F1 scores measured against your ground truth.

**What you need before you start optimizing your blueprints**  
**A blueprint with defined fields**. Create a blueprint using the console or API. Your blueprint should include the field names and initial descriptions for the data you want to extract.

**Example content assets**. Gather 3 to 10 documents assets that represent your production workload on documents. Choose examples that contain all the fields in your blueprint.

**Expected results for your examples**. Prepare the correct values you want to extract from each example asset. You can enter these values manually during optimization or upload them using a manifest file.

**An S3 bucket location**. Specify an S3 bucket where you want to store your example assets and ground truth data. You can provide your own bucket or allow the service to create one for you.

**Step-by-step process to optimize your blueprint**  
To optimize your blueprint, start from the blueprint detail page in the Amazon Bedrock Data Automation console. Note this is only available for your document modality.

Step 1. Select **Optimize blueprint** to begin the optimization workflow.

![Blueprint interface showing Optimize blueprint button with Get result and Download options.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/bda/bda-blueprint-optimize-button.png)


Step 2. **Upload your example assets**. Choose up to 10 content assets from your local device or from an S3 location. The service uploads your assets and displays thumbnails for each file. If you previously optimized this blueprint, you can add new examples or remove existing ones.

![Add files interface showing three uploaded sample data files with file sizes and timestamps.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/bda/bda-optimize-files-selector.png)


Step 3. **Provide ground truth for each asset**. Select an asset to open the ground truth editor. The editor displays your document preview on the left and a simplified table of your blueprint fields on the right. For each field, enter the correct value you expect to extract in the Ground Truth column.

![Ground truth editor showing document preview on left and blueprint fields table on right.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/bda/bda-optimize-files-ground-truth.png)


Step 4. To speed up ground truth entry, select **Auto-populate** to run initial inference on your assets and automatically populate the **Ground Truth** column from values in your **Results** column. Edit any incorrect values before proceeding.

![Ground truth table showing employee and employer data fields with editable values.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/bda/bda-optimize-ground-truth-edit.png)


Step 5. **Start optimization**. After you complete ground truth entry for all selected assets, choose **Start optimization**. Data automation analyzes your examples and refines the natural language instructions for each field. A progress indicator shows the optimization status with messages such as "Reading your assets" and "Iterating on blueprint natural language instructions."

![Ground truth table showing field names, instructions, results, and ground truth values for optimization.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/bda/bda-start-optimization-button.png)


Step 6. **Review the evaluation metrics**. When optimization completes, the **Metrics** section displays accuracy metrics for your blueprint. The metrics compare performance before optimization and after optimization. Review the overall F1 score, confidence score, and exact match rate to assess whether the blueprint meets your accuracy requirements.

The **Metrics by sample file** tab shows field-level accuracy for each example asset. Use these metrics to identify which fields improved and which fields may need additional examples or manual refinement.

![Metrics table showing confidence score, exact match rate, and overall F1 score improvements after optimization.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/bda/bda-optimize-metrics.png)


Step 7. **Complete optimization**. If the evaluation metrics meet your requirements, select **Save optimized blueprint** to promote the optimized blueprint to production. Your blueprint now uses the refined natural language instructions for all future inference requests.

**Re-optimize your blueprint**  
You can re-optimize a blueprint at any time to improve accuracy further. Return to the blueprint detail page and select **Optimize blueprint**. The service displays the assets you previously used for optimization along with their ground truth values.

To re-optimize, you can add new example assets, edit ground truth values for existing assets, or remove assets that no longer represent your workload. When you select **Start optimization**, blueprint instruction optimization calculates relative to your current blueprint instructions versus the new instructions.

**Edit a blueprint after optimization**  
If you add or remove fields from an optimized blueprint, the service removes the optimization history and associated example assets. Before editing, download the manifest file that contains your asset locations and ground truth labels. The manifest file uses JSON format and includes all fields and ground truth values from your previous optimization. To preserve your optimization work, upload the manifest file when you re-optimize the edited blueprint. Data automation automatically applies ground truth values to matching fields. Fields that no longer exist in the blueprint are removed from the manifest. New fields do not have ground truth values until you provide them.

**Manage optimization costs**  
Blueprint instruction optimization consumes incurs the inference costs as you would if manually edit your natural language instructions and iteratively test them against each sample document. For a rough calculation, the number of pages you supply as examples will be the number of pages that will be charged as you optimize your blueprint. Each optimization run processes your example assets multiple times to refine the instructions. To minimize costs, start with 3 to 5 examples for your initial optimization. Add more examples when you inspect the evaluation metrics and believe you need additional accuracy improvements.

In addition, the optimized natural language instructions tend to be longer and more detailed than the original instructions, which can increase runtime inference costs.