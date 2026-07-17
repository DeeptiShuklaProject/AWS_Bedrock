# Section 17 – Lambda Layers

<a name="sec-17"></a>

A **Lambda Layer** is a `.zip` archive containing libraries or other dependencies. This allows you to reference third-party libraries (like NumPy, Pandas, or Requests) without packaging them directly in your code deployment archive.

### Steps to Package a Python requests Layer
AWS Lambda looks for external packages in specific paths. For Python, it searches in the `python/` directory.

```bash
# 1. Create a workspace folder structure
mkdir -p layer_workspace/python

# 2. Install the required target package into the folder
pip install requests -t layer_workspace/python/

# 3. Zip the python directory
cd layer_workspace
zip -r requests_layer.zip python/

# 4. Deploy the layer to AWS
aws lambda publish-layer-version \
    --layer-name requests-layer \
    --description "Contains requests module v2.31" \
    --zip-file fileb://requests_layer.zip \
    --compatible-runtimes python3.12
```

---
