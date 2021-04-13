import copy
from collections import UserList
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

import pandas as pd
from cognite.client.data_classes import ContextualizationJob
from cognite.client.data_classes._base import (
    CognitePrimitiveUpdate,
    CogniteResource,
    CogniteResourceList,
    CogniteUpdate,
)
from cognite.client.utils._auxiliary import to_camel_case

from cognite.experimental.data_classes.utils.pandas import dataframe_summarize
from cognite.experimental.data_classes.utils.rules_output import _color_matches, _label_groups


class EntityMatchingMatchRule(CogniteResource):
    def __init__(
        self,
        conditions=None,
        extractors=None,
        priority=None,
        matches=None,
        flags=None,
        conflicts=None,
        overlaps=None,
        number_of_matches=None,
        num_conflicts=None,
        num_overlaps=None,
        cognite_client=None,
    ):
        self.conditions = conditions
        self.extractors = extractors
        self.priority = priority
        self.matches = matches
        self.flags = flags
        self.conflicts = conflicts
        self.overlaps = overlaps
        self.number_of_matches = number_of_matches
        self.num_conflicts = num_conflicts
        self.num_overlaps = num_overlaps
        self._cognite_client = cognite_client

    def _repr_html_(self):
        extractors = _label_groups(copy.deepcopy(self.extractors), self.conditions)

        info_df = super().to_pandas(camel_case=True)
        info_df = dataframe_summarize(info_df)
        info_df.index.name = "Stats"
        html = info_df._repr_html_()
        if self.matches is not None:
            html += _color_matches(extractors, self.matches)
        return html


class EntityMatchingMatchRuleList(CogniteResourceList):
    _RESOURCE = EntityMatchingMatchRule
    _ASSERT_CLASSES = False

    def _repr_html_(self):
        if not self.data:
            return super()._repr_html_()
        try:
            from ipywidgets import interact  # dont want this as dependency
        except (ImportError, ModuleNotFoundError):
            return super()._repr_html_()

        @interact(rule_number=(0, len(self) - 1))
        def show_results(rule_number=0):
            return self[rule_number]

        return ""


class EntityMatchingMatch(CogniteResource):
    def __init__(self, source=None, target=None, score=None, match_type=None, match_fields=None, cognite_client=None):
        self.source = source
        self.target = target
        self.score = score
        self.match_type = match_type
        self._match_fields = match_fields
        self._cognite_client = cognite_client

    def to_pandas(self, camel_case=False):
        # shows only the relevant fields, in a sensible order, rather than a dict blob
        fields = super().dump(camel_case=camel_case)
        match_fields = self._match_fields
        if match_fields:
            linear_match_fields = [
                (source_target, match_field[source_target])
                for match_field in match_fields
                for source_target in ["source", "target"]
            ]
        else:
            linear_match_fields = [
                (source_target, key_field)
                for key_field in ["externalId", "external_id", "name", "description"]
                for source_target in ["source", "target"]
                if getattr(self, source_target).get(key_field)  # no empty strings
            ]
        if not linear_match_fields:
            linear_match_fields = [
                (source_target, key_field)
                for source_target in ["source", "target"]
                for key_field in getattr(self, source_target)
            ]

        for source_target, field in linear_match_fields:
            entity = getattr(self, source_target)
            fields[f"{source_target}.{field}"] = entity.get(field)
        del fields["source"]
        del fields["target"]
        return pd.DataFrame.from_dict(fields, orient="index", columns=["value"])


class EntityMatchingMatchList(CogniteResourceList):
    _RESOURCE = EntityMatchingMatch
    _ASSERT_CLASSES = False

    @classmethod
    def _load(cls, resource_list: Union[List, str], cognite_client=None):
        loaded = super()._load(resource_list, cognite_client)
        loaded.data = sorted(loaded.data, key=lambda match: -match.score)  # sort matches from highest to lowest score
        return loaded

    def to_pandas(self, camel_case=False):
        return pd.concat([match.to_pandas() for match in self], axis=1).T.reset_index(drop=True)


