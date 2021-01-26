from cognite.client.data_classes._base import *


class SynonymEntry(CogniteResource):
    def __init__(self, sources: List[str], targets: List[str]):
        self.sources = sources
        self.targets = targets


class MatchConditionConfig(CogniteResource):
    def __init__(self, synonyms: List[SynonymEntry]):
        self.synonyms = synonyms


class MatchCondition(CogniteResource):
    def __init__(self, condition_type: str, arguments: List[List[int]], config: MatchConditionConfig):
        self.condition_type = condition_type
        self.arguments = arguments
        self.config = config


class RegexExtractor(CogniteResource):
    def __init__(self, entity_set: str, extractor_type: str, field: str, pattern: str):
        self.entity_set = entity_set
        self.extractor_type = extractor_type
        self.field = field
        self.pattern = pattern


class MatchRule(CogniteResource):
    def __init__(self, extractors: List[RegexExtractor], conditions: List[MatchCondition], priority):
        self.extractors = extractors
        self.conditions = conditions
        self.priority = priority
