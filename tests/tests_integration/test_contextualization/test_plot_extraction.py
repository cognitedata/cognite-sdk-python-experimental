import pytest

from cognite.client.data_classes import ContextualizationJob
from cognite.experimental import CogniteClient

COGNITE_CLIENT = CogniteClient()
PLOT_EXTRACTION_API = COGNITE_CLIENT.plot_extraction
IMAGE = "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAA1ADUDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD3+iiigAooooAy7X/kZdS/697f+clX5p47eJ5ZXVI0GWYnpWO9/Bp+t6ncXLhUFvbj1JOZOAPWsxIL7xTcCa43W+mqcogP3/8AH69q561fkahBXk+n6vsjpoYfnXPN2iuv6Lux83iLU76Vjo9mzwIcF2TO4/0orp4LeG2hWGFFSNeAoFFY/VastZVXfy2NvrVKOkaSt53v8yaikzVS/wBVsdLi82+uooE7b2wT9B3rubscBcqtd3sVjavcTsFjQZJ9fYVxl58R1nmNtoOmz30x6MykKPfA5P6VRsBrniqYxX1yE25ZgqjZEO3A6n8fxrkr4pQVoayeiN8NSVWTcnaK1b/rq+gkms6Vd6zNfa1cLDEgXZAAWZhzgcD2OfrVt/iFNeP9m8PaJPcsOAzrwv8AwFe34irGkeCNHttbvIrmJr1ooonDXHPzMXzwOMfKOtdpFBFBEI4Y0jjHRUUAD8BSoYecFq9Xu+rFiK8q0tNIrZdv+D3PPzZ/ETUv3zXcFiO0QYL/ACDfqaK9ExRW/sl3Zz8p5yNZ8ZeKDjS7IabaN/y2fg4/3iP/AEEVd0/4c2nmi61q8m1C5PLAsQv59T+ddF9p1/8A6Bmm/wDgwk/+M1hXOsaprcj6XaQW8TEkSSwztIhX/eKLgfhz2rGs4UlefvN7Lu/Q2oYZ1peS3b2SFuZ0nl/sLw9BFDEeJpIlCrgdenb1Pfp9el0zTYdMs1t4lHHLP0LH1NZGl2Or6TaeTDpmmljy8h1B8sf+/PT0FaHn6/8A9A3Tf/BhJ/8AGadCjJP2lT4n9yXZfqbV60XFUqWkV+L7v9F0Ftf+Rl1L/r3t/wCclalczbT63/b+oEafp5k8iDcpvnwBmTGD5PPfsO3XPGj9o1//AKBumf8Agwk/+M11HKatFZX2jX/+gbpn/gwk/wDjNFAGN4u1SeKRNOhPlpLHvkcHkgkjb7Djn1/PO9pWlwaXZLFCMseXcjljRRXnYf38TUctbWS8j0sT7mFpRjondvzZfxS0UV6J5pl2o/4qTUf+ve3/AJyVqUUUAFFFFAH/2Q=="


class TestPlotExtractionIntegration:
    def test_extract(self):
        job = PLOT_EXTRACTION_API.extract(image=IMAGE, plot_axes={"xMin": 0, "xMax": 1, "yMin": 0, "yMax": 1})
        assert isinstance(job, ContextualizationJob)
        assert "Queued" == job.status
        assert "items" in set(job.result.keys())
        assert "Completed" == job.status
        assert {"xValues", "xPositions", "yPositions", "yValues"} == set(job.result["items"][0].keys())
