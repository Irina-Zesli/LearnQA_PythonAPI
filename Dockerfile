FROM python
WORKDIR /test_project/
COPY requirenments.txt .
RUN pip install -r requirenments.txt
ENV ENV=dev
CMD python -m pytest -s --alluredir=test_results/ /test_project/tests/