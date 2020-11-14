import mariadb
from math import ceil

con = mariadb.connect(
    user="root",
    password="hacker",
    host="localhost",
    port=3360,
    database="test1"
)
con.autocommit = True
cur = con.cursor()


def student_login():
    print("\n\n\t*****WELCOME TO STUDEDNT LOGIN*****")
    usn = input('student usn : ')
    return usn


def adviser_login():
    print("\n\n\t*****CLASS ADVISER LOGIN*****")
    print('faculty id : ')
    fid = input()
    print("passwordd : ")
    passwordd = input()
    return fid, passwordd


# STUDENT CLASS
class student:
    def __init__(self):
        usn = student_login()
        query = 'select * from student'
        cur.execute(query)
        r = cur.fetchall()
        for i in r:
            if usn == i[0]:
                print("Name: {}\nUSN: {}\n".format(i[1].upper(), i[0].upper()))
                qu = "SELECT i.usn,s.sem,s.section,i.subcode,i.final," \
                     "CASE WHEN final >= 9  THEN 'ELIGIBLE' ELSE 'NOT ELIGIBLE' END AS CAT " \
                     "FROM iamarks i, class c,semsec s " \
                     "WHERE i.usn = c.usn AND c.ssid = s.ssid AND i.usn=%s"
                cur.execute(qu, (usn,))
                res = cur.fetchall()
                print("\n\t\t****results****\n\n  subject \t\tfinal marks\t\teligibility\n")

                for j in res:
                    final = j[4]
                    print("-------------------------------------------------")
                    print("  ", j[3], "\t\t", float(final), "\t\t\t", j[5], "\n")
                print("\n\t\t****attendance****\n\n subject \t\tattendance\t\teligibility")
                query = "select a.subcode,a.attendance, " \
                        "CASE when a.attendance >=75 then 'ELIGIBLE' ELSE 'NOT ELIGIBLE' END AS ATT " \
                        "FROM attendance a where a.usn=%s"
                cur.execute(query, (usn,))
                res = cur.fetchall()
                for j in res:
                    print("-------------------------------------------------")
                    print(j[0], " \t\t", j[1], "\t\t\t", j[2], "\n")
                break
        else:
            print("USN : {} not found".format(usn))


# CLASS 2A
def classs2A(id, password):
    query = 'select * from class_adviser where ssid=1'  #####
    cur.execute(query)
    res = cur.fetchall()
    for i in res:
        if id == i[0]:
            if password == i[2]:
                print("\nname: {}\nFID: {}".format(i[1].upper(), i[0].upper()))
                print("Class Adviser of Class 2A \n")  #####
                while 1:
                    print("\n---options---")
                    print(
                        "1-view class marks\n2-view class attendance\n3-view single student marks\n4-update "
                        "marks\n5-update attendance\n6-add student\n7-add marks and attendance\n0-Exit\n")
                    ch = int(input())

                    # view class marks
                    if ch == 1:
                        query = 'select * from iamarks where ssid=1'  #####
                        cur.execute(query)
                        store = cur.fetchall()
                        print("***MARKS***")
                        print("\nUSN\t\t\t\tSubject Code\t\tssid\t\tTest1\tTest2\tTest3\tfinal marks\t\teligibility\n")
                        print("-----------------------------------------------------------------------------------------------------")
                        for j in store:
                            u = j[0]
                            eligible = 'yes'
                            if j[6] < 9:
                                eligible = 'no'

                            print(j[0], '\t\t', j[1], '\t\t\t', j[2], '\t\t\t', float(j[3]), '\t', float(j[4]),
                                  '\t',
                                  float(j[5]), '\t\t', float(j[6]), "\t\t\t", eligible, "\n")
                            print(
                                "-----------------------------------------------------------------------------------------------------")



                    # view class attendance
                    elif ch == 2:
                        query = 'select * from attendance where ssid=1'  #####
                        cur.execute(query)
                        store = cur.fetchall()
                        print("***ATTENDANCE***")
                        print("\nUSN\t\t\t\tSubject code\tssid\t\tattendance\t\teligibility\n")
                        print("------------------------------------------------------------------------")
                        for j in store:
                            eligible = 'yes'
                            if j[3] < 75:
                                eligible = 'no'
                            print(j[0], "\t\t", j[1], "\t\t", j[2], "\t\t\t", j[3], "\t\t\t", eligible, "\n")
                            print("------------------------------------------------------------------------")

                    # view marks by student usn
                    elif ch == 3:
                        USN = input("Enter usn to View Marks : ")
                        query = 'select * from iamarks where usn=%s AND ssid=1'  #####
                        cur.execute(query, (USN,))
                        store = cur.fetchall()
                        print("\t\tSubject Code\t\tssid\t\tTest1\tTest2\tTest3\t\tfinal marks\t\teligibility\n")
                        for j in store:
                            eligible = 'yes'
                            if j[6] < 9:
                                eligible = 'no'
                            print('\t\t', j[1], '\t\t\t', j[2], '\t\t\t', float(j[3]), '\t', float(j[4]), '\t',
                                  float(j[5]), '\t\t', float(j[6]), "\t\t\t", eligible, "\n")

                    # update marks of student
                    elif ch == 4:
                        print("\nUpdate Marks\n")
                        query1 = 'select * from sub where sem=2'  #####change for different semesters
                        cur.execute(query1)
                        r = cur.fetchall()
                        print("subcode\t\tCourse Name\n")
                        for k in r:
                            print(k[0], "\t\t", k[1], "\n")

                        USN = input("Enter usn to Update Marks : ")
                        sub = input("Enter subject code : ")
                        t1 = int(input("Test 1 marks: "))
                        t2 = int(input("Test 2 marks: "))
                        t3 = int(input("Test 3 marks: "))
                        final = ceil(max((t1 + t2), (t1 + t3), (t2 + t3)))
                        query = "update iamarks set test1=%s,test2=%s,test3=%s,final=%s where usn=%s and subcode=%s and ssid=1"  #####
                        val = (t1, t2, t3, final, USN, sub,)
                        cur.execute(query, val)
                        con.commit()
                        query = "UPDATE iamarks i set final=(SELECT final_m from final_ia f where i.usn=f.usn and i.subcode=f.subcode) where i.ssid=1 AND i.usn=%s"  #####
                        cur.execute(query, (USN,))

                        print("+++++Marks updated+++++ \n")

                    # update attendance of student
                    elif ch == 5:
                        print("\nUpdate Attendance\n")
                        USN = input("Enter usn to Update Attendance : ")
                        sub = input("Enter subject code : ")
                        newAtt = int(input("Enter New attendance in {} :".format(sub)))
                        query = 'update attendance set attendance=%s where usn=%s and subcode=%s and ssid=1'  #####
                        val = (newAtt, USN, sub,)
                        cur.execute(query, val)
                        con.commit()

                        print("+++++Attendance Updated+++++\n")

                    # add new student
                    elif ch == 6:
                        print("\nAdd New Student\n")
                        USN = input("Enter the usn to add :")
                        name = input("Enter the student's Name :")
                        addr = input("Enter Address of student :")
                        ph = input("Enter the Phone No. :")
                        gender = input("M for male and F for female :")
                        query = "INSERT INTO student (usn, sname, address, phone, gender) values(%s,%s,%s,%s,%s)"
                        val = (USN, name, addr, ph, gender,)
                        cur.execute(query, val)
                        query = "INSERT INTO class(usn,ssid) values(%s,%s)"
                        val = (USN, 1,)                                             #####
                        cur.execute(query, val)
                        print("\nNew Student Added\n")
                        con.commit()


                    # ADD IA MARKS AND ATTENDANCE OF NEW/LEFT-OUT STUDENTS
                    elif ch == 7:
                        print("\nAdd IA marks and Attendance\n")
                        query1 = 'select * from sub where sem=2'  #####change for different semesters
                        cur.execute(query1)
                        r = cur.fetchall()
                        print("subcode\t\tCourse Name\n")
                        for k in r:
                            print(k[0], "\t\t", k[1])
                        USN = input("Enter the usn to add :")
                        sub = input("Enter subject code : ")
                        t1 = int(input("Test 1 marks: "))
                        t2 = int(input("Test 2 marks: "))
                        t3 = int(input("Test 3 marks: "))
                        att = int(input("Enter the attendance in {} :".format(sub)))

                        val = (sub, USN,)
                        q = "delete from iamarks where subcode=%s and usn = %s AND ssid = 1"   ####
                        cur.execute(q, val)
                        q1 = "delete from attendance where subcode=%s and usn = %s"
                        cur.execute(q1, val)

                        query = "insert into iamarks(usn,subcode,ssid,test1,test2,test3)values(%s,%s,%s,%s,%s,%s)"
                        val = (USN, sub, 1, t1, t2, t3,)  #####
                        cur.execute(query, val)
                        query = "UPDATE iamarks i set final=(SELECT final_m from final_ia f where i.usn=f.usn and i.subcode=f.subcode) where i.ssid=1 AND i.usn=%s"  #####
                        cur.execute(query, (USN,))
                        print("++++MARKS UPDATED++++")

                        query = "insert into attendance(usn,subcode,ssid,attendance) values(%s,%s,%s,%s)"
                        val = (USN, sub, 1, att,)  ####
                        cur.execute(query, val)
                        print("++++ATTENDANCE UPDATED++++\n\n")


                    # EXIT from class2A
                    elif ch == 0:
                        break

                    else:
                        print("Invalid Choice")
                break
            else:
                print("\t\taccess denied\n\t\tcheck your password ")
                break
    else:
        print("FID : {} not found in class 2A".format(id))  #####


