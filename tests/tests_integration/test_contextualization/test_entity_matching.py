import pytest

from cognite.experimental import CogniteClient
from cognite.experimental.data_classes import ContextualizationJob, ContextualizationModelList, EntityMatchingModel
from cognite.experimental.exceptions import ModelFailedException

COGNITE_CLIENT = CogniteClient()
EMAPI = COGNITE_CLIENT.entity_matching


class TestEntityMatchingIntegration:
    def test_fit(self):
        entities_from = [{"id": 1, "name": "xx-yy"}]
        entities_to = [{"id": 2, "bloop": "yy"}]
        model = EMAPI.fit(
            match_from=entities_from,
            match_to=entities_to,
            true_matches=[(1, 2)],
            feature_type="bigram",
            keys_from_to=[("name", "bloop")],
        )
        assert isinstance(model, EntityMatchingModel)
        assert "Queued" == model.status

        job = model.predict(match_from=[{"name": "foo-bar"}], match_to=[{"bloop": "foo-42"}])
        assert "Completed" == model.status
        assert isinstance(job, ContextualizationJob)
        assert "Queued" == job.status
        assert {"matches", "matchFrom"} == set(job.result["items"][0].keys())
        assert "Completed" == job.status

        job = model.predict()
        assert isinstance(job, ContextualizationJob)
        assert "Queued" == job.status
        assert {"matches", "matchFrom"} == set(job.result["items"][0].keys())
        assert "Completed" == job.status

        # Retrieve model
        model = EMAPI.retrieve(model_id=model.model_id)
        assert model.classifier == "RandomForest"
        assert model.feature_type == "bigram"
        assert model.keys_from_to == [["name", "bloop"]]
        assert model.model_type == "Supervised"

        EMAPI.delete(model)

    def test_ml_fit(self):
        # fit_ml and predict_ml should produce the same output as fit and predict. Will eventually be removed
        entities_from = [{"id": 1, "name": "xx-yy"}]
        entities_to = [{"id": 2, "bloop": "yy"}]
        model = EMAPI.fit_ml(
            match_from=entities_from,
            match_to=entities_to,
            true_matches=[(1, 2)],
            feature_type="bigram",
            keys_from_to=[("name", "bloop")],
        )
        assert isinstance(model, EntityMatchingModel)
        assert "Queued" == model.status

        job = model.predict_ml(match_from=[{"name": "foo-bar"}], match_to=[{"bloop": "foo-42"}])
        assert "Completed" == model.status
        assert isinstance(job, ContextualizationJob)
        assert "Queued" == job.status
        assert {"matches", "matchFrom"} == set(job.result["items"][0].keys())
        assert "Completed" == job.status

        job = model.predict_ml()
        assert isinstance(job, ContextualizationJob)
        assert "Queued" == job.status
        assert {"matches", "matchFrom"} == set(job.result["items"][0].keys())
        assert "Completed" == job.status

        EMAPI.delete(model)

    def test_refit(self):
        entities_from = [{"id": 1, "name": "xx-yy"}]
        entities_to = [{"id": 2, "name": "yy"}, {"id": 3, "name": "xx"}]
        model = EMAPI.fit(match_from=entities_from, match_to=entities_to, true_matches=[(1, 2)], feature_type="bigram")
        assert isinstance(model, EntityMatchingModel)
        assert "Queued" == model.status

        new_model = model.refit(true_matches=[(1, 3)])
        assert new_model.model_id is not None
        assert new_model.model_id != model.model_id
        assert "Completed" == model.status
        assert isinstance(new_model, EntityMatchingModel)
        assert "Queued" == new_model.status

        job = new_model.predict(match_from=[{"name": "foo-bar"}], match_to=[{"name": "foo-42"}])
        assert {"matches", "matchFrom"} == set(job.result["items"][0].keys())
        assert "Completed" == job.status
        EMAPI.delete(model)

    def test_extra_options(self):
        entities_from = [{"id": 1, "name": "xx-yy"}]
        entities_to = [{"id": 2, "name": "yy"}, {"id": 3, "name": "xx", "missing": "yy"}]
        model = EMAPI.fit(
            match_from=entities_from,
            match_to=entities_to,
            true_matches=[(1, 2)],
            feature_type="bigram",
            keys_from_to=[("name", "missing")],
            complete_missing=True,
            classifier="LogisticRegression",
            name="my_bigram_logReg_model",
            description="My model with bigram features",
        )
        assert isinstance(model, EntityMatchingModel)
        assert "Queued" == model.status
        job = model.predict()
        assert {"matches", "matchFrom"} == set(job.result["items"][0].keys())

        EMAPI.delete(model)

    def test_list(self):
        models_list = EMAPI.list()
        assert len(models_list) > 0
        assert type(models_list) == ContextualizationModelList
        assert all([type(x) == EntityMatchingModel for x in models_list])
        # Add filter
        models_list = EMAPI.list(filter={"feature_type": "bigram"})
        assert set([model.feature_type for model in models_list]) == {"bigram"}
        # Filter on two parameters
        models_list = EMAPI.list(filter={"keys_from_to": [["name", "name"]], "feature_type": "bigram"})
        assert set([model.feature_type for model in models_list]) == {"bigram"}
        assert all([model.keys_from_to == [["name", "name"]] for model in models_list])
