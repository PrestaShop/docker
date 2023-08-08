#!/usr/bin/env python

import json
from versions import VERSIONS

jsonVersions = []
for ps_version, php_versions in VERSIONS.items():
    jsonVersions.append(ps_version)

print(json.dumps(jsonVersions))
