from setuptools import setup

TEST_DEPENDENCIES = [
    "coverage==5.4",
    "requests-mock==1.8.0",
    "pytest==6.2.2",
    "pytest-cov==2.11.1"
]

setup(
    name="osirium-ppa-api",
    version="0.0.1",  # https://semver.org/
    author="Osirium",
    maintainer="Tom Guyatt",
    author_email="supportdesk@osirium.com",
    maintainer_email="tom.guyatt@osirium.com",
    url="http://www.osirium.com/",
    packages=["ppa_api"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=["requests~=2.0", "timeout-decorator==0.5.0"],
    tests_require=TEST_DEPENDENCIES,
    extras_require={"test": TEST_DEPENDENCIES},
    test_suite="tests",
)
