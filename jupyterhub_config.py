# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Configuration file for JupyterHub
import os

c = get_config()  # noqa: F821

# We rely on environment variables to configure JupyterHub so that we
# avoid having to rebuild the JupyterHub container every time we change a
# configuration parameter.

#c.JupyterHub.port = os.environ["PORT"]

# Spawn single-user servers as Docker containers
# c.JupyterHub.spawner_class = 'sudospawner.Sudospawner'
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'

# Spawn containers from this image
c.DockerSpawner.image = os.environ.get("DOCKER_NOTEBOOK_IMAGE")

# Connect containers to this Docker network
network_name = os.environ.get("DOCKER_NETWORK_NAME")
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name

# Explicitly set notebook directory because we'll be mounting a volume to it.
# Most `jupyter/docker-stacks` *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
notebook_dir = os.environ.get("DOCKER_NOTEBOOK_DIR", "/home/jovyan/work")
c.DockerSpawner.notebook_dir = notebook_dir

# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = {"jupyterhub-user-{username}": notebook_dir}

# Remove containers once they are stopped
c.DockerSpawner.remove = True

# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True

# User containers will access hub by container name on the Docker network
#c.JupyterHub.hub_ip = "jupyterhub"
#c.JupyterHub.hub_port = 8080
#c.JupyterHub.bind_url = f"{os.environ.get('WEB_URL')}:{os.environ.get('PORT')}"
c.JupyterHub.bind_url = f"http://0.0.0.0:{os.environ.get('PORT')}"
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_port = int(os.environ.get('PORT'))
c.JupyterHub.hub_connect_ip = '0.0.0.0'

# Persist hub data on volume mounted inside container
c.JupyterHub.cookie_secret_file = "/srv/jupyterhub/jupyterhub_cookie_secret"
c.JupyterHub.db_url = "sqlite:////srv/jupyterhub/jupyterhub.sqlite"

# Allow all signed-up users to login
c.Authenticator.allow_all = True

# Authenticate users with Native Authenticator
c.JupyterHub.authenticator_class = "nativeauthenticator.NativeAuthenticator"

# Allow anyone to sign-up without approval
c.NativeAuthenticator.open_signup = True

# Allowed admins
admin = os.environ.get("JUPYTERHUB_ADMIN")
if admin:
    c.Authenticator.admin_users = [admin]

#c.JupyterHub.cleanup_servers = True
#c.ConfigurableHTTPProxy.should_start = True
#c.ConfigurableHTTPProxy.api_url = f'http://localhost:{int(os.environ.get("PORT"))}'
#c.ConfigurableHTTPProxy.auth_token = os.environ.get("CONFIGPROXY_AUTH_TOKEN")

# Proxy configuration
c.JupyterHub.cleanup_servers = False
c.ConfigurableHTTPProxy.should_start = False  # Don't start the proxy

# Clean up the proxy URL and ensure no double /api
proxy_base_url = os.environ.get('PROXY_WEB_URL', '').rstrip('/')
if proxy_base_url.endswith('/api'):
    proxy_base_url = proxy_base_url[:-4]
c.ConfigurableHTTPProxy.api_url = f"{proxy_base_url}/api"
c.ConfigurableHTTPProxy.auth_token = os.environ.get('CONFIGPROXY_AUTH_TOKEN')

# Debug logging for proxy communication
c.ConfigurableHTTPProxy.debug = True

# Ensure these environment variables are required
required_env_vars = ['PORT', 'PROXY_WEB_URL', 'CONFIGPROXY_AUTH_TOKEN']
missing_vars = [var for var in required_env_vars if not os.environ.get(var)]
if missing_vars:
    raise ValueError(f'Required environment variables not set: {", ".join(missing_vars)}')