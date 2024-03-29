# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Changes are grouped as follows
- `Added` for new features.
- `Changed` for changes in existing functionality.
- `Deprecated` for soon-to-be removed features.
- `Removed` for now removed features.
- `Fixed` for any bug fixes.
- `Security` in case of vulnerabilities.

## [1.0.0]

### Changed
  - Bump core SDK to 7.21.1 with major changes.
### Removed
  - Removed all experimental features related to contextualization.

## [0.118.0]

### Changed
 - Hosted extractors support have been updated to comply with the new beta version.

## [0.117.0]
### Removed
- Annotations (v1 API), which are available as part of the regular SDK. See  also
[the documentation](https://cognite-sdk-python.readthedocs-hosted.com/en/latest/data_organization.html#annotations).

## [0.116.0]
### Deprecated
- Legacy annotations, as announced earlier. This will  be removed in a next version.

## [0.115.0]

### Added
 - List and filter simulation runs

## [0.114.0]

### Added
 - Pluto API (Hosted extractors alpha)

## [0.113.2]

### Changed
- Update regex version

## [0.113.1]

### Fixed
- Lock cognite-sdk version to major only

## [0.113.0]

### Added
- Simulators API to run a single simulation

## [0.112.0]

### Changed
- Increase cognite-sdk major version (5 -> 6)

### Fixed
- Lock cognite-sdk version

## [0.111.0]

### Removed
- removed `/findobjects` in Pnid Object Detection as it has been deprecated

### Changed
- mark /alerts/deduplicate as retryable (`client.alerts.deduplicated(...)`)

## [0.110.0]

### Changed
- Increased cognite-sdk major version pin. (4 -> 5)

## [0.109.1]

### Fixed
- Added missing state to GeospatialTask

## [0.109.0]

### Added
- Geospatial create_tasks(...) and get_tasks(...)


## [0.108.2]

### Fixed
- Fixed create deduplicated alert function signature

## [0.108.1]

### Fixed
- Fixed geospatial compute conflict with base SDK

## [0.108.0]

### Added
- Add deduplication endpoint to the alert module.
- Fix existing alerts api tests and add new tests.

## [0.107.0]

### Changed
- Fixed geospatial compute behavior when into_feature_type option is used

## [0.106.0]

### Changed
- Move geospatial raster operations into core SDK

## [0.105.0]

### Fixed
- Dependency specification for `cognite-sdk`; now requiring major version 4
- Bug where the code would try to mutate a now-removed set of path suffixes

## [0.104.0]

### Added

- Support for into_feature_type parameter for the geospatial compute(...) method.

## [0.103.0]

### Added

- Support for left joins in the geospatial compute(...) method.

## [0.102.0]

### Added

- Support for order_by in the geospatial compute(...) method.
- More examples to the compute(...) method

## [0.101.0]

### Removed

- Support for cognite-sdk-core

### Added

- Support for cognite-sdk:4.x.x

### Changed

- CogniteClient constructor to use the new ClientConfig type in cognite-sdk:4.x.x

## [0.100.0]

### Added

- Support for group_by in the geospatial compute(...) method.

## [0.99.0]

### Removed

- Removed everything vision-related as they are now in V1

## [0.98.0]

### Added

- Implemented support for the geospatial upsert_features(...) method.

## [0.97.0]

### Changed

- Update the alert prefix from `/alerts/alerts` to `/alerts`.

## [0.96.0]

### Fixed

- Import statement for ClientConfig conflicting with v4 of `cognite-sdk`.

## [0.95.0]

### Added

- Implemented support for providing feature parameters to `client.vision.extract`

## [0.94.1]

### Added

- Quickstart guide for Vision extract method.

## [0.94.0]

### Removed

- Moved Functions from cognite-sdk-experimental cognite-sdk.

## [0.93.0]

### Added
- Method to revert extraction pipeline config revisions.
- Option to retrieve specific config revision, or retrieve config active at specific time.

## [0.92.0]

### Changed
- Renamed Vision's annotate method to extract
- Updated Vision data classes

### Added
- Method to save predictions made by Vision's extract method (previously called annotate) in CDF using the Annotations API
- Method to retrieve a Vision feature extraction job by job id.

## [0.91.1]

### Added
- Add example for Vision's annotate method

## [0.91.0]

### Added
- Add annotate method for the Vision API

## [0.90.0]

### Added
- properly expose alerts API data_classes

## [0.89.0]

### Added
- added status endpoint calls to functions sdk

## [0.88.0]

### Added
- alerts API (alpha)

## [0.87.0]

### Removed
- Removed plot extractor as it is not in use anymore.

## [0.86.0]

### Added
- added validation of requirements.txt when uploading function from a folder

## [0.85.0]

### Added
- added parsing of requirements from docstring when uploading Cognite Function from function-handle.

## [0.84.0]

### Removed

- diagrams API (has been moved to the stable SDK)

## [0.83.0]

### Changed

- More examples for the geospatial compute method.

## [0.82.0]

### Changed

- Renamed `client.annotations.*` to `client.legacy_annotations.*` and renamed corresponding (data) class and filenames accordingly.
- Renamed `client.annotations_v2.*` to `client.annotations.*` and renamed corresponding (data) class and filenames accordingly.

#### Removed

- Removed documentation for legacy `annotations` (now called `legacy_annotations`), which will soon be deprecated.

## [0.81.0]

### Removed

- `linked_resource_id`, `linked_resource_external_id` and `linked_resource_type` fields to AnnotationsV2.

## [0.80.0]

### Added

- `runtime_version` property to `Function` class.

## [0.79.2]

### Changed

- Geospatial: Dataset support

## [0.79.1]

### Removed

- assets playground API
- types playground API

## [0.79.0]

### Added

- AnnotationsV2 `/suggest` endpoint as `client.annotations_v2.suggest`

### Fixed

- integration tests for AnnotationsV2 update endpoints

## [0.78.0]

### Removed

- Model hosting API

## [0.77.0]

### Added

- Initial Geospatial /compute endpoint support

## [0.76.0]

### Added

- Extraction pipelines config endpoints

### Removed

- Other extraction pipelines functionality in favour of those from the main SDK

## [0.75.0]

### Added

- AnnotationsV2: Support for filtering the annotations data field

## [0.74.1]

### Changed

- Use `v1` sessions endpoint instead of `playground` in functions api.

## [0.74.0]

### Added

- Optional argument `extra_index_urls` and `index_url` to `FunctionsAPI.create` which enables the users to install pip packages from private repositories via adding extra index URLs to Python package manager.

## [0.73.0]

### Changed

- Geospatial: Support pushing and getting raster with crs conversion

## [0.72.0]

### Added

- Geospatial: list MVT mappings definitions

## [0.71.1]

### Fixed

- Geospatial: follow api raster id renaming into rasterPropertyName

## [0.71.0]

### Added

- Geospatial: create, delete and retrieve MVT mappings definitions

## [0.70.1]

### Fixed

- Geospatial rasters: url encode the feature external id and the raster id

## [0.70.0]

### Added

- Geospatial: Get raster data

## [0.69.0]

### Added

- Optional argument `metadata` to `FunctionsAPI.create` which allows metadata in the form of key:value pairs of strings to be added to each function.

## [0.68.3]

### Fixed

- Vision:
  - [certain types are not correctly converted to camelcase, causing a 400 bad request](https://github.com/cognitedata/cognite-sdk-python-experimental/pull/287)


## [0.68.2]

### Added

- Geospatial:
  - [Delete a raster from a feature raster property](https://pr-1632.specs.preview.cogniteapp.com/v1.json.html#operation/deleteRaster)

### Changed

- Fixed typehint for argument `runtime` in `FunctionsAPI.create().`

## [0.68.1]

### Fixed

- Widen typing-extension version to allow v4.

## [0.68.0]

### Added

- Geospatial:
  - [Put a raster into a feature raster property](https://pr-1632.specs.preview.cogniteapp.com/v1.json.html#operation/putRaster)


## [0.67]

### Changed

- `cognite-sdk-experimental` now depends on `cognite-sdk-core` instead of `cognite-sdk`.


## [0.66.1]

### Fixed
- pyproject now allows regex version 2020 - 2022


## [0.66]

### Added
- Method `FunctionsAPI.limits` which returns information about limits associated with the CDF project the user is logged in to.

## [0.65]

### Added

- VisionAPI: playground endpoints:
  - [Detect external ID or name of assets in files](https://docs.cognite.com/api/playground/#operation/visionTagDetection)
  - [Retrieve detected external ID or name of assets in files](https://docs.cognite.com/api/playground/#operation/visionTagDetectionRetrieve)

## [0.64]

### Added

- Optional argument `runtime` to `FunctionsAPI.create` which dictates the function runtime. Valid values are `["py37", "py38", "py39", None]` and `None` translates to the API default.

## [0.63]

### Changed
- GeospatialAPI: create_features, update_features, search_features, stream_features, retrieve_features,
aggregate_features and delete_features to use feature_type_external_id

## [0.62]

### Added
- Experimental annotations_v2 implementation, providing access to the corresponding [AnnotationsV2 API](https://docs.cognite.com/api/playground/#tag/Annotations).
    - Added `AnnotationV2`, `AnnotationV2Filter`, `AnnotationV2Update` dataclasses to `cognite.experimental.data_classes`
    - Added `annotations_v2` API to `cognite.experimental.CogniteClient`
    - **Create** annotations with `client.annotations_v2.create` passing `AnnotationV2` instance(s)
    - **Delete** annotations with `client.annotations_v2.delete` passing the id(s) of annotation(s) to delete
    - **Filter** annotations with `client.annotations_v2.list` passing a `AnnotationV2Filter `dataclass instance or a filter `dict`
    - **Update** annotations with `client.annotations_v2.update` passing updated `AnnotationV2` or `AnnotationV2Update` instance(s)
    - **Get single** annotation with `client.annotations_v2.retrieve` passing the id
    - **Get multiple** annotations with `client.annotations_v2.retrieve_multiple` passing the ids

## [0.61]

### Removed
- Experimental transformations implementation. Transformations is now part of the official python sdk, just need to change your transformations data class imports from `cognite.experimental` to `cognite.client`.

## [0.60.38]

### Fixed
- Geospatial: update to reflect API endpoint change for listing CRSes

## [0.60.37]

### Changed
- When creating a function with `function_handle` or `folder` and with `external_id` specified, the zip file uploaded to the Files API is given an external-id and is overwritten if it already exists.

## [0.60.36]

### Changed
- Geospatial: breaking change, attribute becomes property, following the api terminology

## [0.60.35]

### Fixed
- Geospatial: log should not consume streaming content.
- Geospatial: throw CogniteConnectionError when streaming connection closes

## [0.60.34]

### Fixed
- Geospatial: follow api changes regarding allowCrsTransformation and delete recursive options.

## [0.60.33]

### Changed
- Make geopandas and shapely dependencies optional

## [0.60.32]

### Changed
- Geospatial search: update to reflect API change in order_by

## [0.60.31]

### Changed
- Geospatial new path support and new feature type update format support.

## [0.60.30]

### Added
- new filter by `transformation_external_id` for `transformations.jobs.list()`.

## [0.60.29]

### Changed
- `transformation.job.raw_query` renamed to `query`, because of API changes.

## [0.60.28]

### Removed
- `transformation_schedules.retrieve_multiple()` no longer acepts `is_public` parameter, it's asumed the user wants to retrieve the given ids either they are marked as public or not.
- internal changes in the way `transformation.preview()` sends its parameters to the backend.

## [0.60.27]

### Added
- Geospatial: support `allow_crs_transformation` for creating, updating and searching features.

## [0.60.26]

### Fixed
- added `TransformationBlockedInfo` `time` property to fix decoding `Transformation` objects.

## [0.60.25]

### Added
- added `from_geopandas` static method to `FeatureList`.

## [0.60.23]

### Added
- added `to_geopandas` method on `FeatureList`.

## [0.60.22]

### Fixed
- `str(TransformationJobMetric)`, `str(TransformationJob)`, `str(TransformationNotification)` and `str(TransformationSchedule)` no longer throw an exception.

## [0.60.21]

### Added
- added `destination` filter on `TransformationNotificationsAPI.list()`.

## [0.60.20]

### Added
- added `Transformation.running_job`, `Transformation.last_finished_job`, `Transformation.schedule` and `Transformation.blocked` fields.

## [0.60.19]

### Fixed
- `str(TransformationPreviewResult)` no longer throws an exception.

## [0.60.18]

### Added
- added support for `ignore_unknown_ids` parameter in `transformations.retrieve_multiple` and `transformations.delete`.

## [0.60.17]

### Changed
- Dependencies upgrade

## [0.60.16]

### Added
- added `transformationsAPI.preview()` method, to preview the result of a query before running a transformation.

## [0.60.15]

### Added
- optional `timeout` parameter for `TransformationJob.wait()` and `TransformationJob.wait_async()` methods.

## [0.60.14]

### Added
- `GeospatialAPI.stream_features` method to stream features.

## [0.60.13]

### Added
- `GeospatialAPI.update_feature_types` method to update feature types.

## [0.60.12]

### Changed
- `TransformationDestination.raw()` now uses `type = 'raw'` istead of `'raw_table'` and doesn't use deprecated `raw_type` parameter.

## [0.60.11]

### Added
- `TransformationJobsAPI.list_metrics` method to retrieve job metrics.
- `transformations.jobs.retrieve_multiple` method to get multiple jobs by id in a single API call.

## [0.60.10]

### Added
- `oicdCredentials.audience` parameter for transformations.

## [0.60.9]

### Added
- `transformation_id` parameter in `TransformationJobsAPI.list()`, to list only the jobs associated with a given transformation.

## [0.60.8]

### Added
- `TransformationsApi.retrieve_multiple` method, to get multiple transformations from the backend in a single request.

## [0.60.6]

### Added
- `TransformationJob.transformation_id` field to asossiate a job with it's source transformation.

## [0.60.5]

### Changed
- `transformations.notifications`now uses `transformation_id` and `transformation_external_id` instead of `config_id` and `config_external_id`.

## [0.60.4]

### Added
- `transformations.jobs` api client, which retrieves the  status of transformation runs.
- `transformations.run` method, which runs transformations.

## [0.60.4]

### Changed
- Extraction pipeline entity updated to be same with API entity.

## [0.60.3]

### Added
- `transformations.schema` api client, which allows the retrieval of the expected schema of sql transformations based on the destination data type.

## [0.60.2]

### Changed
- `FunctionsAPI.call` and `FunctionSchedulesAPI.create` fail with CogniteAPIError if the request to the sessions API is unsuccesful (instead of creating calls/schedules without sessions).

## [0.60.1]

### Added
- `transformations.schedules.retrieve_multiple` to retrieve multiple transformation schedules by transformation ids and external ids.

## [0.59.3]

### Fixed
- Classes `DiagramDetectResults` and `DiagramConvertResults` return items-property correctly when the job is not completed.

## [0.59.2]

### Added
- `transformations.notifications` api client, which allows the creation, deletion and retrieval of transformation email notifications.

## [0.59.1]

### Changed
- In `FunctionsAPI.create`, the default value of `cpu` is changed from `0.25` to `None`, thus deferring the default value to the API, which also is `0.25`. The argument is unavailable in Azure.
- In `FunctionsAPI.create`, the default value of `memory` is changed from `1.0` to `None`, thus deferring the default value to the API, which also is `1.0`. The argument is unavailable in Azure.

## [0.59]

### Added
- `transformations` api client, which allows the creation, deletion, update and retrieval of transformations.
- `transformations.schedules` api client, which allows the schedule, unschedule and retrieval of recurring runs of a transformation.

## [0.57.1]

### Added
- `session_id` property to `FunctionSchedule` class, which is the id of the session started when creating a schedule with client credentials.

## [0.57.0]

### Changed
- `FunctionSchedulesAPI.list()` now accepts the argument `function_id`. The arguments `function_external_id` and `function_id` are mutually exclusive.
- `Function.list_schedules()` lists schedules attached to the function with both `function_id` and `function_external_id`.

## [0.56.1]

### Fixed

- Bug: `FunctionSchedulesAPI.create` did not pass `function_id` to request body.

## [0.56.0]

### Changed
- Rename Integrations to Extraction Pipelines.

## [0.55.0]

### Added
- Add functionality to filter integration runs. Some new fields added to integration entity.

## [0.54.0]

### Changed
- `FunctionSchedulesAPI.create` now requires `function_id` to be used when creating a schedule with OIDC through `client_credentials`.
- `FunctionSchedulesAPI.create`: The arguments `function_id` and `function_external_id` are both optional and mutually exclusive.
- `FunctionSchedulesAPI.create`: The argument `function_external_id` has changed position, necessitated by the fact that it is now optional.

### Fixed
- Correct error message when specifying both `function_id` and `function_external_id` on methods `FunctionCallsAPI.list()`, `FunctionCallsAPI.retrieve()`, `FunctionCallsAPI.get_response()` and `FunctionCallsAPI.get_logs()`.

## [0.53.1]

### Fixed
- `FunctionsAPI.call` previously didn't pass the session `nonce` if `data` was set to `None`. This is now fixed.

## [0.53.0]

### Changed
- `FunctionsAPI.call` now uses OIDC tokens if the client was instantiated with a token or client credentials.
- `FunctionSchedulesAPI.create` now supports OIDC tokens through the use of client-credentials, explicitly passed in as an argument.

## [0.52.0]

### Fixed
- `FunctionsAPI.list()` and `FunctionSchedulesAPI.list()` with argument `limit` equal to `None`, `float(inf)` or `-1` now returns all resources. Previously, the default limit of the API was used (100).

## [0.51.0]

### Fixed
- Fixed Templates API

## [0.50.0]

### Added
- Diagrams API

### Removed
- Unstructured API (due to lack of maintenance)
- Templates API (now available in the main SDK). Note that template completion is still available.

## [0.49.0]
### Added
- Update method for the annotations API

## [0.48.2]

### Fixed
- `FunctionsAPI.list()` and `FunctionSchedulesAPI.list()` were missing `cognite_client` from a bug introduced in version [0.47.0].

## [0.48.1]

### Fixed
- Image parameter for plot data extraction

## [0.48.0]

### Added
- replacements parameter in entity matching fit
- suggest fields endpoint in entity matching

## [0.47.0]

### Changed

- The `FunctionsAPI.list()`-method now accepts additional filters: `name`, `owner`, `file_id`, `status`, `external_id_prefix` and `created_time`.
- The `FunctionSchedulesAPI.list()`-method now accepts additional filters: `name`, `function_external_id`, `created_time` and `cron_expression`.
- The `Function.list_schedules()`-method now accepts `limit` argument.

## [0.46.0]

### Added
- Add functionality to add/remove elements in integration list fields.

## [0.45.2]

### Fixed

- The `Function.list_schedules()`-method now correctly returns all schedules tied to the function.

## [0.45.0]

### Added
- Possibility to detect entities with multiple names, as this is now a feature in the API.
- Same functionality in document detect.

## [0.44.0]

### Changed
- Domains/schemas/universes/domains are now consistently called templates in the SDK, and the completion functions are moved to `client.templates.completion`
- Annotations filter updated with additional fields, and to reflect annotated resource type being mandatory.

## [0.43.0]

### Added
- Possibility to add environment variables to functions via the new argument `env_vars` of the `FunctionsAPI.create()` method.
- Optional argument `limit` to `Function.list_calls()`

## [0.42.0] - 21-02-01

### Added
- Template functionality.

### Removed
- Playground relationships.

## [0.41.0] - 2020-01-19

### Added
- New entity match rules endpoints are available in `client.match_rules`

### Changed
- EntityMatchingPipeline update accepts its own suggested rules, despite extra fields.

### Fixed
- Better exception checks for missing packages in notebook output.
- Fixed missing column error in dataframe in notebook output.

## [0.40.1] - 2020-01-19
### Changed
- PNID detect no longer blocks, entities passed as a dict are resolved in the `.matches` helper method.

## [0.40] - 2020-01-19

### Changed
- Richer output for entity matching pipelines and PNID jobs in notebooks
- More specific job types returned from these endpoints, with helper methods that make processing and visualizing output easier.

### Added
- OCR method for PNID parsing

## [0.39] - 2021-01-18
### Changed
- Integrations and IntegrationRuns data classes updated with new fields.

## [0.38] - 2020-01-12
### Changed
- The following methods now accepts a `limit`-parameter, with default of 25, that controls how many elements the methods return:
`FunctionCallAPI.list`, `FunctionAPI.list`, and `FunctionScheduleAPI.list`.
- Removed `data` property from `FunctionSchedule` class.

## [0.37] - 2020-01-11
### Changed
- The `complete` method of the schema completion api was renamed to `complete_type`
### Added
- Method `complete_domain` to schema completion

## [0.36] - 2020-01-05
### Changed
- The `FunctionCallAPI.retrieve` method now utilizes `retrieve_multiple` in the backend. `/calls` -> `/calls/byids`
### Added
- Method `retrieve` to `FunctionScheduleAPI`-class.

## [0.35] - 2020-12-14
### Added
- Added IntegrationsAPI and IntegrationRunsAPI

## [0.34] - 2020-12-08
### Added
- Added relationships_label and use_existing_matches to pipelines

## [0.33.0] - 2020-12-02
### Added
- Method `get_input_data` on the `FunctionSchedule`-class.
- Method `get_input_data` on the `FunctionScheduleAPI`-class.

## [0.32.0] - 2020-12-03
### Fixed
- Fix the client initialization to correctly pass all keyword arguments.

## [0.31.2] - 2020-12-03
### Fixed
- Fix the filter functionality of `annotations`

## [0.31.1] - 2020-11-30
### Added
- Argument `function_call_info` to the definition of the `handle` function. This argument is a dictionary with keys `function_id` and, if the call is scheduled, `schedule_id` and `scheduled_time`.
- Property `scheduled_time` on `FunctionCall` class.

## [0.31.0] - 2020-11-25
### Changed
- Core entity matching moved to beta client, experimental now extends this.

## [0.30.0] - 2020-11-22
### Fixed
- Pnid Object Detection GET endpoint fixed after separation between `/findobjects` and `/findsimilar`

## [0.29.0] - 2020-11-09
### Added
- Arguments `confirmed_matches` and `schedule_interval` for EntityMatchingPipeline
- Method `retrieve_latest` for entity matching pipeline run.
- Various helper methods on EntityMatchingPipeline and EntityMatchingPipelineRun
- EntityMatchingPipeline Update class and method

## [0.28.0] - 2020-10-27
### Changed
- Renamed match_from and match_to in entity matcher, as well as timestamp->time in contextualization jobs.
- Entity matching matches renamed to true_matches

### Added
- Entity matching pipelines rejected_matches and score_threshold options

### Fixed
- Entity matching pipelines now correctly takes model_parameters instead of model_id

## [0.27.0] - 2020-10-20
### Added
- Plot Data Extraction API

## [0.26.0] - 2020-10-09
### Added
- AnnotationsAPI with create, list, retrieve, retrieve_multiple, delete functionalities

## [0.25.0] - 2020-10-08
### Changed
- Entity matcher fields renamed, and added a new format for true_matches. complete_missing -> ignore_missing_fields, keys_from_to -> match_fields.

## [0.24.0] - 2020-10-01
### Changed
- Inherit from the `beta` client
- Old relationships moved to `.relationships_playground`, as beta client contains the new version.
- Entity extraction removed as the API no longer exists.

## [0.23.1] - 2020-10-01
### Added
- Arguments `cpu` and `memory` to `FunctionsAPI.create()`, making it possible to customize function resources.

## [0.23.0] - 2020-09-29
### Added
- Entity matching pipelines, which allows you to deploy an entity matching model with confirmed matches and rules.

### Changed
- Entity matching list calls have a limit parameter which defaults to 100.
- ContextualizationJobs now have timestamp fields consistently as members, and no longer return them in result.

## [0.22.3] - 2020-09-15
### Changed
- `/fit` in entity matcher supports defining which field in matchFrom and matchTo to use as the id field by specifying `id_field`

## [0.22.2] - 2020-09-14
### Changed
- `/detect, /convert, /extractpattern, /ocr` supports referring to a file using file_id and/or file_external_id. file_id and file_external_id are returned in the responses.

## [0.22.1] - 2020-09-09
### Added
- `/detect` in Pnid Parser can accept entities with type `List[Union[str, dict]]` and returns `entities` if the type of input `entities` has type of `List[dict]`

## [0.22.0] - 2020-09-09
### Added
- Added `/findobjects` in Pnid Object Detection

## [0.21.0] - 2020-09-09
### Removed
- Removed `/parse` in Pnid Parser
### Added
- Added `/convert` in Pnid Parser

## [0.20.1] - 2020-09-07
### Fixed
- Fix in EntityMatcher predict method.

## [0.20.0] - 2020-09-01
### Added
- Entity matcher `predict` and `refit` methods now exist on `client.entity_matching` in addition to the model object.

## [0.19.0] - 2020-08-31
### Changed
- Entity matcher methods now all take and return `id` instead of `model_id` and accept `id` or `external_id`.
- Entity matcher uses the new `/entitymatching` endpoints

### Removed
- `fit_ml` and `predict_ml` methods in entity matcher.

## [0.18.0] - 2020-08-25
### Added
- Add py.typed file to inform that package is typed

## [0.17.0] - 2020-08-20
### Changed
- Some methods in entity matcher now take `id` instead of `model_id`

### Added
- Update and retrieve_multiple methods for entity matcher.
- Changed entity matching methods to take external_id where possible.

## [0.16.0] - 2020-08-13
### Changed
- Change list-method to list all models instead of jobs.
- Changed endpoints used for list and list_jobs to comply with updates to the API.
### Added
- Add list_jobs-method that behaves as old list-method, that is returns all jobs.
- Option to filter returned models on based on all input parameters.

## [0.15.4] - 2020-08-13
### Added
- Add name, description and external-id parameters to fit entity matcher.

## [0.15.3] - 2020-08-13
### Fixed
- Fix `import time` bug in functions.

## [0.15.2] - 2020-08-13
### Added
- Insert sleep cycles for files api queries in functions creation

## [0.15.1] - 2020-08-10
### Added
- Add model info for entity matcher models (classifier, feature_type, model_to, keys_from_to) to the output of retrieve.

## [0.15.0] - 2020-08-10
### Changed
- Changed name of the parameter indicating the type of features created from model_type to feature_type, entity matcher.

## [0.14.5] - 2020-08-07
### Added
- Allow users to specify custom path to handle function by setting function_path.

## [0.14.4] - 2020-08-06
### Removed
- Removed everything related to resource typing (contextualization).

## [0.14.3] - 2020-08-06
### Added
- A class for Document parsing, allowing detecting entity in documents
- Detect function also for pnid, similar to the old parse function, which may get deprecated
- min_tokens parameter for entity detecting endpoints. Allowing to set the mimimum number of tokens needed for a detection

## [0.14.2] - 2020-08-05
### Changed
- Renamed refitml refit entity matcher.

## [0.14.1] - 2020-08-03
### Added
- Added retry to functions POST endpoints.

## [0.14.0] - 2020-08-03
### Changed
- Merge fit_ml and fit, and predict_ml and predict endpoints entity matcher - major changes to required parameters and responses.

## [0.13.0] - 2020-07-23
### Changed
- Base version of the SDK changed to 2.x

## [0.12.1] - 2020-07-07
### Added
- The entity matching methods now have additional options for classifier and feature types.
- PNID detect patterns endpoint added.
- Schema completion endpoint added.

## [0.12.0] - 2020-07-07
### Changed
- Synthetic time series and labels removed, as they were moved to non-experimental status in the main SDK.

## [0.11.2] - 2020-06-19
### Added
- The method `Function.update()`, which updates the function object.

## [0.11.1] - 2020-06-10
### Fixed
- Client no longer gives an error on using a token instead of an API key.

## [0.11.0] - 2020-06-08
### Changed
- Removed FunctionCallResponse class. Functions `FunctionCallsAPI.get_response()` and `FunctionCall.get_response()` now returns the actual function response (without being wrapped in an object with `call_id`, `function_id` and `response`).

## [0.10.0] - 2020-06-04
### Changed
- POST endpoints such as search and list will be retried in experimental endpoints, as they are in v1.

## [0.9.1] - 2020-06-04

### Changed
- Updated documentation for functions.

## [0.9.0] - 2020-05-29
### Changed
- Function response is no longer a property of the `FunctionCall` class. Instead, the response can be retrieved by the methods `FunctionCallsAPI.get_response()` or `FunctionCall.get_response()`.
- The documentation for function schedules is put under the expand/collapse header Function Schedules.

### Added
- Filtering of function calls given call attributes and added  an attribute for schedule id to the FunctionCall data class.

## [0.8.3] - 2020-05-28
### Fixed
- The method `Function.call()` now takes the argument `wait` (defaults to `True`) instead of `asynchronous`. This change was supposed to be a part of release 0.8.0.

## [0.8.2] - 2020-05-27
### Fixed
- Allow `true_matches` to be `None` in `fit_ml`.

## [0.8.1] - 2020-05-26
### Changed
- Function calls now returns `functionId`, so the getting logs of a call has a simplified internal structure.

## [0.8.0] - 2020-05-26
### Changed
- In `FunctionsAPI.call()`, the `asynchronous` argument has been removed, reflecting the Functions API which now only supports asynchronous calls. A new argument `wait` has been introduced. When `wait=True` (default), `FunctionsAPI.call()` will block until the call is finished.

## [0.7.3] - 2020-05-19
### Fixed
- Dosctring for `FunctionCallsAPI.list()` erroneously listed `external_id` as optional argument. This has been corrected to `function_external_id`.


## [0.7.2] - 2020-05-15
### Fixed
- Support for no entities passed on predict_ml.

## [0.7.1] - 2020-05-15
### Added
- Support for ML Entity matcher from/to columns and retrain.

## [0.7.0] - 2020-05-14

### Added
- Labels endpoint support
- Assets labelling support

## [0.6.0] - 2020-05-08

### Changed
- SDK updated for changes in ML Entity matcher endpoints.

### Fixed
- `FunctionSchedulesAPI.create()` works when argument `name` contains the character `/`.

## [0.5.8] - 2020-04-30
- Assets playground API uses playground for retrieve

## [0.5.7] - 2020-04-29

### Added
- Added checks that verify that the function handler in an uploaded function is correctly constructed.

### Fixed
- `FunctionSchedulesAPI.create()` works without providing the `data` argument.

## [0.5.6] - 2020-04-28

### Added
- Data classes for contextualization models and job now include time stamps for created_time, start_time, status_time.
- Unstructured search endpoints added in client.files.unstructured.

## [0.5.5] - 2020-04-21

### Changed
- Data class `Function` now has the additional attribute `error`.

## [0.5.4] - 2020-04-20

### Added
- fit_ml function on entity matcher and predict_ml on model object.

## [0.5.3] - 2020-04-16

### Added
- Sphinx documentation for Cognite Functions

## [0.5.2] - 2020-04-16

### Added
- A `FunctionSchedule` class and corresponding api attached to the `Functions` api to interact with function schedules.
Function schedules can now also be listed using the `Function` object through the `list_schedules` method.

## [0.5.1] - 2020-04-15

### Added
- Argument `function_handle` to `FunctionsAPI.create()`, which can be used to create a function directly from code.

## [0.5.0] - 2020-04-08

### Added
- FunctionsAPI to interact with the Cognite Functions API in CDF.

### Changed
- Refactor of contextualization endpoints to not use asyncio and block later.