class EntityMatchingPipelineRun(ContextualizationJob):
    def __init__(self, pipeline_id=None, **kwargs):
        super().__init__(**kwargs)
        self.pipeline_id = pipeline_id
        self._pipeline = None
        self._status_path = "/context/entitymatching/pipelines/run/"  # since we can list this, would like .result even if we didn't this via .run

    @property
    def pipeline(self):
        """Retrieve the pipeline that owns this run, may call the API or use a cached value"""
        if self._pipeline is None:
            self._pipeline = self._cognite_client.entity_matching.pipelines.retrieve(id=self.pipeline_id)
        return self._pipeline

    @pipeline.setter  # TODO: use in .runs etc
    def pipeline(self, value):
        self._pipeline = value

    @property
    def errors(self):
        """Returns list of error messages encountered while running. Depends on .result and may block"""
        return self.result.get("errors")

    @property
    def generated_rules(self):
        """List of suggested new match rules. Depends on .result and may block"""
        return EntityMatchingMatchRuleList._load(self.result["generatedRules"], cognite_client=self._cognite_client)

    @property
    def matches(self) -> EntityMatchingMatchList:
        """List of matches. Depends on .result and may block"""
        matches = self.result["matches"]
        match_fields = (self.pipeline.model_parameters or {}).get("matchFields", [{"source": "name", "target": "name"}])
        for match in matches:
            match["match_fields"] = match_fields  # for nice output
        return EntityMatchingMatchList._load(matches, cognite_client=self._cognite_client)

    def _repr_html_(self):
        result = self.result  # TODO: optional loading? do this first for now for consistent status
        df = super().to_pandas()
        df.loc["matches"] = [result["matches"]]
        df.loc["generatedRules"] = [result["generatedRules"]]
        return dataframe_summarize(df)._repr_html_()


class EntityMatchingPipelineRunList(CogniteResourceList):
    _RESOURCE = EntityMatchingPipelineRun
    _UPDATE = None
    _ASSERT_CLASSES = False


class EntityMatchingPipeline(CogniteResource):
    """Entity matching pipeline, used to continuously iterate and improve an entity matching model.
       The fields below can be filled when creating a pipeline. Other fields should be left empty, and return status information on successful creation and retrieval.

    Args:
        external_id, name, description: standard fields for a resource.
        model_parameters: a dictionary with fields `match_fields`, `feature_type`, `classifier`, as in the `fit` method for entity matching.
        sources, targets: a dictionary of the format {'resource': ..., 'dataSetIds': [{'id':...},{'externalId':...}]}
        true_matches: existing matches with reasonable certainty to use in training.
        confirmed_matches: user-confirmed certain matches which will be used to override any other results.
        rejected_matches: user-confirmed wrong results which will be used to blank output for a match result if it is one of these.
        use_existing_matches: If set, uses existing matches on resources as additional true_matches (but not confirmed_matches).
        replacements: Expects a list of {'field':.., 'string':.. ,'replacement': ..} which will be used to replace substrings in a field with a synonym, such as "Pressure Transmitter" -> "PT", or "Æ" -> AE. Field can be '*' for all.
        relationships_label: If set, writes relationships with this label to the tenant (along with a pipeline-specific and general entity matching label). Requires whitelisting by auth.
        rules: list of matching rules (either old or new format)
        schedule_interval: automatically schedule pipeline to be run every this many seconds.
    """

    _RESOURCE_PATH = "/context/entitymatching/pipelines"
    _STATUS_PATH = _RESOURCE_PATH + "/"

    def __init__(
        self,
        id: int = None,
        external_id: str = None,
        name: str = None,
        description: str = None,
        model_parameters: Dict = None,
        sources: Dict = None,
        targets: Dict = None,
        true_matches: List = None,
        rejected_matches: List = None,
        confirmed_matches: List = None,
        use_existing_matches: bool = None,
        replacements: List[Dict] = None,
        relationships_label: str = None,
        score_threshold: float = None,
        schedule_interval: int = None,
        rules: List = None,
        status=None,
        error_message=None,
        created_time=None,
        start_time=None,
        status_time=None,
        cognite_client=None,
    ):

        self.id = id
        self.external_id = external_id
        self.name = name
        self.description = description
        self.model_parameters = model_parameters
        self.sources = sources
        self.targets = targets
        self.true_matches = true_matches
        self.confirmed_matches = confirmed_matches
        self.rejected_matches = rejected_matches
        self.use_existing_matches = use_existing_matches
        self.replacements = replacements
        self.relationships_label = relationships_label
        self.score_threshold = score_threshold
        self.rules = rules
        self.schedule_interval = schedule_interval

        self.status = status
        self.created_time = created_time
        self.start_time = start_time
        self.status_time = status_time
        self.error_message = error_message

        self._cognite_client = cognite_client

    def run(self) -> EntityMatchingPipelineRun:
        """Runs the pipeline and returns a run job"""
        return self._cognite_client.entity_matching.pipelines.run(id=self.id)

    def runs(self) -> EntityMatchingPipelineRunList:
        """Retrieve the list of runs"""
        return self._cognite_client.entity_matching.pipelines.runs.list(id=self.id)

    def latest_run(self) -> EntityMatchingPipelineRun:
        """Retrieve the latest run"""
        return self._cognite_client.entity_matching.pipelines.runs.retrieve_latest(id=self.id)

    def to_pandas(self, camel_case=False):
        df = dataframe_summarize(super().to_pandas(camel_case=camel_case))
        # expand
        for f in ["sources", "targets", "model_parameters"]:
            for k, v in (getattr(self, f, {}) or {}).items():
                if isinstance(v, list):
                    for i, vi in enumerate(v):
                        df.loc[f"{f}.{k}[{i}]"] = [vi]
                else:
                    df.loc[f"{f}.{k}"] = [v]
            if camel_case:
                f = to_camel_case(f)
            if f in df.index:
                df = df.drop(f)
        return df


