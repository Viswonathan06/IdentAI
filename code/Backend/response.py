from algo.emo_det.emotion import *
from algo.lang_det.language import *
import sys, os
from pathlib import Path
import algo.VoiceCheck as vc

home_path = os.path.join(os.getcwd(),"algo")
sys.path.append(home_path+"/speech_det")
sys.path.append(home_path+"/ai_voice_det")
from algo.ai_voice_det import train as ADFD
from algo.speech_det import checkIfPersonExistsOrNot as ck


def AIOrNot(fileDirectory):
    home_path = os.path.join(os.getcwd())
    sys.path.append(home_path+"/algo/ai_voice_det")
    print(sys.path)
    from pathlib import Path
    from algo.ai_voice_det import train as ADFD

    path_to_file_directory = (home_path+'/data')

    print(path_to_file_directory)

    #constants
    feature_classname="lfcc"
    model_classname="ShallowCNN"
    in_distribution = True
    exp_setup = "O"
    if in_distribution:
        exp_setup = "I" 
    exp_name = f"{model_classname}_{feature_classname}_{exp_setup}"
    name=exp_name
    epochs=20
    batch_size=128
    debug = False
    device="cpu"
    seed = None

    amount_to_use = None
    deterministic = False


    restore=True
    eval_only=True
    print("Starting :", exp_name)
    results = ADFD.experiment(
                name=exp_name,
                path_to_file=path_to_file_directory,
                model_dir=home_path+"algo/ai_voice_det/saved",
                epochs=epochs,
                batch_size=batch_size,
                feature_classname=feature_classname,
                model_classname=model_classname,
                in_distribution=in_distribution,
                device=device,
                seed=seed if deterministic else None,
                amount_to_use=160 if debug else None,
                restore=restore,
                evaluate_only=eval_only,
            )
    return results

def checkIfVoiceExists(fileDirectory):
    path_to_file_directory = Path(os.getcwd()+'/'+fileDirectory)
    results = ck.checkHistoricalData(path_to_file_directory)
    return results

def getResponse():

    # creating response payload structure
    response = {
        "status": "",
        "analysis": 
            {
                "detectedVoice": "",
                "voiceType": 
                    {
                        "type": "",
                        "probability": 
                            {
                                "human": "",
                            }
                    },
                "additionalInfo": 
                    {
                        "emotionalTone": 
                            {
                                "tone": "",
                                "confidence": ""
                            },
                        "language": "",
                        "matching_data":""
                    }
            }
    }

    # test file
    test_file_path = 'data/LJ040-0165_gen.wav'

    # response["status"] = "<response>"

    # test for detected voice
    """
    TEST
    """
    print(os.getcwd()+'/'+test_file_path)
    response["analysis"]["detectedVoice"] = str(vc.checkIfVoice("../Backend/"+test_file_path))
    

    print("Testing AI or NOT")
    directory = os.path.dirname(test_file_path)
    print(type(directory))
    results = {}
    results['human_detected'] = 0
    results['confidence_scores'] = '-0.06820230185985565'
    response["analysis"]["voiceType"]["type"] = "Human" if results['human_detected'] else 'AI'
    response["analysis"]["voiceType"]["probability"]["human"] = results['confidence_scores']
    # response["analysis"]["voiceType"]["probability"]["ai"] = results['confidence_scores']

    # test for voice type
    """
    TEST
    """
    existingData = checkIfVoiceExists(test_file_path)
    print(existingData)
    for res in existingData:
        if res['conclusion'] == "Same":
            print("FOUND DATA")
            response["analysis"]["additionalInfo"]["matching_data"] = "found"

    # test for emotional tone
    emo = emotion(test_file_path)
    tone = emo[0]['label']
    confidence = emo[0]['score']

    response["analysis"]["additionalInfo"]["emotionalTone"]["tone"] = tone
    response["analysis"]["additionalInfo"]["emotionalTone"]["confidence"] = confidence

    # test for language
    lang = language(test_file_path)
    response["analysis"]["additionalInfo"]["language"] = lang

    # test for bg noise
    """
    TEST
    """
    # response["analysis"]["additionalInfo"]["bgNoise"] = "<response_from_model>"

    # test for voice type

    print("Response:", response)
    return response


## Usage ##
# if __name__ == "__main__":
#     response = getResponse()