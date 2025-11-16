<h1 id="microforge" align="center" style="font-size:40px;">
 <b>⚒️MicroForge🗡️</b>
 </h1>

 <p align="center" style="font-size:15px;">
 <em>
Kickstart your microservices projects with secure authentication,
scalable services, automated CI/CD pipelines, and built-in monitoring.
</em></p>

<p align="center">
  <a href="https://github.com/MetalCloud1/MicroForge/actions/workflows/ci-cd.yaml">
    <img src="https://img.shields.io/github/actions/workflow/status/MetalCloud1/MicroForge/ci-cd.yaml?branch=dev&style=for-the-badge&logo=githubactions&logoColor=white" alt="CI/CD">
  </a>
  <img src="https://img.shields.io/badge/version-v1.0.1-4f8cc9?style=for-the-badge&logo=git&logoColor=white" alt="Version">
  <img src="https://img.shields.io/badge/python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/docker-ready-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/template-ready-2ea44f?style=for-the-badge&logo=github&logoColor=white" alt="Template">
</p>

<p align="center">🚀 Version 1.0.1 — stable release</p>
<p align="center">❗ Note: initial/primitive release may contain minor issues.</p>

<h2 align="center">
 
🧭 About MicroForge (context)
 
</h2>

<p>
 
MicroForge began as my first end-to-end cloud learning platform — a practical environment where I taught myself to design, deploy, and operate real infrastructure instead of learning through isolated exercises.
It captures the foundational engineering lessons that shaped how I now approach systems: secure-by-design workflows, reproducible environments, GitOps-driven automation, and observability as a core requirement.

This project is intentionally hands-on and iterative. Every component reflects a decision, a trade-off, or a failure that forced clarity. MicroForge is not meant to be polished; it’s meant to be real.
It documents the exact engineering patterns that built my current technical foundation.

</p>

<h2 id="overview">🔍 Project Overview</h2>

<p>
MicroForge is a cloud-native microservices template that gives you a reproducible base for building service-oriented systems. It includes:
</p>

<ul>
  <li><strong>IaC</strong>: Terraform modules for PostgreSQL RDS, AWS Secrets Manager, and Kubernetes infra.</li>
  <li><strong>Kubernetes</strong>: manifests for Deployments, Services, Namespaces, ServiceAccounts and (optionally) IRSA/OIDC roles.</li>
  <li><strong>CI/CD</strong>: GitHub Actions workflows for linting, testing, building Docker images and optional deployments.</li>
  <li><strong>Security</strong>: environment-specific secrets, password hashing, and optional HIBP checks.</li>
  <li><strong>Observability</strong>: Prometheus metrics, Loki JSON logs, Grafana dashboards (provisionable via Helm).</li>
  <li><strong>Microservices</strong>: `auth_service` (complete auth flow) and `users-api` (scaffold).</li>
</ul>

---

<h1 id="architecture" align="center">

🏗️ Architecture

</h1>

</hr>


<p align="center">
  <img src="docs/diagrams/diagrams-svg-files/ProjectArchitecture.svg" width="600" alt="Project Architecture"/>
</p>


<h1 align="center">

📂 Project Structure

</h1>

---

<h2 id="project-overview-diagram" align="center">

1️⃣ Project Overview

</h2>

<p align="center"><img src="docs/diagrams/diagrams-svg-files/Project-Overview.svg" width="600" alt="Project Overview"/></p>

<h2 id="repo-workflows" align="center">

2️⃣ 

2️⃣  Auth Service

</h2>

<p align="center"><img src="docs/diagrams/diagrams-svg-files/auth-service.svg" width="600" alt="Auth Service"/></p>

<h2 id="monitoring-diagram" align="center">

3️⃣ Monitoring

</h2>

<p align="center"><img src="docs/diagrams/diagrams-svg-files/monitoring.svg" width="600" alt="Monitoring"/></p>

<h2 id="terraform-diagram" align="center">

4️⃣ Terraform

</h2>

<p align="center"><img src="docs/diagrams/diagrams-svg-files/terraform.svg" width="600" alt="Terraform"/></p>

<h2 id="demo-service-diagram" align="center">
 
5️⃣ Template / Demo Service

</h2>

<p align="center"><img src="docs/diagrams/diagrams-svg-files/demo-service.svg" width="600" alt="Demo Service"/></p>

