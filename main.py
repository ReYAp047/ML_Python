import os
import pandas as pd
import numpy as np
import csv
from csv import writer
from csv import DictWriter
from tkinter import *
from tkinter import filedialog
import tkinter.font as font
from functools import partial
from pyresparser import ResumeParser
from sklearn import datasets, linear_model 
from PIL import Image, ImageTk

import PyPDF2
import textract
import re
import string
import matplotlib.pyplot as plt
%matplotlib inline


class train_model:
    
    def train(self):
        data =pd.read_csv('training_dataset.csv')
        
        array = data.values

        for i in range(len(array)):
            if array[i][0]=="Male":
                array[i][0]=1
            else:
                array[i][0]=0


        df=pd.DataFrame(array)

        maindf =df[[0,1,2,3,4,5,6]]
        mainarray=maindf.values

        temp=df[7]
        train_y =temp.values
        
# utilisation de regression lineaire
      
        self.mul_lr = linear_model.LogisticRegression(multi_class='multinomial', solver='newton-cg',max_iter =1000)
        self.mul_lr.fit(mainarray, train_y)
        
    def test(self, test_data):
        try:
            test_predict=list()
            for i in test_data:
                test_predict.append(int(i))
            y_pred = self.mul_lr.predict([test_predict])
            return y_pred

        except:
            print("Merci de bien vérifier : Erreur!")


def check_type(data):
    if type(data)==str or type(data)==str:
        return str(data).title()
    if type(data)==list or type(data)==tuple:
        str_list=""
        for i,item in enumerate(data):
            str_list+=item+", "
        return str_list
    else:   return str(data)

def prediction_result(top, aplcnt_name, cv_path, personality_values):
    "after applying a job"
    top.withdraw()
    applicant_data={"Candidate Name":aplcnt_name.get(),  "CV Location":cv_path}
    
    age = personality_values[1]
    
    print("\n############# Candidate Entered Data #############\n")
    print(applicant_data, personality_values)
    
    personality = model.test(personality_values)
    print("\n############# Predicted Personality #############\n")
    print(personality)
    data = ResumeParser(cv_path).get_extracted_data()
    
    try:
        del data['name']
        if len(data['mobile_number'])<10:
            del data['mobile_number']
    except:
        pass
    
    print("\n############# Resume Parsed Data #############\n")

    for key in data.keys():
        if data[key] is not None:
            print('{} : {}'.format(key,data[key]))
 
            
  #representation graphique   
  
    result=Tk()
  #  result.geometry('700x550')
    result.overrideredirect(False)
    result.geometry("{0}x{1}+0+0".format(result.winfo_screenwidth(), result.winfo_screenheight()))
    result.title("Evaluation")
    
    #Title
    titleFont = font.Font(family='Arial', size=40, weight='bold')
    Label(result, text="Resultat de traitement", foreground='red', bg='white', font=titleFont, pady=10, anchor=CENTER).pack(fill=BOTH)
    
    Label(result, text = str('{} : {}'.format("Nom:", aplcnt_name.get())).title(), foreground='black', bg='white', anchor='w').pack(fill=BOTH)
    Label(result, text = str('{} : {}'.format("Age:", age)), foreground='black', bg='white', anchor='w').pack(fill=BOTH)
    
    for key in data.keys():
        if data[key] is not None:
            Label(result, text = str('{} : {}'.format(check_type(key.title()),check_type(data[key]))), foreground='black', bg='white', anchor='w', width=60).pack(fill=BOTH)
    Label(result, text = str("Personalité: "+personality).title(), foreground='black', bg='white', anchor='w').pack(fill=BOTH)
  
    
    personality = model.test(personality_values)
     # list of column names 
    field_names = ['nom','age','genre','personalite','note']
       
     # Dictionary
    dict={'nom':aplcnt_name.get(),
           'age':age,
           'genre':personality_values[0],
           'personalite':personality,
           'note':personality_values[6]
           }
       
     # Open your CSV file in append mode
     # Create a file object for this file
    with open('Grille.csv', 'a',encoding='UTF8', newline='') as f_object:
           
         # Pass the file object and a list 
         # of column names to DictWriter()
         # You will get a object of DictWriter
         dictwriter_object = DictWriter(f_object, fieldnames=field_names)
       
         #Pass the dictionary as an argument to the Writerow()
         dictwriter_object.writerow(dict)
       
         #Close the file object
         f_object.close()
    
    terms_mean = """
   
"""
    
    Label(result, text = terms_mean, foreground='red', bg='white', anchor='w', justify=LEFT).pack(fill=BOTH)
    beval=Button(result, padx=2, pady=0, text="Affichage de grille d'evaluation", bg='black', foreground='white', bd=1, command=grille_evaluation).place(x=800, y=600, width=200)
    #begraf=Button(result, padx=2, pady=0, text="realisation de graphe", bg='red', foreground='white', bd=1, command=graphique_presentation).place(x=400, y=600, width=200)
    begraf=Button(result, padx=2, pady=0, text="Affichage de graphe", bg='black', foreground='white', bd=1, command=affichague_graphe).place(x=100, y=600, width=200)
    quitBtn = Button(result, text="Quitter",foreground='white', bg='black',width=120, command =lambda:  result.destroy()).pack()

    result.mainloop()
    

