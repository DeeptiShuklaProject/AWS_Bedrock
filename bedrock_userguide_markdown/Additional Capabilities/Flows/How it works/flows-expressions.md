

# Use expressions to define inputs by extracting the relevant part of a whole input in Amazon Bedrock Flows
<a name="flows-expressions"></a>

When you configure the inputs for a node, you must define it in relation to the whole input that will enter the node. The whole input can be a string, number, boolean, array, or object. To define an input in relation to the whole input, you use a subset of supported expressions based off [JsonPath](https://github.com/json-path/JsonPath). Every expression must begin with `$.data`, which refers to the whole input. Note the following for using expressions:
+ If the whole input is a string, number, or boolean, the only expression that you can use to define an individual input is `$.data`
+ If the whole input is an array or object, you can use extract a part of it to define an individual input.

As an example to understand how to use expressions, let's say that the whole input is the following JSON object:

```
{
    "animals": {
        "mammals": ["cat", "dog"],
        "reptiles": ["snake", "turtle", "iguana"]
    },
    "organisms": {
        "mammals": ["rabbit", "horse", "mouse"],
        "flowers": ["lily", "daisy"]
    },
    "numbers": [1, 2, 3, 5, 8]
}
```

You can use the following expressions to extract a part of the input (the examples refer to what would be returned from the preceding JSON object):


****  

| Expression | Meaning | Example | Example result | 
| --- | --- | --- | --- | 
| $.data | The entire input. | $.data | The entire object | 
| .{{name}} | The value for a field called {{name}} in a JSON object. | $.data.numbers | [1, 2, 3, 5, 8] | 
| [{{int}}] | The member at the index specified by {{int}} in an array. | $.data.animals.reptiles[2] | iguana | 
| [{{int1}}, {{int2}}, ...] | The members at the indices specified by each {{int}} in an array. | $.data.numbers[0, 3] | [1, 5] | 
| [{{int1}}:{{int2}}] | An array consisting of the items at the indices between {{int1}} (inclusive) and {{int2}} (exclusive) in an array. Omitting {{int1}} or {{int2}} is equivalent to the marking the beginning or end of the array. | $.data.organisms.mammals[1:] | ["horse", "mouse"] | 
| \* | A wildcard that can be used in place of a {{name}} or {{int}}. If there are multiple results, the results are returned in an array. | $.data.\*.mammals | [["cat", "dog"], ["rabbit", "horse", "mouse"]] | 