# CLASS 2B
def classs2B(id, password):
    query = 'select * from class_adviser where ssid=2'  #####
    cur.execute(query)
    res = cur.fetchall()
    for i in res:
        if id == i[0]:
            if password == i[2]:
                print("\nname: {}\nFID: {}".format(i[1].upper(), i[0].upper()))
                print("Class Adviser of Class 2B \n")  #####
                while 1:
                    print("\n---options---")
                    print(
                        "1-view class marks\n2-view class attendance\n3-view single student marks\n4-update "
                        "marks\n5-update attendance\n6-add student\n7-add marks and attendance\n0-Exit\n")
                    ch = int(input())

                    # view class marks
                    if ch == 1:
                        query = 'select * from iamarks where ssid=2'  #####
                        cur.execute(query)
                        store = cur.fetchall()
                        print("***MARKS***")
                        print("\nUSN\t\t\t\tSubject Code\t\tssid\t\tTest1\tTest2\tTest3\tfinal marks\t\teligibility\n")
                        print("-----------------------------------------------------------------------------------------------------")
                        for j in store:
                            u = j[0]
                            eligible = 'yes'
                            if j[6] < 9:
                                eligible = 'no'

                            print(j[0], '\t\t', j[1], '\t\t\t', j[2], '\t\t\t', float(j[3]), '\t', float(j[4]),
                                  '\t',
                                  float(j[5]), '\t\t', float(j[6]), "\t\t\t", eligible, "\n")
                            print(
                                "-----------------------------------------------------------------------------------------------------")



                    # view class attendance
                    elif ch == 2:
                        query = 'select * from attendance where ssid=2'  #####
                        cur.execute(query)
                        store = cur.fetchall()
                        print("***ATTENDANCE***")
                        print("\nUSN\t\t\t\tSubject code\tssid\t\tattendance\t\teligibility\n")
                        print("------------------------------------------------------------------------")
                        for j in store:
                            eligible = 'yes'
                            if j[3] < 75:
                                eligible = 'no'
                            print(j[0], "\t\t", j[1], "\t\t", j[2], "\t\t\t", j[3], "\t\t\t", eligible, "\n")
                            print("------------------------------------------------------------------------")

                    # view marks by student usn
                    elif ch == 3:
                        USN = input("Enter usn to View Marks : ")
                        query = 'select * from iamarks where usn=%s AND ssid=2'  #####
                        cur.execute(query, (USN,))
                        store = cur.fetchall()
                        print("\t\tSubject Code\t\tssid\t\tTest1\tTest2\tTest3\t\tfinal marks\t\teligibility\n")
                        for j in store:
                            eligible = 'yes'
                            if j[6] < 9:
                                eligible = 'no'
                            print('\t\t', j[1], '\t\t\t', j[2], '\t\t\t', float(j[3]), '\t', float(j[4]), '\t',
                                  float(j[5]), '\t\t', float(j[6]), "\t\t\t", eligible, "\n")

                    # update marks of student
                    elif ch == 4:
                        print("\nUpdate Marks\n")
                        query1 = 'select * from sub where sem=2'  #####change for different semesters
                        cur.execute(query1)
                        r = cur.fetchall()
                        print("subcode\t\tCourse Name\n")
                        for k in r:
                            print(k[0], "\t\t", k[1], "\n")

                        USN = input("Enter usn to Update Marks : ")
                        sub = input("Enter subject code : ")
                        t1 = int(input("Test 1 marks: "))
                        t2 = int(input("Test 2 marks: "))
                        t3 = int(input("Test 3 marks: "))
                        final = ceil(max((t1 + t2), (t1 + t3), (t2 + t3)))
                        query = "update iamarks set test1=%s,test2=%s,test3=%s,final=%s where usn=%s and subcode=%s and ssid=2"  #####
                        val = (t1, t2, t3, final, USN, sub,)
                        cur.execute(query, val)
                        con.commit()
                        query = "UPDATE iamarks i set final=(SELECT final_m from final_ia f where i.usn=f.usn and i.subcode=f.subcode) where i.ssid=2 AND i.usn=%s"  #####
                        cur.execute(query, (USN,))

                        print("+++++Marks updated+++++ \n")

                    # update attendance of student
                    elif ch == 5:
                        print("\nUpdate Attendance\n")
                        USN = input("Enter usn to Update Attendance : ")
                        sub = input("Enter subject code : ")
                        newAtt = int(input("Enter New attendance in {} :".format(sub)))
                        query = 'update attendance set attendance=%s where usn=%s and subcode=%s and ssid=2'  #####
                        val = (newAtt, USN, sub,)
                        cur.execute(query, val)
                        con.commit()

                        print("+++++Attendance Updated+++++\n")

                    # add new student
                    elif ch == 6:
                        print("\nAdd New Student\n")
                        USN = input("Enter the usn to add :")
                        name = input("Enter the student's Name :")
                        addr = input("Enter Address of student :")
                        ph = input("Enter the Phone No. :")
                        gender = input("M for male and F for female :")
                        query = "INSERT INTO student (usn, sname, address, phone, gender) values(%s,%s,%s,%s,%s)"
                        val = (USN, name, addr, ph, gender,)
                        cur.execute(query, val)
                        query = "INSERT INTO class(usn,ssid) values(%s,%s)"
                        val = (USN, 2,)                                             #####
                        cur.execute(query, val)
                        print("\nNew Student Added\n")
                        con.commit()


                    # ADD IA MARKS AND ATTENDANCE OF NEW/LEFT-OUT STUDENTS
                    elif ch == 7:
                        print("\nAdd IA marks and Attendance\n")
                        query1 = 'select * from sub where sem=2'  #####change for different semesters
                        cur.execute(query1)
                        r = cur.fetchall()
                        print("subcode\t\tCourse Name\n")
                        for k in r:
                            print(k[0], "\t\t", k[1])
                        USN = input("Enter the usn to add :")
                        sub = input("Enter subject code : ")
                        t1 = int(input("Test 1 marks: "))
                        t2 = int(input("Test 2 marks: "))
                        t3 = int(input("Test 3 marks: "))
                        att = int(input("Enter the attendance in {} :".format(sub)))

                        val = (sub, USN,)
                        q = "delete from iamarks where subcode=%s and usn = %s AND ssid = 2"   ####
                        cur.execute(q, val)
                        q1 = "delete from attendance where subcode=%s and usn = %s"
                        cur.execute(q1, val)

                        query = "insert into iamarks(usn,subcode,ssid,test1,test2,test3)values(%s,%s,%s,%s,%s,%s)"
                        val = (USN, sub, 2, t1, t2, t3,)  #####
                        cur.execute(query, val)
                        query = "UPDATE iamarks i set final=(SELECT final_m from final_ia f where i.usn=f.usn and i.subcode=f.subcode) where i.ssid=2 AND i.usn=%s"  #####
                        cur.execute(query, (USN,))
                        print("++++MARKS UPDATED++++")

                        query = "insert into attendance(usn,subcode,ssid,attendance) values(%s,%s,%s,%s)"
                        val = (USN, sub, 2, att,)  ####
                        cur.execute(query, val)
                        print("++++ATTENDANCE UPDATED++++\n\n")


                    # EXIT from class2B
                    elif ch == 0:
                        break

                    else:
                        print("Invalid Choice")
                break
            else:
                print("\t\taccess denied\n\t\tcheck your password ")
                break
    else:
        print("FID : {} not found in class 2B".format(id))  #####


# CLASS 2C
def classs2C(id, password):
    query = 'select * from class_adviser where ssid=3'  #####
    cur.execute(query)
    res = cur.fetchall()
    for i in res:
        if id == i[0]:
            if password == i[2]:
                print("\nname: {}\nFID: {}".format(i[1].upper(), i[0].upper()))
                print("Class Adviser of Class 2C \n")  #####
                while 1:
                    print("\n---options---")
                    print(
                        "1-view class marks\n2-view class attendance\n3-view single student marks\n4-update "
                        "marks\n5-update attendance\n6-add student\n7-add marks and attendance\n0-Exit\n")
                    ch = int(input())

                    # view class marks
                    if ch == 1:
                        query = 'select * from iamarks where ssid=3'  #####
                        cur.execute(query)
                        store = cur.fetchall()
                        print("***MARKS***")
                        print("\nUSN\t\t\t\tSubject Code\t\tssid\t\tTest1\tTest2\tTest3\tfinal marks\t\teligibility\n")
                        print("-----------------------------------------------------------------------------------------------------")
                        for j in store:
                            u = j[0]
                            eligible = 'yes'
                            if j[6] < 9:
                                eligible = 'no'

                            print(j[0], '\t\t', j[1], '\t\t\t', j[2], '\t\t\t', float(j[3]), '\t', float(j[4]),
                                  '\t',
                                  float(j[5]), '\t\t', float(j[6]), "\t\t\t", eligible, "\n")
                            print(
                                "-----------------------------------------------------------------------------------------------------")



                    # view class attendance
                    elif ch == 2:
                        query = 'select * from attendance where ssid=3'  #####
                        cur.execute(query)
                        store = cur.fetchall()
                        print("***ATTENDANCE***")
                        print("\nUSN\t\t\t\tSubject code\tssid\t\tattendance\t\teligibility\n")
                        print("------------------------------------------------------------------------")
                        for j in store:
                            eligible = 'yes'
                            if j[3] < 75:
                                eligible = 'no'
                            print(j[0], "\t\t", j[1], "\t\t", j[2], "\t\t\t", j[3], "\t\t\t", eligible, "\n")
                            print("------------------------------------------------------------------------")

                    # view marks by student usn
                    elif ch == 3:
                        USN = input("Enter usn to View Marks : ")
                        query = 'select * from iamarks where usn=%s AND ssid=3'  #####
                        cur.execute(query, (USN,))
                        store = cur.fetchall()
                        print("\t\tSubject Code\t\tssid\t\tTest1\tTest2\tTest3\t\tfinal marks\t\teligibility\n")
                        for j in store:
                            eligible = 'yes'
                            if j[6] < 9:
                                eligible = 'no'
                            print('\t\t', j[1], '\t\t\t', j[2], '\t\t\t', float(j[3]), '\t', float(j[4]), '\t',
                                  float(j[5]), '\t\t', float(j[6]), "\t\t\t", eligible, "\n")

                    # update marks of student
                    elif ch == 4:
                        print("\nUpdate Marks\n")
                        query1 = 'select * from sub where sem=2'  #####change for different semesters
                        cur.execute(query1)
                        r = cur.fetchall()
                        print("subcode\t\tCourse Name\n")
                        for k in r:
                            print(k[0], "\t\t", k[1], "\n")

                        USN = input("Enter usn to Update Marks : ")
                        sub = input("Enter subject code : ")
                        t1 = int(input("Test 1 marks: "))
                        t2 = int(input("Test 2 marks: "))
                        t3 = int(input("Test 3 marks: "))
                        final = ceil(max((t1 + t2), (t1 + t3), (t2 + t3)))
                        query = "update iamarks set test1=%s,test2=%s,test3=%s,final=%s where usn=%s and subcode=%s and ssid=3"  #####
                        val = (t1, t2, t3, final, USN, sub,)
                        cur.execute(query, val)
                        con.commit()
                        query = "UPDATE iamarks i set final=(SELECT final_m from final_ia f where i.usn=f.usn and i.subcode=f.subcode) where i.ssid=3 AND i.usn=%s"  #####
                        cur.execute(query, (USN,))

                        print("+++++Marks updated+++++ \n")

                    # update attendance of student
                    elif ch == 5:
                        print("\nUpdate Attendance\n")
                        USN = input("Enter usn to Update Attendance : ")
                        sub = input("Enter subject code : ")
                        newAtt = int(input("Enter New attendance in {} :".format(sub)))
                        query = 'update attendance set attendance=%s where usn=%s and subcode=%s and ssid=3'  #####
                        val = (newAtt, USN, sub,)
                        cur.execute(query, val)
                        con.commit()

                        print("+++++Attendance Updated+++++\n")

                    # add new student
                    elif ch == 6:
                        print("\nAdd New Student\n")
                        USN = input("Enter the usn to add :")
                        name = input("Enter the student's Name :")
                        addr = input("Enter Address of student :")
                        ph = input("Enter the Phone No. :")
                        gender = input("M for male and F for female :")
                        query = "INSERT INTO student (usn, sname, address, phone, gender) values(%s,%s,%s,%s,%s)"
                        val = (USN, name, addr, ph, gender,)
                        cur.execute(query, val)
                        query = "INSERT INTO class(usn,ssid) values(%s,%s)"
                        val = (USN, 3,)                                             #####
                        cur.execute(query, val)
                        print("\nNew Student Added\n")
                        con.commit()


                    # ADD IA MARKS AND ATTENDANCE OF NEW/LEFT-OUT STUDENTS
                    elif ch == 7:
                        print("\nAdd IA marks and Attendance\n")
                        query1 = 'select * from sub where sem=2'  #####change for different semesters
                        cur.execute(query1)
                        r = cur.fetchall()
                        print("subcode\t\tCourse Name\n")
                        for k in r:
                            print(k[0], "\t\t", k[1])
                        USN = input("Enter the usn to add :")
                        sub = input("Enter subject code : ")
                        t1 = int(input("Test 1 marks: "))
                        t2 = int(input("Test 2 marks: "))
                        t3 = int(input("Test 3 marks: "))
                        att = int(input("Enter the attendance in {} :".format(sub)))

                        val = (sub, USN,)
                        q = "delete from iamarks where subcode=%s and usn = %s AND ssid = 3"   ####
                        cur.execute(q, val)
                        q1 = "delete from attendance where subcode=%s and usn = %s"
                        cur.execute(q1, val)

                        query = "insert into iamarks(usn,subcode,ssid,test1,test2,test3)values(%s,%s,%s,%s,%s,%s)"
                        val = (USN, sub, 3, t1, t2, t3,)  #####
                        cur.execute(query, val)
                        query = "UPDATE iamarks i set final=(SELECT final_m from final_ia f where i.usn=f.usn and i.subcode=f.subcode) where i.ssid=3 AND i.usn=%s"  #####
                        cur.execute(query, (USN,))
                        print("++++MARKS UPDATED++++")

                        query = "insert into attendance(usn,subcode,ssid,attendance) values(%s,%s,%s,%s)"
                        val = (USN, sub, 3, att,)  ####
                        cur.execute(query, val)
                        print("++++ATTENDANCE UPDATED++++\n\n")


                    # EXIT from class2C         ###
                    elif ch == 0:
                        break

                    else:
                        print("Invalid Choice")
                break
            else:
                print("\t\taccess denied\n\t\tcheck your password ")
                break
    else:
        print("FID : {} not found in class 2C".format(id))  #####


