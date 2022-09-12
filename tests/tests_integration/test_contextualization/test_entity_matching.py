import pytest

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import (
    EntityMatchingMatchList,
    EntityMatchingPipeline,
    EntityMatchingPipelineRunList,
    EntityMatchingPipelineUpdate,
)

COGNITE_CLIENT = CogniteClient()
EMAPI = COGNITE_CLIENT.entity_matching


class TestEntityMatchingIntegration:
    def test_pipeline(self):
        sources = targets = {"assetSubtreeIds": [{"externalId": "test__asset_0"}], "resource": "assets"}
        pipeline = EntityMatchingPipeline(
            name="foo",
            sources=sources,
            targets=targets,
            model_parameters={"featureType": "insensitive"},
            use_existing_matches=True,
        )
        new_pipeline = EMAPI.pipelines.create(pipeline)
        run = new_pipeline.run()
        assert {"matches", "generatedRules", "errors"} == run.result.keys()
        list_runs = new_pipeline.runs()
        assert isinstance(list_runs, EntityMatchingPipelineRunList)
        assert [run] == list_runs
        assert run == new_pipeline.latest_run()
        assert run == EMAPI.pipelines.runs.retrieve_latest(id=new_pipeline.id)
        assert [run] == EMAPI.pipelines.runs.retrieve_latest(id=[new_pipeline.id])
        assert run.result == new_pipeline.latest_run().result
        assert isinstance(run.matches, EntityMatchingMatchList)

        run2 = new_pipeline.run()
        assert run2 == EMAPI.pipelines.runs.retrieve_latest(id=new_pipeline.id)

        EMAPI.pipelines.update(EntityMatchingPipelineUpdate(id=new_pipeline.id).name.set("abc").sources.set(targets))
        retrieved = EMAPI.pipelines.retrieve(id=new_pipeline.id)
        assert "abc" == retrieved.name
        assert targets == retrieved.sources
        EMAPI.pipelines.update(new_pipeline)
        assert pipeline.name == EMAPI.pipelines.retrieve(id=new_pipeline.id).name

        EMAPI.pipelines.delete(id=new_pipeline.id)

        assert isinstance(pipeline._repr_html_(), str)
        assert isinstance(run._repr_html_(), str)
        assert isinstance(run.generated_rules._repr_html_(), str)
        assert isinstance(run.matches._repr_html_(), str)
