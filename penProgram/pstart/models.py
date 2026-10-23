from django.db import models

# Create your models here.
class tipe_kriteria(models.Model):
    id_kriteria = models.TextField(primary_key=True)
    nama_tipe = models.TextField()
    
    class Meta:
        db_table = 'tipe_kriteria'

class daftar_kriteria(models.Model):
    id_subkrt = models.TextField(primary_key=True)
    nama_subkrit = models.TextField()
    id_kriteria = models.TextField()
    pilih_kriteria = models.IntegerField()
    id_opsi = models.TextField()
    tipe_input = models.TextField()
    class Meta:
        db_table = 'daftar_kriteria'

class nilai_persamaan(models.Model):
    id_persamaan = models.TextField(primary_key=True)
    id_subkrit1 = models.TextField()
    id_subkrit2 = models.TextField()
    nilai = models.FloatField()
    id_kriteria = models.TextField()
    class Meta:
        db_table = 'nilai_persamaan'

class proyek(models.Model):
    id_pro = models.TextField(primary_key=True)
    kt_pro = models.TextField()
    nm_pro = models.TextField()
    nilai_pro = models.TextField()
    jml_mod = models.IntegerField()
    waktu_perb = models.IntegerField()
    manual = models.IntegerField()
    selesai = models.IntegerField()
    class Meta:
        db_table = 'proyek'


class nilai_kriteria(models.Model):
    id_nilai = models.TextField(primary_key=True)
    id_pro = models.TextField()
    id_subkrit = models.TextField()
    nilai = models.FloatField()
    class Meta:
        db_table = 'nilai_kriteria'

class daftar_opsi(models.Model):
    id = models.TextField(primary_key=True)
    id_daftar = models.TextField()
    deskripsi_opsi = models.TextField()
    value_opsi = models.TextField()
    class Meta:
        db_table = 'daftar_opsi'

class opsi_kriteria(models.Model):
    id_opsi = models.TextField(primary_key=True)
    nama_opsi = models.TextField()
    class Meta:
        db_table = 'opsi_kriteria'

class user(models.Model):
    id_user = models.TextField(primary_key=True)
    nama_user = models.TextField()
    username = models.TextField()
    password = models.TextField()
    perusahaan = models.TextField()
    hak_akses = models.TextField()
    class Meta:
        db_table = 'user'