# CLASS 4A
def classs4A(id, password):
    query = 'select * from class_adviser where ssid=4'  #####
    cur.execute(query)
    res = cur.fetchall()
    for i in res:
        if id == i[0]:
            if password == i[2]:
                print("\nname: {}\nFID: {}".format(i[1].upper(), i[0].upper()))
                print("Class Adviser of Class 4A \n")  #####
                while 1:
                    print("\n---options---")
                    print(
                        "1-view class marks\n2-view class attendance\n3-view single student marks\n4-update "
                        "marks\n5-update attendance\n6-add student\n7-add marks and attendance\n0-Exit\n")
                    ch = int(input())

                    # view class marks
                    if ch == 1:
                        query = 'select * from iamarks where ssid=4'  #####
                        cur.execute(query)
                        store = cur.fetchall()
                        print("***MARKS***")
                        print("\nUSN\t\t\t\tSubject Code\t\tssid\t\tTest1\tTest2\tTest3\tfinal marks\t\teligibility\n")
                        print("-----------------------------------------------------------------------------------------------------")
                        for j in store:
                            u = j[0]
                            eligible = 'yes'
                            if j[6] < 9:
                                eligible = 'no'

                            print(j[0], '\t\t', j[1], '\t\t\t', j[2], '\t\t\t', float(j[3]), '\t', float(j[4]),
                                  '\t',
                                  float(j[5]), '\t\t', float(j[6]), "\t\t\t", eligible, "\n")
                            print(
                                "-----------------------------------------------------------------------------------------------------")



                    # view class attendance
                    elif ch == 2:
                        query = 'select * from attendance where ssid=4'  #####
                        cur.execute(query)
                        store = cur.fetchall()
                        print("***ATTENDANCE***")
                        print("\nUSN\t\t\t\tSubject code\tssid\t\tattendance\t\teligibility\n")
                        print("------------------------------------------------------------------------")
                        for j in store:
                            eligible = 'yes'
                            if j[3] < 75:
                                eligible = 'no'
                            print(j[0], "\t\t", j[1], "\t\t", j[2], "\t\t\t", j[3], "\t\t\t", eligible, "\n")
                            print("------------------------------------------------------------------------")

                    # view marks by student usn
                    elif ch == 3:
                        USN = input("Enter usn to View Marks : ")
                        query = 'select * from iamarks where usn=%s AND ssid=4'  #####
                        cur.execute(query, (USN,))
                        store = cur.fetchall()
                        print("\t\tSubject Code\t\tssid\t\tTest1\tTest2\tTest3\t\tfinal marks\t\teligibility\n")
                        for j in store:
                            eligible = 'yes'
                            if j[6] < 9:
                                eligible = 'no'
                            print('\t\t', j[1], '\t\t\t', j[2], '\t\t\t', float(j[3]), '\t', float(j[4]), '\t',
                                  float(j[5]), '\t\t', float(j[6]), "\t\t\t", eligible, "\n")

                    # update marks of student
                    elif ch == 4:
                        print("\nUpdate Marks\n")
                        query1 = 'select * from sub where sem=4'  #####change for different semesters
                        cur.execute(query1)
                        r = cur.fetchall()
                        print("subcode\t\tCourse Name\n")
                        for k in r:
                            print(k[0], "\t\t", k[1], "\n")

                        USN = input("Enter usn to Update Marks : ")
                        sub = input("Enter subject code : ")
                        t1 = int(input("Test 1 marks: "))
                        t2 = int(input("Test 2 marks: "))
                        t3 = int(input("Test 3 marks: "))
                        final = ceil(max((t1 + t2), (t1 + t3), (t2 + t3)))
                        query = "update iamarks set test1=%s,test2=%s,test3=%s,final=%s where usn=%s and subcode=%s and ssid=4"  #####
                        val = (t1, t2, t3, final, USN, sub,)
                        cur.execute(query, val)
                        con.commit()
                        query = "UPDATE iamarks i set final=(SELECT final_m from final_ia f where i.usn=f.usn and i.subcode=f.subcode) where i.ssid=4 AND i.usn=%s"  #####
                        cur.execute(query, (USN,))

                        print("+++++Marks updated+++++ \n")

                    # update attendance of student
                    elif ch == 5:
                        print("\nUpdate Attendance\n")
                        USN = input("Enter usn to Update Attendance : ")
                        sub = input("Enter subject code : ")
                        newAtt = int(input("Enter New attendance in {} :".format(sub)))
                        query = 'update attendance set attendance=%s where usn=%s and subcode=%s and ssid=4'  #####
                        val = (newAtt, USN, sub,)
                        cur.execute(query, val)
                        con.commit()

                        print("+++++Attendance Updated+++++\n")

                    # add new student
                    elif ch == 6:
                        print("\nAdd New Student\n")
                        USN = input("Enter the usn to add :")
                        name = input("Enter the student's Name :")
                        addr = input("Enter Address of student :")
                        ph = input("Enter the Phone No. :")
                        gender = input("M for male and F for female :")
                        query = "INSERT INTO student (usn, sname, address, phone, gender) values(%s,%s,%s,%s,%s)"
                        val = (USN, name, addr, ph, gender,)
                        cur.execute(query, val)
                        query = "INSERT INTO class(usn,ssid) values(%s,%s)"
                        val = (USN, 4,)                                             #####
                        cur.execute(query, val)
                        print("\nNew Student Added\n")
                        con.commit()


                    # ADD IA MARKS AND ATTENDANCE OF NEW/LEFT-OUT STUDENTS
                    elif ch == 7:
                        print("\nAdd IA marks and Attendance\n")
                        query1 = 'select * from sub where sem=4'  #####change for different semesters
                        cur.execute(query1)
                        r = cur.fetchall()
                        print("subcode\t\tCourse Name\n")
                        for k in r:
                            print(k[0], "\t\t", k[1])
                        USN = input("Enter the usn to add :")
                        sub = input("Enter subject code : ")
                        t1 = int(input("Test 1 marks: "))
                        t2 = int(input("Test 2 marks: "))
                        t3 = int(input("Test 3 marks: "))
                        att = int(input("Enter the attendance in {} :".format(sub)))

                        val = (sub, USN,)
                        q = "delete from iamarks where subcode=%s and usn = %s AND ssid = 4"   ####
                        cur.execute(q, val)
                        q1 = "delete from attendance where subcode=%s and usn = %s"
                        cur.execute(q1, val)

                        query = "insert into iamarks(usn,subcode,ssid,test1,test2,test3)values(%s,%s,%s,%s,%s,%s)"
                        val = (USN, sub, 4, t1, t2, t3,)  #####
                        cur.execute(query, val)
                        query = "UPDATE iamarks i set final=(SELECT final_m from final_ia f where i.usn=f.usn and i.subcode=f.subcode) where i.ssid=4 AND i.usn=%s"  #####
                        cur.execute(query, (USN,))
                        print("++++MARKS UPDATED++++")

                        query = "insert into attendance(usn,subcode,ssid,attendance) values(%s,%s,%s,%s)"
                        val = (USN, sub, 4, att,)  ####
                        cur.execute(query, val)
                        print("++++ATTENDANCE UPDATED++++\n\n")


                    # EXIT from class4A
                    elif ch == 0:
                        break

                    else:
                        print("Invalid Choice")
                break
            else:
                print("\t\taccess denied\n\t\tcheck your password ")
                break
    else:
        print("FID : {} not found in class 4A".format(id))  #####


