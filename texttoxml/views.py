from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.shortcuts import render
from xml.etree.ElementTree import Element, SubElement, Comment, tostring,ElementTree
import re
#from .forms import UploadFileForm
# Create your views here.
class textToxmlConverterView(View):
    template_name = "texttoxml/home.html"
    def get(self,request,*args,**kwargs):
        #form = UploadFileForm()
        context ={}
        return render(request,self.template_name,context)
    def post(self,request,*args,**kwargs):
        myfile = request.FILES['myfile']
        self.handlefileupload(myfile)
        context ={}
        return render(request,self.template_name,context)
    def handlefileupload(self,filename):
        with open('name.txt', 'wb+') as destination:
            for chunk in filename.chunks():
                destination.write(chunk)
        self.converttoxml("name.txt")
    def converttoxml(self,filepath):
        with open(filepath) as fp:
            #filepath = 'sample.txt'
            outputfilename = "sample.xml"
            answemapping = {"A":1,"B":2,"C":3,"D":4}
            top = Element('quiz')
            top.set('version', '1.0')
            lines = fp.readlines()
            index=0
            while index < len(lines)-1:
                questiontext = ""
                options =[]
                done = False
                offset = 0
                while done == False:
                    #reading text file line by one check whether its a question ,option or answer
                    nextline = lines[index].strip()
                    index=index+1
                    match = re.search("^[A-D]\.",nextline)
                    if match:
                        #its an option
                        option = nextline.split('.')[1].strip()
                        options.append( option)
                    elif nextline.find("ANSWER") != -1:
                        #its an answer
                        answer = nextline.split(":")[1].strip()
                        done = True
                    else:
                        #its a part of question
                        questiontext += nextline
                questionnode = SubElement(top, 'question',{'type':'multichoice'})
                namenode = SubElement(questionnode,'name')
                nametextnode = SubElement(namenode,"text")
                nametextnode.text=questiontext
                questiontextnode = SubElement(questionnode,'questiontext',{"format":"html"})
                questiontextTextnode = SubElement(questiontextnode,"text")
                questiontextTextnode.text = questiontext
                answertypenode = SubElement(questionnode,"single")
                answertypenode.text = "true"
                optionnumber=1
                for option in options:
                    if (optionnumber == answemapping[answer]):
                        answernode = SubElement(questionnode,'answer' ,{'fraction':"100"})
                    else:
                        answernode = SubElement(questionnode,'answer' ,{'fraction':"-33.33333"})
                    answertextnode = SubElement(answernode,"text")
                    answertextnode.text = option
                    optionnumber +=1
            tree = ElementTree(top)
            with open (outputfilename, "wb") as files : 
                tree.write(files)