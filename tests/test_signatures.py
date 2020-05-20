import inspect
import json

import pytest

from cognite.experimental._api import assets, labels, relationships, types


class TestListAndIterSignatures:
    @pytest.mark.parametrize(
        "api, filter, ignore",
        [
            (
                assets.ExperimentalAssetsAPI,
                assets.AssetFilter,
                [
                    "root_external_ids",
                    "parent_external_ids",
                    "data_set_external_ids",
                    "asset_subtree_external_ids",
                    "aggregated_properties",
                    "partitions",
                ],
            ),
            (relationships.RelationshipsAPI, relationships.RelationshipFilter, ["data_sets", "relationship_types"]),
            (types.TypesAPI, types.TypeFilter, []),
            (labels.LabelsAPI, labels.LabelFilter, []),
        ],
    )
    def test_list_and_iter_signatures_same_as_filter_signature(self, api, filter, ignore):
        iter_parameters = dict(inspect.signature(api.__call__).parameters)
        for name in set(ignore + ["chunk_size", "limit"]) - {"partitions"}:
            if name in iter_parameters:
                del iter_parameters[name]

        list_parameters = dict(inspect.signature(api.list).parameters)
        for name in ignore + ["limit"]:
            if name in list_parameters:
                del list_parameters[name]

        filter_parameters = dict(inspect.signature(filter.__init__).parameters)
        for name in ignore + ["cognite_client"]:
            if name in filter_parameters:
                del filter_parameters[name]

        iter_parameters = {v.name for _, v in iter_parameters.items()}
        filter_parameters = {v.name for _, v in filter_parameters.items()}
        list_parameters = {v.name for _, v in list_parameters.items()}

        assert iter_parameters == filter_parameters, signature_error_msg(filter_parameters, iter_parameters)
        assert list_parameters == filter_parameters, signature_error_msg(filter_parameters, list_parameters)


def signature_error_msg(expected, actual):
    pretty_expected_params = json.dumps(list(expected), indent=4, sort_keys=True)
    pretty_actual_params = json.dumps(list(actual), indent=4, sort_keys=True)
    return "Signatures don't match. \nexpected: {}\ngot: {}\n diff: {}".format(
        pretty_expected_params, pretty_actual_params, list(expected - actual) + list(actual - expected)
    )
