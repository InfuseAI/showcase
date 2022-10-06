install-python-packages:
	pip install -r requirements.txt

download-data:
	kaggle datasets download -d ashishjangra27/face-mask-12k-images-dataset -p ./data/
	unzip ./data/face-mask-12k-images-dataset.zip -d ./data/

show-pipeline:
	python src/model_pipeline_flow.py show

run-pipeline:
	python src/model_pipeline_flow.py run

reset-folder:
	rm -rf ./result/model_* ./data/*