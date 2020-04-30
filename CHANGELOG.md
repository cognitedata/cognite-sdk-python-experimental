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

### Fixed
- `FunctionSchedulesAPI.create()` works without providing the `data` argument.

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
