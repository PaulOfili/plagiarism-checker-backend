import os
from similarity_checker.module.copyleaks.copyleakscloud import CopyleaksCloud
from similarity_checker.module.copyleaks.consts import Consts

cloud = None
def initializeCopyleaks():
    global cloud
    cloud = CopyleaksCloud(Consts.PRODUCT, os.environ.get("COPYLEAKS_EMAIL"), os.environ.get("COPYLEAKS_API_KEY"))

def calculateSimilarityScoreWithWeb(fileParams):
    print("Submitting a scan request...")
    cloud.createByUrl(fileParams)
    return None