class EntityMatchingPipelineUpdate(CogniteUpdate):  # not implemented yet
    """Changes applied to entity matching pipeline

    Args:
        id (int): A server-generated ID for the object.
        external_id (str): The external ID provided by the client. Must be unique for the resource type.
    """

    class _PrimitiveUpdate(CognitePrimitiveUpdate):
        def set(self, value: Any) -> "EntityMatchingPipelineUpdate":
            return self._set(value)

    @property
    def name(self):
        return EntityMatchingPipelineUpdate._PrimitiveUpdate(self, "name")

    @property
    def description(self):
        return EntityMatchingPipelineUpdate._PrimitiveUpdate(self, "description")

    @property
    def model_parameters(self):
        return EntityMatchingPipelineUpdate._PrimitiveUpdate(self, "modelParameters")

    @property
    def sources(self):
        return EntityMatchingPipelineUpdate._PrimitiveUpdate(self, "sources")

    @property
    def targets(self):
        return EntityMatchingPipelineUpdate._PrimitiveUpdate(self, "targets")

    @property
    def true_matches(self):
        return EntityMatchingPipelineUpdate._PrimitiveUpdate(self, "trueMatches")

    @property
    def confirmed_matches(self):
        return EntityMatchingPipelineUpdate._PrimitiveUpdate(self, "confirmedMatches")

    @property
    def rejected_matches(self):
        return EntityMatchingPipelineUpdate._PrimitiveUpdate(self, "rejectedMatches")

    @property
    def rules(self):
        return EntityMatchingPipelineUpdate._PrimitiveUpdate(self, "rules")

    @property
    def replacements(self):
        return EntityMatchingPipelineUpdate._PrimitiveUpdate(self, "replacements")

    @property
    def score_threshold(self):
        return EntityMatchingPipelineUpdate._PrimitiveUpdate(self, "scoreThreshold")

    @property
    def schedule_interval(self):
        return EntityMatchingPipelineUpdate._PrimitiveUpdate(self, "scheduleInterval")


class EntityMatchingPipelineList(CogniteResourceList):
    _RESOURCE = EntityMatchingPipeline
    _UPDATE = EntityMatchingPipelineUpdate


class MatchRulesSuggestJob(ContextualizationJob):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._status_path = "/context/matchrules/suggest/"

    @property
    def rules(self) -> EntityMatchingMatchRuleList:
        """Depends on .result and may block"""
        return EntityMatchingMatchRuleList._load(self.result["rules"])

    def _repr_html_(self):
        rules = self.rules  # TODO: optional loading? before super() for status
        df = super().to_pandas()
        df.loc["rules"] = [f"{len(rules)} items"]
        return df._repr_html_()


