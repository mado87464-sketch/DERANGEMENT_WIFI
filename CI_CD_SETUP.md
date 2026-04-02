# CI/CD Setup Instructions

## 🚀 GitHub Actions Configuration

### Current Workflows

#### 1. **Docker CI/CD** (`.github/workflows/docker.yml`)
- **Trigger**: Push to main branch, Pull requests
- **Action**: Build and push Docker image to Docker Hub
- **Platforms**: linux/amd64, linux/arm64
- **Testing**: Automatic Docker image testing

#### 2. **CI Tests** (`.github/workflows/ci.yml`)
- **Trigger**: Push to main/develop branches, Pull requests
- **Action**: Run Python tests on multiple versions
- **Python versions**: 3.8, 3.9, 3.10, 3.11
- **Testing**: Unit tests, linting, application startup

#### 3. **Deploy to Production** (`.github/workflows/deploy.yml`)
- **Trigger**: Release publication, manual dispatch
- **Action**: Deploy to production server
- **Requirements**: Server SSH configuration

#### 4. **Trigger CI/CD** (`.github/workflows/trigger.yml`)
- **Trigger**: Push to main branch
- **Action**: Ensure CI/CD workflows activation

## 🔧 Required GitHub Secrets

Configure these secrets in your GitHub repository settings:

### Docker Hub Configuration
```
DOCKER_USERNAME=mado87464
DOCKER_PASSWORD=votre_docker_hub_token
```

### Production Deployment (Optional)
```
PROD_HOST=votre_serveur_ip
PROD_USER=votre_utilisateur_ssh
PROD_SSH_KEY=votre_cle_ssh_privee
PROD_URL=https://votre-domaine.com
```

## 🎯 How CI/CD Works

### Automatic Pipeline
1. **Push to main** → Triggers Docker CI/CD
2. **Build Docker image** → Multi-architecture build
3. **Push to Docker Hub** → Automatic deployment
4. **Run tests** → Verify image functionality
5. **Generate summary** → Deployment report

### Manual Trigger
1. Go to **Actions** tab in GitHub
2. Select **Docker CI/CD** workflow
3. Click **Run workflow**
4. Choose branch (default: main)

## 📊 Monitoring CI/CD

### GitHub Actions Dashboard
- **URL**: https://github.com/mado87464-sketch/DERANGEMENT_WIFI/actions
- **Workflows**: 4 active workflows
- **Status**: Real-time execution status
- **Logs**: Detailed execution logs

### Docker Hub Integration
- **Repository**: https://hub.docker.com/r/mado87464/derangement-wifi
- **Tags**: Automatic versioning
- **Builds**: GitHub Actions integration
- **Security**: Automated vulnerability scanning

## 🔍 Troubleshooting CI/CD

### Common Issues

#### 1. Docker Hub Authentication
```bash
# Check Docker Hub credentials
docker login
# Update DOCKER_USERNAME and DOCKER_PASSWORD secrets
```

#### 2. Build Failures
```bash
# Local testing
docker build -t test-image .
docker run -p 5000:5000 test-image
```

#### 3. Test Failures
```bash
# Run tests locally
python -m pytest tests/
python app.py
```

### Debug Steps

1. **Check GitHub Actions logs**
2. **Verify Docker Hub credentials**
3. **Test local Docker build**
4. **Run local tests**
5. **Check repository permissions**

## 🎉 CI/CD Benefits

### Automated Features
- ✅ **Multi-platform builds** (AMD64/ARM64)
- ✅ **Automatic testing** on each push
- ✅ **Docker Hub integration**
- ✅ **Version management**
- ✅ **Security scanning**
- ✅ **Deployment automation**

### Development Workflow
1. **Code changes** → Push to GitHub
2. **Automatic build** → Docker image creation
3. **Testing** → Quality assurance
4. **Deployment** → Docker Hub publication
5. **Monitoring** → Real-time status

## 📚 Additional Resources

### GitHub Actions Documentation
- **Getting Started**: https://docs.github.com/en/actions
- **Workflow Syntax**: https://docs.github.com/en/actions/using-workflows
- **Docker Actions**: https://github.com/docker/build-push-action

### Docker Hub Documentation
- **Automated Builds**: https://docs.docker.com/docker-hub/builds/
- **Repository Management**: https://docs.docker.com/docker-hub/repos/

---

**CI/CD is now fully configured and ready for automated deployments!** 🚀

For any issues, check the GitHub Actions logs and verify the required secrets are properly configured.
