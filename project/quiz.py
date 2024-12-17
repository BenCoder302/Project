import mysql.connector as sqltor
import random

con = None
cur = None

def connect_and_create_database():
    global con, cur
    # Connecting to MYSQL
    con = sqltor.connect(host="localhost", user="root", password="12345678")
    if con.is_connected():
        print("Successfully connected!")

    # Creating database
    cur = con.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS quiz;")
    cur.execute("USE quiz;")
    
def create_table_questions():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            question TEXT,
            option_1 VARCHAR(255),
            option_2 VARCHAR(255),
            option_3 VARCHAR(255),
            option_4 VARCHAR(255),
            correct_answer INT
        );
    """)

def insert_questions():
    with open("load.txt", "r") as file:
        lines = file.readlines()
        i = 0
        with open("load.txt", "r") as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]  
            i = 0
            while i < len(lines):
                if i + 5 >= len(lines):
                    break  
                question = lines[i]  
                option_1 = lines[i + 1][3:].strip()  
                option_2 = lines[i + 2][3:].strip()   
                option_3 = lines[i + 3][3:].strip()  
                option_4 = lines[i + 4][3:].strip()          
                correct_answer_line = lines[i + 5].strip()
                correct_answer = int(correct_answer_line.split('.')[0].strip()) 

                cur.execute("""INSERT INTO questions(question, option_1, option_2, option_3, option_4, correct_answer) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')""".format(question, option_1, option_2, option_3, option_4, correct_answer))
                i += 6
        con.commit()
        print("Updated questions succesfully ...", end="")
        input()

def show_questions():
    cur.execute("SELECT * from questions;")
    result = cur.fetchall()
    print(result)

def fetch_all_questions():
    cur.execute("""
        SELECT id, question, option_1, option_2, option_3, option_4, correct_answer
        FROM questions
    """)
    return cur.fetchall()

def ask_question(question_data):
    question = question_data[1]
    options = [question_data[2], question_data[3], question_data[4], question_data[5]]
    correct_answer = question_data[6]

    random.shuffle(options)

    print(f"\nQuestion: {question}")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")

    while True:
        try:
            user_answer = int(input(f"\nEnter the option number (1-4): "))
            if user_answer < 1 or user_answer > 4:
                print("Invalid choice! Please choose a number between 1 and 4.")
            else:
                break
        except ValueError:
            print("Invalid input! Please enter a valid number.")

    correct_option_index = options.index(question_data[correct_answer + 1]) + 1
    return user_answer == correct_option_index

def start_quiz():
    # Ask for difficulty level
    print("\nSelect Difficulty Level:")
    print("1. Easy (5 questions)")
    print("2. Moderate (10 questions)")
    print("3. Hard (15 questions)")

    difficulty = input("\nEnter your choice (1-3): ")

    if difficulty == "1":
        num_questions = 5
    elif difficulty == "2":
        num_questions = 10
    elif difficulty == "3":
        num_questions = 15
    else:
        print("Invalid choice! Defaulting to Easy.")
        num_questions = 5

    score = 0
    questions = fetch_all_questions()
    total_questions = len(questions)
    
    random.shuffle(questions)
    for question_data in questions[:num_questions]:  
        if ask_question(question_data):
            score += 1

    print(f"\nQuiz Over! Your score: {score}/{num_questions}", end="")
    input()

def finish():
    cur.close()
    con.close()

def print_title():
    title = r"""

   ___  _   _ ___ _____
  / _ \| | | |_ _|__  /
 | | | | | | || |  / /
 | |_| | |_| || | / /_
  \__\_\\___/|___/____|


    """
    print(title)
    print("This is a quiz program which uses mysql database. It loads questions from a file 'load.txt'.")

def user_menu():
    while True:
        print("\n===== Quiz Menu =====")
        print("1. Start Quiz")
        print("2. Update Questions (from load.txt)")
        print("3. Exit")

        choice = input("\nEnter your choice (1-3): ")

        if choice == "1":
            start_quiz()
        elif choice == "2":
            cur.execute("DROP TABLE questions");
            create_table_questions()
            insert_questions()
        elif choice == "3":
            print("Exiting the program...")
            finish()
            break
        else:
            print("Invalid choice! Please choose a valid option (1-3).")

if __name__ == "__main__":
    connect_and_create_database()
    create_table_questions()
    print_title()
    user_menu()
