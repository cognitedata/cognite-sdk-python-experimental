import os

from openapi.generator import CodeGenerator

# DEFAULT_SPEC_URL = "https://storage.googleapis.com/cognitedata-api-docs/dist/v1.json"
PLAYGROUND_SPEC_URL = "https://storage.googleapis.com/cognitedata-api-docs/dist/playground.json"


if __name__ == "__main__":
    codegen_playground = CodeGenerator(
        PLAYGROUND_SPEC_URL, exclude_schemas=["CustomMenuHierarchy", "CustomMenuHierarchyNode"]
    )
    spec = codegen_playground.open_api_spec

    print("=" * 100)  # noqa
    print(f"{spec.info.title}: {spec.info.version}")  # noqa
    print(spec.info.description)  # noqa
    print("=" * 100)  # noqa

    for root, dirs, files in os.walk("./cognite/experimental/data_classes"):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.endswith(".py"):
                print(f"* Generating playground code in {file_path}")  # noqa
                codegen_playground.generate(file_path, file_path)
