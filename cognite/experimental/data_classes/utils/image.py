
def draw_boxes(file_bytes, items):
    try:
        import warnings
        from PIL import Image
        import numpy as np
        from bounding_box import bounding_box as bb
        from pdf2image import convert_from_bytes
    except ImportError as e:
        warnings.warn(f"Module {e.name} missing, 'pip install PIL numpy bounding_box pdf2image' for advanced visualization of results")
        return ""

    def draw_bbox(pnid_img, result):
        img_arr = np.array(pnid_img)
        height, width = img_arr.shape[:-1]
        img_arr_copy = img_arr[:, :, ::-1].copy()
        for obj in result:
            bbox = obj["boundingBox"]
            label = obj.get("text")
            bb.add(
                img_arr_copy,
                int(bbox["xMin"] * width),
                int(bbox["yMin"] * height),
                int(bbox["xMax"] * width),
                int(bbox["yMax"] * height),
                label,
                "red"
            )
        return Image.fromarray(img_arr_copy[:, :, ::-1])

    image = convert_from_bytes(file_bytes)[0]
    image_with_bb = draw_bbox(image, items)
    return image_with_bb