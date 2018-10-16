# model-storage

![master Branch](https://img.shields.io/badge/branch-master-blue.svg)
[![master Build Status](https://travis-ci.org/DD-DeCaF/model-storage.svg?branch=master)](https://travis-ci.org/DD-DeCaF/model-storage)
[![master Codecov](https://codecov.io/gh/DD-DeCaF/model-storage/branch/master/graph/badge.svg)](https://codecov.io/gh/DD-DeCaF/model-storage/branch/master)
[![master Requirements Status](https://requires.io/github/DD-DeCaF/model-storage/requirements.svg?branch=master)](https://requires.io/github/DD-DeCaF/model-storage/requirements/?branch=master)

![devel Branch](https://img.shields.io/badge/branch-devel-blue.svg)
[![devel Build Status](https://travis-ci.org/DD-DeCaF/model-storage.svg?branch=devel)](https://travis-ci.org/DD-DeCaF/model-storage)
[![devel Codecov](https://codecov.io/gh/DD-DeCaF/model-storage/branch/devel/graph/badge.svg)](https://codecov.io/gh/DD-DeCaF/model-storage/branch/devel)
[![devel Requirements Status](https://requires.io/github/DD-DeCaF/model-storage/requirements.svg?branch=devel)](https://requires.io/github/DD-DeCaF/model-storage/requirements/?branch=devel)

## Development

Run `make setup` first when initializing the project for the first time. Type
`make` to see all commands.

### Environment

Specify environment variables in a `.env` file. See `docker-compose.yml` for the
possible variables and their default values.

* Set `ENVIRONMENT` to either
  * `development`,
  * `testing`, or
  * `production`.
* `SECRET_KEY` Flask secret key. Will be randomly generated in development and testing environments.
* `SENTRY_DSN` DSN for reporting exceptions to
  [Sentry](https://docs.sentry.io/clients/python/integrations/flask/).
* `ALLOWED_ORIGINS`: Comma-seperated list of CORS allowed origins.
