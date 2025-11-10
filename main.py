import json
import time
from src.explainer import generate_explanation



def main():
    
    # Result_1
    start_time_r1=time.time()
    result_1 = generate_explanation(topic="Gravity", language="English", tone="friendly")
    print(json.dumps(result_1, indent=2, ensure_ascii=False))

    with open("output/generated_text.txt",'a', encoding="utf-8")as file:
        file.write(f"The Total Time Taken By the Process: {(time.time()-start_time_r1)/60}\n\n\n\n")

    # Result_2
    start_time_r2=time.time()
    result_2 = generate_explanation(topic="Photosynthesis", language="English", tone="friendly")
    print(json.dumps(result_2, indent=2, ensure_ascii=False))

    with open("output/generated_text.txt",'a', encoding="utf-8")as file:
        file.write(f"The Total Time Taken By the Process: {(time.time()-start_time_r2)/60}\n\n\n\n")

 
    # Result_3
    start_time_r3=time.time()
    result_3 = generate_explanation(topic="Tamil Poet Bharathiyaar", language="English", tone="formal")
    print(json.dumps(result_3, indent=2, ensure_ascii=False))

    with open("output/generated_text.txt",'a', encoding="utf-8")as file:
        file.write(f"The Total Time Taken By the Process: {(time.time()-start_time_r3)/60}\n\n\n\n")





if __name__ == "__main__":

    main()