class MatchRulesApplyJob(ContextualizationJob):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._status_path = "/context/matchrules/suggest/"

    @property
    def rules(self) -> EntityMatchingMatchRuleList:
        """Depends on .result and may block"""
        reformated_rules = [{**item["rule"], **item} for item in self.result["items"]]
        for rule in reformated_rules:
            rule.pop("rule")
        return EntityMatchingMatchRuleList._load(reformated_rules)

    def _repr_html_(self):
        rules = self.rules  # TODO: optional loading? before super() for status
        df = super().to_pandas()
        df.loc["rules"] = [f"{len(rules)} items"]
        return df._repr_html_()


class PNIDDetection(CogniteResource):
    def __init__(self, text=None, type=None, confidence=None, bounding_box=None, entities=None, cognite_client=None):
        self.text = text
        self.type = type
        self.confidence = confidence
        self.bounding_box = bounding_box
        self.entities = entities
        self._cognite_client = cognite_client


import warnings


class PNIDDetectionList(CogniteResourceList):
    _RESOURCE = PNIDDetection
    _UPDATE = None
    _ASSERT_CLASSES = False

    def image_with_bounding_boxes(self, file_id: int) -> "PIL.Image":
        """returns an image with bounding boxes on top of the pdf specified by file_id"""
        file_bytes = self._cognite_client.files.download_bytes(id=file_id)

        try:
            import numpy as np
            from bounding_box import bounding_box as bb
            from pdf2image import convert_from_bytes
            from PIL import Image
        except (ImportError, ModuleNotFoundError) as e:
            warnings.warn(
                f"Module {e.name} missing, 'pip install Pillow numpy bounding_box pdf2image' for advanced visualization of results"
            )
            raise

        def draw_bbox(pnid_img):
            img_arr = np.array(pnid_img)
            height, width = img_arr.shape[:-1]
            img_arr_copy = img_arr[:, :, ::-1].copy()
            for detected_item in self.data:
                bbox = detected_item.bounding_box
                label = detected_item.text
                bb.add(
                    img_arr_copy,
                    int(bbox["xMin"] * width),
                    int(bbox["yMin"] * height),
                    int(bbox["xMax"] * width),
                    int(bbox["yMax"] * height),
                    label,
                    "red",
                )
            return Image.fromarray(img_arr_copy[:, :, ::-1])

        try:
            return draw_bbox(convert_from_bytes(file_bytes)[0])
        except Exception:
            return None

    @classmethod
    def _load(cls, resource_list: Union[List, str], cognite_client=None):
        loaded = super()._load(resource_list, cognite_client)
        return loaded


class PNIDDetectionPageList(UserList):
    def __init__(self, data, file_id):
        super().__init__(data)
        self.file_id = file_id

    def _repr_html_(self):
        df = pd.DataFrame(
            [[i + 1, f"{len(page)} items"] for i, page in enumerate(self.data)], columns=["page", "matches"]
        )
        df.index.name = "index"
        return df._repr_html_()

    @property
    def image(self) -> "PIL.Image":
        """Returns the file as an image with bounding boxes for detected items"""
        return self[0].image_with_bounding_boxes(file_id=self.file_id)


class PNIDConvertResults(ContextualizationJob):
    @property
    def image(self):
        """Returns the result as an SVG image for output in jupyter"""
        from IPython.display import SVG

        return SVG(self.result["svgUrl"])


