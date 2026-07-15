

# Packaging your layer content
<a name="packaging-layers"></a>

A Lambda layer is a .zip file archive that contains supplementary code or data. Layers usually contain library dependencies, a [custom runtime](runtimes-custom.md), or configuration files. 

This section explains how to properly package your layer content. For more conceptual information about layers and why you might consider using them, see [Managing Lambda dependencies with layers](chapter-layers.md).

The first step to creating a layer is to bundle all of your layer content into a .zip file archive. Because Lambda functions run on [Amazon Linux](https://docs.aws.amazon.com/linux/al2023/ug/what-is-amazon-linux.html), your layer content must be able to compile and build in a Linux environment.

To ensure that your layer content works properly in a Linux environment, we recommend creating your layer content using a tool like [Docker](https://docs.docker.com/get-docker).

**Topics**
+ [Layer paths for each Lambda runtime](#packaging-layers-paths)

## Layer paths for each Lambda runtime
<a name="packaging-layers-paths"></a>

When you add a layer to a function, Lambda loads the layer content into the `/opt` directory of that execution environment. For each Lambda runtime, the `PATH` variable already includes specific folder paths within the `/opt` directory. To ensure that Lambda picks up your layer content, your layer .zip file should have its dependencies in one of the following folder paths:



- ** Node.js **
  - `nodejs/node_modules`
  - `nodejs/node18/node_modules` (`NODE_PATH`)
  - `nodejs/node20/node_modules` (`NODE_PATH`)
  - `nodejs/node22/node_modules` (`NODE_PATH`)

- ** Python **
  - `python`
  - `python/lib/{{python3.x}}/site-packages` (site directories)

- ** Java **
  - `java/lib` (`CLASSPATH`)

- ** Ruby **
  - `ruby/gems/3.4.0` (`GEM_PATH`)
  - `ruby/lib` (`RUBYLIB`)

- ** All runtimes **
  - `bin` (`PATH`) 
  - `lib` (`LD_LIBRARY_PATH`)



The following examples show how you can structure the folders in your layer .zip archive.

------
#### [ Node.js ]

**Example file structure for the AWS X-Ray SDK for Node.js**  

```
xray-sdk.zip
└ nodejs/node_modules/aws-xray-sdk
```

------
#### [ Python ]

**Example**  

```
{{python/}}              # Required top-level directory
└── requests/
└── boto3/
└── numpy/
└── (dependencies of the other packages)
```

------
#### [ Ruby ]

**Example file structure for the JSON gem**  

```
json.zip
└ ruby/gems/3.4.0/
               | build_info
               | cache
               | doc
               | extensions
               | gems
               | └ json-2.1.0
               └ specifications
                 └ json-2.1.0.gemspec
```

------
#### [ Java ]

**Example file structure for the Jackson JAR file**  

```
layer_content.zip
└ java
    └ lib
        └ jackson-core-2.17.0.jar
        └ <other potential dependencies>
        └ ...
```

------
#### [ All ]

**Example file structure for the jq library**  

```
jq.zip
└ bin/jq
```

------

For language-specific instructions on packaging, creating, and adding a layer, refer to the following pages:
+ **Node.js** – [Working with layers for Node.js Lambda functions](nodejs-layers.md)
+ **Python** – [Working with layers for Python Lambda functions](python-layers.md)
+ **Ruby** – [Working with layers for Ruby Lambda functions](ruby-layers.md)
+ **Java** – [Working with layers for Java Lambda functions](java-layers.md)

We recommend **against** using layers to manage dependencies for Lambda functions written in Go and Rust. This is because Lambda functions written in these languages compile into a single executable, which you provide to Lambda when you deploy your function. This executable contains your compiled function code, along with all of its dependencies. Using layers not only complicates this process, but also leads to increased cold start times because your functions need to manually load extra assemblies into memory during the init phase.

To use external dependencies with Go and Rust Lambda functions, include them directly in your deployment package.