def perdict_person():
    """Predict Personality"""
    
    # Closing The Previous Window
    root.withdraw()
    
    # Creating new window
    top = Toplevel()
    top.geometry('800x500')
    top.configure(background='grey')
    top.title("Postuler pour un travail")
    
    #Title
    titleFont = font.Font(family='Helvetica', size=20, weight='bold')
    lab=Label(top, text="Evaluation Condidats", foreground='white', bg='grey', font=titleFont, pady=10).pack()

    #Job_Form
    job_list=('Select Job', '101-Developer at TTC', '102-Chef at Taj', '103-Professor at MIT')
    job = StringVar(top)
    job.set(job_list[0])

    l1=Label(top, text="Nom", foreground='white', bg='grey').place(x=70, y=130)
    l2=Label(top, text="Age", foreground='white', bg='grey').place(x=70, y=160)
    l3=Label(top, text="Genre", foreground='white', bg='grey').place(x=70, y=190)
    l4=Label(top, text="Upload Resume", foreground='white', bg='grey').place(x=70, y=220)
    l5=Label(top, text="Profitez d'une nouvelle expérience ou chose (ouverture)", foreground='white', bg='grey').place(x=70, y=250)
    l6=Label(top, text="À quel point vous ressentez de la négativité (névrosisme)", foreground='white', bg='grey').place(x=70, y=280)
    l7=Label(top, text="Vouloir bien faire son travail (Conscienciosité)", foreground='white', bg='grey').place(x=70, y=310)
    l8=Label(top, text="Dans quelle mesure aimeriez-vous travailler avec vos pairs (agréabilité)", foreground='white', bg='grey').place(x=70, y=340)
    l9=Label(top, text="assosier une notation(note)", foreground='white', bg='grey').place(x=70, y=370)
    
    
    sName=Entry(top)
    sName.place(x=450, y=130, width=160)
    age=Entry(top)
    age.place(x=450, y=160, width=160)
    gender = IntVar()
    R1 = Radiobutton(top, text="Homme", variable=gender, value=1, padx=7)
    R1.place(x=450, y=190)
    R2 = Radiobutton(top, text="Femme", variable=gender, value=0, padx=3)
    R2.place(x=540, y=190)
    cv=Button(top, text="Select CV", command=lambda:  OpenFile(cv))
    cv.place(x=450, y=220, width=160)
    openness=Entry(top)
    openness.insert(0,'1..10')
    openness.place(x=450, y=250, width=160)
    neuroticism=Entry(top)
    neuroticism.insert(0,'1..10')
    neuroticism.place(x=450, y=280, width=160)
    conscientiousness=Entry(top)
    conscientiousness.insert(0,'1..10')
    conscientiousness.place(x=450, y=310, width=160)
    agreeableness=Entry(top)
    agreeableness.insert(0,'1..10')
    agreeableness.place(x=450, y=340, width=160)
    extraversion=Entry(top)
    extraversion.insert(0,'1..5')
    extraversion.place(x=450, y=370, width=160)

    
    

    
    submitBtn=Button(top, padx=2, pady=0, text="Valider", bd=0, foreground='white', bg='black', font=(12))
    submitBtn.config(command=lambda:prediction_result(top,sName,loc,(gender.get(),age.get(),openness.get(),neuroticism.get(),conscientiousness.get(),agreeableness.get(),extraversion.get())))
    submitBtn.place(x=350, y=430, width=250)
    
    
    

  
    top.mainloop()
    