<hr/>

<h1 id="ci-cd-pipeline" align="center">

🔄 CI/CD Pipeline

</h1>

<p align="center">
  <img src="docs/diagrams/diagrams-svg-files/PipelineCI-CD.svg" width="600" alt="CI/CD Pipeline"/>
</p>

<p><strong>Workflow summary</strong>:</p>
<ol>
  <li><code>lint</code> → static checks (ruff / mypy / black)</li>
  <li><code>test</code> → unit + integration tests (<code>pytest</code>)</li>
  <li><code>build</code> → Docker image build & tag</li>
  <li><code>publish</code> → push image to registry (optional)</li>
  <li><code>deploy</code> → manual/automated deployment to staging/production</li>
</ol>

<h2 id="observability">🛰️ Observability & Monitoring (clear scope)</h2>

<p>
Monitoring is provided and intentionally scoped to two dedicated namespaces so you can compare Dev vs Prod easily:
</p>


<ul>
  <li><strong>Namespaces monitored</strong>:
    <ul>
      <li><code>auth-dev</code> — development / staging environment</li>
      <li><code>auth-prod</code> — production environment</li>
    </ul>
  </li>
  <li><strong>Monitoring stack (recommended)</strong>:
    <ul>
      <li>Prometheus (kube-prometheus-stack) — scrapes service endpoints and kube metrics</li>
      <li>Loki (loki-stack) — collects structured JSON logs</li>
      <li>Grafana — dashboards for latency, throughput, errors; dashboards are pre-bundled and can be provisioned</li>
    </ul>
  </li>
</ul>

<h3>How monitoring is configured</h3>

---

<p>
- Prometheus is configured to <strong>scrape metrics from pods/services in the namespaces <code>auth-dev</code> and <code>auth-prod</code></strong>. Use the Prometheus Helm values file at <code>monitoring/prometheus-values.yaml</code> to set the namespaceSelectors/namespaceRegex or static targets.  
- Loki is installed with a values file at <code>monitoring/values.yaml</code> and configured to collect pod logs cluster-wide but dashboards are filtered by namespace.  
- Grafana contains pre-made dashboards that use the <code>namespace</code> label so you can switch between <code>auth-dev</code> and <code>auth-prod</code> views.
</p>

<h3>Quick install (Helm)</h3>

```bash
# add chart repos
helm repo add grafana https://grafana.github.io/helm-charts
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# install Loki (replace monitoring/values.yaml with your values)
helm upgrade --install loki-stack grafana/loki-stack -n monitoring -f monitoring/values.yaml --create-namespace

# install kube-prometheus-stack (replace monitoring/prometheus-values.yaml with your values)
helm upgrade --install prom-stack prometheus-community/kube-prometheus-stack -n monitoring -f monitoring/prometheus-values.yaml
```
<h3>Notes: ensuring Prometheus scrapes only the auth namespaces</h3>

In your monitoring/prometheus-values.yaml you can add a serviceMonitor or modify the namespaceSelector so Prometheus scrapes only auth-dev and auth-prod. Example snippet:

```yaml
prometheus:
  prometheusSpec:
    serviceMonitorSelectorNilUsesHelmValues: false
    serviceMonitorSelector:
      matchExpressions:
        - {key: kubernetes.io/metadata.name, operator: In, values: ["auth-dev", "auth-prod"]}
```

(Adjust according to the chart version — the repo contains example values.)

<h3>Access Grafana</h3>

```bash
# port-forward Grafana (example service name for kube-prometheus-stack)
kubectl port-forward svc/prom-stack-grafana -n monitoring 3000:80
# then open http://localhost:3000
```

<h1 id="quick-start" align="center">⚡ Quick Start</h1>

<h2 id="prerequisites" align="center">Pre-requisites</h2>

<ul>
  <li>Docker & Docker Compose (for local/demo)</li>
  <li>Python 3.11+</li>
  <li>PostgreSQL (local or managed) — or use the provided Docker image</li>
  <li><code>kubectl</code>, <code>helm</code> (if testing Kubernetes/Helm flows)</li>
  <li>(Optional) AWS CLI + credentials for Terraform / real deployments</li>
</ul>

<h3>1) Create namespaces</h3>

