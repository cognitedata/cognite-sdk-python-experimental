Quickstart
==========

.. WARNING::
  All of these extentions are experimental and subject to breaking changes. They should not be used in production code.

For a quickstart guide see the main SDK Documentation at https://cognite-docs.readthedocs-hosted.com/projects/cognite-sdk-python/en/latest/cognite.html

The currently available extensions for a `client` ( `CogniteClient`_) instance are:

* client.assets: `Assets`_ (Playground Assets API with Types support)
* client.assets_v1: Equivalent to client.assets in the base SDK
* client.types: `Types`_
* client.model_hosting = `Model Hosting`_
* client.datapoints: includes extensions described in `Synthetic time series`_
* client.relationships: `Relationships`_
* client.entity_matching: `Fit Entity Matching Model`_ and  `Create Entity Matching Rules`_
* client.entity_extraction: `Extract Entities from Files`_
* client.pnid_parsing: `Parse PNID`_
* client.resource_typing: `Fit Resource Typing Model`_


CogniteClient
-------------
.. autoclass:: cognite.experimental.CogniteClient
    :members:
    :member-order: bysource


Assets
------
The assets API is currently duplicated in the
experimental package to support testing of the types feature in playground.
Note that asset objects passed to this API should be created using the data type from the experimental package (``cognite.experimental.data_classes``).

Retrieve an asset by id
^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.assets.ExperimentalAssetsAPI.retrieve

Retrieve multiple assets by id
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.assets.ExperimentalAssetsAPI.retrieve_multiple

Retrieve an asset subtree
^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.assets.ExperimentalAssetsAPI.retrieve_subtree

List assets
^^^^^^^^^^^
.. automethod:: cognite.experimental._api.assets.ExperimentalAssetsAPI.list

Search for assets
^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.assets.ExperimentalAssetsAPI.search

Create assets
^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.assets.ExperimentalAssetsAPI.create

Create asset hierarchy
^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.assets.ExperimentalAssetsAPI.create_hierarchy

Delete assets
^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.assets.ExperimentalAssetsAPI.delete

Update assets
^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.assets.ExperimentalAssetsAPI.update

Data classes
^^^^^^^^^^^^
.. automodule:: cognite.experimental.data_classes.assets
    :members:
    :show-inheritance:


Relationships
-------------

Retrieve a relationship by id
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.relationships.RelationshipsAPI.retrieve

Retrieve multiple relationships by id
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.relationships.RelationshipsAPI.retrieve_multiple

List relationships
^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.relationships.RelationshipsAPI.list

Create a relationship
^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.relationships.RelationshipsAPI.create

Delete relationships
^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.relationships.RelationshipsAPI.delete

Data classes
^^^^^^^^^^^^
.. automodule:: cognite.experimental.data_classes.relationships
    :members:
    :show-inheritance:

Synthetic time series
---------------------

Calculate the result of a function on time series
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.synthetic_time_series.SyntheticDatapointsAPI.retrieve


Types
-----

Retrieve a type definition by id
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.types.TypesAPI.retrieve

Retrieve multiple type definitions by id
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.types.TypesAPI.retrieve_multiple

List type definitions
^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.types.TypesAPI.list

Create type definitions
^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.types.TypesAPI.create

Delete type definitions
^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.types.TypesAPI.delete

Update type definitions
^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.types.TypesAPI.update

Data classes
^^^^^^^^^^^^
.. automodule:: cognite.experimental.data_classes.types
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

Fit Entity Matching Model
^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.entity_matching.EntityMatchingAPI.fit

Create Entity Matching Rules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.entity_matching.EntityMatchingAPI.create_rules

Fit Resource Typing Model
^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.resource_typing.ResourceTypingAPI.fit

Parse PNID
^^^^^^^^^^
.. automethod:: cognite.experimental._api.pnid_parsing.PNIDParsingAPI.parse

Extract Entities from Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automethod:: cognite.experimental._api.entity_extraction.EntityExtractionAPI.extract

Contextualization Data Classes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: cognite.experimental.data_classes.contextualization
    :members:
    :undoc-members:
    :show-inheritance:
    :inherited-members:

