from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from .models import tipe_kriteria
from .models import daftar_kriteria
from .models import nilai_persamaan
from .models import nilai_kriteria
from .models import proyek
import numpy as num
import pandas as pd
from .models import opsi_kriteria
from .models import daftar_opsi
import uuid
from .models import user


# Create your views here.
def index(request):
    return redirect('/home')


def inputP(request):
    if 'logintkn' in request.session:
        dataTipekriteria = tipe_kriteria.objects.all()
        dataDaftarkriteria = daftar_kriteria.objects.all()
        dataOpsi = daftar_opsi.objects.all()
        template = loader.get_template('form_input_proyek.html')
        return HttpResponse(template.render({"daftar_tipe":dataTipekriteria,"daftar_kriteria":dataDaftarkriteria,"opsi": dataOpsi}, request))
    else:
        return redirect('/login')
        


def inputKriteria(request):
    if 'logintkn' in request.session:
        template = loader.get_template('form_input_kriteria.html')
        dataOpsi = opsi_kriteria.objects.all()
        return HttpResponse(template.render({"increment":0,"dataopsi":dataOpsi}, request))
    else:
        return redirect('/login')


def prosesKriteria(request):
    if 'logintkn' in request.session:
        idkriter = []
        namakrter = []
        pilihankrt = []
        opsi = [] 
        radio = []
        databasedata = daftar_kriteria.objects.all()
        databasetipekriteria = tipe_kriteria.objects.all()
        for c in request.POST.getlist("id_subkrt[]"):
            idkriter.append(c)
        for d in request.POST.getlist("nama_subkrit[]"):
            namakrter.append(d)
        for e in request.POST.getlist("pilih_kriteria[]"):
            pilihankrt.append(e)
        for j in request.POST.getlist("daftar_opsi[]"):
            opsi.append(j)
        for p in request.POST.getlist("pilihanrad[]"):
            radio.append(p)
        for cek in databasetipekriteria:
            if(request.POST["id_kriteria"] == cek.id_kriteria):
                request.session['suc'] = 0
                request.session['msg'] = "ID Kriteria Sudah Ada"
                return redirect("/inputk")
        for check in range(len(idkriter)):
            for data in databasedata:
                print(data.id_subkrt)
                if(idkriter[check] == data.id_subkrt):
                    request.session['suc'] = 0
                    request.session['msg'] = "ID Sub Kriteria Sudah Ada"
                    return redirect('/inputk')
        form = tipe_kriteria(
            id_kriteria=request.POST["id_kriteria"], nama_tipe=request.POST["nama_tipe"])
        form.save()
        for inputdata in range(len(idkriter)):
            subinput = daftar_kriteria(id_subkrt=idkriter[inputdata], nama_subkrit=namakrter[inputdata],
                                       id_kriteria=request.POST["id_kriteria"], pilih_kriteria=pilihankrt[inputdata],id_opsi=opsi[inputdata],tipe_input=radio[inputdata])
            subinput.save()
        for persamaan in range(len(idkriter)):
            for persamaan1 in range(len(idkriter)):
                if(idkriter[persamaan] == idkriter[persamaan1]):
                    addpersamaan = nilai_persamaan(
                        id_subkrit1=idkriter[persamaan], id_subkrit2=idkriter[persamaan1], nilai=1,id_kriteria=request.POST["id_kriteria"])
                    addpersamaan.save()
                else:
                    addpersamaan = nilai_persamaan(
                        id_subkrit1=idkriter[persamaan], id_subkrit2=idkriter[persamaan1], nilai=0,id_kriteria=request.POST["id_kriteria"])
                    addpersamaan.save()
        template = loader.get_template('beranda.html')
        return HttpResponse(template.render({"suc": 1, "msg": "Kriteria Berhasil Di Input"}, request))
    else:
        return redirect('/login')


def inputProyek(request):
    if 'logintkn' in request.session:
        template = loader.get_template('form_input_proyek.html')
        return HttpResponse(template.render({},request))
    else:
        return redirect('/login')