#Tableau d'evaluation----------------------------

def grille_evaluation():
    import tkinter   
    root.withdraw()
    grille=tkinter.Tk()
    #grille.geometry('800x600')
    grille.title('grille devaluation')
    # open file
    with open("Grille.csv", newline = "") as file:
       reader = csv.reader(file)

       # r and c tell us where to grid the labels
       r = 0
       for col in reader:
          c = 0
          for row in col:
             # i've added some styling
             label = tkinter.Label(grille, width = 20, height = 2, \
                                   text = row, relief = tkinter.RIDGE)
             label.grid(row = r, column = c)
             c += 1
          r += 1

    root.mainloop()
    


def affichague_graphe():
    os.system('python showimg.py')
    
 #Fonction permet de creer le graphe a partir d'un fichier pdf
   
def graphique_presentation():
    # Open pdf file
    pdfFileObj = open('C:/Users/whammami/Desktop/Projet-Python/Test.pdf','rb')

    # Read file
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    # Get total number of pages
    num_pages = pdfReader.numPages

    # Initialize a count for the number of pages
    count = 0

    # Initialize a text empty string variable
    text = ""

    # Extract text from every page on the file
    while count < num_pages:
        pageObj = pdfReader.getPage(count)
        count +=1
        text += pageObj.extractText()
        
    # Convert all strings to lowercase
    text = text.lower()

    # Remove numbers
    text = re.sub(r'\d+','',text)

    # Remove punctuation
    text = text.translate(str.maketrans('','',string.punctuation))

    # Create dictionary with industrial and system engineering key terms by area
    terms = {'Quality/Six Sigma':['black belt','capability analysis','control charts','doe','dmaic','fishbone',
                                  'gage r&r', 'green belt','ishikawa','iso','kaizen','kpi','lean','metrics',
                                  'pdsa','performance improvement','process improvement','quality',
                                  'quality circles','quality tools','root cause','six sigma',
                                  'stability analysis','statistical analysis','tqm'],      
            'Operations management':['automation','bottleneck','constraints','cycle time','efficiency','fmea',
                                     'machinery','maintenance','manufacture','line balancing','oee','operations',
                                     'operations research','optimization','overall equipment effectiveness',
                                     'pfmea','process','process mapping','production','resources','safety',
                                     'stoppage','value stream mapping','utilization'],
            'Supply chain':['abc analysis','apics','customer','customs','delivery','distribution','eoq','epq',
                            'fleet','forecast','inventory','logistic','materials','outsourcing','procurement',
                            'reorder point','rout','safety stock','scheduling','shipping','stock','suppliers',
                            'third party logistics','transport','transportation','traffic','supply chain',
                            'vendor','warehouse','wip','work in progress'],
            'Project management':['administration','agile','budget','cost','direction','feasibility analysis',
                                  'finance','kanban','leader','leadership','management','milestones','planning',
                                  'pmi','pmp','problem','project','risk','schedule','scrum','stakeholders'],
            'Data analytics':['analytics','api','aws','big data','business intelligence','clustering','code',
                              'coding','data','database','data mining','data science','deep learning','hadoop',
                              'hypothesis test','iot','internet','machine learning','modeling','nosql','nlp',
                              'predictive','programming','python','r','sql','tableau','text mining',
                              'visualuzation'],
            'Healthcare':['adverse events','care','clinic','cphq','ergonomics','healthcare',
                          'health care','health','hospital','human factors','medical','near misses',
                          'patient','reporting system']}

    # Initializie score counters for each area
    quality = 0
    operations = 0
    supplychain = 0
    project = 0
    data = 0
    healthcare = 0

    # Create an empty list where the scores will be stored
    scores = []

    # Obtain the scores for each area
    for area in terms.keys():
            
        if area == 'Quality/Six Sigma':
            for word in terms[area]:
                if word in text:
                    quality +=1
            scores.append(quality)
            
        elif area == 'Operations management':
            for word in terms[area]:
                if word in text:
                    operations +=1
            scores.append(operations)
            
        elif area == 'Supply chain':
            for word in terms[area]:
                if word in text:
                    supplychain +=1
            scores.append(supplychain)
            
        elif area == 'Project management':
            for word in terms[area]:
                if word in text:
                    project +=1
            scores.append(project)
            
        elif area == 'Data analytics':
            for word in terms[area]:
                if word in text:
                    data +=1
            scores.append(data)
            
        else:
            for word in terms[area]:
                if word in text:
                    healthcare +=1
            scores.append(healthcare)
            
    # Create a data frame with the scores summary
    summary = pd.DataFrame(scores,index=terms.keys(),columns=['score']).sort_values(by='score',ascending=False)
    summary



    # Create pie chart visualization
    pie = plt.figure(figsize=(11,11))
    plt.pie(summary['score'], labels=summary.index, explode = (0.1,0,0,0,0,0), autopct='%1.0f%%',shadow=True,startangle=90)
    plt.title('Statistique Compétatnce Condidats')
    plt.axis('equal')
    plt.show()



    # Save pie chart as a .png file
    pie.savefig('resume_screening_results.png')
    
    
    
    
    
