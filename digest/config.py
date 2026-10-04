"""What the digest tracks. Edit this file to follow other tools."""

TRACKED_REPOS = {
    "Kubernetes": "kubernetes/kubernetes",
    "Terraform": "hashicorp/terraform",
    "Helm": "helm/helm",
    "Argo CD": "argoproj/argo-cd",
    "Prometheus": "prometheus/prometheus",
    "Grafana": "grafana/grafana",
    "Trivy": "aquasecurity/trivy",
    "Ansible": "ansible/ansible",
    "Docker (moby)": "moby/moby",
    "containerd": "containerd/containerd",
}

# GitHub Advisory Database ecosystems relevant to the stack
ADVISORY_ECOSYSTEMS = ["pip", "go", "actions"]
ADVISORY_SEVERITIES = "critical,high"
ADVISORY_LIMIT = 10
