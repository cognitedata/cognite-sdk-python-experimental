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

## [0.11.0] - 2020-06-08
### Changed
- Removed FunctionCallResponse class. Functions `FunctionCallsAPI.get_response()` and `FunctionCall.get_response()` now returns the actual function response (without being wrapped in an object with `call_id`, `function_id` and `response`).

## [0.10.0] - 2020-06-04
### Changed
- POST endpoints such as search and list will be retried in experimetal endpoints, as they are in v1.

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
- Data classes for contextualization models and job now include time stamps for request_timestamp, start_timestamp, status_timestamp.
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
