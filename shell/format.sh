#!/bin/bash
isort --sl knowledge_gpt/
black --line-length 120 knowledge_gpt/
flake8 knowledge_gpt/