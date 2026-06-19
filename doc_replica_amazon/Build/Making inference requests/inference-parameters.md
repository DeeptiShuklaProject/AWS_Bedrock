

# Influence response generation with inference parameters
<a name="inference-parameters"></a>

When running model inference, you can adjust inference parameters to influence the model response. Inference parameters can change the pool of possible outputs that the model considers during generation, or they can limit the final response.

Inference parameter default values and ranges depend on the model. To learn about inference parameters for different models, see [Inference request parameters and response fields for foundation models](model-parameters.md).

The following categories of parameters are commonly found across different models:

**Topics**
+ [Randomness and diversity](#inference-randomness)
+ [Length](#inference-length)

## Randomness and diversity
<a name="inference-randomness"></a>

For any given sequence, a model determines a probability distribution of options for the next token in the sequence. To generate each token in an output, the model samples from this distribution. Randomness and diversity refer to the amount of variation in a model's response. You can control these factors by limiting or adjusting the distribution. Foundation models typically support the following parameters to control randomness and diversity in the response.
+ **Temperature**– Affects the shape of the probability distribution for the predicted output and influences the likelihood of the model selecting lower-probability outputs.
  + Choose a lower value to influence the model to select higher-probability outputs.
  + Choose a higher value to influence the model to select lower-probability outputs.

  In technical terms, the temperature modulates the probability mass function for the next token. A lower temperature steepens the function and leads to more deterministic responses, and a higher temperature flattens the function and leads to more random responses.
+ **Top K** – The number of most-likely candidates that the model considers for the next token.
  + Choose a lower value to decrease the size of the pool and limit the options to more likely outputs.
  + Choose a higher value to increase the size of the pool and allow the model to consider less likely outputs.

  For example, if you choose a value of 50 for Top K, the model selects from 50 of the most probable tokens that could be next in the sequence.
+ **Top P** – The percentage of most-likely candidates that the model considers for the next token.
  + Choose a lower value to decrease the size of the pool and limit the options to more likely outputs.
  + Choose a higher value to increase the size of the pool and allow the model to consider less likely outputs.

  In technical terms, the model computes the cumulative probability distribution for the set of responses and considers only the top P% of the distribution.

  For example, if you choose a value of 0.8 for Top P, the model selects from the top 80% of the probability distribution of tokens that could be next in the sequence.

The following table summarizes the effects of these parameters.


****  

| Parameter | Effect of lower value | Effect of higher value | 
| --- | --- | --- | 
| Temperature | Increase likelihood of higher-probability tokens Decrease likelihood of lower-probability tokens | Increase likelihood of lower-probability tokensDecrease likelihood of higher-probability tokens | 
| Top K | Remove lower-probability tokens | Allow lower-probability tokens | 
| Top P | Remove lower-probability tokens | Allow lower-probability tokens | 

As an example to understand these parameters, consider the example prompt **I hear the hoof beats of "**. Let's say that the model determines the following three words to be candidates for the next token. The model also assigns a probability for each word.

```
{
    "horses": 0.7,
    "zebras": 0.2,
    "unicorns": 0.1
}
```
+ If you set a high **temperature**, the probability distribution is flattened and the probabilities become less different, which would increase the probability of choosing "unicorns" and decrease the probability of choosing "horses".
+ If you set **Top K** as 2, the model only considers the top 2 most likely candidates: "horses" and "zebras."
+ If you set **Top P** as 0.7, the model only considers "horses" because it is the only candidate that lies in the top 70% of the probability distribution. If you set **Top P** as 0.9, the model considers "horses" and "zebras" as they are in the top 90% of probability distribution.

## Length
<a name="inference-length"></a>

Foundation models typically support parameters that limit the length of the response. Examples of these parameters are provided below.
+ **Response length** – An exact value to specify the minimum or maximum number of tokens to return in the generated response.
+ **Penalties** – Specify the degree to which to penalize outputs in a response. Examples include the following.
  + The length of the response.
  + Repeated tokens in a response.
  + Frequency of tokens in a response.
  + Types of tokens in a response.
+ **Stop sequences** – Specify sequences of characters that stop the model from generating further tokens. If the model generates a stop sequence that you specify, it will stop generating after that sequence.