def prosesinputproyek(request):
    if 'logintkn' in request.session:
        dataproyek = proyek.objects.all()
        datasubkritre = daftar_kriteria.objects.all()
        idproyek = 0
        nilaipro = 0
        for dpro in dataproyek:
            idproyek = dpro.id_pro
        idproyek = idproyek + 1
        if request.POST["pilihan_radio"] == "manual":
            form = proyek(id_pro=idproyek,kt_pro=request.POST["kt_pro"],nm_pro=request.POST["nm_pro"],nilai_pro=request.POST["kl_02"],jml_mod=request.POST["kl_06"],waktu_perb=request.POST["kl_04"],manual=1,selesai=0)
            form.save()
        elif request.POST["pilihan_radio"] == "otomatis":
            if request.POST["kl_02"] == "0.0": 
                nilaipro = 70000000
            elif request.POST["kl_02"] == "0.2":
                nilaipro = 200000000
            elif request.POST["kl_02"] == "0.4":
                nilaipro = 850000000
            elif request.POST["kl_02"] == "0.6":
                nilaipro = 2000000000
            elif request.POST["kl_02"] == "0.8":
                nilaipro = 7000000000
            elif request.POST["kl_02"] == "1.0":
                nilaipro = 8000000000
            form = proyek(id_pro=idproyek,kt_pro=request.POST["kt_pro"],nm_pro=request.POST["nm_pro"],nilai_pro=nilaipro,jml_mod=request.POST["kl_06"],waktu_perb=request.POST["kl_04"],manual=0,selesai=0)
            form.save()
        for dsubkr in datasubkritre:
            if dsubkr.id_subkrt == "kl_02":
                if request.POST["pilihan_radio"] == "otomatis":
                    form1 = nilai_kriteria(id_pro=idproyek,id_subkrit=dsubkr.id_subkrt,nilai=request.POST[dsubkr.id_subkrt])
                elif request.POST["pilihan_radio"] == "manual":
                    if int(request.POST[dsubkr.id_subkrt]) >= 0 and int(request.POST[dsubkr.id_subkrt]) < 71000000 :
                        form1 = nilai_kriteria(id_pro=idproyek,id_subkrit=dsubkr.id_subkrt,nilai="0.0")
                    elif int(request.POST[dsubkr.id_subkrt]) >= 71000000 and int(request.POST[dsubkr.id_subkrt]) < 201000000:
                        form1 = nilai_kriteria(id_pro=idproyek,id_subkrit=dsubkr.id_subkrt,nilai="0.2")
                    elif int(request.POST[dsubkr.id_subkrt]) >= 201000000 and int(request.POST[dsubkr.id_subkrt]) < 851000000:
                        form1 = nilai_kriteria(id_pro=idproyek,id_subkrit=dsubkr.id_subkrt,nilai="0.4")
                    elif int(request.POST[dsubkr.id_subkrt]) >= 851000000 and int(request.POST[dsubkr.id_subkrt]) < 2100000000:
                        form1 = nilai_kriteria(id_pro=idproyek,id_subkrit=dsubkr.id_subkrt,nilai="0.6")
                    elif int(request.POST[dsubkr.id_subkrt]) >= 2100000000 and int(request.POST[dsubkr.id_subkrt]) < 70000000000:
                        form1 = nilai_kriteria(id_pro=idproyek,id_subkrit=dsubkr.id_subkrt,nilai="0.8")
                    elif int(request.POST[dsubkr.id_subkrt]) > 70000000000:
                        form1 = nilai_kriteria(id_pro=idproyek,id_subkrit=dsubkr.id_subkrt,nilai="1.0")
            elif dsubkr.id_subkrt == "kl_04":
                if int(request.POST[dsubkr.id_subkrt]) <= 1 :
                    form1 = nilai_kriteria(id_pro=idproyek,id_subkrit=dsubkr.id_subkrt,nilai="0.0")
                elif int(request.POST[dsubkr.id_subkrt]) > 1 and int(request.POST[dsubkr.id_subkrt]) < 2:
                    form1 = nilai_kriteria(id_pro=idproyek,id_subkrit=dsubkr.id_subkrt,nilai="0.2")
                elif int(request.POST[dsubkr.id_subkrt]) > 2 and int(request.POST[dsubkr.id_subkrt]) < 3:
                    form1 = nilai_kriteria(id_pro=idproyek,id_subkrit=dsubkr.id_subkrt,nilai="0.4")
                elif int(request.POST[dsubkr.id_subkrt]) > 3 and int(request.POST[dsubkr.id_subkrt]) < 4:
                    form1 = nilai_kriteria(id_pro=idproyek,id_subkrit=dsubkr.id_subkrt,nilai="0.6")
                elif int(request.POST[dsubkr.id_subkrt]) > 4 and int(request.POST[dsubkr.id_subkrt]) < 5:
                    form1 = nilai_kriteria(id_pro=idproyek,id_subkrit=dsubkr.id_subkrt,nilai="0.8")
                elif int(request.POST[dsubkr.id_subkrt]) > 5:
                    form1 = nilai_kriteria(id_pro=idproyek,id_subkrit=dsubkr.id_subkrt,nilai="1.0")
            elif dsubkr.id_subkrt == "kl_06":
                if int(request.POST[dsubkr.id_subkrt]) <= 5 :
                    form1 = nilai_kriteria(id_pro=idproyek,id_subkrit=dsubkr.id_subkrt,nilai="0.0")
                elif int(request.POST[dsubkr.id_subkrt]) >= 6 and int(request.POST[dsubkr.id_subkrt]) < 11:
                    form1 = nilai_kriteria(id_pro=idproyek,id_subkrit=dsubkr.id_subkrt,nilai="0.2")
                elif int(request.POST[dsubkr.id_subkrt]) >= 11 and int(request.POST[dsubkr.id_subkrt])< 16:
                    form1 = nilai_kriteria(id_pro=idproyek,id_subkrit=dsubkr.id_subkrt,nilai="0.4")
                elif int(request.POST[dsubkr.id_subkrt]) >= 16 and int(request.POST[dsubkr.id_subkrt]) < 21:
                    form1 = nilai_kriteria(id_pro=idproyek,id_subkrit=dsubkr.id_subkrt,nilai="0.6")
                elif int(request.POST[dsubkr.id_subkrt]) >= 21 and int(request.POST[dsubkr.id_subkrt]) < 26:
                    form1 = nilai_kriteria(id_pro=idproyek,id_subkrit=dsubkr.id_subkrt,nilai="0.8")
                elif int(request.POST[dsubkr.id_subkrt]) >= 26:
                    form1 = nilai_kriteria(id_pro=idproyek,id_subkrit=dsubkr.id_subkrt,nilai="1.0")
            elif dsubkr.tipe_input == "text":
                opsikrit = daftar_opsi.objects.all()
                for ol in opsikrit:
                    if ol.id_daftar == dsubkr.id_opsi:
                        if ol.deskripsi_opsi == request.POST[dsubkr.id_subkrt]:
                            form1 = nilai_kriteria(id_pro=idproyek,id_subkrit=dsubkr.id_subkrt,nilai=ol.value_opsi)
            else:
                form1 = nilai_kriteria(id_pro=idproyek,id_subkrit=dsubkr.id_subkrt,nilai=request.POST[dsubkr.id_subkrt])
            form1.save()
        template = loader.get_template('beranda.html')
        return HttpResponse(template.render({"suc": 1, "msg": "Kriteria Berhasil Di Input"}, request))
    else:
        return redirect('/login')

def displayPersamaan(request):
    if 'logintkn' in request.session:
        if request.method == 'GET':
            template = loader.get_template('form_input_ubah_persamaan.html')
            getdatatipe = tipe_kriteria.objects.all()
            return HttpResponse(template.render({"datatampil":None,"datatipekrite":getdatatipe},request))
        elif request.method == 'POST':
            template = loader.get_template('form_input_ubah_persamaan.html')
            getdatatipe = tipe_kriteria.objects.all()
            getdata = nilai_persamaan.objects.all()
            getdatas = getdata.filter(id_kriteria=request.POST["datadisplay"])
            getdatasubkriter  = daftar_kriteria.objects.all()
            return HttpResponse(template.render({"datatampil":getdatas,"datatipekrite":getdatatipe,"daftarsub":getdatasubkriter,"id_krite":request.POST["datadisplay"]},request))
    else:
        return redirect('/login')

def ubahdataPersamaan(request):
    if 'logintkn' in request.session:
        nilai_persamaan.objects.filter(id_subkrit1=request.POST["id_sub1"],id_subkrit2=request.POST["id_sub2"]).update(nilai=request.POST["ubah"])
        hasil = float(1 / int(request.POST["ubah"]))
        nilai_persamaan.objects.filter(id_subkrit1=request.POST["id_sub2"],id_subkrit2=request.POST["id_sub1"]).update(nilai=hasil)
        template = loader.get_template('form_input_ubah_persamaan.html')
        getdatatipe = tipe_kriteria.objects.all()
        getdata = nilai_persamaan.objects.all()
        getdatas = getdata.filter(id_kriteria=request.POST["idkriteria"])
        getdatasubkriter  = daftar_kriteria.objects.all()
        return HttpResponse(template.render({"datatampil":getdatas,"datatipekrite":getdatatipe,"daftarsub":getdatasubkriter,"id_krite":request.POST["idkriteria"],"suc":1},request))
    else:
        return redirect('/login')

def hasil(request):
    if 'logintkn' in request.session:
        datatipekriter = tipe_kriteria.objects.all()
        proyk = proyek.objects.filter(selesai=0)
        bprior = []
        ranking = []
        overloadcost = []

        for dps in datatipekriter:
            bprior.append(hitungpersamaan(request,dps.id_kriteria))  
        ranking = normalisaimatrik(request,bprior)
        borda = hitungborda(request,ranking)
        for proyeks in proyk:
            if int(proyeks.nilai_pro) >= 0 and int(proyeks.nilai_pro) < 71000000 :
                hasil = 0.00 * float(proyeks.nilai_pro)
                overloadcost.append({"id_proyek":proyeks.id_pro,"hasil":hasil})
            elif int(proyeks.nilai_pro) >= 71000000 and int(proyeks.nilai_pro) < 201000000:
                hasil = 0.02 * float(proyeks.nilai_pro)
                overloadcost.append({"id_proyek":proyeks.id_pro,"hasil":hasil})
            elif int(proyeks.nilai_pro) >= 201000000 and int(proyeks.nilai_pro) < 851000000:
                hasil = 0.04 * float(proyeks.nilai_pro)
                overloadcost.append({"id_proyek":proyeks.id_pro,"hasil":hasil})
            elif int(proyeks.nilai_pro) >= 851000000 and int(proyeks.nilai_pro) < 2100000000:
                hasil = 0.06 * float(proyeks.nilai_pro)
                overloadcost.append({"id_proyek":proyeks.id_pro,"hasil":hasil})
            elif int(proyeks.nilai_pro) >= 2100000000 and int(proyeks.nilai_pro) < 70000000000:
                hasil = 0.08 * float(proyeks.nilai_pro)
                overloadcost.append({"id_proyek":proyeks.id_pro,"hasil":hasil})
            elif int(proyeks.nilai_pro) > 70000000000:
                hasil = 0.10 * float(proyeks.nilai_pro)
                overloadcost.append({"id_proyek":proyeks.id_pro,"hasil":hasil})
        template = loader.get_template('form_prioritas_proyek.html')
        return HttpResponse(template.render({"rank":borda,"dpro":proyk,"ocost":overloadcost},request))
    else:
        return redirect('/login')

def hitungpersamaan(request,idkriter):
    if 'logintkn' in request.session:
        jumlah = 0 
        jumlahpersamaan = []
        jumlahnormalisasi = []
        hasilbp = []
        id_subkrit = ""
        datapersamaan = nilai_persamaan.objects.filter(id_kriteria=idkriter)
        datadaftarsub = daftar_kriteria.objects.filter(id_kriteria=idkriter)
        for dsub in datadaftarsub:
            for dp in datapersamaan:
                if  dsub.id_subkrt == dp.id_subkrit2 :
                    jumlah = jumlah + dp.nilai
                    id_subkrit = dp.id_subkrit2
            jumlahpersamaan.append([id_subkrit,jumlah])
            jumlah = 0
        for dsub1 in datadaftarsub:
            for dp1 in datapersamaan:
                if  dp1.id_subkrit1 == dsub1.id_subkrt :
                    for jper in range(len(jumlahpersamaan)):
                        if jumlahpersamaan[jper][0] == dp1.id_subkrit2:
                            jumlah = jumlah + (dp1.nilai / jumlahpersamaan[jper][1])
            jumlahnormalisasi.append({"id_subkrit" : dsub1.id_subkrt ,"jumlah" : jumlah})
            jumlah = 0
        for jmlnr in jumlahnormalisasi:
            for dsub2 in datadaftarsub:
                if dsub2.id_subkrt == jmlnr["id_subkrit"]:    
                    jumlah = jmlnr["jumlah"]/len(jumlahnormalisasi)
                    hasilbp.append({"id_subkrit" : jmlnr["id_subkrit"] , "hasil" : jumlah})
            jumlah = 0
        return hasilbp
    else:
        return redirect('/login')

def normalisaimatrik(request,bpriority):
    if 'logintkn' in request.session:
        jumlahnormal = 0
        datanilaiproyek = nilai_kriteria.objects.all()    
        datatipekriter = tipe_kriteria.objects.all()
        datasubkriter = daftar_kriteria.objects.all()
        dataproyek = proyek.objects.filter(selesai=0)
        matrix = []
        matrixnormal = []
        hasilrank = []
        ranking = []
        for dtpike in datatipekriter:
            matrix.append({"id_kriteria" : dtpike.id_kriteria,"data":[]})
            matrixnormal.append({"id_kriteria" : dtpike.id_kriteria,"data":[]})
            ranking.append({"id_kriteria" : dtpike.id_kriteria,"data":[]})
            for dsub5 in datasubkriter:
                for mtx in range(len(matrix)):
                    if matrix[mtx]["id_kriteria"] == dtpike.id_kriteria:
                        if dsub5.id_kriteria == dtpike.id_kriteria:
                            matrix[mtx]["data"].append({"id_subkrit" : dsub5.id_subkrt , "data" : []})
                    if matrixnormal[mtx]["id_kriteria"] == dtpike.id_kriteria:
                        if(dsub5.id_kriteria == dtpike.id_kriteria):
                            matrixnormal[mtx]["data"].append({"id_subkrit" : dsub5.id_subkrt , "data" : []})

        for tpkrits80 in datatipekriter:
            hasilrank.append({"id_kriteria": tpkrits80.id_kriteria,"data":[]})
        
        for proyesk in dataproyek:
            for hrank in hasilrank:
                hrank["data"].append({"id_proyek":proyesk.id_pro,"hasil": 0})

        for dnilaiproy in datanilaiproyek:
            for dsubkri in datasubkriter:
                if dnilaiproy.id_subkrit == dsubkri.id_subkrt:
                    for mtrx in range(len(matrix)):
                        if matrix[mtrx]["id_kriteria"] == dsubkri.id_kriteria:
                            if dsubkri.id_subkrt == dnilaiproy.id_subkrit:
                                for mtrxs in range(len(matrix[mtrx]["data"])):
                                    if matrix[mtrx]["data"][mtrxs]["id_subkrit"] == dnilaiproy.id_subkrit :
                                        matrix[mtrx]["data"][mtrxs]["data"].append({"id_proyek": dnilaiproy.id_pro,"nilai": dnilaiproy.nilai})

        for matrixs in matrix:
            for sub01 in datasubkriter:
                for matrixdata in matrixs["data"]:
                    if matrixdata["id_subkrit"] == sub01.id_subkrt:
                        if sub01.pilih_kriteria == 0:
                            for rtvmatn in matrixdata["data"]:
                                matrixcz = []
                                for lenin in range(len(matrixdata["data"])):
                                    matrixcz.append(matrixdata["data"][lenin]["nilai"])
                                if rtvmatn["nilai"] != 0:
                                    jumlahnormal = min(matrixcz)/rtvmatn["nilai"]
                                else:
                                    jumlahnormal = 0
                                for mtxnormal in matrixnormal:
                                    for mtxndata in mtxnormal["data"]:
                                        if mtxndata["id_subkrit"] == sub01.id_subkrt:
                                            mtxndata["data"].append({"id_proyek":rtvmatn["id_proyek"],"jumlah":jumlahnormal})
                                jumlahnormal = 0
                        elif sub01.pilih_kriteria == 1:
                            for rtvmatn1 in matrixdata["data"]:
                                matrixcz1 = []
                                for lenin in range(len(matrixdata["data"])):
                                    matrixcz1.append(matrixdata["data"][lenin]["nilai"])
                                if max(matrixcz1) == 0:
                                    jumlahnormal = 0
                                else:
                                    jumlahnormal = rtvmatn1["nilai"]/max(matrixcz1)
                                for mtxnormal in matrixnormal:
                                    for mtxndata in mtxnormal["data"]:
                                        if mtxndata["id_subkrit"] == sub01.id_subkrt:
                                            mtxndata["data"].append({"id_proyek":rtvmatn1["id_proyek"],"jumlah":jumlahnormal})
                                jumlahnormal = 0

        for tkrite in datatipekriter:
            for proyk in dataproyek:
                for mtxnormal in matrixnormal:
                    jumlahnormal = 0
                    if mtxnormal["id_kriteria"] == tkrite.id_kriteria:
                        for mtrxp in mtxnormal["data"]:
                            for mtrxhasiln in mtrxp["data"]:
                                if mtrxhasiln["id_proyek"] == proyk.id_pro:
                                    for bprior in bpriority:
                                        for poix in range(len(bprior)):
                                            if bprior[poix]["id_subkrit"] == mtrxp["id_subkrit"]:
                                                jumlahnormal = jumlahnormal + (mtrxhasiln["jumlah"] * bprior[poix]["hasil"])
                                    for hrank1 in hasilrank:
                                        if hrank1["id_kriteria"] == tkrite.id_kriteria:
                                            for hrank1s in hrank1["data"]:
                                                if hrank1s["id_proyek"] == mtrxhasiln["id_proyek"]:
                                                    hrank1s["hasil"] = jumlahnormal
        for tpkris in datatipekriter:
            arrayisi = []
            for hmtixs in hasilrank:
                if hmtixs["id_kriteria"] == tpkris.id_kriteria:
                    for hmtixs1 in hmtixs["data"]:
                        arrayisi.append({"id_proyek":hmtixs1["id_proyek"],"hasil":hmtixs1["hasil"],"rank":0})
            #sorting after that borda
            arrayisi.sort(key=getkey,reverse=True)
            rank = 1
            for arrayisi1 in arrayisi:
                arrayisi1["rank"] = rank
                rank = rank + 1
            for rankis in ranking:
                if rankis["id_kriteria"] == tpkris.id_kriteria:
                    rankis["data"] = arrayisi
        return ranking
    else:
        return redirect('/login')

    #print(matrixnormal[0]["data"][0])
                         
def hitungborda(request,ranking):
    if 'logintkn' in request.session:
        dproyx = proyek.objects.filter(selesai=0)
        pborda = 0 
        bobot = []
        rank = 1
        hasil = []
        totalhasl = []
        nborda = []
        sumtotalhasil = 0 
        for i in range(len(dproyx),0,-1):
            bobot.append({"rank": rank ,"bobot":i})
            rank = rank + 1
        rank = 1
        for dpr in dproyx:
            hasil.append({"id_proyek": dpr.id_pro,"data":[]})
        for hsl in hasil:
            for dpr in dproyx:
                hsl["data"].append({"rank":rank,"nilai":0})
                rank = rank + 1
            rank = 1
       
        for dataproyekd in dproyx:
            for raksd in ranking:
                for dpxls in raksd["data"]:
                    if dpxls["id_proyek"] == dataproyekd.id_pro:
                        for bbt in bobot:
                            if bbt["rank"] == dpxls["rank"]:
                                pborda = pborda + (dpxls["hasil"] * bbt["bobot"])
                    #kesalahan hiitung disini   
                    for hasx in hasil:
                        if hasx["id_proyek"] == dpxls["id_proyek"]:
                            for ipsod in hasx["data"]:
                                if ipsod["rank"] == dpxls["rank"]:
                                    if ipsod["nilai"] == 0:
                                        ipsod["nilai"] = pborda
                                    else:
                                        ipsod["nilai"] = ipsod["nilai"] + pborda
                    pborda = 0
        print(ranking)
        for haxin in hasil:
            for hsum in haxin["data"]:
                pborda = pborda + hsum["nilai"]
            totalhasl.append({"id_proyek":haxin["id_proyek"],"total":pborda})
            pborda = 0 

        for toths in totalhasl:
            sumtotalhasil = sumtotalhasil + toths["total"]
        
        for tti in totalhasl:
            hit = tti["total"]/sumtotalhasil
            nborda.append({"id_proyek":tti["id_proyek"],"hasil":hit,"rank":0})
        
        nborda.sort(key=getkey,reverse=True)
        ranks = 1
        for nps in nborda:
            nps["rank"] = ranks
            ranks = ranks + 1
        print(nborda)
        return nborda
    else:
        return redirect('/login')

def getkey(obj):
    return obj["hasil"]

def editProyek(request,idpro):
    if 'logintkn' in request.session:
        proyesk = proyek.objects.all()
        subkri = daftar_kriteria.objects.all()
        datanilai = nilai_kriteria.objects.all()
        dataTipekriteria = tipe_kriteria.objects.all()
        dataOpsi = daftar_opsi.objects.all()
        isikriteria = proyesk.filter(id_pro=idpro)
        dfil = datanilai.filter(id_pro=idpro)
        template = loader.get_template('form_edit_proyek.html')
        return HttpResponse(template.render({"isikrite":isikriteria,"dkrit":subkri,'daftar_tipe':dataTipekriteria,"nkriter":dfil,"id_pro":idpro,"opsi":dataOpsi},request))
    else:
        return redirect('/login')

def prosesedit(request,idpro):
    if 'logintkn' in request.session:
        datasubkritre = daftar_kriteria.objects.all()
        if request.POST["pilihan_radio"] == "manual":
            proyek.objects.filter(id_pro=idpro).update(kt_pro=request.POST["kt_pro"],nm_pro=request.POST["nm_pro"],nilai_pro=request.POST["kl_02"],jml_mod=request.POST["kl_06"],waktu_perb=request.POST["kl_04"],manual=1)
        elif request.POST["pilihan_radio"] == "otomatis":
            if request.POST["kl_02"] == "0.0": 
                nilaipro = 70000000
            elif request.POST["kl_02"] == "0.2":
                nilaipro = 200000000
            elif request.POST["kl_02"] == "0.4":
                nilaipro = 850000000
            elif request.POST["kl_02"] == "0.6":
                nilaipro = 2000000000
            elif request.POST["kl_02"] == "0.8":
                nilaipro = 7000000000
            elif request.POST["kl_02"] == "1.0":
                nilaipro = 8000000000
            proyek.objects.filter(id_pro=idpro).update(kt_pro=request.POST["kt_pro"],nm_pro=request.POST["nm_pro"],nilai_pro=nilaipro,jml_mod=request.POST["kl_06"],waktu_perb=request.POST["kl_04"],manual=0)
        for dsubkr in datasubkritre:
            if dsubkr.id_subkrt == "kl_02":
                if request.POST["pilihan_radio"] == "otomatis":
                    if len(nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt)) == 0:
                        form1 = nilai_kriteria(id_pro=idpro,id_subkrit=dsubkr.id_subkrt,nilai=request.POST[dsubkr.id_subkrt])
                        form1.save()
                    else:
                        nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt).update(nilai=request.POST[dsubkr.id_subkrt])
                elif request.POST["pilihan_radio"] == "manual":
                    if int(request.POST[dsubkr.id_subkrt]) >= 0 and int(request.POST[dsubkr.id_subkrt]) < 71000000 :
                        if len(nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt)) == 0:
                            form1 = nilai_kriteria(id_pro=idpro,id_subkrit=dsubkr.id_subkrt,nilai="0.0")
                            form1.save()
                        else:
                            nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt).update(nilai="0.0")
                    elif int(request.POST[dsubkr.id_subkrt]) >= 71000000 and int(request.POST[dsubkr.id_subkrt]) < 201000000:
                        if len(nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt)) == 0:
                            form1 = nilai_kriteria(id_pro=idpro,id_subkrit=dsubkr.id_subkrt,nilai="0.2")
                            form1.save()
                        else:
                            nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt).update(nilai="0.2")
                    elif int(request.POST[dsubkr.id_subkrt]) >= 201000000 and int(request.POST[dsubkr.id_subkrt]) < 851000000:
                        if len(nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt)) == 0:
                            form1 = nilai_kriteria(id_pro=idpro,id_subkrit=dsubkr.id_subkrt,nilai="0.4")
                            form1.save()
                        else:
                            nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt).update(nilai="0.4")
                    elif int(request.POST[dsubkr.id_subkrt]) >= 851000000 and int(request.POST[dsubkr.id_subkrt]) < 2100000000:
                        if len(nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt)) == 0:
                            form1 = nilai_kriteria(id_pro=idpro,id_subkrit=dsubkr.id_subkrt,nilai="0.6")
                            form1.save()
                        else:
                            nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt).update(nilai="0.6")
                    elif int(request.POST[dsubkr.id_subkrt]) >= 2100000000 and int(request.POST[dsubkr.id_subkrt]) < 70000000000:
                        if len(nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt)) == 0:
                            form1 = nilai_kriteria(id_pro=idpro,id_subkrit=dsubkr.id_subkrt,nilai="0.8")
                            form1.save()
                        else:
                            nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt).update(nilai="0.8")
                    elif int(request.POST[dsubkr.id_subkrt]) > 70000000000:
                        if len(nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt)) == 0:
                            form1 = nilai_kriteria(id_pro=idpro,id_subkrit=dsubkr.id_subkrt,nilai="1.0")
                            form1.save()
                        else:
                            nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt).update(nilai="1.0")
            elif dsubkr.id_subkrt == "kl_04":
                if int(request.POST[dsubkr.id_subkrt]) <= 1 :
                    if len(nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt)) == 0:
                        form1 = nilai_kriteria(id_pro=idpro,id_subkrit=dsubkr.id_subkrt,nilai="0.0")
                        form1.save()
                    else:
                        nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt).update(nilai="0.0")
                elif int(request.POST[dsubkr.id_subkrt]) > 1 and int(request.POST[dsubkr.id_subkrt]) < 2:
                    if len(nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt)) == 0: 
                        form1 = nilai_kriteria(id_pro=idpro,id_subkrit=dsubkr.id_subkrt,nilai="0.2")
                        form1.save()
                    else:
                        nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt).update(nilai="0.2")
                elif int(request.POST[dsubkr.id_subkrt]) > 2 and int(request.POST[dsubkr.id_subkrt]) < 3:
                    if len(nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt)) == 0:
                        form1 = nilai_kriteria(id_pro=idpro,id_subkrit=dsubkr.id_subkrt,nilai="0.4")
                        form1.save()
                    else:
                        nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt).update(nilai="0.4")
                elif int(request.POST[dsubkr.id_subkrt]) > 3 and int(request.POST[dsubkr.id_subkrt]) < 4:
                    if len(nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt)) == 0:
                        form1 = nilai_kriteria(id_pro=idpro,id_subkrit=dsubkr.id_subkrt,nilai="0.6")
                        form1.save()
                    else:
                        nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt).update(nilai="0.6")
                elif int(request.POST[dsubkr.id_subkrt]) > 4 and int(request.POST[dsubkr.id_subkrt]) < 5:
                    if len(nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt)) == 0:
                        form1 = nilai_kriteria(id_pro=idpro,id_subkrit=dsubkr.id_subkrt,nilai="0.8")
                        form1.save()
                    else:
                        nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt).update(nilai="0.8")
                elif int(request.POST[dsubkr.id_subkrt]) > 5:
                    if len(nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt)) == 0:
                        form1 = nilai_kriteria(id_pro=idpro,id_subkrit=dsubkr.id_subkrt,nilai="1.0")
                        form1.save()
                    else:
                        nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt).update(nilai="1.0")
            elif dsubkr.id_subkrt == "kl_06":
                if int(request.POST[dsubkr.id_subkrt]) <= 5 :
                    if len(nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt)) == 0:
                        form1 = nilai_kriteria(id_pro=idpro,id_subkrit=dsubkr.id_subkrt,nilai="0.0")
                        form1.save()
                    else:
                        nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt).update(nilai="0.0")
                elif int(request.POST[dsubkr.id_subkrt]) >= 6 and int(request.POST[dsubkr.id_subkrt]) < 11:
                    if len(nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt)) == 0:
                        form1 = nilai_kriteria(id_pro=idpro,id_subkrit=dsubkr.id_subkrt,nilai="0.2")
                        form1.save()
                    else:
                        nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt).update(nilai="0.2")
                elif int(request.POST[dsubkr.id_subkrt]) >= 11 and int(request.POST[dsubkr.id_subkrt])< 16:
                    if len(nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt)) == 0:
                        form1 = nilai_kriteria(id_pro=idpro,id_subkrit=dsubkr.id_subkrt,nilai="0.4")
                        form1.save()
                    else:
                        nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt).update(nilai="0.4")
                elif int(request.POST[dsubkr.id_subkrt]) >= 16 and int(request.POST[dsubkr.id_subkrt]) < 21:
                    if len(nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt)) == 0:
                        form1 = nilai_kriteria(id_pro=idpro,id_subkrit=dsubkr.id_subkrt,nilai="0.6")
                        form1.save()
                    else:
                        nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt).update(nilai="0.6")
                elif int(request.POST[dsubkr.id_subkrt]) >= 21 and int(request.POST[dsubkr.id_subkrt]) < 26:
                    if len(nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt)) == 0:
                        form1 = nilai_kriteria(id_pro=idpro,id_subkrit=dsubkr.id_subkrt,nilai="0.8")
                        form1.save()
                    else:
                        nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt).update(nilai="0.8")
                elif int(request.POST[dsubkr.id_subkrt]) >= 26:
                    if len(nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt)) == 0:
                        form1 = nilai_kriteria(id_pro=idpro,id_subkrit=dsubkr.id_subkrt,nilai="1.0")
                        form1.save()
                    else:
                        nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt).update(nilai="1.0")
            elif dsubkr.tipe_input == "text":
                opsikrit = daftar_opsi.objects.all()
                for ol in opsikrit:
                    if ol.id_daftar == dsubkr.id_opsi:
                        if ol.deskripsi_opsi == request.POST[dsubkr.id_subkrt]:
                            if len(nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt)) == 0:
                                form1 = nilai_kriteria(id_pro=idproyek,id_subkrit=dsubkr.id_subkrt,nilai=ol.value_opsi)
                                form1.save()
                            else:
                                nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt).update(nilai=ol.value_opsi)
            else:
                if len(nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt)) == 0:
                    form1 = nilai_kriteria(id_pro=idpro,id_subkrit=dsubkr.id_subkrt,nilai=request.POST[dsubkr.id_subkrt])
                    form1.save()
                else:
                    nilai_kriteria.objects.filter(id_pro=idpro,id_subkrit=dsubkr.id_subkrt).update(nilai=request.POST[dsubkr.id_subkrt])
        request.session["suc"] = 1
        request.session["msg"] = "Proyek Berhasil Diubah"
        return redirect('/displayproyek')
    else:
        return redirect('/login')
    

def displaypro(request):
    if 'logintkn' in request.session:
        datasubkritre = daftar_kriteria.objects.all()
        dproy = proyek.objects.all()
        dnilai = nilai_kriteria.objects.all()
        dopt = daftar_opsi.objects.all()
        num = []
        nomor = 1
        rangex = len(dproy)
        for i in dproy:
            num.append({"id_pro":i.id_pro,"nomor":nomor})
            nomor = nomor + 1
        template = loader.get_template('form_daftar_proyek.html')
        return HttpResponse(template.render({"dsub":datasubkritre,"dnilai":dnilai,"dproyek":dproy,"num":num,"count":rangex,"opsi":dopt},request))
    else:
        return redirect('/login')

def hapuspro(request,idpro):
    if 'logintkn' in request.session:
        nilai_kriteria.objects.filter(id_pro=idpro).delete()
        proyek.objects.filter(id_pro=idpro).delete()
        request.session["suc"] = 1
        request.session["msg"] = "Proyek Berhasil Dihapus"
        return redirect('/displayproyek')
    else:
        return redirect('/login')

def setselesai(request,idpro):
    if 'logintkn' in request.session:
        proyek.objects.filter(id_pro=idpro).update(selesai=1)
        request.session["suc"] = 1
        request.session["msg"] = "Proyek Berhasil Diset Selesai"
        return redirect('/displayproyek')
    else:
        return redirect('/login')

