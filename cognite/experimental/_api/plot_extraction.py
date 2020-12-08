import base64
from io import BytesIO
from typing import Dict, List, Union

from cognite.client.data_classes import ContextualizationJob

from cognite.experimental._context_client import ContextAPI


class PlotDataExtractionAPI(ContextAPI):
    _RESOURCE_PATH = "/context/plotextractor"

    def extract(self, image: Union[str, "PIL.Image"], plot_axes: Dict, num_curves=None) -> ContextualizationJob:
        """Completes a schema uploaded in CDF as a type.

        Args:
            image: base64 encoded image, or a PIL Image.
            plot_axes: axis limits, given as {"xMin": .., "xMax": ..., "yMin": ..., "yMax": ...}
            num_curves: number of curves to extract. If ommitted, will try to detect automatically.

        Returns:
            ContextualizationJob: Resulting queued job. Note that .results property of this job will block waiting for results."""
        if not isinstance(image, str):
            try:
                from PIL import Image

                def image_to_base64_str(image: Image) -> str:
                    im_file = BytesIO()
                    image.save(im_file, format="JPEG")
                    im_bytes = im_file.getvalue()
                    return str(base64.b64encode(im_bytes), "utf-8")

            except Exception as e:
                raise ValueError(f"Image parameter was not a string and failed to import PIL: {e}")
            if not isinstance(image, Image):
                raise ValueError(f"Image parameter was not a string or a PIL Image")
            image = image_to_base64_str(image)

        return self._run_job(
            job_path="/extractdata", status_path="/", plot_image=image, plot_axes=plot_axes, num_curves=num_curves
        )
