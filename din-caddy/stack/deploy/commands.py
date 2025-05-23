# Copyright © 2023 Vulcanize
# Copyright © 2025 Bozeman Pass, Inc.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http:#www.gnu.org/licenses/>.

import os

from pathlib import Path
from shutil import copy


def create(deploy_cmd_ctx, deployment_ctx, stack):
    #k8s
    deployment_config_dir = deployment_ctx.deployment_dir.joinpath("configmaps", "din-caddy-config")

    #docker
    if not os.path.exists(deployment_config_dir):
        deployment_config_dir = deployment_ctx.deployment_dir.joinpath("data", "din-caddy-config")

    compose_file = stack.get_pod_file_path("din-caddy")

    # Choose the config file to use based on the broader spec we are a part of.
    caddyfile = "Caddyfile.mainnet"
    if "fixturenet-eth" in deployment_ctx.spec.get_pod_list():
        caddyfile = "Caddyfile.fixturenet"

    source_config_file = Path(compose_file).parent.joinpath("config", caddyfile)
    copy(source_config_file, os.path.join(deployment_config_dir, "Caddyfile"))