```bash
# create dev namespace
kubectl apply -f k8s/namespaces/auth-dev.yaml

# create prod namespace (if you want to test prod layout too)
kubectl apply -f k8s/namespaces/auth-prod.yaml
```

Example content for the namespace manifest (k8s/namespaces/auth-dev.yaml):

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: auth-dev
  labels:
    environment: dev
```
<h3>2) Deploy Postgres and services (relative paths)</h3>

```bash
# deploy Postgres into auth-dev
kubectl apply -n auth-dev -f ./k8s/postgres/

# deploy auth service into auth-dev
kubectl apply -n auth-dev -f ./k8s/auth_service/

# deploy users-api into auth-dev
kubectl apply -n auth-dev -f ./k8s/users-api/
```
> **Tip:** if manifests already include a namespace: field, -n is still ok; keep the YAMLs consistent.

<h3>3) Verify pods & services</h3>

```bash
kubectl get pods -n auth-dev
kubectl get svc -n auth-dev
kubectl get deploy -n auth-dev
```

<h3>4) Port-forward for local testing</h3>

```bash
# get the auth-service pod name
POD_AUTH=$(kubectl get pods -n auth-dev -l app=auth-service -o jsonpath='{.items[0].metadata.name}')

# forward auth-service pod (example: pod exposes 8000)
kubectl port-forward -n auth-dev $POD_AUTH 8000:8000 &
echo "auth service forwarded at http://localhost:8000"

# get postgres pod name and forward
POD_PG=$(kubectl get pods -n auth-dev -l app=postgres -o jsonpath='{.items[0].metadata.name}')
kubectl port-forward -n auth-dev $POD_PG 5432:5432 &
echo "postgres forwarded at localhost:5432"
```

<h3>5) Smoke tests (curl)</h3>

```bash
# register a user
curl -s -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"email":"tester@example.com","password":"Test1234!"}' | jq

# request a token (form style)
curl -s -X POST http://localhost:8000/token \
  -d "username=tester@example.com&password=Test1234!" | jq
```

<h3>6) Running tests inside the cluster (recommended for integration tests)</h3>

* If your test suite expects pods and DB, run the tests from a ephemeral pod with the repo mounted or using an image that has pytest and dependencies:

```bash
# run tests from a temporary pod mounting current repo (requires accessible files from runner)
kubectl run -n auth-dev test-runner --rm -i --tty --image=python:3.11 -- bash -c "
  pip install -r /tmp/repo/auth_service/requirements-test.txt &&
  pytest /tmp/repo/auth_service/tests -q
"
```

(Alternative: kubectl exec into an existing test pod if you have one.)

<hr/> <h2 id="docker-quickstart">🐳 Quick Start — Docker (alternative)</h2> 

<p> If you prefer to test locally with Docker, use a dedicated Docker network so containers can talk to each other. </p>

 <h3>1) Create Docker network</h3>

 ```bash
 docker network create microforge-net || true
```

<h3>2) Start Postgres</h3>

```bash
docker run -d --name mg-postgres --network microforge-net \
  -e POSTGRES_USER=authuser -e POSTGRES_PASSWORD=authpass -e POSTGRES_DB=authdb \
  -p 5432:5432 postgres:13
```
<h3>3) Start services (default images)</h3>

```bash
docker run -d --name auth-service --network microforge-net \
  -e POSTGRES_HOST=mg-postgres -e POSTGRES_USER=authuser -e POSTGRES_PASSWORD=authpass -e POSTGRES_DB=authdb \
  -p 8000:8000 gilbr/auth-service:latest

docker run -d --name users-api --network microforge-net \
  -e POSTGRES_HOST=mg-postgres -e POSTGRES_USER=authuser -e POSTGRES_PASSWORD=authpass -e POSTGRES_DB=authdb \
  -p 8080:8080 gilbr/users-api:latest
