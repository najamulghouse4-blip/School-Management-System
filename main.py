import json 
from abc import ABC, abstractmethod
from pathlib import Path

database = "school_data.json"
data = {"students":[], "teachers":[]}

if Path(database).exists():
    with open(database,'r') as f:
        content = f.read()
        if content:
            data = json.loads(content)

def save():
    with open(database,"w") as f:
        json.dump(data,f,indent=4)

class Persons(ABC):
    @abstractmethod
    def get_roles():
        pass
    @abstractmethod
    def register(self):
        pass
    @abstractmethod
    def show_details(self):
        pass
    @staticmethod
    def validate_email(e_mail):
        if "@" in e_mail and "." in e_mail:
            return True
        else:
            return False

class Student(Persons):
    def get_roles(self):
        return "Student"
    def register(self):
        name = input("Enter Your Name: ")
        age = int(input("Enter Your Age: "))
        e_mail = input("Enter Your Email: ")
        roll_no = input("Enter Your Roll_no: ")

        if not Persons.validate_email(e_mail):
            print("Invalid E_mail")

        for i in data["students"]:
            if i["roll_no"] == roll_no:
                print("Student already Exist")
                return

        data["students"].append({
            "name":name,
            "age":age,
            "e_mail":e_mail,
            "roll_no":roll_no,
            "grades":{}
        })
        save()
        print(f"Student {name} registered")
    def show_details(self):
        roll_no = input("Enter your Roll_no:")

        for n in data['students']:
            if n['roll_no'] == roll_no:
                grades = n['grades']
                avg = sum(grades.values()) /len(grades) if grades else 0

                print(f"\n Name: {n["name"]}")
                print(f"\n Roll_no: {n["roll_no"]}")
                print(f"\n Grades: {grades}")
                print(f"Average: {avg:.1f}")
                return


    def add_grade(self):
        roll_no = input("Enter your Roll_No: ")
        subject = input("Enter your Subject: ")
        marks = float(input("Enter your marks: "))

        for i in data['students']:
            if i["roll_no"] == roll_no:
                i['grades'] [subject] = marks
                save()
                print("Grade added successfully")
                return
        print("Student not found")

    
        

stud = Student()

class Teacher(Persons):
    def get_roles(self):
        return "Teacher"
    
    def register(self):
          name = input("Enter your name: ")
          age = int(input("Enter your age:"))
          subject = input("Subject: ")
          emp_id = input("Enter your emp_id: ")
          e_mail = input("Enter your e_mail:" )

          if not Persons.validate_email(e_mail):
              print("Invalid Email")
         
          for i in data["teachers"]:
              if i["emp_id"] == emp_id:
                  print("Teacher already exist")
                  return 
        
              
          data["teachers"].append({
                "name":name,
                "age":age,
                "subject":subject,
                "emp_id":emp_id,
                "e_mail":e_mail
            })
          save()
          print(f"Teacher {name} registered")
          
    def show_details(self):
        emp_id = input("Enter you emp_id: ")

        for e in data["teachers"]:
            if e["emp_id"] == emp_id:
                print(f"\n Emp_id {e["emp_id"]}")
                print(f"\n Name: {e["name"]}")
                print(f"\n Subject: {e["subject"]}")


tech = Teacher()

print("Press 1 to register a Student: ")
print("Press 2 to register a Teacher: ")
print("Press 3 to add Grades: ")
print("Press 4 to show a Student details: ")
print("Press 5 to show a Teacher details: ")

choice = int(input("Please Enter Your choice: "))

if choice == 1:
    stud.register()
elif choice ==2:
    tech.register()
elif choice == 3:
    stud.add_grade()
elif choice == 4:
    stud.show_details()
elif choice == 5:
    tech.show_details()
    