# CLASS 4B
def classs4B(id, password):
    query = 'select * from class_adviser where ssid=5'  #####
    cur.execute(query)
    res = cur.fetchall()
    for i in res:
        if id == i[0]:
            if password == i[2]:
                print("\nname: {}\nFID: {}".format(i[1].upper(), i[0].upper()))
                print("Class Adviser of Class 4B \n")  #####
                while 1:
                    print("\n---options---")
                    print(
                        "1-view class marks\n2-view class attendance\n3-view single student marks\n4-update "
                        "marks\n5-update attendance\n6-add student\n7-add marks and attendance\n0-Exit\n")
                    ch = int(input())

                    # view class marks
                    if ch == 1:
                        query = 'select * from iamarks where ssid=5'  #####
                        cur.execute(query)
                        store = cur.fetchall()
                        print("***MARKS***")
                        print("\nUSN\t\t\t\tSubject Code\t\tssid\t\tTest1\tTest2\tTest3\tfinal marks\t\teligibility\n")
                        print("-----------------------------------------------------------------------------------------------------")
                        for j in store:
                            u = j[0]
                            eligible = 'yes'
                            if j[6] < 9:
                                eligible = 'no'

                            print(j[0], '\t\t', j[1], '\t\t\t', j[2], '\t\t\t', float(j[3]), '\t', float(j[4]),
                                  '\t',
                                  float(j[5]), '\t\t', float(j[6]), "\t\t\t", eligible, "\n")
                            print(
                                "-----------------------------------------------------------------------------------------------------")



                    # view class attendance
                    elif ch == 2:
                        query = 'select * from attendance where ssid=5'  #####
                        cur.execute(query)
                        store = cur.fetchall()
                        print("***ATTENDANCE***")
                        print("\nUSN\t\t\t\tSubject code\tssid\t\tattendance\t\teligibility\n")
                        print("------------------------------------------------------------------------")
                        for j in store:
                            eligible = 'yes'
                            if j[3] < 75:
                                eligible = 'no'
                            print(j[0], "\t\t", j[1], "\t\t", j[2], "\t\t\t", j[3], "\t\t\t", eligible, "\n")
                            print("------------------------------------------------------------------------")

                    # view marks by student usn
                    elif ch == 3:
                        USN = input("Enter usn to View Marks : ")
                        query = 'select * from iamarks where usn=%s AND ssid=5'  #####
                        cur.execute(query, (USN,))
                        store = cur.fetchall()
                        print("\t\tSubject Code\t\tssid\t\tTest1\tTest2\tTest3\t\tfinal marks\t\teligibility\n")
                        for j in store:
                            eligible = 'yes'
                            if j[6] < 9:
                                eligible = 'no'
                            print('\t\t', j[1], '\t\t\t', j[2], '\t\t\t', float(j[3]), '\t', float(j[4]), '\t',
                                  float(j[5]), '\t\t', float(j[6]), "\t\t\t", eligible, "\n")

                    # update marks of student
                    elif ch == 4:
                        print("\nUpdate Marks\n")
                        query1 = 'select * from sub where sem=4'  #####change for different semesters
                        cur.execute(query1)
                        r = cur.fetchall()
                        print("subcode\t\tCourse Name\n")
                        for k in r:
                            print(k[0], "\t\t", k[1], "\n")

                        USN = input("Enter usn to Update Marks : ")
                        sub = input("Enter subject code : ")
                        t1 = int(input("Test 1 marks: "))
                        t2 = int(input("Test 2 marks: "))
                        t3 = int(input("Test 3 marks: "))
                        final = ceil(max((t1 + t2), (t1 + t3), (t2 + t3)))
                        query = "update iamarks set test1=%s,test2=%s,test3=%s,final=%s where usn=%s and subcode=%s and ssid=5"  #####
                        val = (t1, t2, t3, final, USN, sub,)
                        cur.execute(query, val)
                        con.commit()
                        query = "UPDATE iamarks i set final=(SELECT final_m from final_ia f where i.usn=f.usn and i.subcode=f.subcode) where i.ssid=5 AND i.usn=%s"  #####
                        cur.execute(query, (USN,))

                        print("+++++Marks updated+++++ \n")

                    # update attendance of student
                    elif ch == 5:
                        print("\nUpdate Attendance\n")
                        USN = input("Enter usn to Update Attendance : ")
                        sub = input("Enter subject code : ")
                        newAtt = int(input("Enter New attendance in {} :".format(sub)))
                        query = 'update attendance set attendance=%s where usn=%s and subcode=%s and ssid=5'  #####
                        val = (newAtt, USN, sub,)
                        cur.execute(query, val)
                        con.commit()

                        print("+++++Attendance Updated+++++\n")

                    # add new student
                    elif ch == 6:
                        print("\nAdd New Student\n")
                        USN = input("Enter the usn to add :")
                        name = input("Enter the student's Name :")
                        addr = input("Enter Address of student :")
                        ph = input("Enter the Phone No. :")
                        gender = input("M for male and F for female :")
                        query = "INSERT INTO student (usn, sname, address, phone, gender) values(%s,%s,%s,%s,%s)"
                        val = (USN, name, addr, ph, gender,)
                        cur.execute(query, val)
                        query = "INSERT INTO class(usn,ssid) values(%s,%s)"
                        val = (USN, 5,)                                             #####
                        cur.execute(query, val)
                        print("\nNew Student Added\n")
                        con.commit()


                    # ADD IA MARKS AND ATTENDANCE OF NEW/LEFT-OUT STUDENTS
                    elif ch == 7:
                        print("\nAdd IA marks and Attendance\n")
                        query1 = 'select * from sub where sem=4'  #####change for different semesters
                        cur.execute(query1)
                        r = cur.fetchall()
                        print("subcode\t\tCourse Name\n")
                        for k in r:
                            print(k[0], "\t\t", k[1])
                        USN = input("Enter the usn to add :")
                        sub = input("Enter subject code : ")
                        t1 = int(input("Test 1 marks: "))
                        t2 = int(input("Test 2 marks: "))
                        t3 = int(input("Test 3 marks: "))
                        att = int(input("Enter the attendance in {} :".format(sub)))

                        val = (sub, USN,)
                        q = "delete from iamarks where subcode=%s and usn = %s AND ssid = 5"   ####
                        cur.execute(q, val)
                        q1 = "delete from attendance where subcode=%s and usn = %s"
                        cur.execute(q1, val)

                        query = "insert into iamarks(usn,subcode,ssid,test1,test2,test3)values(%s,%s,%s,%s,%s,%s)"
                        val = (USN, sub, 5, t1, t2, t3,)  #####
                        cur.execute(query, val)
                        query = "UPDATE iamarks i set final=(SELECT final_m from final_ia f where i.usn=f.usn and i.subcode=f.subcode) where i.ssid=5 AND i.usn=%s"  #####
                        cur.execute(query, (USN,))
                        print("++++MARKS UPDATED++++")

                        query = "insert into attendance(usn,subcode,ssid,attendance) values(%s,%s,%s,%s)"
                        val = (USN, sub, 5, att,)  ####
                        cur.execute(query, val)
                        print("++++ATTENDANCE UPDATED++++\n\n")


                    # EXIT from class4B
                    elif ch == 0:
                        break

                    else:
                        print("Invalid Choice")
                break
            else:
                print("\t\taccess denied\n\t\tcheck your password ")
                break
    else:
        print("FID : {} not found in class 4B".format(id))  #####


# CLASS 4C
def classs4C(id, password):
    query = 'select * from class_adviser where ssid=6'  #####
    cur.execute(query)
    res = cur.fetchall()
    for i in res:
        if id == i[0]:
            if password == i[2]:
                print("\nname: {}\nFID: {}".format(i[1].upper(), i[0].upper()))
                print("Class Adviser of Class 4C \n")  #####
                while 1:
                    print("\n---options---")
                    print(
                        "1-view class marks\n2-view class attendance\n3-view single student marks\n4-update "
                        "marks\n5-update attendance\n6-add student\n7-add marks and attendance\n0-Exit\n")
                    ch = int(input())

                    # view class marks
                    if ch == 1:
                        query = 'select * from iamarks where ssid=6'  #####
                        cur.execute(query)
                        store = cur.fetchall()
                        print("***MARKS***")
                        print("\nUSN\t\t\t\tSubject Code\t\tssid\t\tTest1\tTest2\tTest3\tfinal marks\t\teligibility\n")
                        print("-----------------------------------------------------------------------------------------------------")
                        for j in store:
                            u = j[0]
                            eligible = 'yes'
                            if j[6] < 9:
                                eligible = 'no'

                            print(j[0], '\t\t', j[1], '\t\t\t', j[2], '\t\t\t', float(j[3]), '\t', float(j[4]),
                                  '\t',
                                  float(j[5]), '\t\t', float(j[6]), "\t\t\t", eligible, "\n")
                            print(
                                "-----------------------------------------------------------------------------------------------------")



                    # view class attendance
                    elif ch == 2:
                        query = 'select * from attendance where ssid=6'  #####
                        cur.execute(query)
                        store = cur.fetchall()
                        print("***ATTENDANCE***")
                        print("\nUSN\t\t\t\tSubject code\tssid\t\tattendance\t\teligibility\n")
                        print("------------------------------------------------------------------------")
                        for j in store:
                            eligible = 'yes'
                            if j[3] < 75:
                                eligible = 'no'
                            print(j[0], "\t\t", j[1], "\t\t", j[2], "\t\t\t", j[3], "\t\t\t", eligible, "\n")
                            print("------------------------------------------------------------------------")

                    # view marks by student usn
                    elif ch == 3:
                        USN = input("Enter usn to View Marks : ")
                        query = 'select * from iamarks where usn=%s AND ssid=6'  #####
                        cur.execute(query, (USN,))
                        store = cur.fetchall()
                        print("\t\tSubject Code\t\tssid\t\tTest1\tTest2\tTest3\t\tfinal marks\t\teligibility\n")
                        for j in store:
                            eligible = 'yes'
                            if j[6] < 9:
                                eligible = 'no'
                            print('\t\t', j[1], '\t\t\t', j[2], '\t\t\t', float(j[3]), '\t', float(j[4]), '\t',
                                  float(j[5]), '\t\t', float(j[6]), "\t\t\t", eligible, "\n")

                    # update marks of student
                    elif ch == 4:
                        print("\nUpdate Marks\n")
                        query1 = 'select * from sub where sem=4'  #####change for different semesters
                        cur.execute(query1)
                        r = cur.fetchall()
                        print("subcode\t\tCourse Name\n")
                        for k in r:
                            print(k[0], "\t\t", k[1], "\n")

                        USN = input("Enter usn to Update Marks : ")
                        sub = input("Enter subject code : ")
                        t1 = int(input("Test 1 marks: "))
                        t2 = int(input("Test 2 marks: "))
                        t3 = int(input("Test 3 marks: "))
                        final = ceil(max((t1 + t2), (t1 + t3), (t2 + t3)))
                        query = "update iamarks set test1=%s,test2=%s,test3=%s,final=%s where usn=%s and subcode=%s and ssid=6"  #####
                        val = (t1, t2, t3, final, USN, sub,)
                        cur.execute(query, val)
                        con.commit()
                        query = "UPDATE iamarks i set final=(SELECT final_m from final_ia f where i.usn=f.usn and i.subcode=f.subcode) where i.ssid=6 AND i.usn=%s"  #####
                        cur.execute(query, (USN,))

                        print("+++++Marks updated+++++ \n")

                    # update attendance of student
                    elif ch == 5:
                        print("\nUpdate Attendance\n")
                        USN = input("Enter usn to Update Attendance : ")
                        sub = input("Enter subject code : ")
                        newAtt = int(input("Enter New attendance in {} :".format(sub)))
                        query = 'update attendance set attendance=%s where usn=%s and subcode=%s and ssid=6'  #####
                        val = (newAtt, USN, sub,)
                        cur.execute(query, val)
                        con.commit()

                        print("+++++Attendance Updated+++++\n")

                    # add new student
                    elif ch == 6:
                        print("\nAdd New Student\n")
                        USN = input("Enter the usn to add :")
                        name = input("Enter the student's Name :")
                        addr = input("Enter Address of student :")
                        ph = input("Enter the Phone No. :")
                        gender = input("M for male and F for female :")
                        query = "INSERT INTO student (usn, sname, address, phone, gender) values(%s,%s,%s,%s,%s)"
                        val = (USN, name, addr, ph, gender,)
                        cur.execute(query, val)
                        query = "INSERT INTO class(usn,ssid) values(%s,%s)"
                        val = (USN, 6,)                                             #####
                        cur.execute(query, val)
                        print("\nNew Student Added\n")
                        con.commit()


                    # ADD IA MARKS AND ATTENDANCE OF NEW/LEFT-OUT STUDENTS
                    elif ch == 7:
                        print("\nAdd IA marks and Attendance\n")
                        query1 = 'select * from sub where sem=4'  #####change for different semesters
                        cur.execute(query1)
                        r = cur.fetchall()
                        print("subcode\t\tCourse Name\n")
                        for k in r:
                            print(k[0], "\t\t", k[1])
                        USN = input("Enter the usn to add :")
                        sub = input("Enter subject code : ")
                        t1 = int(input("Test 1 marks: "))
                        t2 = int(input("Test 2 marks: "))
                        t3 = int(input("Test 3 marks: "))
                        att = int(input("Enter the attendance in {} :".format(sub)))

                        val = (sub, USN,)
                        q = "delete from iamarks where subcode=%s and usn = %s AND ssid = 6"   ####
                        cur.execute(q, val)
                        q1 = "delete from attendance where subcode=%s and usn = %s"
                        cur.execute(q1, val)

                        query = "insert into iamarks(usn,subcode,ssid,test1,test2,test3)values(%s,%s,%s,%s,%s,%s)"
                        val = (USN, sub, 6, t1, t2, t3,)  #####
                        cur.execute(query, val)
                        query = "UPDATE iamarks i set final=(SELECT final_m from final_ia f where i.usn=f.usn and i.subcode=f.subcode) where i.ssid=6 AND i.usn=%s"  #####
                        cur.execute(query, (USN,))
                        print("++++MARKS UPDATED++++")

                        query = "insert into attendance(usn,subcode,ssid,attendance) values(%s,%s,%s,%s)"
                        val = (USN, sub, 6, att,)  ####
                        cur.execute(query, val)
                        print("++++ATTENDANCE UPDATED++++\n\n")


                    # EXIT from class4C
                    elif ch == 0:
                        break

                    else:
                        print("Invalid Choice")
                break
            else:
                print("\t\taccess denied\n\t\tcheck your password ")
                break
    else:
        print("FID : {} not found in class 4C".format(id))  #####


