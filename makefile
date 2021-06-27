setup:
	pyenv install 3.8.5
	pyenv virtualenv 3.8.5 meal-plan-optimizer
	pyenv local meal-plan-optimizer
	pip install -r requirements.txt