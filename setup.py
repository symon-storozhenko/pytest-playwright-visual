from pathlib import Path
from setuptools import setup


setup(
    name="pytest-playwright-visual",
    author="Symon Storozhenko",
    author_email="symon.storozhenko@gmail.com",
    description="A pytest fixture for visual testing with Playwright",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/symon-storozhenko/pytest-playwright-visual",
    packages=["pytest_playwright_visual"],
    include_package_data=True,
    install_requires=[
        "pytest_playwright>=0.1.2",
        "Pillow>=8.2.0",
        "pixelmatch>=0.3.0",
    ],
    entry_points={
        "pytest11": ["playwright_visual = pytest_playwright_visual.plugin"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Framework :: Pytest",
    ],
    python_requires=">=3.8",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
)