# CLASS 6A
def classs6A(id, password):
    query = 'select * from class_adviser where ssid=7'  #####
    cur.execute(query)
    res = cur.fetchall()
    for i in res:
        if id == i[0]:
            if password == i[2]:
                print("\nname: {}\nFID: {}".format(i[1].upper(), i[0].upper()))
                print("Class Adviser of Class 6A \n")  #####
                while 1:
                    print("\n---options---")
                    print(
                        "1-view class marks\n2-view class attendance\n3-view single student marks\n4-update "
                        "marks\n5-update attendance\n6-add student\n7-add marks and attendance\n0-Exit\n")
                    ch = int(input())

                    # view class marks
                    if ch == 1:
                        query = 'select * from iamarks where ssid=7'  #####
                        cur.execute(query)
                        store = cur.fetchall()
                        print("***MARKS***")
                        print("\nUSN\t\t\t\tSubject Code\t\tssid\t\tTest1\tTest2\tTest3\tfinal marks\t\teligibility\n")
                        print("-----------------------------------------------------------------------------------------------------")
                        for j in store:
                            u = j[0]
                            eligible = 'yes'
                            if j[6] < 9:
                                eligible = 'no'

                            print(j[0], '\t\t', j[1], '\t\t\t', j[2], '\t\t\t', float(j[3]), '\t', float(j[4]),
                                  '\t',
                                  float(j[5]), '\t\t', float(j[6]), "\t\t\t", eligible, "\n")
                            print(
                                "-----------------------------------------------------------------------------------------------------")



                    # view class attendance
                    elif ch == 2:
                        query = 'select * from attendance where ssid=7'  #####
                        cur.execute(query)
                        store = cur.fetchall()
                        print("***ATTENDANCE***")
                        print("\nUSN\t\t\t\tSubject code\tssid\t\tattendance\t\teligibility\n")
                        print("------------------------------------------------------------------------")
                        for j in store:
                            eligible = 'yes'
                            if j[3] < 75:
                                eligible = 'no'
                            print(j[0], "\t\t", j[1], "\t\t", j[2], "\t\t\t", j[3], "\t\t\t", eligible, "\n")
                            print("------------------------------------------------------------------------")

                    # view marks by student usn
                    elif ch == 3:
                        USN = input("Enter usn to View Marks : ")
                        query = 'select * from iamarks where usn=%s AND ssid=7'  #####
                        cur.execute(query, (USN,))
                        store = cur.fetchall()
                        print("\t\tSubject Code\t\tssid\t\tTest1\tTest2\tTest3\t\tfinal marks\t\teligibility\n")
                        for j in store:
                            eligible = 'yes'
                            if j[6] < 9:
                                eligible = 'no'
                            print('\t\t', j[1], '\t\t\t', j[2], '\t\t\t', float(j[3]), '\t', float(j[4]), '\t',
                                  float(j[5]), '\t\t', float(j[6]), "\t\t\t", eligible, "\n")

                    # update marks of student
                    elif ch == 4:
                        print("\nUpdate Marks\n")
                        query1 = 'select * from sub where sem=6'  #####change for different semesters
                        cur.execute(query1)
                        r = cur.fetchall()
                        print("subcode\t\tCourse Name\n")
                        for k in r:
                            print(k[0], "\t\t", k[1], "\n")

                        USN = input("Enter usn to Update Marks : ")
                        sub = input("Enter subject code : ")
                        t1 = int(input("Test 1 marks: "))
                        t2 = int(input("Test 2 marks: "))
                        t3 = int(input("Test 3 marks: "))
                        final = ceil(max((t1 + t2), (t1 + t3), (t2 + t3)))
                        query = "update iamarks set test1=%s,test2=%s,test3=%s,final=%s where usn=%s and subcode=%s and ssid=7"  #####
                        val = (t1, t2, t3, final, USN, sub,)
                        cur.execute(query, val)
                        con.commit()
                        query = "UPDATE iamarks i set final=(SELECT final_m from final_ia f where i.usn=f.usn and i.subcode=f.subcode) where i.ssid=7 AND i.usn=%s"  #####
                        cur.execute(query, (USN,))

                        print("+++++Marks updated+++++ \n")

                    # update attendance of student
                    elif ch == 5:
                        print("\nUpdate Attendance\n")
                        USN = input("Enter usn to Update Attendance : ")
                        sub = input("Enter subject code : ")
                        newAtt = int(input("Enter New attendance in {} :".format(sub)))
                        query = 'update attendance set attendance=%s where usn=%s and subcode=%s and ssid=7'  #####
                        val = (newAtt, USN, sub,)
                        cur.execute(query, val)
                        con.commit()

                        print("+++++Attendance Updated+++++\n")

                    # add new student
                    elif ch == 6:
                        print("\nAdd New Student\n")
                        USN = input("Enter the usn to add :")
                        name = input("Enter the student's Name :")
                        addr = input("Enter Address of student :")
                        ph = input("Enter the Phone No. :")
                        gender = input("M for male and F for female :")
                        query = "INSERT INTO student (usn, sname, address, phone, gender) values(%s,%s,%s,%s,%s)"
                        val = (USN, name, addr, ph, gender,)
                        cur.execute(query, val)
                        query = "INSERT INTO class(usn,ssid) values(%s,%s)"
                        val = (USN, 7,)                                             #####
                        cur.execute(query, val)
                        print("\nNew Student Added\n")
                        con.commit()


                    # ADD IA MARKS AND ATTENDANCE OF NEW/LEFT-OUT STUDENTS
                    elif ch == 7:
                        print("\nAdd IA marks and Attendance\n")
                        query1 = 'select * from sub where sem=6'  #####change for different semesters
                        cur.execute(query1)
                        r = cur.fetchall()
                        print("subcode\t\tCourse Name\n")
                        for k in r:
                            print(k[0], "\t\t", k[1])
                        USN = input("Enter the usn to add :")
                        sub = input("Enter subject code : ")
                        t1 = int(input("Test 1 marks: "))
                        t2 = int(input("Test 2 marks: "))
                        t3 = int(input("Test 3 marks: "))
                        att = int(input("Enter the attendance in {} :".format(sub)))

                        val = (sub, USN,)
                        q = "delete from iamarks where subcode=%s and usn = %s AND ssid = 7"   ####
                        cur.execute(q, val)
                        q1 = "delete from attendance where subcode=%s and usn = %s"
                        cur.execute(q1, val)

                        query = "insert into iamarks(usn,subcode,ssid,test1,test2,test3)values(%s,%s,%s,%s,%s,%s)"
                        val = (USN, sub, 7, t1, t2, t3,)  #####
                        cur.execute(query, val)
                        query = "UPDATE iamarks i set final=(SELECT final_m from final_ia f where i.usn=f.usn and i.subcode=f.subcode) where i.ssid=7 AND i.usn=%s"  #####
                        cur.execute(query, (USN,))
                        print("++++MARKS UPDATED++++")

                        query = "insert into attendance(usn,subcode,ssid,attendance) values(%s,%s,%s,%s)"
                        val = (USN, sub, 7, att,)  ####
                        cur.execute(query, val)
                        print("++++ATTENDANCE UPDATED++++\n\n")


                    # EXIT from class6A
                    elif ch == 0:
                        break

                    else:
                        print("Invalid Choice")
                break
            else:
                print("\t\taccess denied\n\t\tcheck your password ")
                break
    else:
        print("FID : {} not found in class 6A".format(id))  #####


# CLASS 6B
def classs6B(id, password):
    query = "select * from class_adviser where ssid=8"  #####
    cur.execute(query)
    res = cur.fetchall()
    for i in res:
        if id == i[0]:
            if password == i[2]:
                print("\nname: {}\nFID: {}".format(i[1].upper(), i[0].upper()))
                print("Class Adviser of Class 6B \n")  #####
                while 1:
                    print("\n---options---")
                    print(
                        "1-view class marks\n2-view class attendance\n3-view single student marks\n4-update "
                        "marks\n5-update attendance\n6-add student\n7-add marks and attendance\n0-Exit\n")
                    ch = int(input())

                    # view class marks
                    if ch == 1:
                        query = 'select * from iamarks where ssid=8'  #####
                        cur.execute(query)
                        store = cur.fetchall()
                        print("***MARKS***")
                        print("\nUSN\t\t\t\tSubject Code\t\tssid\t\tTest1\tTest2\tTest3\tfinal marks\t\teligibility\n")
                        print("-----------------------------------------------------------------------------------------------------")
                        for j in store:
                            u = j[0]
                            eligible = 'yes'
                            if j[6] < 9:
                                eligible = 'no'

                            print(j[0], '\t\t', j[1], '\t\t\t', j[2], '\t\t\t', float(j[3]), '\t', float(j[4]),
                                  '\t',
                                  float(j[5]), '\t\t', float(j[6]), "\t\t\t", eligible, "\n")
                            print(
                                "-----------------------------------------------------------------------------------------------------")



                    # view class attendance
                    elif ch == 2:
                        query = 'select * from attendance where ssid=8'  #####
                        cur.execute(query)
                        store = cur.fetchall()
                        print("***ATTENDANCE***")
                        print("\nUSN\t\t\t\tSubject code\tssid\t\tattendance\t\teligibility\n")
                        print("------------------------------------------------------------------------")
                        for j in store:
                            eligible = 'yes'
                            if j[3] < 75:
                                eligible = 'no'
                            print(j[0], "\t\t", j[1], "\t\t", j[2], "\t\t\t", j[3], "\t\t\t", eligible, "\n")
                            print("------------------------------------------------------------------------")

                    # view marks by student usn
                    elif ch == 3:
                        USN = input("Enter usn to View Marks : ")
                        query = 'select * from iamarks where usn=%s AND ssid=8'  #####
                        cur.execute(query, (USN,))
                        store = cur.fetchall()
                        print("\t\tSubject Code\t\tssid\t\tTest1\tTest2\tTest3\t\tfinal marks\t\teligibility\n")
                        for j in store:
                            eligible = 'yes'
                            if j[6] < 9:
                                eligible = 'no'
                            print('\t\t', j[1], '\t\t\t', j[2], '\t\t\t', float(j[3]), '\t', float(j[4]), '\t',
                                  float(j[5]), '\t\t', float(j[6]), "\t\t\t", eligible, "\n")

                    # update marks of student
                    elif ch == 4:
                        print("\nUpdate Marks\n")
                        query1 = 'select * from sub where sem=6'  #####change for different semesters
                        cur.execute(query1)
                        r = cur.fetchall()
                        print("subcode\t\tCourse Name\n")
                        for k in r:
                            print(k[0], "\t\t", k[1], "\n")

                        USN = input("Enter usn to Update Marks : ")
                        sub = input("Enter subject code : ")
                        t1 = int(input("Test 1 marks: "))
                        t2 = int(input("Test 2 marks: "))
                        t3 = int(input("Test 3 marks: "))
                        final = ceil(max((t1 + t2), (t1 + t3), (t2 + t3)))
                        query = "update iamarks set test1=%s,test2=%s,test3=%s,final=%s where usn=%s and subcode=%s and ssid=8"  #####
                        val = (t1, t2, t3, final, USN, sub,)
                        cur.execute(query, val)
                        con.commit()
                        query = "UPDATE iamarks i set final=(SELECT final_m from final_ia f where i.usn=f.usn and i.subcode=f.subcode) where i.ssid=8 AND i.usn=%s"  #####
                        cur.execute(query, (USN,))

                        print("+++++Marks updated+++++ \n")

                    # update attendance of student
                    elif ch == 5:
                        print("\nUpdate Attendance\n")
                        USN = input("Enter usn to Update Attendance : ")
                        sub = input("Enter subject code : ")
                        newAtt = int(input("Enter New attendance in {} :".format(sub)))
                        query = 'update attendance set attendance=%s where usn=%s and subcode=%s and ssid=8'  #####
                        val = (newAtt, USN, sub,)
                        cur.execute(query, val)
                        con.commit()

                        print("+++++Attendance Updated+++++\n")

                    # add new student
                    elif ch == 6:
                        print("\nAdd New Student\n")
                        USN = input("Enter the usn to add :")
                        name = input("Enter the student's Name :")
                        addr = input("Enter Address of student :")
                        ph = input("Enter the Phone No. :")
                        gender = input("M for male and F for female :")
                        query = "INSERT INTO student (usn, sname, address, phone, gender) values(%s,%s,%s,%s,%s)"
                        val = (USN, name, addr, ph, gender,)
                        cur.execute(query, val)
                        query = "INSERT INTO class(usn,ssid) values(%s,%s)"
                        val = (USN, 8,)                                             #####
                        cur.execute(query, val)
                        print("\nNew Student Added\n")
                        con.commit()


                    # ADD IA MARKS AND ATTENDANCE OF NEW/LEFT-OUT STUDENTS
                    elif ch == 7:
                        print("\nAdd IA marks and Attendance\n")
                        query1 = 'select * from sub where sem=6'  #####change for different semesters
                        cur.execute(query1)
                        r = cur.fetchall()
                        print("subcode\t\tCourse Name\n")
                        for k in r:
                            print(k[0], "\t\t", k[1])
                        USN = input("Enter the usn to add :")
                        sub = input("Enter subject code : ")
                        t1 = int(input("Test 1 marks: "))
                        t2 = int(input("Test 2 marks: "))
                        t3 = int(input("Test 3 marks: "))
                        att = int(input("Enter the attendance in {} :".format(sub)))

                        val = (sub, USN,)
                        q = "delete from iamarks where subcode=%s and usn = %s AND ssid = 8"   ####
                        cur.execute(q, val)
                        q1 = "delete from attendance where subcode=%s and usn = %s"
                        cur.execute(q1, val)

                        query = "insert into iamarks(usn,subcode,ssid,test1,test2,test3)values(%s,%s,%s,%s,%s,%s)"
                        val = (USN, sub, 8, t1, t2, t3,)  #####
                        cur.execute(query, val)
                        query = "UPDATE iamarks i set final=(SELECT final_m from final_ia f where i.usn=f.usn and i.subcode=f.subcode) where i.ssid=1 AND i.usn=%s"  #####
                        cur.execute(query, (USN,))
                        print("++++MARKS UPDATED++++")

                        query = "insert into attendance(usn,subcode,ssid,attendance) values(%s,%s,%s,%s)"
                        val = (USN, sub, 8, att,)  ####
                        cur.execute(query, val)
                        print("++++ATTENDANCE UPDATED++++\n\n")


                    # EXIT from class6B
                    elif ch == 0:
                        break

                    else:
                        print("Invalid Choice")
                break
            else:
                print("\t\taccess denied\n\t\tcheck your password ")
                break
    else:
        print("FID : {} not found in class 6B".format(id))  #####


