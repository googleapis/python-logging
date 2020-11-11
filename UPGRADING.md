# 2.0.0 Migration Guide

The 2.0 release of the `google-cloud-logging` client is a significant upgrade based on a [next-gen code generator](https://github.com/googleapis/gapic-generator-python), and includes substantial interface changes. Existing code written for earlier versions of this library will likely require updates to use this version. This document describes the changes that have been made, and what you need to do to update your usage.

If you experience issues or have questions, please file an [issue](https://github.com/googleapis/python-logging/issues).

## Supported Python Versions

> **WARNING**: Breaking change

The 2.0.0 release requires Python 3.6+.


## Primary Changes

This section lists the most relevant breaking changes in `google.cloud.logging`.
See 'Changes in GAPIC Layer' if you were directly using `google.cloud.logging_v2.proto` or `google.cloud.logging_v2.gapic`.


### Optional arguments *must* be passed as keyword arguments.

Optional arguments are keyword-only arguments and *must* be passed by name.
See [PEP 3102](https://www.python.org/dev/peps/pep-3102/).

```Before
from google.cloud import logging

logging_client = logging.Client()
logging_client.sink("my-sink")

```

### Support for non-project resources

Where appropriate, sinks, entries, and metrics can be associated with non-project resources like folders and organizations.

Methods generally default to the project bound to the client.

This resulted in breaking changes to some methods which now expect full resource paths instead of just the name, to 
disambiguate the location of a resource.


#### `google.cloud.logging_v2.client.Client`

`list_entries` accepts `resource_names`.


**After**:
```py
from google.cloud import logging_v2

client = logging_v2.Client()
client.list_entries(resource_names=["folders/myFolder", "projects/myProject"])
client.list_entries() # defaults to project bound to client
```

`list_sinks` accept a `parent` parameter which is expected to be a single resource path.



**After**:
```py
from google.cloud import logging_v2

client = loggign_v2.Client()
client.list_sinks(parent="folder/myFolder")
client.list_sinks()  # defaults to project bound to client
```

#### `google.cloud.logging_v2.logger.Logger`

`list_entries` accepts `resource_names`.

**After**:
```py
from google.cloud import logging_v2

client = logging_v2.Client()
logger = logging_v2.Logger("myLog", client)
logger.list_entries(resource_names=["folders/myFolder", "projects/myProject"])
logger.list_entries() # defaults to project bound to client
```



#### `google.cloud.loggign_v2.sinks.Sink`


> **WARNING**: Breaking change
* Sinks no longer have a `project` property. The attribute is replaced by `parent` (e.g. `projects/my-project`)


### `google.cloud.logging` is an alias for `google.cloud.logging_v2`

`google.cloud.logging` serves as a default alias for `google.cloud.logging_v2`.

All library code has been moved to `google.cloud.logging_v2`.



## Changes in GAPIC layer

This section describes changes in the GAPIC layer (produced by the generator) that previously lived in  `google.cloud.logging_v2.proto` / `google.cloud.logging_v2.gapic`.
Most users are unlikely to have been using this layer directly.

## Method Calls

> **WARNING**: Breaking change

Methods expect request objects. We provide a script that will convert most common use cases.

* Install the library and `libcst`. `libcst` is required to run the fixup script.

```py
python3 -m pip install google-cloud-logging libcst
```

* The script `fixup_automl_{version}_keywords.py` is shipped with the library. It expects
an input directory (with the code to convert) and an empty destination directory.

```sh
$ fixup_automl_v1_keywords.py --input-directory .samples/ --output-directory samples/
```

**Before:**
```py
from google.cloud import automl

project_id = "YOUR_PROJECT_ID"
model_id = "YOUR_MODEL_ID"

client = automl.AutoMlClient()
# Get the full path of the model.
model_full_id = client.model_path(project_id, "us-central1", model_id)
response = client.deploy_model(model_full_id)
```


**After:**
```py
from google.cloud import automl

project_id = "YOUR_PROJECT_ID"
model_id = "YOUR_MODEL_ID"

client = automl.AutoMlClient()
# Get the full path of the model.
model_full_id = client.model_path(project_id, "us-central1", model_id)
response = client.deploy_model(name=model_full_id)
```

### More Details

In `google-cloud-logging<2.0.0`, parameters required by the API were positional parameters and optional parameters were keyword parameters.

**Before:**
```py
    def batch_predict(
        self,
        name,
        input_config,
        output_config,
        params=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
```

In the 2.0.0 release, all methods have a single positional parameter `request`. Method docstrings indicate whether a parameter is required or optional.

Some methods have additional keyword only parameters. The available parameters depend on the [`google.api.method_signature` annotation](https://github.com/googleapis/googleapis/blob/2db5725bf898b544a0cf951e1694d3b0fce5eda3/google/cloud/automl/v1/prediction_service.proto#L86) specified by the API producer.


**After:**
```py
def batch_predict(
        self,
        request: prediction_service.BatchPredictRequest = None,
        *,
        name: str = None,
        input_config: io.BatchPredictInputConfig = None,
        output_config: io.BatchPredictOutputConfig = None,
        params: Sequence[prediction_service.BatchPredictRequest.ParamsEntry] = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
```

> **NOTE:** The `request` parameter and flattened keyword parameters for the API are mutually exclusive.
> Passing both will result in an error.


Both of these calls are valid:

```py
response = client.batch_predict(
    request={
        "name": name,
        "input_config": input_config,
        "output_config": output_config,
        "params": params,
    }
)
```

```py
response = client.batch_predict(
    name=name,
    input_config=input_config,
    output_config=output_config,
    params=params,
)
```

This call is invalid because it mixes `request` with a keyword argument `params`. Executing this code
will result in an error.

```py
response = client.batch_predict(
    request={
        "name": name,
        "input_config": input_config,
        "output_config": output_config,
    },
    params=params,
)
```


The method `list_datasets` takes an argument `filter` instead of `filter_`.

**Before**
```py
from google.cloud import automl

project_id = "PROJECT_ID"

client = automl.AutoMlClient()
project_location = client.location_path(project_id, "us-central1")

# List all the datasets available in the region.
response = client.list_datasets(project_location, filter_="")
```

**After**
```py
from google.cloud import automl

project_id = "PROJECT_ID"
client = automl.AutoMlClient()
# A resource that represents Google Cloud Platform location.
project_location = f"projects/{project_id}/locations/us-central1"

# List all the datasets available in the region.
response = client.list_datasets(parent=project_location, filter="")
```

### Changes to v1beta1 Tables Client

Optional arguments are now keyword-only arguments and *must* be passed by name.
See [PEP 3102](https://www.python.org/dev/peps/pep-3102/).

***Before**
```py
    def predict(
        self,
        inputs,
        model=None,
        model_name=None,
        model_display_name=None,
        feature_importance=False,
        project=None,
        region=None,
        **kwargs
    ):
```

**After**
```py
    def predict(
        self,
        inputs,
        *,
        model=None,
        model_name=None,
        model_display_name=None,
        feature_importance=False,
        project=None,
        region=None,
        **kwargs,
    ):
```

**kwargs passed to methods must be either (1) kwargs on the underlying method (`retry`, `timeout`, or `metadata`) or (2) attributes of the request object.

The following call is valid because `filter` is an attribute of `automl_v1beta1.ListDatasetsRequest`.

```py
from google.cloud import automl_v1beta1 as automl

client = automl.TablesClient(project=project_id, region=compute_region)

# List all the datasets available in the region by applying filter.
response = client.list_datasets(filter=filter)
```



## Enums and types


> **WARNING**: Breaking change

The submodule `enums` and `types` have been removed.

**Before:**
```py

from google.cloud import automl

gcs_source = automl.types.GcsSource(input_uris=["gs://YOUR_BUCKET_ID/path/to/your/input/csv_or_jsonl"])
deployment_state = automl.enums.Model.DeploymentState.DEPLOYED
```


**After:**
```py
from google.cloud import automl

gcs_source = automl.GcsSource(input_uris=["gs://YOUR_BUCKET_ID/path/to/your/input/csv_or_jsonl"])
deployment_state = automl.Model.DeploymentState.DEPLOYED
```


## Resource Path Helper Methods

The following resource name helpers have been removed. Please construct the strings manually.

```py
from google.cloud import automl

project = "my-project"
location = "us-central1"
dataset = "my-dataset"
model = "my-model"
annotation_spec = "test-annotation"
model_evaluation = "test-evaluation"

# AutoMlClient
annotation_spec_path = f"projects/{project}/locations/{location}/datasets/{dataset}/annotationSpecs/{annotation_spec}"
location_path = f"projects/{project}/locations/{location}"
model_evaluation_path = f"projects/{project}/locations/{location}/models/{model}/modelEvaluations/{model_evaluation}",

# PredictionServiceClient
model_path = f"projects/{project}/locations/{location}/models/{model}"
# alternatively you can use `model_path` from AutoMlClient
model_path = automl.AutoMlClient.model_path(project_id, location, model_id)

```