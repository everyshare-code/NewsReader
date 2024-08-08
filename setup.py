from setuptools import setup, find_packages

setup(
    name="news_crawler",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4",
        "requests",
        "ray",
        "playwright"
    ],
    entry_points={
        "console_scripts": [
            "crawl-news=news_crawler.crawler:main"
        ]
    },
    author="everyshare",
    author_email="park20542040@gmail.com",
    description="A web scraping module to fetch news articles",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/everyshare/news_crawler",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