# CLASS 6C
def classs6C(id, password):
    query = 'select * from class_adviser where ssid=9'  #####
    cur.execute(query)
    res = cur.fetchall()
    for i in res:
        if id == i[0]:
            if password == i[2]:
                print("\nname: {}\nFID: {}".format(i[1].upper(), i[0].upper()))
                print("Class Adviser of Class 6C \n")  #####
                while 1:
                    print("\n---options---")
                    print(
                        "1-view class marks\n2-view class attendance\n3-view single student marks\n4-update "
                        "marks\n5-update attendance\n6-add student\n7-add marks and attendance\n0-Exit\n")
                    ch = int(input())

                    # view class marks
                    if ch == 1:
                        query = 'select * from iamarks where ssid=9'  #####
                        cur.execute(query)
                        store = cur.fetchall()
                        print("***MARKS***")
                        print("\nUSN\t\t\t\tSubject Code\t\tssid\t\tTest1\tTest2\tTest3\tfinal marks\t\teligibility\n")
                        print("-----------------------------------------------------------------------------------------------------")
                        for j in store:
                            u = j[0]
                            eligible = 'yes'
                            if j[6] < 9:
                                eligible = 'no'

                            print(j[0], '\t\t', j[1], '\t\t\t', j[2], '\t\t\t', float(j[3]), '\t', float(j[4]),
                                  '\t',
                                  float(j[5]), '\t\t', float(j[6]), "\t\t\t", eligible, "\n")
                            print(
                                "-----------------------------------------------------------------------------------------------------")



                    # view class attendance
                    elif ch == 2:
                        query = 'select * from attendance where ssid=9'  #####
                        cur.execute(query)
                        store = cur.fetchall()
                        print("***ATTENDANCE***")
                        print("\nUSN\t\t\t\tSubject code\tssid\t\tattendance\t\teligibility\n")
                        print("------------------------------------------------------------------------")
                        for j in store:
                            eligible = 'yes'
                            if j[3] < 75:
                                eligible = 'no'
                            print(j[0], "\t\t", j[1], "\t\t", j[2], "\t\t\t", j[3], "\t\t\t", eligible, "\n")
                            print("------------------------------------------------------------------------")

                    # view marks by student usn
                    elif ch == 3:
                        USN = input("Enter usn to View Marks : ")
                        query = 'select * from iamarks where usn=%s AND ssid=9'  #####
                        cur.execute(query, (USN,))
                        store = cur.fetchall()
                        print("\t\tSubject Code\t\tssid\t\tTest1\tTest2\tTest3\t\tfinal marks\t\teligibility\n")
                        for j in store:
                            eligible = 'yes'
                            if j[6] < 9:
                                eligible = 'no'
                            print('\t\t', j[1], '\t\t\t', j[2], '\t\t\t', float(j[3]), '\t', float(j[4]), '\t',
                                  float(j[5]), '\t\t', float(j[6]), "\t\t\t", eligible, "\n")

                    # update marks of student
                    elif ch == 4:
                        print("\nUpdate Marks\n")
                        query1 = 'select * from sub where sem=6'  #####change for different semesters
                        cur.execute(query1)
                        r = cur.fetchall()
                        print("subcode\t\tCourse Name\n")
                        for k in r:
                            print(k[0], "\t\t", k[1], "\n")

                        USN = input("Enter usn to Update Marks : ")
                        sub = input("Enter subject code : ")
                        t1 = int(input("Test 1 marks: "))
                        t2 = int(input("Test 2 marks: "))
                        t3 = int(input("Test 3 marks: "))
                        final = ceil(max((t1 + t2), (t1 + t3), (t2 + t3)))
                        query = "update iamarks set test1=%s,test2=%s,test3=%s,final=%s where usn=%s and subcode=%s and ssid=9"  #####
                        val = (t1, t2, t3, final, USN, sub,)
                        cur.execute(query, val)
                        con.commit()
                        query = "UPDATE iamarks i set final=(SELECT final_m from final_ia f where i.usn=f.usn and i.subcode=f.subcode) where i.ssid=9 AND i.usn=%s"  #####
                        cur.execute(query, (USN,))

                        print("+++++Marks updated+++++ \n")

                    # update attendance of student
                    elif ch == 5:
                        print("\nUpdate Attendance\n")
                        USN = input("Enter usn to Update Attendance : ")
                        sub = input("Enter subject code : ")
                        newAtt = int(input("Enter New attendance in {} :".format(sub)))
                        query = 'update attendance set attendance=%s where usn=%s and subcode=%s and ssid=9'  #####
                        val = (newAtt, USN, sub,)
                        cur.execute(query, val)
                        con.commit()

                        print("+++++Attendance Updated+++++\n")

                    # add new student
                    elif ch == 6:
                        print("\nAdd New Student\n")
                        USN = input("Enter the usn to add :")
                        name = input("Enter the student's Name :")
                        addr = input("Enter Address of student :")
                        ph = input("Enter the Phone No. :")
                        gender = input("M for male and F for female :")
                        query = "INSERT INTO student (usn, sname, address, phone, gender) values(%s,%s,%s,%s,%s)"
                        val = (USN, name, addr, ph, gender,)
                        cur.execute(query, val)
                        query = "INSERT INTO class(usn,ssid) values(%s,%s)"
                        val = (USN, 9,)                                             #####
                        cur.execute(query, val)
                        print("\nNew Student Added\n")
                        con.commit()


                    # ADD IA MARKS AND ATTENDANCE OF NEW/LEFT-OUT STUDENTS
                    elif ch == 7:
                        print("\nAdd IA marks and Attendance\n")
                        query1 = 'select * from sub where sem=9'  #####change for different semesters
                        cur.execute(query1)
                        r = cur.fetchall()
                        print("subcode\t\tCourse Name\n")
                        for k in r:
                            print(k[0], "\t\t", k[1])
                        USN = input("Enter the usn to add :")
                        sub = input("Enter subject code : ")
                        t1 = int(input("Test 1 marks: "))
                        t2 = int(input("Test 2 marks: "))
                        t3 = int(input("Test 3 marks: "))
                        att = int(input("Enter the attendance in {} :".format(sub)))

                        val = (sub, USN,)
                        q = "delete from iamarks where subcode=%s and usn = %s AND ssid = 9"   ####
                        cur.execute(q, val)
                        q1 = "delete from attendance where subcode=%s and usn = %s"
                        cur.execute(q1, val)

                        query = "insert into iamarks(usn,subcode,ssid,test1,test2,test3)values(%s,%s,%s,%s,%s,%s)"
                        val = (USN, sub, 9, t1, t2, t3,)  #####
                        cur.execute(query, val)
                        query = "UPDATE iamarks i set final=(SELECT final_m from final_ia f where i.usn=f.usn and i.subcode=f.subcode) where i.ssid=9 AND i.usn=%s"  #####
                        cur.execute(query, (USN,))
                        print("++++MARKS UPDATED++++")

                        query = "insert into attendance(usn,subcode,ssid,attendance) values(%s,%s,%s,%s)"
                        val = (USN, sub, 9, att,)  ####
                        cur.execute(query, val)
                        print("++++ATTENDANCE UPDATED++++\n\n")


                    # EXIT from class6C
                    elif ch == 0:
                        break

                    else:
                        print("Invalid Choice")
                break
            else:
                print("\t\taccess denied\n\t\tcheck your password ")
                break
    else:
        print("FID : {} not found in class 6C".format(id))  #####


