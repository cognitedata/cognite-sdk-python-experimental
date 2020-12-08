import random

import pytest
from cognite.client.data_classes import ContextualizationJob, EntityMatchingModel, EntityMatchingModelList
from cognite.client.exceptions import CogniteAPIError

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import (
    EntityMatchingPipeline,
    EntityMatchingPipelineRunList,
    EntityMatchingPipelineUpdate,
)

COGNITE_CLIENT = CogniteClient()
EMAPI = COGNITE_CLIENT.entity_matching


@pytest.fixture
def fitted_model():
    extid = "abc" + str(random.randint(1, 1000000000))
    try:
        EMAPI.delete(external_id=extid)
    except CogniteAPIError as e:
        pass  # expected
    entities_from = [{"id": 1, "name": "xx-yy"}]
    entities_to = [{"id": 2, "bloop": "yy"}, {"id": 3, "bloop": "zz"}]
    model = EMAPI.fit(
        sources=entities_from,
        targets=entities_to,
        true_matches=[{"sourceId": 1, "targetId": 2}],
        feature_type="bigram",
        match_fields=[("name", "bloop")],
        external_id=extid,
    )
    yield model
    EMAPI.delete(id=model.id)


class TestEntityMatchingIntegration:
    def test_fit_retrieve_update(self, fitted_model):
        assert isinstance(fitted_model, EntityMatchingModel)
        assert "Queued" == fitted_model.status

        job = fitted_model.predict(sources=[{"name": "foo-bar"}], targets=[{"bloop": "foo-42"}])
        assert "Completed" == fitted_model.status
        assert isinstance(job, ContextualizationJob)
        assert "Queued" == job.status
        assert {"matches", "source"} == set(job.result["items"][0].keys()) - {"matchFrom"}
        assert "Completed" == job.status

        job = fitted_model.predict()
        assert isinstance(job, ContextualizationJob)
        assert "Queued" == job.status
        assert {"matches", "source"} == set(job.result["items"][0].keys()) - {"matchFrom"}
        assert "Completed" == job.status

        # Retrieve model
        model = EMAPI.retrieve(id=fitted_model.id)
        assert model.classifier == "randomforest"
        assert model.feature_type == "bigram"
        assert model.match_fields == [{"source": "name", "target": "bloop"}]

        # Retrieve models
        models = EMAPI.retrieve_multiple(ids=[model.id, model.id])
        assert 2 == len(models)
        assert model == models[0]
        assert model == models[1]

        # Update model
        model.name = "new_name"
        updated_model = EMAPI.update(model)
        assert type(updated_model) == EntityMatchingModel
        assert updated_model.name == "new_name"

    def test_refit(self, fitted_model):
        new_model = fitted_model.refit(true_matches=[(1, 3)])
        assert new_model.id is not None
        assert new_model.id != fitted_model.id
        assert "Completed" == fitted_model.status
        assert isinstance(new_model, EntityMatchingModel)
        assert "Queued" == new_model.status

        job = new_model.predict(sources=[{"name": "foo-bar"}], targets=[{"bloop": "foo-42"}])
        assert {"matches", "source"} == set(job.result["items"][0].keys()) - {"matchFrom"}
        assert "Completed" == job.status
        EMAPI.delete(id=new_model.id)

    def test_true_match_formats(self):
        entities_from = [{"id": 1, "name": "xx-yy"}]
        entities_to = [{"id": 2, "name": "yy"}, {"id": 3, "externalId": "aa", "name": "xx"}]
        model = EMAPI.fit(
            sources=entities_from,
            targets=entities_to,
            true_matches=[{"sourceId": 1, "targetExternalId": "aa"}, (1, 2)],
        )
        assert isinstance(model, EntityMatchingModel)
        assert "Queued" == model.status
        EMAPI.delete(id=model.id)

    def test_extra_options(self):
        entities_from = [{"id": 1, "name": "xx-yy"}]
        entities_to = [{"id": 2, "name": "yy"}, {"id": 3, "name": "xx", "missing": "yy"}]
        model = EMAPI.fit(
            sources=entities_from,
            targets=entities_to,
            true_matches=[(1, 2)],
            feature_type="bigram",
            match_fields=[("name", "missing")],
            ignore_missing_fields=True,
            classifier="LogisticRegression",
            name="my_bigram_logReg_model",
            description="My model with bigram features",
        )
        assert isinstance(model, EntityMatchingModel)
        assert "Queued" == model.status
        job = model.predict()
        assert {"matches", "source"} == set(job.result["items"][0].keys()) - {"matchFrom"}

        EMAPI.delete(id=model.id)

    def test_list(self):
        models_list = EMAPI.list()
        assert len(models_list) > 0
        assert type(models_list) == EntityMatchingModelList
        assert all([type(x) == EntityMatchingModel for x in models_list])
        # Add filter
        models_list = EMAPI.list(feature_type="bigram")
        assert set([model.feature_type for model in models_list]) == {"bigram"}

    def test_direct_predict(self, fitted_model):
        job = EMAPI.predict(external_id=fitted_model.external_id)
        job2 = EMAPI.predict(id=fitted_model.id)
        assert isinstance(job, ContextualizationJob)
        assert "Queued" == job.status
        assert isinstance(job2, ContextualizationJob)

    def test_direct_refit(self, fitted_model):
        new_model = EMAPI.refit(external_id=fitted_model.external_id, true_matches=[(1, 3)])
        new_model2 = EMAPI.refit(id=fitted_model.id, true_matches=[(1, 3)])
        assert isinstance(new_model, EntityMatchingModel)
        assert isinstance(new_model2, EntityMatchingModel)

    @pytest.mark.skip(reason="Broken test. See MLOPS-604")
    def test_pipeline(self):
        pipeline = EntityMatchingPipeline(
            name="foo",
            sources={"dataSetIds": [], "resource": "sequences"},
            targets={"dataSetIds": []},
            model_parameters={"featureType": "insensitive"},
        )
        new_pipeline = EMAPI.pipelines.create(pipeline)
        run = new_pipeline.run()
        assert {"suggestedRules", "matches"} == run.result.keys()
        list_runs = new_pipeline.runs()
        assert isinstance(list_runs, EntityMatchingPipelineRunList)
        assert [run] == list_runs
        assert run == new_pipeline.latest_run()
        assert run == EMAPI.pipelines.runs.retrieve_latest(id=new_pipeline.id)
        assert [run] == EMAPI.pipelines.runs.retrieve_latest(id=[new_pipeline.id])
        assert run.result == new_pipeline.latest_run().result
        assert isinstance(run.suggested_rules, list)
        assert isinstance(run.matches, list)

        run2 = new_pipeline.run()
        assert run2 == EMAPI.pipelines.runs.retrieve_latest(id=new_pipeline.id)

        EMAPI.pipelines.update(EntityMatchingPipelineUpdate(id=new_pipeline.id).name.set("abc").sources.set({}))
        retrieved = EMAPI.pipelines.retrieve(id=new_pipeline.id)
        assert "abc" == retrieved.name
        assert {"resource": "time_series", "dataSetIds": []} == retrieved.sources
        EMAPI.pipelines.update(new_pipeline)
        assert pipeline.name == EMAPI.pipelines.retrieve(id=new_pipeline.id).name

        EMAPI.pipelines.delete(id=new_pipeline.id)