```

<hr/> <h2 id="postgres-test-config">🗄️ PostgreSQL test configuration</h2>

Environment used by the workflow's PostgreSQL service:

```ini
POSTGRES_USER=testuser
POSTGRES_PASSWORD=testpass
POSTGRES_DB=testdb
```

Database URL for tests (used in CI jobs):

```bash
postgresql+asyncpg://testuser:testpass@localhost:5432/testdb
```

Environment variables used in CI:

```bash
DATABASE_URL — See PostgreSQL test configuration above.
PYTHONPATH — add service src dirs when running tests locally (example in workflow).
```

<hr/> <h2 id="ci-cd">🔄 CI/CD pipeline (high level)</h2> 

<p> The GitHub Actions workflow runs on PRs and pushes to <code>dev</code> / <code>main</code>. Typical steps: </p>

 <ol> <li><code>lint</code> — ruff / mypy / black</li> <li><code>test</code> — pytest (unit + integration) using the test Postgres service</li> <li><code>build</code> — build Docker images (local or CI registry)</li> <li><code>publish</code> — optional push to container registry</li> <li><code>deploy</code> — manual or automated promotion (staging → prod)</li> </ol>

---

  <h1 id="microservices" align="center">📦 Microservices</h1>

<ul>
  <li><strong>Auth Service (<code>auth_service</code>)</strong> — Full authentication flow: registration, email verification, JWT login/refresh, password hashing, user management.</li>
  <li><strong>Users API (<code>users-api</code>)</strong> — Minimal scaffold service: health endpoint, basic CRUD layout, designed to be copied & extended.</li>
</ul>

   <h2 id="testing">🧪 Testing & Linting</h2> 

   <p> 

   **Run tests locally (example):**

  </p>

```bash
  # run pytest
pytest -q

# run lint/static checks
ruff check .
black --check .
mypy src
```

<p>For integration tests that depend on pods (Postgres/Services), prefer running tests from inside the cluster (see Kubernetes instructions above) or create ephemeral containers that connect to the running Postgres container.</p> 

<hr/>

<h1 id="roadmap" align="center">
📍 Roadmap
</h1>

<p align="center"><img src="docs/diagrams/diagrams-svg-files/roadmap.svg" width="600" alt="Roadmap"/></p>

<p><strong>Planned near-term improvements:</strong></p>
<ul>
  <li>Future releases will pin versions; 1.0 is stable. streamline Helm charts for demo deploys</li>
  <li>Add OAuth2 / social login options</li>
  <li>Add alerting rules for Prometheus + Grafana alertmanager</li>
  <li>Harden Terraform modules; add automated IaC tests</li>
</ul>

<hr/>

<h1 id="contributing--license" align="center">

🤝 Contributing & License

</h1> 

<h2 id="contributing" align="center">

Contributing (short)

</h2> 

<p>This template is intended for learning, inspiration, and building new projects. If you'd like to contribute improvements:</p> <ul> <li>Open an issue describing the change / improvement.</li> <li>Send a PR against the <code>dev</code> branch.</li> <li>Respect the license: contact the author before public redistribution or claiming work as your own.</li> </ul> 

<h2 id="license" align="center">License (short)</h2> 

<p>This project is a <strong>template created by Gilbert Ramírez</strong> (GitHub: <a href="https://github.com/MetalCloud1">
https://github.com/MetalCloud1</a>).

</p> <p><strong>License:</strong> CC BY-NC-ND (custom) — full terms in <code>LICENSE.md</code>.

</p> <p><strong>You may:</strong></p> 

<ul> <li>View, study, and use this template for personal, educational, or inspiration purposes.</li> 

<li>Modify or extend it; substantial transformations that add new functionality may be used as your own work <strong>if you properly acknowledge the original template</strong>.</li> 

</ul> <p><strong>You may NOT:

</strong></p> <ul> <li>Claim the original template as entirely your own in resumes/portfolios without prior notice to the author.</li> <li>Sell, redistribute, or deploy the original template commercially without consent.</li> </ul> <p>



<h2 id="notes">📝 Notes & tips</h2> 

<ul> <li>Docker Compose is useful for quick demos (ephemeral). For more realistic tests use Kubernetes + Helm.</li> <li>Monitoring dashboards are pre-made and filtered by namespace — use <code>auth-dev</code> vs <code>auth-prod</code> to compare behavior.</li> 

<li>Keep a <code>k8s/namespaces/</code> folder with namespace manifests so applying the same namespace is reproducible.</li> <li>Before running a rebase/squash, create a backup branch: <code>git branch backup-main</code>.</li> </ul>

<p align="center">Built with ❤️ by Gilbert Ramírez — <a href="https://github.com/MetalCloud1">github.com/MetalCloud1</a></p> ```
