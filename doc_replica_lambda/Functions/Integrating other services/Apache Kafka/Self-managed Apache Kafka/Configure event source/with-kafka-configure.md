

# Configuring self-managed Apache Kafka event sources for Lambda
<a name="with-kafka-configure"></a>

To use a self-managed Apache Kafka cluster as an event source for your Lambda function, you create an [event source mapping](invocation-eventsourcemapping.md) that connects the two resources. This page describes how to create an event source mapping for self-managed Apache Kafka.

This page assumes that you've already properly configured your Kafka cluster and the network it resides in. If you need to set up your cluster or network, see [Configuring your self-managed Apache Kafka cluster and network for Lambda](with-kafka-cluster-network.md).

**Topics**
+ [Using a self-managed Apache Kafka cluster as an event source](#kafka-esm-overview)
+ [Configuring cluster authentication methods in Lambda](kafka-cluster-auth.md)
+ [Creating a Lambda event source mapping for a self-managed Apache Kafka event source](kafka-esm-create.md)
+ [All self-managed Apache Kafka event source configuration parameters in Lambda](kafka-esm-parameters.md)

## Using a self-managed Apache Kafka cluster as an event source
<a name="kafka-esm-overview"></a>

When you add your Apache Kafka or Amazon MSK cluster as a trigger for your Lambda function, the cluster is used as an [event source](invocation-eventsourcemapping.md).

Lambda reads event data from the Kafka topics that you specify as `Topics` in a [CreateEventSourceMapping](https://docs.aws.amazon.com/lambda/latest/api/API_CreateEventSourceMapping.html) request, based on the [starting position](kafka-starting-positions.md) that you specify. After successful processing, your Kafka topic is committed to your Kafka cluster.

Lambda reads messages sequentially for each Kafka topic partition. A single Lambda payload can contain messages from multiple partitions. When more records are available, Lambda continues processing records in batches, based on the BatchSize value that you specify in a [CreateEventSourceMapping](https://docs.aws.amazon.com/lambda/latest/api/API_CreateEventSourceMapping.html) request, until your function catches up with the topic.

After Lambda processes each batch, it commits the offsets of the messages in that batch. If your function returns an error for any of the messages in a batch, Lambda retries the whole batch of messages until processing succeeds or the messages expire. You can send records that fail all retry attempts to an on-failure destination for later processing.

**Note**  
While Lambda functions typically have a maximum timeout limit of 15 minutes, event source mappings for Amazon MSK, self-managed Apache Kafka, Amazon DocumentDB, and Amazon MQ for ActiveMQ and RabbitMQ only support functions with maximum timeout limits of 14 minutes.