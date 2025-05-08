from setuptools import setup, find_packages

setup(
    name="cut_numbering_manager",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "PyQt5>=5.15.0",
        "python-osc>=1.8.0",
    ],
    entry_points={
        "console_scripts": [
            "cut-numbering-manager=main:main",
        ],
    },
    python_requires=">=3.6",
    author="bassdrum-org",
    description="カット番号管理システム (Cut Numbering Manager)",
    keywords="anime, production, cut, numbering, OBS",
)
