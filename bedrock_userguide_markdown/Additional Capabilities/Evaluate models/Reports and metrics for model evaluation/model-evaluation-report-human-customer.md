

# Review a human-based model evaluation job in Amazon Bedrock (console)
<a name="model-evaluation-report-human-customer"></a>

You can review the data for human evaluation presented in a report using the Amazon Bedrock console.

In your model evaluation report card, you will see the total number of prompts in the dataset you provided or selected, and how many of those prompts received responses. If the number of responses is less than the number of input prompts times the number of workers per prompt you configured in the job (either 1,2 or 3), make sure to check the data output file in your Amazon S3 bucket. It is possible that the prompt caused an error with the model and there was no inference retrieved. Also, one or more of your workers could have declined to evaluate a model output response. Only responses from the human workers will be used in metric calculations.

Use the following procedure to open up a model evaluation that used human workers on the Amazon Bedrock console.

1. Open the Amazon Bedrock console.

1. From the navigation pane, choose **Model evaluation**.

1. Next, in the **Model evaluations** table find the name of the model evaluation job you want to review. Then, choose it.

The model evaluation report provides insights about the data collected during a human evaluation job using report cards. Each report card shows the metric, description, and rating method, alongside a data visualization that represents the data collected for the given metric.

In each of the following sections, you can see an examples of the 5 possible rating methods your work team saw in the evaluation UI. The examples also show what key value pair is used to save the results in Amazon S3.

## Likert scale, comparison of multiple model outputs
<a name="likert-compare"></a>

Human evaluators indicate their preference between the two responses from the model on a 5 point Likert scale in accordance with your instructions. The results in the final report will be shown as a histogram of preference strength ratings from the evaluators over your whole dataset.

Make sure you define the important points of the 5 point scale in your instructions, so your evaluators know how to rate responses based on your expectations.

![This is my image.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/model-evaluation/likert-compare.png)


**JSON output**  
The first child-key under `evaluationResults` is where the selected rating method is returned. In the output file saved to your Amazon S3 bucket, the results from each worker are saved to the `"evaluationResults": "comparisonLikertScale"` key value pair.

## Choice buttons (radio button)
<a name="choice-buttons"></a>

Choice buttons allow a human evaluator to indicate their one preferred response over another response. Evaluators indicate their preference between two responses according to your instructions with radio buttons. The results in the final report will be shown as a percentage of responses that workers preferred for each model. Be sure to explain your evaluation method clearly in the instructions.

![This is my image.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/model-evaluation/radiobuttons.png)


**JSON output**  
The first child-key under `evaluationResults` is where the selected rating method is returned. In the output file saved to your Amazon S3 bucket, the results from each worker are saved to the `"evaluationResults": "comparisonChoice"` key value pair.

## Ordinal rank
<a name="ordinal-rank"></a>

Ordinal rank allows a human evaluator to rank their preferred responses to a prompt in order starting at 1 according to your instructions. The results in the final report will be shown as a histogram of the rankings from the evaluators over the whole dataset. Be sure to define what a rank of 1 means in your instructions. This data type is called Preference Rank.

![This is my image.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/model-evaluation/ordinal-rank.png)


**JSON output**  
The first child-key under `evaluationResults` is where the selected rating method is returned. In the output file saved to your Amazon S3 bucket, the results from each worker are saved to the `"evaluationResults": "comparisonRank"` key value pair.

## Thumbs up/down
<a name="thump-up-down"></a>

Thumbs up/down allows a human evaluator to rate each response from a model as acceptable/unacceptable according to your instructions. The results in the final report will be shown as a percentage of the total number of ratings by evaluators that received a thumbs up rating for each model. You may use this rating method for a model evaluation job that contains one or more models. If you use this in an evaluation that contains two models, a thumbs up/down will be presented to your work team for each model response and the final report will show the aggregated results for each model individually. Be sure to define what is acceptable (that is, what is a thumbs up rating) in your instructions.

![This is my image.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/model-evaluation/thumb-up.png)


**JSON output**  
The first child-key under `evaluationResults` is where the selected rating method is returned. In the output file saved to your Amazon S3 bucket, the results from each worker are saved to the `"evaluationResults": "thumbsUpDown"` key value pair.

## Likert scale, evaluation of a single model response
<a name="likert-single"></a>

Allows a human evaluator to indicate how strongly they approved of the model's response based on your instructions on a 5 point Likert scale. The results in the final report will be shown as a histogram of the 5 point ratings from the evaluators over your whole dataset. You may use this for an evaluation containing one or more models. If you select this rating method in an evaluation that contains more than one model, a 5 point Likert scale will be presented to your work team for each model response and the final report will show the aggregated results for each model individually. Be sure to define the important points on the 5 point scale in your instructions so your evaluators know how to rate the responses according to your expectations.

![This is my image.](http://docs.aws.amazon.com/bedrock/latest/userguide/images/model-evaluation/model-eval-likert2-final.png)


**JSON output**  
The first child-key under `evaluationResults` is where the selected rating method is returned. In the output file saved to your Amazon S3 bucket, the results from each worker are saved to the `"evaluationResults": "individualLikertScale"` key value pair.