# CLASS 8A
def classs8A(id, password):
    query = 'select * from class_adviser where ssid=10'  #####
    cur.execute(query)
    res = cur.fetchall()
    for i in res:
        if id == i[0]:
            if password == i[2]:
                print("\nname: {}\nFID: {}".format(i[1].upper(), i[0].upper()))
                print("Class Adviser of Class 8A \n")  #####
                while 1:
                    print("\n---options---")
                    print(
                        "1-view class marks\n2-view class attendance\n3-view single student marks\n4-update "
                        "marks\n5-update attendance\n6-add student\n7-add marks and attendance\n0-Exit\n")
                    ch = int(input())

                    # view class marks
                    if ch == 1:
                        query = 'select * from iamarks where ssid=10'  #####
                        cur.execute(query)
                        store = cur.fetchall()
                        print("***MARKS***")
                        print("\nUSN\t\t\t\tSubject Code\t\tssid\t\tTest1\tTest2\tTest3\tfinal marks\t\teligibility\n")
                        print("-----------------------------------------------------------------------------------------------------")
                        for j in store:
                            u = j[0]
                            eligible = 'yes'
                            if j[6] < 9:
                                eligible = 'no'

                            print(j[0], '\t\t', j[1], '\t\t\t', j[2], '\t\t\t', float(j[3]), '\t', float(j[4]),
                                  '\t',
                                  float(j[5]), '\t\t', float(j[6]), "\t\t\t", eligible, "\n")
                            print(
                                "-----------------------------------------------------------------------------------------------------")



                    # view class attendance
                    elif ch == 2:
                        query = 'select * from attendance where ssid=10'  #####
                        cur.execute(query)
                        store = cur.fetchall()
                        print("***ATTENDANCE***")
                        print("\nUSN\t\t\t\tSubject code\tssid\t\tattendance\t\teligibility\n")
                        print("------------------------------------------------------------------------")
                        for j in store:
                            eligible = 'yes'
                            if j[3] < 75:
                                eligible = 'no'
                            print(j[0], "\t\t", j[1], "\t\t", j[2], "\t\t\t", j[3], "\t\t\t", eligible, "\n")
                            print("------------------------------------------------------------------------")

                    # view marks by student usn
                    elif ch == 3:
                        USN = input("Enter usn to View Marks : ")
                        query = 'select * from iamarks where usn=%s AND ssid=10'  #####
                        cur.execute(query, (USN,))
                        store = cur.fetchall()
                        print("\t\tSubject Code\t\tssid\t\tTest1\tTest2\tTest3\t\tfinal marks\t\teligibility\n")
                        for j in store:
                            eligible = 'yes'
                            if j[6] < 9:
                                eligible = 'no'
                            print('\t\t', j[1], '\t\t\t', j[2], '\t\t\t', float(j[3]), '\t', float(j[4]), '\t',
                                  float(j[5]), '\t\t', float(j[6]), "\t\t\t", eligible, "\n")

                    # update marks of student
                    elif ch == 4:
                        print("\nUpdate Marks\n")
                        query1 = 'select * from sub where sem=8'  #####change for different semesters
                        cur.execute(query1)
                        r = cur.fetchall()
                        print("subcode\t\tCourse Name\n")
                        for k in r:
                            print(k[0], "\t\t", k[1], "\n")

                        USN = input("Enter usn to Update Marks : ")
                        sub = input("Enter subject code : ")
                        t1 = int(input("Test 1 marks: "))
                        t2 = int(input("Test 2 marks: "))
                        t3 = int(input("Test 3 marks: "))
                        final = ceil(max((t1 + t2), (t1 + t3), (t2 + t3)))
                        query = "update iamarks set test1=%s,test2=%s,test3=%s,final=%s where usn=%s and subcode=%s and ssid=10"  #####
                        val = (t1, t2, t3, final, USN, sub,)
                        cur.execute(query, val)
                        con.commit()
                        query = "UPDATE iamarks i set final=(SELECT final_m from final_ia f where i.usn=f.usn and i.subcode=f.subcode) where i.ssid=10 AND i.usn=%s"  #####
                        cur.execute(query, (USN,))

                        print("+++++Marks updated+++++ \n")

                    # update attendance of student
                    elif ch == 5:
                        print("\nUpdate Attendance\n")
                        USN = input("Enter usn to Update Attendance : ")
                        sub = input("Enter subject code : ")
                        newAtt = int(input("Enter New attendance in {} :".format(sub)))
                        query = 'update attendance set attendance=%s where usn=%s and subcode=%s and ssid=10'  #####
                        val = (newAtt, USN, sub,)
                        cur.execute(query, val)
                        con.commit()

                        print("+++++Attendance Updated+++++\n")

                    # add new student
                    elif ch == 6:
                        print("\nAdd New Student\n")
                        USN = input("Enter the usn to add :")
                        name = input("Enter the student's Name :")
                        addr = input("Enter Address of student :")
                        ph = input("Enter the Phone No. :")
                        gender = input("M for male and F for female :")
                        query = "INSERT INTO student (usn, sname, address, phone, gender) values(%s,%s,%s,%s,%s)"
                        val = (USN, name, addr, ph, gender,)
                        cur.execute(query, val)
                        query = "INSERT INTO class(usn,ssid) values(%s,%s)"
                        val = (USN, 10,)                                             #####
                        cur.execute(query, val)
                        print("\nNew Student Added\n")
                        con.commit()


                    # ADD IA MARKS AND ATTENDANCE OF NEW/LEFT-OUT STUDENTS
                    elif ch == 7:
                        print("\nAdd IA marks and Attendance\n")
                        query1 = 'select * from sub where sem=8'  #####change for different semesters
                        cur.execute(query1)
                        r = cur.fetchall()
                        print("subcode\t\tCourse Name\n")
                        for k in r:
                            print(k[0], "\t\t", k[1])
                        USN = input("Enter the usn to add :")
                        sub = input("Enter subject code : ")
                        t1 = int(input("Test 1 marks: "))
                        t2 = int(input("Test 2 marks: "))
                        t3 = int(input("Test 3 marks: "))
                        att = int(input("Enter the attendance in {} :".format(sub)))

                        val = (sub, USN,)
                        q = "delete from iamarks where subcode=%s and usn = %s AND ssid = 10"   ####
                        cur.execute(q, val)
                        q1 = "delete from attendance where subcode=%s and usn = %s"
                        cur.execute(q1, val)

                        query = "insert into iamarks(usn,subcode,ssid,test1,test2,test3)values(%s,%s,%s,%s,%s,%s)"
                        val = (USN, sub, 10, t1, t2, t3,)  #####
                        cur.execute(query, val)
                        query = "UPDATE iamarks i set final=(SELECT final_m from final_ia f where i.usn=f.usn and i.subcode=f.subcode) where i.ssid=10 AND i.usn=%s"  #####
                        cur.execute(query, (USN,))
                        print("++++MARKS UPDATED++++")

                        query = "insert into attendance(usn,subcode,ssid,attendance) values(%s,%s,%s,%s)"
                        val = (USN, sub, 10, att,)  ####
                        cur.execute(query, val)
                        print("++++ATTENDANCE UPDATED++++\n\n")


                    # EXIT from class8A
                    elif ch == 0:
                        break

                    else:
                        print("Invalid Choice")
                break
            else:
                print("\t\taccess denied\n\t\tcheck your password ")
                break
    else:
        print("FID : {} not found in class 8A".format(id))  #####


# CLASS 8B
def classs8B(id, password):
    query = 'select * from class_adviser where ssid=11'  #####
    cur.execute(query)
    res = cur.fetchall()
    for i in res:
        if id == i[0]:
            if password == i[2]:
                print("\nname: {}\nFID: {}".format(i[1].upper(), i[0].upper()))
                print("Class Adviser of Class 8B \n")  #####
                while 1:
                    print("\n---options---")
                    print(
                        "1-view class marks\n2-view class attendance\n3-view single student marks\n4-update "
                        "marks\n5-update attendance\n6-add student\n7-add marks and attendance\n0-Exit\n")
                    ch = int(input())

                    # view class marks
                    if ch == 1:
                        query = 'select * from iamarks where ssid=11'  #####
                        cur.execute(query)
                        store = cur.fetchall()
                        print("***MARKS***")
                        print("\nUSN\t\t\t\tSubject Code\t\tssid\t\tTest1\tTest2\tTest3\tfinal marks\t\teligibility\n")
                        print("-----------------------------------------------------------------------------------------------------")
                        for j in store:
                            u = j[0]
                            eligible = 'yes'
                            if j[6] < 9:
                                eligible = 'no'

                            print(j[0], '\t\t', j[1], '\t\t\t', j[2], '\t\t\t', float(j[3]), '\t', float(j[4]),
                                  '\t',
                                  float(j[5]), '\t\t', float(j[6]), "\t\t\t", eligible, "\n")
                            print(
                                "-----------------------------------------------------------------------------------------------------")



                    # view class attendance
                    elif ch == 2:
                        query = 'select * from attendance where ssid=11'  #####
                        cur.execute(query)
                        store = cur.fetchall()
                        print("***ATTENDANCE***")
                        print("\nUSN\t\t\t\tSubject code\tssid\t\tattendance\t\teligibility\n")
                        print("------------------------------------------------------------------------")
                        for j in store:
                            eligible = 'yes'
                            if j[3] < 75:
                                eligible = 'no'
                            print(j[0], "\t\t", j[1], "\t\t", j[2], "\t\t\t", j[3], "\t\t\t", eligible, "\n")
                            print("------------------------------------------------------------------------")

                    # view marks by student usn
                    elif ch == 3:
                        USN = input("Enter usn to View Marks : ")
                        query = 'select * from iamarks where usn=%s AND ssid=11'  #####
                        cur.execute(query, (USN,))
                        store = cur.fetchall()
                        print("\t\tSubject Code\t\tssid\t\tTest1\tTest2\tTest3\t\tfinal marks\t\teligibility\n")
                        for j in store:
                            eligible = 'yes'
                            if j[6] < 9:
                                eligible = 'no'
                            print('\t\t', j[1], '\t\t\t', j[2], '\t\t\t', float(j[3]), '\t', float(j[4]), '\t',
                                  float(j[5]), '\t\t', float(j[6]), "\t\t\t", eligible, "\n")

                    # update marks of student
                    elif ch == 4:
                        print("\nUpdate Marks\n")
                        query1 = 'select * from sub where sem=8'  #####change for different semesters
                        cur.execute(query1)
                        r = cur.fetchall()
                        print("subcode\t\tCourse Name\n")
                        for k in r:
                            print(k[0], "\t\t", k[1], "\n")

                        USN = input("Enter usn to Update Marks : ")
                        sub = input("Enter subject code : ")
                        t1 = int(input("Test 1 marks: "))
                        t2 = int(input("Test 2 marks: "))
                        t3 = int(input("Test 3 marks: "))
                        final = ceil(max((t1 + t2), (t1 + t3), (t2 + t3)))
                        query = "update iamarks set test1=%s,test2=%s,test3=%s,final=%s where usn=%s and subcode=%s and ssid=11"  #####
                        val = (t1, t2, t3, final, USN, sub,)
                        cur.execute(query, val)
                        con.commit()
                        query = "UPDATE iamarks i set final=(SELECT final_m from final_ia f where i.usn=f.usn and i.subcode=f.subcode) where i.ssid=11 AND i.usn=%s"  #####
                        cur.execute(query, (USN,))

                        print("+++++Marks updated+++++ \n")

                    # update attendance of student
                    elif ch == 5:
                        print("\nUpdate Attendance\n")
                        USN = input("Enter usn to Update Attendance : ")
                        sub = input("Enter subject code : ")
                        newAtt = int(input("Enter New attendance in {} :".format(sub)))
                        query = 'update attendance set attendance=%s where usn=%s and subcode=%s and ssid=11'  #####
                        val = (newAtt, USN, sub,)
                        cur.execute(query, val)
                        con.commit()

                        print("+++++Attendance Updated+++++\n")

                    # add new student
                    elif ch == 6:
                        print("\nAdd New Student\n")
                        USN = input("Enter the usn to add :")
                        name = input("Enter the student's Name :")
                        addr = input("Enter Address of student :")
                        ph = input("Enter the Phone No. :")
                        gender = input("M for male and F for female :")
                        query = "INSERT INTO student (usn, sname, address, phone, gender) values(%s,%s,%s,%s,%s)"
                        val = (USN, name, addr, ph, gender,)
                        cur.execute(query, val)
                        query = "INSERT INTO class(usn,ssid) values(%s,%s)"
                        val = (USN, 11,)                                             #####
                        cur.execute(query, val)
                        print("\nNew Student Added\n")
                        con.commit()


                    # ADD IA MARKS AND ATTENDANCE OF NEW/LEFT-OUT STUDENTS
                    elif ch == 7:
                        print("\nAdd IA marks and Attendance\n")
                        query1 = 'select * from sub where sem=8'  #####change for different semesters
                        cur.execute(query1)
                        r = cur.fetchall()
                        print("subcode\t\tCourse Name\n")
                        for k in r:
                            print(k[0], "\t\t", k[1])
                        USN = input("Enter the usn to add :")
                        sub = input("Enter subject code : ")
                        t1 = int(input("Test 1 marks: "))
                        t2 = int(input("Test 2 marks: "))
                        t3 = int(input("Test 3 marks: "))
                        att = int(input("Enter the attendance in {} :".format(sub)))

                        val = (sub, USN,)
                        q = "delete from iamarks where subcode=%s and usn = %s AND ssid = 11"   ####
                        cur.execute(q, val)
                        q1 = "delete from attendance where subcode=%s and usn = %s"
                        cur.execute(q1, val)

                        query = "insert into iamarks(usn,subcode,ssid,test1,test2,test3)values(%s,%s,%s,%s,%s,%s)"
                        val = (USN, sub, 11, t1, t2, t3,)  #####
                        cur.execute(query, val)
                        query = "UPDATE iamarks i set final=(SELECT final_m from final_ia f where i.usn=f.usn and i.subcode=f.subcode) where i.ssid=1 AND i.usn=%s"  #####
                        cur.execute(query, (USN,))
                        print("++++MARKS UPDATED++++")

                        query = "insert into attendance(usn,subcode,ssid,attendance) values(%s,%s,%s,%s)"
                        val = (USN, sub, 11, att,)  ####
                        cur.execute(query, val)
                        print("++++ATTENDANCE UPDATED++++\n\n")


                    # EXIT from class8B
                    elif ch == 0:
                        break

                    else:
                        print("Invalid Choice")
                break
            else:
                print("\t\taccess denied\n\t\tcheck your password ")
                break
    else:
        print("FID : {} not found in class 8B".format(id))  #####

