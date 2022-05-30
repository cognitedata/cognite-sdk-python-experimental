Quickstart
==========

.. WARNING::
  All of these extensions are experimental and subject to breaking changes. They should not be used in production code.

For a quickstart guide see the main SDK Documentation at https://cognite-docs.readthedocs-hosted.com/projects/cognite-sdk-python/en/latest/cognite.html

The currently available extensions for a `client` ( `CogniteClient`_) instance are:

* client.model_hosting = `Model Hosting`_
* client.annotations: `Annotations`_ (New Annotations API, see also the `API documentation <https://docs.cognite.com/api/playground/#tag/Annotations>`_ )
* client.entity_matching: Extensions for entity matching `Create Entity Matching Pipeline`_
* client.match_rules: New multi-field entity matching rules `Suggest match rules`_
* client.pnid_parsing: `Detect entities in a PNID`_
* client.diagrams: `Detect entities in Engineering Diagrams`_
* client.pnid_object_detection: `Detect common objects in a PNID`_
* client.functions: `Functions`_
* client.templates: `Extensions for Templates`_
* client.geospatial: `Geospatial`_

CogniteClient
-------------
.. autoclass:: cognite.experimental.CogniteClient
    :members:
    :member-order: bysource


Annotations
-----------

Retrieve an annotation by id
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.annotations.AnnotationsAPI.retrieve

Retrieve multiple annotations by id
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.annotations.AnnotationsAPI.retrieve_multiple

List annotation
^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.annotations.AnnotationsAPI.list

Create an annotation
^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.annotations.AnnotationsAPI.create

Suggest an annotation
^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.annotations.AnnotationsAPI.suggest

Update annotations
^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.annotations.AnnotationsAPI.update

Delete annotations
^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.annotations.AnnotationsAPI.delete

Data classes
^^^^^^^^^^^^
.. automodule:: cognite.experimental.data_classes.annotations
    :members:
    :show-inheritance:

Model Hosting
-------------

Models
^^^^^^
Retrieve model by name
~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.model_hosting.models.ModelsAPI.get_model

List models
~~~~~~~~~~~
.. automethod:: cognite.experimental._api.model_hosting.models.ModelsAPI.list_models

Create model
~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.model_hosting.models.ModelsAPI.create_model

Update model
~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.model_hosting.models.ModelsAPI.update_model

Deprecate model
~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.model_hosting.models.ModelsAPI.deprecate_model

Delete model
~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.model_hosting.models.ModelsAPI.delete_model

Perform online prediction
~~~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.model_hosting.models.ModelsAPI.online_predict


Model Versions
^^^^^^^^^^^^^^
Retrieve model version by name
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.model_hosting.versions.ModelVersionsAPI.get_model_version

List model versions
~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.model_hosting.versions.ModelVersionsAPI.list_model_versions

Create and deploy model version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.model_hosting.versions.ModelVersionsAPI.deploy_model_version

Create model version without deploying
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.model_hosting.versions.ModelVersionsAPI.create_model_version

Deploy awaiting model version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.model_hosting.versions.ModelVersionsAPI.deploy_awaiting_model_version

Update model version
~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.model_hosting.versions.ModelVersionsAPI.update_model_version

Deprecate model version
~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.model_hosting.versions.ModelVersionsAPI.deprecate_model_version

Delete model version
~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.model_hosting.versions.ModelVersionsAPI.delete_model_version


Model Version Artifacts
^^^^^^^^^^^^^^^^^^^^^^^
List artifacts for a model version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.model_hosting.versions.ModelVersionsAPI.list_artifacts

Upload an artifact from a file to a model version awating deployment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.model_hosting.versions.ModelVersionsAPI.upload_artifact_from_file

Upload artifacts from a directory to a model version awating deployment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.model_hosting.versions.ModelVersionsAPI.upload_artifacts_from_directory

Download an artifact for a model version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.model_hosting.versions.ModelVersionsAPI.download_artifact


Schedules
^^^^^^^^^
Retrieve schedule by name
~~~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.model_hosting.schedules.SchedulesAPI.get_schedule

List schedules
~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.model_hosting.schedules.SchedulesAPI.list_schedules

Create Schedule
~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.model_hosting.schedules.SchedulesAPI.create_schedule

Deprecate Schedule
~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.model_hosting.schedules.SchedulesAPI.deprecate_schedule

Delete Schedule
~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.model_hosting.schedules.SchedulesAPI.delete_schedule

Retrieve schedule logs
~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.model_hosting.schedules.SchedulesAPI.get_log


Source Packages
^^^^^^^^^^^^^^^
Retrieve source package by id
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.model_hosting.source_packages.SourcePackagesAPI.get_source_package

List source packages
~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.model_hosting.source_packages.SourcePackagesAPI.list_source_packages

Upload a source package
~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.model_hosting.source_packages.SourcePackagesAPI.upload_source_package

Build and upload a source package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.model_hosting.source_packages.SourcePackagesAPI.build_and_upload_source_package

Deprecate source package
~~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.model_hosting.source_packages.SourcePackagesAPI.deprecate_source_package

Delete source package
~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.model_hosting.source_packages.SourcePackagesAPI.delete_source_package

Download source package code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.model_hosting.source_packages.SourcePackagesAPI.download_source_package_code

Delete source package code
~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.model_hosting.source_packages.SourcePackagesAPI.delete_source_package_code

