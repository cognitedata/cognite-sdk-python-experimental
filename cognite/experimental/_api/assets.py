from typing import *

from cognite.client import utils
from cognite.client._api.assets import AssetsAPI
from cognite.client.data_classes import TimestampRange
from cognite.experimental.data_classes import Asset, AssetFilter, AssetList


class ExperimentalAssetsAPI(AssetsAPI):
    _RESOURCE_PATH = "/assets"
    _LIST_CLASS = AssetList

    def __call__(
        self,
        chunk_size: int = None,
        name: str = None,
        parent_ids: List[int] = None,
        parent_external_ids: List[str] = None,
        root_ids: List[int] = None,
        root_external_ids: List[str] = None,
        asset_subtree_ids: List[int] = None,
        asset_subtree_external_ids: List[str] = None,
        metadata: Dict[str, str] = None,
        source: str = None,
        created_time: Union[Dict[str, Any], TimestampRange] = None,
        last_updated_time: Union[Dict[str, Any], TimestampRange] = None,
        root: bool = None,
        external_id_prefix: str = None,
        types: List = None,
        aggregated_properties: List[str] = None,
        limit: int = None,
    ) -> Generator[Union[Asset, AssetList], None, None]:
        """Iterate over assets

        Fetches assets as they are iterated over, so you keep a limited number of assets in memory.

        Args:
            chunk_size (int, optional): Number of assets to return in each chunk. Defaults to yielding one asset a time.
            name (str): Name of asset. Often referred to as tag.
            parent_ids (List[int]): Return only the direct descendants of the specified assets.
            parent_external_ids (List[str]): Return only the direct descendants of the specified assets.
            root_ids (List[int], optional): List of root ids ids to filter on.
            root_external_ids (List[str], optional): List of root external ids to filter on.
            asset_subtree_ids (List[int]): List of asset subtrees ids to filter on.
            asset_subtree_external_ids (List[str]): List of asset subtrees external ids to filter on.
            metadata (Dict[str, str]): Custom, application specific metadata. String key -> String value
            source (str): The source of this asset
            created_time (Union[Dict[str, int], TimestampRange]):  Range between two timestamps. Possible keys are `min` and `max`, with values given as time stamps in ms.
            last_updated_time (Union[Dict[str, int], TimestampRange]):  Range between two timestamps. Possible keys are `min` and `max`, with values given as time stamps in ms.
            root (bool): filtered assets are root assets or not
            external_id_prefix (str): Filter by this (case-sensitive) prefix for the external ID.
            types (List): List of type filters.
            aggregated_properties (List[str]): Set of aggregated properties to include.
            limit (int, optional): Maximum number of assets to return. Defaults to return all items.

        Yields:
            Union[Asset, AssetList]: yields Asset one by one if chunk is not specified, else AssetList objects.
        """
        if aggregated_properties:
            aggregated_properties = [utils._auxiliary.to_camel_case(s) for s in aggregated_properties]
        # dict option for backward compatibility
        if (root_ids and not isinstance(root_ids[0], dict)) or root_external_ids:
            root_ids = self._process_ids(root_ids, root_external_ids, wrap_ids=True)
        if asset_subtree_ids or asset_subtree_external_ids:
            asset_subtree_ids = self._process_ids(asset_subtree_ids, asset_subtree_external_ids, wrap_ids=True)

        filter = AssetFilter(
            name=name,
            parent_ids=parent_ids,
            parent_external_ids=parent_external_ids,
            root_ids=root_ids,
            asset_subtree_ids=asset_subtree_ids,
            metadata=metadata,
            source=source,
            created_time=created_time,
            last_updated_time=last_updated_time,
            root=root,
            external_id_prefix=external_id_prefix,
        ).dump(camel_case=True)
        return self._list_generator(
            method="POST",
            chunk_size=chunk_size,
            filter=filter,
            limit=limit,
            other_params={"aggregatedProperties": aggregated_properties} if aggregated_properties else {},
        )

    def list(
        self,
        name: str = None,
        parent_ids: List[int] = None,
        parent_external_ids: List[str] = None,
        root_ids: List[int] = None,
        root_external_ids: List[str] = None,
        asset_subtree_ids: List[int] = None,
        asset_subtree_external_ids: List[str] = None,
        metadata: Dict[str, str] = None,
        source: str = None,
        created_time: Union[Dict[str, Any], TimestampRange] = None,
        last_updated_time: Union[Dict[str, Any], TimestampRange] = None,
        root: bool = None,
        external_id_prefix: str = None,
        types: List = None,
        aggregated_properties: List[str] = None,
        partitions: int = None,
        limit: int = 25,
    ) -> AssetList:
        """`List assets <https://docs.cognite.com/api/v1/#operation/listAssets>`_

        Args:
            name (str): Name of asset. Often referred to as tag.
            parent_ids (List[int]): Return only the direct descendants of the specified assets.
            parent_external_ids (List[str]): Return only the direct descendants of the specified assets.
            root_ids (List[int], optional): List of root ids ids to filter on.
            root_external_ids (List[str], optional): List of root external ids to filter on.
            asset_subtree_ids (List[int]): List of asset subtrees ids to filter on.
            asset_subtree_external_ids (List[str]): List of asset subtrees external ids to filter on.
            metadata (Dict[str, str]): Custom, application specific metadata. String key -> String value.
            source (str): The source of this asset.
            created_time (Union[Dict[str, int], TimestampRange]):  Range between two timestamps. Possible keys are `min` and `max`, with values given as time stamps in ms.
            last_updated_time (Union[Dict[str, int], TimestampRange]):  Range between two timestamps. Possible keys are `min` and `max`, with values given as time stamps in ms.
            root (bool): filtered assets are root assets or not.
            external_id_prefix (str): Filter by this (case-sensitive) prefix for the external ID.
            types (List): List of type filters.
            aggregated_properties (List[str]): Set of aggregated properties to include.
            partitions (int): Retrieve assets in parallel using this number of workers. Also requires `limit=None` to be passed.
            limit (int, optional): Maximum number of assets to return. Defaults to 25. Set to -1, float("inf") or None
                to return all items.

        Returns:
            AssetList: List of requested assets

        Examples:

            List assets::

                >>> from cognite.client import CogniteClient
                >>> c = CogniteClient()
                >>> asset_list = c.assets.list(limit=5)

            Iterate over assets::

                >>> from cognite.client import CogniteClient
                >>> c = CogniteClient()
                >>> for asset in c.assets:
                ...     asset # do something with the asset

            Iterate over chunks of assets to reduce memory load::

                >>> from cognite.client import CogniteClient
                >>> c = CogniteClient()
                >>> for asset_list in c.assets(chunk_size=2500):
                ...     asset_list # do something with the assets
        """
        if aggregated_properties:
            aggregated_properties = [utils._auxiliary.to_camel_case(s) for s in aggregated_properties]

        # dict option for backward compatibility
        if (root_ids and not isinstance(root_ids[0], dict)) or root_external_ids:
            root_ids = self._process_ids(root_ids, root_external_ids, wrap_ids=True)
        if asset_subtree_ids or asset_subtree_external_ids:
            asset_subtree_ids = self._process_ids(asset_subtree_ids, asset_subtree_external_ids, wrap_ids=True)

        filter = AssetFilter(
            name=name,
            parent_ids=parent_ids,
            parent_external_ids=parent_external_ids,
            root_ids=root_ids,
            asset_subtree_ids=asset_subtree_ids,
            metadata=metadata,
            source=source,
            created_time=created_time,
            last_updated_time=last_updated_time,
            root=root,
            external_id_prefix=external_id_prefix,
            types=types,
        ).dump(camel_case=True)
        return self._list(
            method="POST",
            limit=limit,
            filter=filter,
            other_params={"aggregatedProperties": aggregated_properties} if aggregated_properties else {},
            partitions=partitions,
        )
