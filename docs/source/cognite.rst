Quickstart
==========

.. WARNING::
  All of these extensions are experimental and subject to breaking changes. They should not be used in production code.

For a quickstart guide see the `documentation for the main SDK <https://cognite-sdk-python.readthedocs-hosted.com>`_.

The currently available extensions for a `client` (`CogniteClient`_) instance are:

* client.entity_matching: Extensions for entity matching `Create Entity Matching Pipeline`_
* client.match_rules: New multi-field entity matching rules `Suggest match rules`_
* client.pnid_parsing: `Detect entities in a PNID`_
* client.templates: `Extensions for Templates`_
* client.geospatial: `Geospatial`_
* client.alerts: `Alerting`_
* client.simulators: `Simulators`_

CogniteClient
-------------
.. autoclass:: cognite.experimental.CogniteClient
    :members:
    :member-order: bysource


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



Contextualization Data Classes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: cognite.experimental.data_classes.contextualization
    :members:
    :undoc-members:
    :show-inheritance:
    :inherited-members:

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

List MVT Mappings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.geospatial.ExperimentalGeospatialAPI.list_mvt_mappings_definitions

Compute
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Compute
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.geospatial.ExperimentalGeospatialAPI.compute

Data classes
^^^^^^^^^^^^
.. automodule:: cognite.experimental.data_classes.geospatial
    :members:
    :show-inheritance:

Alerting
--------

Channels
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
A Channel is a bus to which Subscribers can make a Subscription and that Alerts can be sent to. Upon the receival of an Alert, a notification is sent on all registered providers of its Subscribers. A Channel can have a Parent, Alerts are propagated recursively from a Channel to its Parent and all of their Parents.

List channels
~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.alerts.AlertChannelsAPI.list

Create channels
~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.alerts.AlertChannelsAPI.create

Update channels
~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.alerts.AlertChannelsAPI.update

Delete channels
~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.alerts.AlertChannelsAPI.delete

Alerts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
An Alert is an event detected by a monitoring system, raised to trigger a notification. The Alert is linked to a channel, and upon Alert creation, a Notification sent to all subscribers of the Channel and the Channels' parents

List alerts
~~~~~~~~~~~
.. automethod:: cognite.experimental._api.alerts.AlertsAPI.list

Create alerts
~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.alerts.AlertsAPI.create

Close alerts
~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.alerts.AlertsAPI.close

Subscribers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Subscribers are the people or groups thereof that should be notified when an Alert is fired. Subscribers can subscribe to multiple Channels

Create subscribers
~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.alerts.AlertSubscribersAPI.create

Subscriptions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Subscriptions link subscribers to channels, subscribing them to Alerts sent to the channel or channels that are children of that channel

Create subscriptions
~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.alerts.AlertSubscriptionsAPI.create

Delete subscriptions
~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.alerts.AlertSubscriptionsAPI.delete

Data classes
^^^^^^^^^^^^
.. automodule:: cognite.experimental.data_classes.alerts
    :members:
    :show-inheritance:

Simulators
----------

Simulation Runs
^^^^^^^^^^^^^^^

Run a simulation routine
~~~~~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.simulators.SimulatorsAPI.run

List simulation runs
~~~~~~~~~~~~~~~~~~~~
.. automethod:: cognite.experimental._api.simulators.SimulatorsAPI.list_runs

Data classes
^^^^^^^^^^^^
.. automodule:: cognite.experimental.data_classes.simulators
    :members:
    :show-inheritance:
