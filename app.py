from flask import Flask
from dotenv import load_dotenv
from flask_cors import cross_origin

from similarity_checker.similarity_checker_route import similarity_checker_bp
from similarity_checker.module.copyleaks.commandfailederror import CommandFailedError
from similarity_checker.contollers.similarity_service import  initializeCopyleaks

load_dotenv()

app = Flask(__name__)

@app.route('/health', methods=["GET"])
@cross_origin()
def getHealth():
   return "Ok"

app.register_blueprint(similarity_checker_bp, url_prefix="/calculate-similarity")

initializeCopyleaks()

@app.errorhandler(CommandFailedError)
def handle_bad_request(e):
    return {"message": e.copyleaksErrorMessage}, 400

if __name__ == '__main__':
    app.run(debug=True)