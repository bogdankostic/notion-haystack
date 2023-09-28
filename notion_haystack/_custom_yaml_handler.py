from datetime import datetime

from frontmatter import YAMLHandler
import yaml


class CustomYAMLHandler(YAMLHandler):
    """
    Custom YAMLHandler that does not convert dates to datetime objects.
    """

    def load(self, fm, **kwargs):
        """
        Parse YAML front matter. This uses yaml.SafeLoader by default.
        """
        kwargs.setdefault("Loader", yaml.SafeLoader)
        meta = yaml.load(fm, **kwargs)
        for key, value in meta.items():
            if isinstance(value, datetime):
                meta[key] = value.isoformat()

        return meta