# CLASS 8C
def classs8C(id, password):
    query = 'select * from class_adviser where ssid=12'  #####
    cur.execute(query)
    res = cur.fetchall()
    for i in res:
        if id == i[0]:
            if password == i[2]:
                print("\nname: {}\nFID: {}".format(i[1].upper(), i[0].upper()))
                print("Class Adviser of Class 8C \n")  #####
                while 1:
                    print("\n---options---")
                    print(
                        "1-view class marks\n2-view class attendance\n3-view single student marks\n4-update "
                        "marks\n5-update attendance\n6-add student\n7-add marks and attendance\n0-Exit\n")
                    ch = int(input())

                    # view class marks
                    if ch == 1:
                        query = 'select * from iamarks where ssid=12'  #####
                        cur.execute(query)
                        store = cur.fetchall()
                        print("***MARKS***")
                        print("\nUSN\t\t\t\tSubject Code\t\tssid\t\tTest1\tTest2\tTest3\tfinal marks\t\teligibility\n")
                        print("-----------------------------------------------------------------------------------------------------")
                        for j in store:
                            u = j[0]
                            eligible = 'yes'
                            if j[6] < 9:
                                eligible = 'no'

                            print(j[0], '\t\t', j[1], '\t\t\t', j[2], '\t\t\t', float(j[3]), '\t', float(j[4]),
                                  '\t',
                                  float(j[5]), '\t\t', float(j[6]), "\t\t\t", eligible, "\n")
                            print(
                                "-----------------------------------------------------------------------------------------------------")



                    # view class attendance
                    elif ch == 2:
                        query = 'select * from attendance where ssid=12'  #####
                        cur.execute(query)
                        store = cur.fetchall()
                        print("***ATTENDANCE***")
                        print("\nUSN\t\t\t\tSubject code\tssid\t\tattendance\t\teligibility\n")
                        print("------------------------------------------------------------------------")
                        for j in store:
                            eligible = 'yes'
                            if j[3] < 75:
                                eligible = 'no'
                            print(j[0], "\t\t", j[1], "\t\t", j[2], "\t\t\t", j[3], "\t\t\t", eligible, "\n")
                            print("------------------------------------------------------------------------")

                    # view marks by student usn
                    elif ch == 3:
                        USN = input("Enter usn to View Marks : ")
                        query = 'select * from iamarks where usn=%s AND ssid=12'  #####
                        cur.execute(query, (USN,))
                        store = cur.fetchall()
                        print("\t\tSubject Code\t\tssid\t\tTest1\tTest2\tTest3\t\tfinal marks\t\teligibility\n")
                        for j in store:
                            eligible = 'yes'
                            if j[6] < 9:
                                eligible = 'no'
                            print('\t\t', j[1], '\t\t\t', j[2], '\t\t\t', float(j[3]), '\t', float(j[4]), '\t',
                                  float(j[5]), '\t\t', float(j[6]), "\t\t\t", eligible, "\n")

                    # update marks of student
                    elif ch == 4:
                        print("\nUpdate Marks\n")
                        query1 = 'select * from sub where sem=8'  #####change for different semesters
                        cur.execute(query1)
                        r = cur.fetchall()
                        print("subcode\t\tCourse Name\n")
                        for k in r:
                            print(k[0], "\t\t", k[1], "\n")

                        USN = input("Enter usn to Update Marks : ")
                        sub = input("Enter subject code : ")
                        t1 = int(input("Test 1 marks: "))
                        t2 = int(input("Test 2 marks: "))
                        t3 = int(input("Test 3 marks: "))
                        final = ceil(max((t1 + t2), (t1 + t3), (t2 + t3)))
                        query = "update iamarks set test1=%s,test2=%s,test3=%s,final=%s where usn=%s and subcode=%s and ssid=12"  #####
                        val = (t1, t2, t3, final, USN, sub,)
                        cur.execute(query, val)
                        con.commit()
                        query = "UPDATE iamarks i set final=(SELECT final_m from final_ia f where i.usn=f.usn and i.subcode=f.subcode) where i.ssid=12 AND i.usn=%s"  #####
                        cur.execute(query, (USN,))

                        print("+++++Marks updated+++++ \n")

                    # update attendance of student
                    elif ch == 5:
                        print("\nUpdate Attendance\n")
                        USN = input("Enter usn to Update Attendance : ")
                        sub = input("Enter subject code : ")
                        newAtt = int(input("Enter New attendance in {} :".format(sub)))
                        query = 'update attendance set attendance=%s where usn=%s and subcode=%s and ssid=12'  #####
                        val = (newAtt, USN, sub,)
                        cur.execute(query, val)
                        con.commit()

                        print("+++++Attendance Updated+++++\n")

                    # add new student
                    elif ch == 6:
                        print("\nAdd New Student\n")
                        USN = input("Enter the usn to add :")
                        name = input("Enter the student's Name :")
                        addr = input("Enter Address of student :")
                        ph = input("Enter the Phone No. :")
                        gender = input("M for male and F for female :")
                        query = "INSERT INTO student (usn, sname, address, phone, gender) values(%s,%s,%s,%s,%s)"
                        val = (USN, name, addr, ph, gender,)
                        cur.execute(query, val)
                        query = "INSERT INTO class(usn,ssid) values(%s,%s)"
                        val = (USN, 12,)                                             #####
                        cur.execute(query, val)
                        print("\nNew Student Added\n")
                        con.commit()


                    # ADD IA MARKS AND ATTENDANCE OF NEW/LEFT-OUT STUDENTS
                    elif ch == 7:
                        print("\nAdd IA marks and Attendance\n")
                        query1 = 'select * from sub where sem=8'  #####change for different semesters
                        cur.execute(query1)
                        r = cur.fetchall()
                        print("subcode\t\tCourse Name\n")
                        for k in r:
                            print(k[0], "\t\t", k[1])
                        USN = input("Enter the usn to add :")
                        sub = input("Enter subject code : ")
                        t1 = int(input("Test 1 marks: "))
                        t2 = int(input("Test 2 marks: "))
                        t3 = int(input("Test 3 marks: "))
                        att = int(input("Enter the attendance in {} :".format(sub)))

                        val = (sub, USN,)
                        q = "delete from iamarks where subcode=%s and usn = %s AND ssid = 12"   ####
                        cur.execute(q, val)
                        q1 = "delete from attendance where subcode=%s and usn = %s"
                        cur.execute(q1, val)

                        query = "insert into iamarks(usn,subcode,ssid,test1,test2,test3)values(%s,%s,%s,%s,%s,%s)"
                        val = (USN, sub, 12, t1, t2, t3,)  #####
                        cur.execute(query, val)
                        query = "UPDATE iamarks i set final=(SELECT final_m from final_ia f where i.usn=f.usn and i.subcode=f.subcode) where i.ssid=12 AND i.usn=%s"  #####
                        cur.execute(query, (USN,))
                        print("++++MARKS UPDATED++++")

                        query = "insert into attendance(usn,subcode,ssid,attendance) values(%s,%s,%s,%s)"
                        val = (USN, sub, 12, att,)  ####
                        cur.execute(query, val)
                        print("++++ATTENDANCE UPDATED++++\n\n")


                    # EXIT from class8C
                    elif ch == 0:
                        break

                    else:
                        print("Invalid Choice")
                break
            else:
                print("\t\taccess denied\n\t\tcheck your password ")
                break
    else:
        print("FID : {} not found in class 8C".format(id))  #####


# CLASS ADVISER
class class_adviser:
    def __init__(self):
        print("\nCSE Department\n1) class 2A\n2) class 2B\n3) class 2C\n4) class 4A\n5) class 4B\n6) class 4C\n7) class 6A\n8) class 6B\n9) class 6C\n10) class 8A\n11) class 8B\n12) class 8C\n\nSelect Your Class : ",
            end='')
        ch = int(input())
        if ch > 12:
            print("wrong choice")
        else:
            id, password = adviser_login()
            if ch == 1:
                classs2A(id, password)
            elif ch == 2:
                classs2B(id, password)
            elif ch == 3:
                classs2C(id, password)
            elif ch == 4:
                classs4A(id, password)
            elif ch == 5:
                classs4B(id, password)
            elif ch == 6:
                classs4C(id, password)
            elif ch == 7:
                classs6A(id, password)
            elif ch == 8:
                classs6B(id, password)
            elif ch == 9:
                classs6C(id, password)
            elif ch == 10:
                classs8A(id, password)
            elif ch == 11:
                classs8B(id, password)
            elif ch == 12:
                classs8C(id, password)



def main():
    while 1:
        print(
            '\n\n\n----------------------------------------------------\n--------------SEMESTER EXAM '
            'ELEGIBILITY--------------\n----------------------------------------------------\nENTER 1 FOR : STUDENT '
            'ELIGIBILITY RESULT\nENTER 2 FOR : FACULTY LOGIN\nENTER 0 : EXIT\nCHOICE : ',
            end='')
        ch = int(input())

        if ch == 1:
            h = student()
        elif ch == 2:
            f = class_adviser()
        elif ch == 0:
            exit()
        else:
            print("wrong input")


if __name__ == '__main__':
    main()