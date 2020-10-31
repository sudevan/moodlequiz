from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.shortcuts import render
from xml.etree.ElementTree import Element, SubElement, Comment, tostring,ElementTree
import re
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
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
        outputfilename = self.handlefileupload(myfile)
        print(outputfilename)
        context ={"uploaded_file_url":"/media/"+outputfilename,"filename":outputfilename}
        return render(request,self.template_name,context)
    def handlefileupload(self,myfile):
        fs = FileSystemStorage()
        if fs.exists(myfile.name):
            os.remove(os.path.join(settings.MEDIA_ROOT, myfile.name))
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)
        outputfilename = self.converttoxml(filename)
        """         with open('name.txt', 'wb+') as destination:
                    for chunk in filename.chunks():
                        destination.write(chunk)
                self.converttoxml("name.txt") """
        return outputfilename
    def converttoxml(self,filename):
        filepath=os.path.join(settings.MEDIA_ROOT, filename)
        with open(filepath) as fp:
            #filepath = 'sample.txt'
            outputfilename = filepath.split(".")[0]+".xml"
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
                    nextline = lines[index].rstrip()
                    index=index+1
                    match = re.search("^[A-D]\.",nextline)
                    if match:
                        #its an option
                        s = "."
                        #to handle answers with . symbol like 0.25 etc
                        option = s.join ( nextline.split('.')[1:]).lstrip()
                        
                        options.append( option)
                    elif nextline.find("ANSWER") != -1:
                        #its an answer
                        answer = nextline.split(":")[1].strip()
                        done = True
                    else:
                        #its a part of question
                        questiontext += nextline
                #space where not coming in the unicode text fixed
                questiontext = questiontext.replace(" ","\u00A0")
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
            return os.path.basename(outputfilename)