Data classes
^^^^^^^^^^^^
.. automodule:: cognite.experimental.data_classes.model_hosting.models
    :members:
    :show-inheritance:

.. automodule:: cognite.experimental.data_classes.model_hosting.versions
    :members:
    :show-inheritance:

.. automodule:: cognite.experimental.data_classes.model_hosting.schedules
    :members:
    :show-inheritance:

.. automodule:: cognite.experimental.data_classes.model_hosting.source_packages
    :members:
    :show-inheritance:

Contextualization
-----------------
These APIs will return as soon as possible, defering a blocking wait until the last moment. Nevertheless, they can block for a long time awaiting results.
For examples of using this api, see: https://github.com/cognitedata/cognite-sdk-python-experimental/blob/master/CONTEXTUALIZATION.md

Entity Matching Methods
^^^^^^^^^^^^^^^^^^^^^^^
See the main SDK documentation for most other methods.

Fit Entity Matching Model
^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.entity_matching.EntityMatchingAPI.fit


Suggest Match Fields
^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.entity_matching.EntityMatchingAPI.suggest_fields

Create Entity Matching Pipeline
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.entity_matching.EntityMatchingPipelinesAPI.create

Retrieve Entity Matching Pipelines
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.entity_matching.EntityMatchingPipelinesAPI.retrieve
.. automethod:: cognite.experimental._api.entity_matching.EntityMatchingPipelinesAPI.retrieve_multiple
.. automethod:: cognite.experimental._api.entity_matching.EntityMatchingPipelinesAPI.list

Run Entity Matching Pipeline
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.entity_matching.EntityMatchingPipelinesAPI.run

Delete Entity Matching Pipeline
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.entity_matching.EntityMatchingPipelinesAPI.delete

Retrieve Entity Matching Pipelines Run
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.entity_matching.EntityMatchingPipelineRunsAPI.retrieve
.. automethod:: cognite.experimental._api.entity_matching.EntityMatchingPipelineRunsAPI.retrieve_latest
.. automethod:: cognite.experimental._api.entity_matching.EntityMatchingPipelineRunsAPI.list

Suggest match rules
^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.match_rules.MatchRulesAPI.suggest

Apply match rules
^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.match_rules.MatchRulesAPI.apply

Detect entities in a PNID
^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.pnid_parsing.PNIDParsingAPI.detect

Extract tags from P&ID based on pattern
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.pnid_parsing.PNIDParsingAPI.extract_pattern

Convert a P&ID to an interactive SVG where the provided annotations are highlighted
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.pnid_parsing.PNIDParsingAPI.convert

Retrieve caches OCR results
^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.pnid_parsing.PNIDParsingAPI.ocr

Detect common objects in a PNID
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.pnid_object_detection.PNIDObjectDetectionAPI.find_objects


Detect entities in Engineering Diagrams
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.pnid_parsing.DiagramsAPI.detect

Convert to an interactive SVG where the provided annotations are highlighted
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.pnid_parsing.DiagramsAPI.convert



Contextualization Data Classes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: cognite.experimental.data_classes.contextualization
    :members:
    :undoc-members:
    :show-inheritance:
    :inherited-members:

Plot Data Extraction
--------------------

Extract curve data
^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.plot_extraction.PlotDataExtractionAPI.extract

Functions
---------

Create function
^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.functions.FunctionsAPI.create

Delete function
^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.functions.FunctionsAPI.delete

List functions
^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.functions.FunctionsAPI.list

Retrieve function
^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.functions.FunctionsAPI.retrieve

Retrieve multiple functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.functions.FunctionsAPI.retrieve_multiple

Call function
^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.functions.FunctionsAPI.call


Function calls
^^^^^^^^^^^^^^
List function calls
~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.functions.FunctionCallsAPI.list

Retrieve function call
~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.functions.FunctionCallsAPI.retrieve

Retrieve function call response
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.functions.FunctionCallsAPI.get_response

Retrieve function call logs
~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.functions.FunctionCallsAPI.get_logs

Function schedules
^^^^^^^^^^^^^^^^^^
List function schedules
~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.functions.FunctionSchedulesAPI.list

Create function schedule
~~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.functions.FunctionSchedulesAPI.create

Delete function schedule
~~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.functions.FunctionSchedulesAPI.delete

Data classes
^^^^^^^^^^^^
.. automodule:: cognite.experimental.data_classes.functions
    :members:
    :show-inheritance:


Extensions for Templates
------------------------
The main templates SDK is available through the main sdk.

Get suggestions for missing entries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.templatecompletion.TemplateCompletionAPI.complete

Geospatial
------------------------
.. note::
    Check https://github.com/cognitedata/geospatial-examples for some complete examples.

Rasters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Put Raster
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.geospatial.ExperimentalGeospatialAPI.put_raster

Delete Raster
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.geospatial.ExperimentalGeospatialAPI.delete_raster

Get Raster
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.geospatial.ExperimentalGeospatialAPI.get_raster

Mapbox Vector Tiles (MVTs)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create MVT Mappings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.geospatial.ExperimentalGeospatialAPI.create_mvt_mappings_definitions

Delete MVT Mappings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.geospatial.ExperimentalGeospatialAPI.delete_mvt_mappings_definitions

Retrieve MVT Mappings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.geospatial.ExperimentalGeospatialAPI.retrieve_mvt_mappings_definitions

Data classes
^^^^^^^^^^^^
.. automodule:: cognite.experimental.data_classes.geospatial
    :members:
    :show-inheritance:
