import setuptools

setuptools.setup(
    name="runnerlib",
    version="0.0.1",
    author="Shai",
    author_email="bianchishai@gmail.com",
    description="Modules to run as command in runner containers",
    url="https://shaiperson.github.io/2022/03/02/plug-play-worker-pattern-3.html",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(include=['runnerlib']),
    install_requires=[
        'requests',
    ],
    python_requires=">=3.7",
)
