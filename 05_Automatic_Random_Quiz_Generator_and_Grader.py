import random
import json
import time
import pandas as pd

def load_quiz_questions():
    with open("quiz_questions.json","r") as f:
        return json.load(f)["Questions"]

def load_participatnt_details():
    with open("participant_details.json", "r") as f:
        return json.load(f)["Details"]
    

def dump_participatnt_details(details):
    with open("participant_details.json", "w") as f:
        json.dump({"Details":details},f,indent=4)

def inp_participant_details():
    while True:
        name=input("\nEnter your full name: ").title()
        age=input("Enter your age: ")
        gender=input("Gender (M/F/other): ")
        email_id=input("Enter your email-id: ")
        
        again=input("Do you want to 'Save' or 'Edit' (s/e): ").lower()
        if again=='e':
            continue
        elif again=='s':
            return name,age,gender,email_id
        else:
            print("Invalid input, try again")
    

def quiz(quiz_Q,details_of_participant,inp_details_of_participant):
    num_of_questions=10 # letting the code to decide itself number of questions to ask
    random_questions=random.sample(quiz_Q,num_of_questions)
    start_time=time.time()
    score=0
    for ind_questions, question in enumerate(random_questions):
        print(f"\nQ{ind_questions+1}. {question['Question']}\n")
        for ind_options, option in enumerate(question['Options']):
            print(f"{ind_options+1}. {option} ")    
        while True:
            try:
                user_ans=int(input("Enter the correct number: "))
                if user_ans>0 and user_ans<5:
                    break
                else:
                    print(f"{user_ans} is not in the list, try again.\n")
            except IndexError as i:
                print("Enter only integer number from options\n")
            except Exception as e:
                print("Invalid input, Enter only integer number from options\n")
        
        if question['Options'][user_ans-1]==question['Answer']:
                    score+=1
        
    end_time=time.time()
    time_taken=end_time-start_time
    name,age,gender,email_id=inp_details_of_participant
    score_percentage=round(score/num_of_questions,2)*100
    details_of_participant.append({"name":name,"age":age,"gender":gender,"email-id":email_id,"score_percentage":score_percentage,"time_taken":f"{time_taken:.2f}"})
    dump_participatnt_details(details_of_participant)
    print("\n----------------------------------------------------------")
    print("Here is the Quiz result:")
    print(f"Correct answers: {score}")
    print(f"Incorrect answers: {num_of_questions-score}")
    print(f"Your score is: {score_percentage}%")
    print(f"Total time took for the quiz is {time_taken:.2f} seconds.")

def leader_board():
    with open("participant_details.json","r") as f:
        load_score=json.load(f)["Details"]
        if load_score:
            df=pd.DataFrame(load_score)
            df["time_taken"]=pd.to_numeric(df["time_taken"])
            sorted_leader_board=df.sort_values(by=["score_percentage","time_taken"], ascending=[False,True])[["name","score_percentage","time_taken"]].reset_index(drop=True)
            sorted_leader_board.index+=1
            print(sorted_leader_board)
        else:
            print("\nEmpty leader board.")
    
    
if __name__=='__main__':
    inp_details_of_participant=inp_participant_details()
    details_of_participant=load_participatnt_details()
    quiz_Q=load_quiz_questions()
    quiz(quiz_Q,details_of_participant,inp_details_of_participant)
    leader_board()