def home(request):
    if 'logintkn' in request.session:
        template = loader.get_template('beranda.html')
        return HttpResponse(template.render({}, request))
    else:
        return redirect('/login')

def editKriteria(request,idkrit):
    if 'logintkn' in request.session:
        dataTipekriteria = tipe_kriteria.objects.filter(id_kriteria=idkrit)
        dataSubKriteria = daftar_kriteria.objects.filter(id_kriteria=idkrit)
        dataOpsi = opsi_kriteria.objects.all()
        template = loader.get_template('form_edit_kriteria.html')
        return HttpResponse(template.render({"tipe":dataTipekriteria,"subkrit":dataSubKriteria,"dataopsi":dataOpsi},request))
    else:
        return redirect('/login')

def daftarKriteria(request):
    if 'logintkn' in request.session:
        dataTipeKriteria = tipe_kriteria.objects.all()
        dataSubKriteria = daftar_kriteria.objects.all()
        arraydisp = []
        nomor = 0
        for p in dataTipeKriteria:
            arraydisp.append({"id_krit": p.id_kriteria,"nomor" : nomor + 1  })
            nomor = nomor + 1
        template = loader.get_template('form_daftar_kriteria.html')
        return HttpResponse(template.render({"tipe":dataTipeKriteria,"subkrit":dataSubKriteria,"nomor":arraydisp},request))
    else:
        return redirect('/login')

def daftarSubKrit(request,idkrit):
    if 'logintkn' in request.session:
        dataSubKriteria = daftar_kriteria.objects.filter(id_kriteria=idkrit)
        dataopsi = opsi_kriteria.objects.all()
        arraydisp = []
        nomor = 0
        for p in dataSubKriteria:
            arraydisp.append({"id_subkrit": p.id_subkrt,"nomor" : nomor + 1  })
            nomor = nomor + 1
        template = loader.get_template('form_daftar_subkrit.html')
        return HttpResponse(template.render({"subkrit":dataSubKriteria,"nomor":arraydisp,"opsi":dataopsi},request))
    else:
        return redirect('/login')


def prosesUbahKrit(request,idkrit):
    if 'logintkn' in request.session:
        idkriter = []
        namakrter = []
        pilihankrt = []
        opsi = [] 
        radio = []
        for c in request.POST.getlist("id_subkrt[]"):
            idkriter.append(c)
        for d in request.POST.getlist("nama_subkrit[]"):
            namakrter.append(d)
        for e in request.POST.getlist("pilih_kriteria[]"):
            pilihankrt.append(e)
        for j in request.POST.getlist("daftar_opsi[]"):
            opsi.append(j)
        for p in request.POST.getlist("pilihanrad[]"):
            radio.append(p)
        nilai_persamaan.objects.filter(id_kriteria=idkrit).delete()
        daftar_kriteria.objects.filter(id_kriteria=idkrit).delete()
        tipe_kriteria.objects.filter(id_kriteria=idkrit).update(nama_tipe=request.POST.get("nama_tipe"))
        for inputdata in range(len(idkriter)):
            subinput = daftar_kriteria(id_subkrt=idkriter[inputdata], nama_subkrit=namakrter[inputdata],
                                   id_kriteria=idkrit ,pilih_kriteria=pilihankrt[inputdata],id_opsi=opsi[inputdata],tipe_input=radio[inputdata])
            subinput.save()
        for persamaan in range(len(idkriter)):
            for persamaan1 in range(len(idkriter)):
                if(idkriter[persamaan] == idkriter[persamaan1]):
                    addpersamaan = nilai_persamaan(
                        id_subkrit1=idkriter[persamaan], id_subkrit2=idkriter[persamaan1], nilai=1,id_kriteria=idkrit)
                    addpersamaan.save()
                else:
                    addpersamaan = nilai_persamaan(
                        id_subkrit1=idkriter[persamaan], id_subkrit2=idkriter[persamaan1], nilai=0,id_kriteria=idkrit)
                    addpersamaan.save()
        request.session["suc"] = 1
        request.session["msg"] = "Kriteria Berhasil Diubah"
        return redirect('/daftarkrit')
    else:
        return redirect('/login')


def hapuskriteria(request,idkrit):
    if 'logintkn' in request.session:
        nilai_persamaan.objects.filter(id_kriteria=idkrit).delete()
        daftar_kriteria.objects.filter(id_kriteria=idkrit).delete()
        tipe_kriteria.objects.filter(id_kriteria=idkrit).delete()
        request.session["suc"] = 1
        request.session["msg"] = "Kriteria Berhasil Dihapus"
        return redirect('/daftarkrit')
    else:
        return redirect('/login')


def tambahOpsi(request):
    if 'logintkn' in request.session:
        template = loader.get_template('form_tambah_opsi.html')
        return HttpResponse(template.render({},request))
    else:
        return redirect('/login')


def prosestambah(request):
    if 'logintkn' in request.session:
        ids = uuid.uuid1()
        form1 = opsi_kriteria(id_opsi=ids,nama_opsi=request.POST.get('nm_opsi')).save()
        daftaropsi = []
        opsinow = 1
        for p in request.POST.getlist("opsi[]"):
            val = opsinow/len(request.POST.getlist("opsi[]"))
            daftaropsi.append({"desk":p,"val":val})
            opsinow = opsinow + 1
        for c in daftaropsi:
            daftar_opsi(id_daftar=ids,deskripsi_opsi=c["desk"],value_opsi=c["val"]).save()
            template = loader.get_template('beranda.html')
        return HttpResponse(template.render({"suc": 1, "msg": "Opsi Kriteria Berhasil Di Input"}, request))
    else:
        return redirect('/login')