class PNIDDetectResults(ContextualizationJob):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def matches(self) -> PNIDDetectionList:
        """Returns detected items"""
        return PNIDDetectionList._load(self.result["items"], cognite_client=self._cognite_client,)

    def to_pandas(self, camel_case: bool = False):
        df = super().to_pandas(camel_case=camel_case)
        df.loc["matches"] = f"{len(self.matches)} items"
        return df

    @property
    def image(self):
        """Returns the file as an image with bounding boxes for matches"""
        return self.matches.image_with_bounding_boxes(file_id=self.file_id)

    @property
    def file_id(self):
        return self.result.get("fileId")

    @property
    def file_external_id(self):
        return self.result.get("fileExternalId")

    def convert(self, ocr=False) -> PNIDConvertResults:
        """Convert a P&ID to an interactive SVG where the provided annotations are highlighted

        Arguments:
            ocr(bool): show raw OCR results, rather than detected entities.
        """
        if ocr:
            items = self.ocr()[0].dump(camel_case=True)
        else:
            items = self.result["items"]

        return self._cognite_client.pnid_parsing.convert(items=items, file_id=self.file_id)

    def ocr(self) -> PNIDDetectionPageList:
        """Retrieve raw OCR results, for example, to visualize"""
        return self._cognite_client.pnid_parsing.ocr(file_id=self.file_id)


class DiagramConvertPage(CogniteResource):
    def __init__(self, page=None, png_url=None, svg_url=None, cognite_client=None):
        self.page = page
        self.png_url = png_url
        self.svg_url = svg_url
        self._cognite_client = cognite_client


class DiagramConvertPageList(CogniteResourceList):
    _RESOURCE = DiagramConvertPage
    _ASSERT_CLASSES = False


class DiagramConvertItem(CogniteResource):
    def __init__(self, file_id=None, file_external_id=None, results=None, cognite_client=None):
        self.file_id = file_id
        self.file_external_id = file_external_id
        self.results = results
        self._cognite_client = cognite_client

    def __len__(self):
        return len(self.results)

    @property
    def pages(self):
        return DiagramConvertPageList._load(self.results, cognite_client=self._cognite_client)

    def to_pandas(self, camel_case: bool = False):
        df = super().to_pandas(camel_case=camel_case)
        df.loc["results"] = f"{len(df['results'])} pages"
        return df


class DiagramConvertResults(ContextualizationJob):
    def __getitem__(self, find_id) -> DiagramConvertItem:
        """retrieves the results for the file with (external) id"""
        found = [
            item
            for item in self.result["items"]
            if item.get("fileId") == find_id or item.get("fileExternalId") == find_id
        ]
        if not found:
            raise IndexError(f"File with (external) id {find_id} not found in results")
        if len(found) != 1:
            raise IndexError(f"Found multiple results for file with (external) id {find_id}, use .items instead")
        return DiagramConvertItem._load(found[0], cognite_client=self._cognite_client)

    @property
    def items(self) -> List[DiagramConvertItem]:
        """returns a list of all results by file"""
        return [DiagramConvertItem._load(item, cognite_client=self._cognite_client) for item in self.result["items"]]


class DiagramDetectItem(CogniteResource):
    def __init__(self, file_id=None, file_external_id=None, annotations=None, error_message=None, cognite_client=None):
        self.file_id = file_id
        self.file_external_id = file_external_id
        self.annotations = annotations
        self.error_message = error_message
        self._cognite_client = cognite_client

    def to_pandas(self, camel_case: bool = False):
        df = super().to_pandas(camel_case=camel_case)
        df.loc["annotations"] = f"{len(df['annotations'])} annotations"
        return df


class DiagramDetectResults(ContextualizationJob):
    def __getitem__(self, find_id) -> DiagramDetectItem:
        """retrieves the results for the file with (external) id"""
        found = [
            item
            for item in self.result["items"]
            if item.get("fileId") == find_id or item.get("fileExternalId") == find_id
        ]
        if not found:
            raise IndexError(f"File with (external) id {find_id} not found in results")
        if len(found) != 1:
            raise IndexError(f"Found multiple results for file with (external) id {find_id}, use .items instead")
        return DiagramDetectItem._load(found[0], cognite_client=self._cognite_client)

    @property
    def items(self) -> List[DiagramDetectItem]:
        """returns a list of all results by file"""
        return [DiagramDetectItem._load(item, cognite_client=self._cognite_client) for item in self.result["items"]]

    @property
    def errors(self) -> List[str]:
        """returns a list of all error messages across files"""
        return [item["errorMessage"] for item in self.result["items"] if "errorMessage" in item]

    def convert(self) -> DiagramConvertResults:
        """Convert a P&ID to an interactive SVG where the provided annotations are highlighted"""
        return self._cognite_client.diagrams.convert(detect_job=self)
