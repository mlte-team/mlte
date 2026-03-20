#!/usr/bin/env bash
set -e

# Build python dockerfile and QA dockerfile
(bash build_base.sh)
(cd .. && docker build -t mlte-frontend-ops . -f docker/Dockerfile.frontend_ops)

docker run --rm \
    -v "$(pwd)/../mlte/frontend/nuxt-app/components:/mnt/app/mlte/frontend/nuxt-app/components" \
    -v "$(pwd)/../mlte/frontend/nuxt-app/composables:/mnt/app/mlte/frontend/nuxt-app/composables" \
    -v "$(pwd)/../mlte/frontend/nuxt-app/layouts:/mnt/app/mlte/frontend/nuxt-app/layouts" \
    -v "$(pwd)/../mlte/frontend/nuxt-app/middleware:/mnt/app/mlte/frontend/nuxt-app/middleware" \
    -v "$(pwd)/../mlte/frontend/nuxt-app/modules:/mnt/app/mlte/frontend/nuxt-app/modules" \
    -v "$(pwd)/../mlte/frontend/nuxt-app/pages:/mnt/app/mlte/frontend/nuxt-app/pages" \
    -v "$(pwd)/../mlte/frontend/nuxt-app/plugins:/mnt/app/mlte/frontend/nuxt-app/plugins" \
    mlte-frontend-ops "$@"
