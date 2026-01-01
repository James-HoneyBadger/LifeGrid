# Deployment Guide

This guide covers deploying LifeGrid to various platforms and creating distributable packages.

## Table of Contents

- [PyPI Deployment](#pypi-deployment)
- [Executable Builds](#executable-builds)
- [GitHub Releases](#github-releases)
- [Documentation Deployment](#documentation-deployment)
- [CI/CD Pipeline](#cicd-pipeline)

## PyPI Deployment

### Prerequisites

1. **PyPI Account**: Create an account at [pypi.org](https://pypi.org/)
2. **API Token**: Generate an API token from your PyPI account settings
3. **Build Tools**: Install required packages
   ```bash
   pip install build twine
   ```

### Manual Deployment

1. **Clean previous builds**:
   ```bash
   make clean
   # or
   rm -rf build/ dist/ *.egg-info
   ```

2. **Build distribution packages**:
   ```bash
   python -m build
   ```
   
   This creates:
   - `dist/lifegrid-2.0.0.tar.gz` (source distribution)
   - `dist/lifegrid-2.0.0-py3-none-any.whl` (wheel)

3. **Check package**:
   ```bash
   twine check dist/*
   ```

4. **Test on TestPyPI** (optional but recommended):
   ```bash
   twine upload --repository testpypi dist/*
   pip install --index-url https://test.pypi.org/simple/ lifegrid
   ```

5. **Upload to PyPI**:
   ```bash
   twine upload dist/*
   ```
   
   Enter your PyPI credentials or API token when prompted.

### Automated Deployment (GitHub Actions)

The `.github/workflows/ci-cd.yml` automatically publishes to PyPI when a release is created:

1. **Create a PyPI API Token**
2. **Add token to GitHub Secrets**:
   - Go to repository Settings → Secrets → Actions
   - Add `PYPI_API_TOKEN` with your token
3. **Create a release** (see below)
4. **CI/CD pipeline automatically publishes**

## Executable Builds

### Using PyInstaller

Build standalone executables that include Python and all dependencies.

#### Single Platform

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller lifegrid.spec

# Output in dist/lifegrid or dist/lifegrid.exe
```

#### Customization

Edit `lifegrid.spec`:
- Add icon: `icon='path/to/icon.ico'`
- Console mode: `console=True` for debugging
- Hidden imports: Add to `hiddenimports` list
- Data files: Add to `datas` list

#### Multiple Platforms

Use GitHub Actions (`.github/workflows/release.yml`):
- Builds for Linux, Windows, macOS
- Uploads to GitHub release automatically
- Triggered by version tags

### Platform-Specific Notes

**Windows**:
- Output: `lifegrid.exe`
- May trigger antivirus (false positive)
- Test with Windows Defender

**macOS**:
- Output: `LifeGrid.app` bundle
- May need code signing for distribution
- Users may need to right-click → Open first time

**Linux**:
- Output: `lifegrid` binary
- Requires `chmod +x lifegrid`
- May need to install system dependencies

## GitHub Releases

### Automated Release Process

1. **Update version** in `pyproject.toml` and `src/version.py`

2. **Update CHANGELOG.md** with release notes

3. **Commit changes**:
   ```bash
   git add .
   git commit -m "Release v2.0.0"
   ```

4. **Create and push tag**:
   ```bash
   git tag -a v2.0.0 -m "Release v2.0.0"
   git push origin v2.0.0
   ```

5. **GitHub Actions automatically**:
   - Runs all tests
   - Builds distribution packages
   - Creates GitHub release
   - Builds executables for all platforms
   - Uploads artifacts
   - Publishes to PyPI

### Manual GitHub Release

1. Go to repository → Releases → Draft a new release
2. Choose or create a tag (e.g., `v2.0.0`)
3. Add release title: "LifeGrid v2.0.0"
4. Add release notes from CHANGELOG
5. Attach build artifacts (optional if using CI/CD)
6. Publish release

### Release Checklist

- [ ] All tests passing
- [ ] Version updated in `pyproject.toml`
- [ ] Version updated in `src/version.py`
- [ ] CHANGELOG.md updated
- [ ] Documentation updated
- [ ] Examples tested
- [ ] No uncommitted changes
- [ ] Tag created
- [ ] Release notes prepared

## Documentation Deployment

### GitHub Pages

Deploy Sphinx documentation to GitHub Pages:

1. **Build documentation**:
   ```bash
   cd docs
   make html
   ```

2. **Deploy to gh-pages branch**:
   ```bash
   # Install ghp-import
   pip install ghp-import
   
   # Deploy
   ghp-import -n -p -f docs/_build/html
   ```

3. **Enable GitHub Pages**:
   - Go to repository Settings → Pages
   - Source: Deploy from branch
   - Branch: `gh-pages` / `root`
   - Save

Documentation will be available at: `https://james-honeybadger.github.io/LifeGrid/`

### Read the Docs

Alternative documentation hosting:

1. Go to [readthedocs.org](https://readthedocs.org/)
2. Import repository
3. Configure build
4. Documentation builds automatically on push

## CI/CD Pipeline

### GitHub Actions Workflows

#### CI/CD Pipeline (`.github/workflows/ci-cd.yml`)

Runs on:
- Push to master/main/develop
- Pull requests
- Release events

Jobs:
- **Test**: Run tests on multiple Python versions and platforms
- **Lint**: Code quality checks (black, isort, flake8)
- **Docs**: Build Sphinx documentation
- **Build**: Create distribution packages
- **Publish**: Upload to PyPI (on release only)

#### Release Workflow (`.github/workflows/release.yml`)

Runs on:
- Version tags (e.g., `v2.0.0`)

Jobs:
- **Create Release**: Generate GitHub release with changelog
- **Build Executables**: Create binaries for all platforms
- **Upload**: Attach executables to release

### Setting Up CI/CD

1. **GitHub Secrets** (repository Settings → Secrets):
   - `PYPI_API_TOKEN`: Your PyPI API token
   - `CODECOV_TOKEN`: Codecov token (optional)

2. **Branch Protection** (recommended):
   - Require status checks to pass
   - Require tests to pass before merging
   - Require reviews for pull requests

3. **Test Locally** before pushing:
   ```bash
   make test
   make lint
   make docs
   make build
   ```

### Monitoring CI/CD

- **GitHub Actions**: Check Actions tab in repository
- **Codecov**: View coverage reports at codecov.io
- **PyPI**: Check package page for latest version

## Version Management

### Version Files

Update version in:
1. `pyproject.toml` - `version = "2.0.0"`
2. `src/version.py` - `__version__ = "2.0.0"`
3. `docs/conf.py` - `release = "2.0.0"`

### Version Bumping Script

```bash
#!/bin/bash
# bump_version.sh
NEW_VERSION=$1

if [ -z "$NEW_VERSION" ]; then
    echo "Usage: ./bump_version.sh 2.1.0"
    exit 1
fi

# Update pyproject.toml
sed -i "s/version = \".*\"/version = \"$NEW_VERSION\"/" pyproject.toml

# Update version.py
echo "__version__ = \"$NEW_VERSION\"" > src/version.py

# Update docs/conf.py
sed -i "s/release = '.*'/release = '$NEW_VERSION'/" docs/conf.py

echo "Version bumped to $NEW_VERSION"
echo "Don't forget to:"
echo "  1. Update CHANGELOG.md"
echo "  2. Commit changes"
echo "  3. Create tag: git tag v$NEW_VERSION"
echo "  4. Push: git push origin v$NEW_VERSION"
```

## Distribution Checklist

Before releasing:

### Code Quality
- [ ] All tests pass (`make test`)
- [ ] No linting errors (`make lint`)
- [ ] Type checking clean (`make typecheck`)
- [ ] Code formatted (`make format`)
- [ ] Documentation builds (`make docs`)

### Version Management
- [ ] Version bumped in all files
- [ ] CHANGELOG updated
- [ ] Release notes prepared

### Testing
- [ ] Examples run successfully
- [ ] Executables tested on target platforms
- [ ] Package installs correctly (`pip install dist/*.whl`)
- [ ] Import works: `python -c "from src.core.simulator import Simulator"`

### Documentation
- [ ] README updated
- [ ] API docs current
- [ ] Examples work
- [ ] Links valid

### Distribution
- [ ] Built successfully (`make build`)
- [ ] Twine check passes
- [ ] TestPyPI upload successful (optional)
- [ ] Tag created
- [ ] GitHub release created
- [ ] PyPI published
- [ ] Executables available

## Troubleshooting

### Build Failures

**Issue**: Tests fail on Windows
- Check line endings (use `.gitattributes`)
- Verify Windows-specific paths

**Issue**: PyInstaller missing modules
- Add to `hiddenimports` in `lifegrid.spec`
- Test import: `python -c "import module_name"`

**Issue**: Documentation build fails
- Check Sphinx extensions installed
- Verify RST syntax
- Check cross-references

### PyPI Issues

**Issue**: Upload rejected
- Check version not already exists
- Verify package metadata
- Run `twine check dist/*`

**Issue**: Package not installable
- Test: `pip install dist/*.whl`
- Check dependencies in `pyproject.toml`
- Verify Python version requirement

### CI/CD Issues

**Issue**: GitHub Actions failing
- Check workflow syntax
- Verify secrets configured
- Review action logs

**Issue**: Codecov not updating
- Verify token configured
- Check coverage.xml generated
- Review Codecov dashboard

## Support

For deployment issues:
- Check [GitHub Issues](https://github.com/James-HoneyBadger/LifeGrid/issues)
- Review [CI/CD logs](https://github.com/James-HoneyBadger/LifeGrid/actions)
- Consult [PyPI documentation](https://packaging.python.org/)

---

**Ready to Deploy!** 🚀
