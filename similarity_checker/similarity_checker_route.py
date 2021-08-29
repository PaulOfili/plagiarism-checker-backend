from flask import Blueprint, jsonify, request
from .contollers.similarity_service import calculateSimilarityScoreWithWeb
from flask_cors import cross_origin

similarity_checker_bp = Blueprint('similarity_checker', __name__)

@similarity_checker_bp.route('/online', methods=["POST"])
@cross_origin()
def calculateSimilarityWithWeb():
    file_params = request.get_json()
    calculateSimilarityScoreWithWeb(file_params)
    response = jsonify(message = 'Successfully uploaded document to be checked. Please wait a few seconds to get scan results.')
    return response