def OpenFile(b4):
    global loc;
    name = filedialog.askopenfilename(initialdir="C:/Users/Batman/Documents/Programming/tkinter/",
                            filetypes =(("Document","*.docx*"),("PDF","*.pdf*"),('All files', '*')),
                           title = "Choose a file."
                           )
    try:
        filename=os.path.basename(name)
        loc=name
    except:
        filename=name
        loc=name
    b4.config(text=filename)
    return

if __name__ == "__main__":
    model = train_model()
    model.train()

    root = Tk()
    root.geometry('800x700')
    root.configure(background='white')
    root.title("Evaluation cv condidats")
    titleFont = font.Font(family='Helvetica', size=22, weight='bold')
    titleFont2 = font.Font(family='Helvetica', size=16, weight='bold')
    titleFont3 = font.Font(family='Helvetica', size=13, weight='bold')


    homeBtnFont = font.Font(size=14, weight='bold')
    lab=Label(root, text="Evaluation cv condidats", font=titleFont, pady=30).pack()
    lab=Label(root, text="--------Description de poste---------- :", font=titleFont2, bg='white' ,  pady=30).pack()
    lab=Label(root, text="Pour compléter notre équipe web, nous recherchons un(e) développeur(se) web", font=titleFont3, bg='white' ,  pady=30).pack()
    lab=Label(root, text="et web mobile expérimenté(e) à l’aise avec le travail en équipe.", font=titleFont3, bg='white' ,  pady=30).pack()

    b2=Button(root, padx=4, pady=4, width=30, text="Commencer l'évaluation", bg='black', foreground='white', bd=1, font=homeBtnFont, command=perdict_person).place(relx=0.5, rely=0.5, anchor=CENTER)
    root.mainloop()