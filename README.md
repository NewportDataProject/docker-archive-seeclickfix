Update the Newport Data Project archive of seeclickfix data.  The container will run and then shutdown.

## Usage
1. Build the docker container
`docker build scf-archive .`
2. Run the docker container with the github password
`docker run -e GITHUB_PASSWORD=<git_password> scf-archive`

User can be set with `GITHUB_USER` environment variable.