def displayOpsi(request):
    if 'logintkn' in request.session:
        dataOpsi = opsi_kriteria.objects.all()
        dataOpsia = daftar_opsi.objects.all()
        nomor = [] 
        nmm = 0
        for x in dataOpsi:
            nomor.append({"id_opsi":x.id_opsi,"nomor": nmm+1})
            nmm = nmm + 1
        template = loader.get_template('form_display_option.html')
        return HttpResponse(template.render({"dopsi": dataOpsia, "opsi": dataOpsi,"nomor":nomor}, request))
    else:
        return redirect('/login')

def ubahOpsi(request,idopsi):
    if 'logintkn' in request.session:
        dataOpsi = opsi_kriteria.objects.filter(id_opsi=idopsi)
        dataOpsia = daftar_opsi.objects.filter(id_daftar=idopsi)
        template = loader.get_template('form_edit_opsi.html')
        return HttpResponse(template.render({"dopsi": dataOpsia, "opsi": dataOpsi}, request))
    else:
        return redirect('/login')

def procUbahOpsi(request,idopsi):
    if 'logintkn' in request.session:
        opsi_kriteria.objects.filter(id_opsi=idopsi).update(nama_opsi=request.POST.get("nm_opsi"))
        daftar_opsi.objects.filter(id_daftar=idopsi).delete()
        daftaropsi = []
        opsinow = 1
        for p in request.POST.getlist("opsi[]"):
            val = opsinow/len(request.POST.getlist("opsi[]"))
            daftaropsi.append({"desk":p,"val":val})
            opsinow = opsinow + 1
        for c in daftaropsi:
            daftar_opsi(id_daftar=idopsi,deskripsi_opsi=c["desk"],value_opsi=c["val"]).save()
        request.session["suc"] = 1
        request.session["msg"] = "Opsi Kriteria Berhasil Diubah"
        return redirect('/daftaropsi')
    else:
        return redirect('/login')

def deleteOpsi(request,idopsi):
    if 'logintkn' in request.session:
        daftar_opsi.objects.filter(id_daftar=idopsi).delete()
        opsi_kriteria.objects.filter(id_opsi=idopsi).delete()
        request.session["suc"] = 1
        request.session["msg"] = "Opsi Kriteria Berhasil Dihapus"
        return redirect('/daftaropsi')
    else:
        return redirect('/login')

def login(request):
    template = loader.get_template('form_login.html')
    return HttpResponse(template.render({}, request))

def inputuser(request):
    if request.session["akses"] == "SU" and 'logintkn' in request.session:
        template = loader.get_template('form_input_user.html')
        return HttpResponse(template.render({}, request))
    else:
        return redirect('/login')

def proseslogin(request):
    ceklog = user.objects.filter(username=request.POST.get("username"))
    if len(ceklog) > 0:
        if ceklog[0].password == request.POST.get("password"):
            request.session["username"] = request.POST.get("username")
            request.session["akses"] = ceklog[0].hak_akses
            request.session["namauser"] = ceklog[0].nama_user
            request.session["logintkn"] = "loginkn"
            if 'error' in request.session:
                del request.session["error"]
                del request.session["msg"]
            return redirect('/home')
        else:
            template = loader.get_template('form_login.html')
            request.session["error"] = 0
            request.session["msg"] = "Username Atau Password Salah"
            return redirect('/login')
    else:
        template = loader.get_template('form_login.html')
        request.session["error"] = 0
        request.session["msg"] = "Username Atau Password Salah"
        return redirect('/login')

def viuser(request):
    if request.session["akses"] == "SU" and 'logintkn' in request.session:
        template = loader.get_template('form_input_user.html')
        return HttpResponse(template.render({}, request))
    else:
        return redirect('/login')

def procinputuser(request):
    if request.session["akses"] == "SU" and 'logintkn' in request.session:
        cekuser = user.objects.filter(username=request.POST.get("username"))
        if len(cekuser) > 0:
            request.session["error"] = 0
            request.session["msg"] = "Username Sudah Ada"
            return redirect('/iuser')
        else:
            form1 = user(id_user=uuid.uuid1(),nama_user=request.POST.get("namau"),username=request.POST.get("username"),password=request.POST.get("password"),perusahaan=request.POST.get("namap"),hak_akses="MP")
            form1.save()
            if "error" in request.session:
                del request.session["error"]
                del request.session["msg"]
            request.session["suc"] = 1
            request.session["msg"] = "User Berhasil Ditambah"
            return redirect('/home')
    else:
        return redirect('/login')

def viuser(request):
    if request.session["akses"] == "SU" and 'logintkn' in request.session:
        template = loader.get_template('form_display_user.html')
        nomor = []
        nomors = 1
        datauser = user.objects.filter(hak_akses="MP")
        for i in datauser:
            nomor.append({"id_user":i.id_user,"nomor":nomors})
            nomors = nomors + 1
        return HttpResponse(template.render({"user":datauser,"nomor":nomor}, request))
    else:
        return redirect('/login')

def edituser(request,iduser):
    if request.session["akses"] == "SU" and 'logintkn' in request.session:
        cekuser = user.objects.filter(id_user=iduser)
        template = loader.get_template('form_ubah_user.html')
        return HttpResponse(template.render({"user":cekuser}, request))
    else:
        return redirect('/login')

def procedituser(request,iduser):
    if request.session["akses"] == "SU" and 'logintkn' in request.session:
        user.objects.filter(id_user=iduser).update(nama_user=request.POST.get("namau"),username=request.POST.get("username"),password=request.POST.get("password"),perusahaan=request.POST.get("namap"))
        request.session["suc"] = 1
        request.session["msg"] = "User Berhasil Diubah"
        return redirect('/daftaruser')
    else:
        return redirect('/login')

def deleteuser(request,iduser):
    if request.session["akses"] == "SU" and 'logintkn' in request.session:
        user.objects.filter(id_user=iduser).delete()
        request.session["suc"] = 1
        request.session["msg"] = "User Berhasil DiHapus"
        return redirect('/daftaruser')
    else:
        return redirect('/login')

def logout(request):
    del request.session["akses"]
    del request.session["username"]
    del request.session["logintkn"]
    del request.session["namauser"]
    if "suc" in request.session:
        del request.session["suc"]
        del request.session["msg"]
    return redirect('/login')
